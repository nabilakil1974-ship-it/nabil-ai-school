import base64
import logging
import os
import threading
import time
from typing import Optional

from openai import OpenAI

from app.core.config import settings


logger = logging.getLogger("nabil_ai.gateway")


class NabilAIGateway:
    """
    Production-oriented AI gateway for NABIL AI.

    Features:
    - Multiple providers: Gemini, OpenRouter, Groq, OpenAI
    - Per-provider and per-Gemini-key cooldowns
    - Fast failover after 429/quota/temporary provider errors
    - No SDK auto-retry storms
    - Clean student-facing failure messages
    - Detailed provider errors stay in server logs
    - Configurable provider order
    """

    def __init__(self):

        self._state_lock = threading.Lock()
        self._blocked_until: dict[str, float] = {}
        self._failure_count: dict[str, int] = {}
        self._gemini_cursor = 0
        # If all Gemini keys share the same exhausted project/billing pool,
        # stop retrying every key on every student request.
        self._gemini_global_blocked_until = 0.0

        self.request_timeout_seconds = float(
            os.getenv("NABIL_AI_TIMEOUT_SECONDS", "45")
        )

        self.sdk_max_retries = 0

        raw_order = os.getenv(
            "NABIL_AI_PROVIDER_ORDER",
            "gemini,openrouter,groq,openai",
        )

        supported = {"gemini", "openrouter", "groq", "openai"}

        requested_order = [
            item.strip().lower()
            for item in raw_order.split(",")
            if item.strip()
        ]

        self.provider_order = [
            item
            for item in requested_order
            if item in supported
        ]

        if not self.provider_order:
            self.provider_order = [
                "gemini",
                "openrouter",
                "groq",
                "openai",
            ]

        self.openrouter_api_key = getattr(
            settings,
            "OPENROUTER_API_KEY",
            "",
        )

        self.openrouter_client = None

        if self.openrouter_api_key:
            self.openrouter_client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_api_key,
                timeout=self.request_timeout_seconds,
                max_retries=self.sdk_max_retries,
            )

        self.openrouter_text_model = getattr(
            settings,
            "OPENROUTER_TEXT_MODEL",
            "openrouter/free",
        )

        self.openrouter_vision_model = getattr(
            settings,
            "OPENROUTER_VISION_MODEL",
            "openrouter/free",
        )

        self.gemini_api_keys = []

        for key_name in [
            "GEMINI_API_KEY",
            "GEMINI_API_KEY_2",
            "GEMINI_API_KEY_3",
            "GEMINI_API_KEY_4",
            "GEMINI_API_KEY_5",
        ]:

            value = getattr(
                settings,
                key_name,
                "",
            )

            if value:
                self.gemini_api_keys.append(value)

        self.gemini_text_model = (
            os.getenv("GEMINI_TEXT_MODEL", "")
            or getattr(
                settings,
                "GEMINI_TEXT_MODEL",
                "gemini-3.6-flash",
            )
            or "gemini-3.6-flash"
        )

        self.gemini_vision_model = (
            os.getenv("GEMINI_VISION_MODEL", "")
            or getattr(
                settings,
                "GEMINI_VISION_MODEL",
                self.gemini_text_model,
            )
            or self.gemini_text_model
        )

        self.groq_api_key = getattr(
            settings,
            "GROQ_API_KEY",
            "",
        )

        self.groq_client = None

        if self.groq_api_key:
            self.groq_client = OpenAI(
                base_url="https://api.groq.com/openai/v1",
                api_key=self.groq_api_key,
                timeout=self.request_timeout_seconds,
                max_retries=self.sdk_max_retries,
            )

        self.groq_text_model = getattr(
            settings,
            "GROQ_TEXT_MODEL",
            "openai/gpt-oss-120b",
        )

        self.openai_api_key = (
            os.getenv("OPENAI_API_KEY", "")
            or getattr(
                settings,
                "OPENAI_API_KEY",
                "",
            )
        )

        self.openai_client = None

        if self.openai_api_key:
            self.openai_client = OpenAI(
                api_key=self.openai_api_key,
                timeout=self.request_timeout_seconds,
                max_retries=self.sdk_max_retries,
            )

        self.openai_text_model = (
            os.getenv("OPENAI_TEXT_MODEL", "")
            or getattr(
                settings,
                "OPENAI_TEXT_MODEL",
                "gpt-5.5",
            )
            or "gpt-5.5"
        )

        self.openai_vision_model = (
            os.getenv("OPENAI_VISION_MODEL", "")
            or getattr(
                settings,
                "OPENAI_VISION_MODEL",
                self.openai_text_model,
            )
            or self.openai_text_model
        )

        if (
            self.openrouter_client is None
            and not self.gemini_api_keys
            and self.groq_client is None
            and self.openai_client is None
        ):
            raise RuntimeError(
                "لا يوجد أي مزود ذكاء اصطناعي مضبوط في إعدادات السيرفر."
            )

    def _is_available(
        self,
        provider_key: str,
    ) -> bool:

        now = time.monotonic()

        with self._state_lock:
            until = self._blocked_until.get(
                provider_key,
                0.0,
            )

        return now >= until

    def _clear_failure(
        self,
        provider_key: str,
    ) -> None:

        with self._state_lock:
            self._failure_count[provider_key] = 0
            self._blocked_until.pop(
                provider_key,
                None,
            )

    def _error_kind(
        self,
        error: Exception,
    ) -> str:

        text = str(error).lower()

        if any(
            marker in text
            for marker in [
                "no credits remaining",
                "credit_balance_exhausted",
                "insufficient_quota",
                "prepayment credits are depleted",
                "billing",
            ]
        ):
            return "billing"

        if any(
            marker in text
            for marker in [
                "429",
                "rate limit",
                "rate_limit",
                "quota",
                "resource_exhausted",
                "resource exhausted",
                "tokens per day",
                "requests per day",
            ]
        ):
            return "quota"

        if any(
            marker in text
            for marker in [
                "404",
                "not_found",
                "no longer available",
            ]
        ):
            return "model"

        if any(
            marker in text
            for marker in [
                "timeout",
                "timed out",
                "temporarily",
                "overloaded",
                "503",
                "502",
                "500",
                "upstream",
                "connection",
                "server error",
            ]
        ):
            return "temporary"

        return "other"

    def _cooldown_seconds(
        self,
        kind: str,
        failures: int,
    ) -> int:

        if kind == "billing":
            return int(
                os.getenv(
                    "NABIL_AI_BILLING_COOLDOWN_SECONDS",
                    "1800",
                )
            )

        if kind == "quota":
            return int(
                os.getenv(
                    "NABIL_AI_QUOTA_COOLDOWN_SECONDS",
                    "300",
                )
            )

        if kind == "model":
            return int(
                os.getenv(
                    "NABIL_AI_MODEL_COOLDOWN_SECONDS",
                    "1800",
                )
            )

        if kind == "temporary":
            base = 20
            return min(
                180,
                base * max(1, failures),
            )

        return min(
            120,
            10 * max(1, failures),
        )

    def _register_failure(
        self,
        provider_key: str,
        error: Exception,
    ) -> None:

        kind = self._error_kind(error)

        with self._state_lock:

            failures = (
                self._failure_count.get(
                    provider_key,
                    0,
                )
                + 1
            )

            self._failure_count[
                provider_key
            ] = failures

            seconds = self._cooldown_seconds(
                kind=kind,
                failures=failures,
            )

            self._blocked_until[
                provider_key
            ] = (
                time.monotonic()
                + seconds
            )

        logger.warning(
            "NABIL AI provider failure: provider=%s kind=%s "
            "cooldown=%ss error=%s",
            provider_key,
            kind,
            seconds,
            str(error),
        )

    def _extract_content(
        self,
        response,
    ) -> str:

        if response is None:
            return ""

        choices = getattr(
            response,
            "choices",
            None,
        )

        if not choices:
            return ""

        message = getattr(
            choices[0],
            "message",
            None,
        )

        if message is None:
            return ""

        content = getattr(
            message,
            "content",
            None,
        )

        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):

            parts = []

            for item in content:

                if isinstance(item, str):
                    parts.append(item)

                elif isinstance(item, dict):

                    text = item.get("text")

                    if text:
                        parts.append(str(text))

                else:

                    text = getattr(
                        item,
                        "text",
                        None,
                    )

                    if text:
                        parts.append(str(text))

            return "\n".join(parts).strip()

        return ""

    def _build_messages(
        self,
        instructions: str,
        messages: list[dict],
        image_bytes: Optional[bytes],
        image_mime_type: str,
    ) -> list[dict]:

        chat_messages = [
            {
                "role": "system",
                "content": instructions,
            }
        ]

        for msg in messages:

            chat_messages.append(
                {
                    "role": msg.get(
                        "role",
                        "user",
                    ),
                    "content": msg.get(
                        "content",
                        "",
                    ),
                }
            )

        if image_bytes is not None:

            encoded = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            chat_messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "اقرأ الصورة كاملة بدقة. "
                                "إذا كانت سؤالًا أو تمرينًا، "
                                "استخرج السؤال كما هو ثم حلّه خطوة خطوة. "
                                "إذا كانت صفحة درس، "
                                "اشرح محتواها تدريجيًا. "
                                "إذا كانت تحتوي على رسم أو جدول أو مخطط، "
                                "اقرأ عناصره واستعملها في الحل. "
                                "لا تخترع أي معلومة غير واضحة."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": (
                                    f"data:{image_mime_type};"
                                    f"base64,{encoded}"
                                )
                            },
                        },
                    ],
                }
            )

        return chat_messages

    def _call_provider(
        self,
        client,
        model: str,
        chat_messages: list[dict],
        max_output_tokens: int,
        provider_name: str,
        provider_key: str,
    ) -> str:

        response = (
            client
            .chat
            .completions
            .create(
                model=model,
                messages=chat_messages,
                max_tokens=max_output_tokens,
            )
        )

        content = self._extract_content(response)

        if not content:
            raise RuntimeError(
                f"{provider_name} لم يُرجع إجابة نصية."
            )

        self._clear_failure(provider_key)

        return content

    def _gemini_globally_available(self) -> bool:
        with self._state_lock:
            return time.monotonic() >= self._gemini_global_blocked_until

    def _block_gemini_globally(self, seconds: int) -> None:
        with self._state_lock:
            self._gemini_global_blocked_until = max(
                self._gemini_global_blocked_until,
                time.monotonic() + max(1, seconds),
            )

    def _all_configured_providers_blocked(self) -> bool:
        checks = []

        if self.gemini_api_keys:
            checks.append(not self._gemini_globally_available())

        if self.openrouter_client is not None:
            checks.append(not self._is_available("openrouter"))

        if self.groq_client is not None:
            checks.append(not self._is_available("groq"))

        if self.openai_client is not None:
            checks.append(not self._is_available("openai"))

        return bool(checks) and all(checks)

    def _try_gemini_keys(
        self,
        chat_messages: list[dict],
        image_bytes: Optional[bytes],
        max_output_tokens: int,
        debug_errors: list[str],
    ) -> Optional[str]:

        if (
            not self.gemini_api_keys
            or not self._gemini_globally_available()
        ):
            return None

        model = (
            self.gemini_vision_model
            if image_bytes is not None
            else self.gemini_text_model
        )

        total = len(self.gemini_api_keys)

        with self._state_lock:
            start_index = (
                self._gemini_cursor
                % total
            )

            self._gemini_cursor = (
                self._gemini_cursor
                + 1
            ) % total

        for offset in range(total):

            index = (
                start_index
                + offset
            ) % total

            api_key = self.gemini_api_keys[index]

            provider_key = f"gemini:{index + 1}"

            if not self._is_available(provider_key):
                continue

            client = OpenAI(
                base_url=(
                    "https://generativelanguage.googleapis.com/"
                    "v1beta/openai/"
                ),
                api_key=api_key,
                timeout=self.request_timeout_seconds,
                max_retries=self.sdk_max_retries,
            )

            try:

                return self._call_provider(
                    client=client,
                    model=model,
                    chat_messages=chat_messages,
                    max_output_tokens=max_output_tokens,
                    provider_name=f"Gemini #{index + 1}",
                    provider_key=provider_key,
                )

            except Exception as exc:

                kind = self._error_kind(exc)

                self._register_failure(
                    provider_key,
                    exc,
                )

                debug_errors.append(
                    f"Gemini #{index + 1}: {exc}"
                )

                # Billing/prepayment exhaustion is usually project-wide.
                # Do not burn the remaining Gemini keys in the same request.
                if kind == "billing":
                    self._block_gemini_globally(
                        self._cooldown_seconds(
                            kind="billing",
                            failures=1,
                        )
                    )
                    break

        return None

    def _try_openrouter(
        self,
        chat_messages: list[dict],
        image_bytes: Optional[bytes],
        max_output_tokens: int,
        debug_errors: list[str],
    ) -> Optional[str]:

        provider_key = "openrouter"

        if (
            self.openrouter_client is None
            or not self._is_available(provider_key)
        ):
            return None

        model = (
            self.openrouter_vision_model
            if image_bytes is not None
            else self.openrouter_text_model
        )

        try:

            return self._call_provider(
                client=self.openrouter_client,
                model=model,
                chat_messages=chat_messages,
                max_output_tokens=max_output_tokens,
                provider_name="OpenRouter",
                provider_key=provider_key,
            )

        except Exception as exc:

            self._register_failure(
                provider_key,
                exc,
            )

            debug_errors.append(
                f"OpenRouter: {exc}"
            )

            return None

    def _try_groq(
        self,
        chat_messages: list[dict],
        image_bytes: Optional[bytes],
        max_output_tokens: int,
        debug_errors: list[str],
    ) -> Optional[str]:

        provider_key = "groq"

        if (
            image_bytes is not None
            or self.groq_client is None
            or not self._is_available(provider_key)
        ):
            return None

        try:

            return self._call_provider(
                client=self.groq_client,
                model=self.groq_text_model,
                chat_messages=chat_messages,
                max_output_tokens=max_output_tokens,
                provider_name="Groq",
                provider_key=provider_key,
            )

        except Exception as exc:

            self._register_failure(
                provider_key,
                exc,
            )

            debug_errors.append(
                f"Groq: {exc}"
            )

            return None

    def _try_openai(
        self,
        chat_messages: list[dict],
        image_bytes: Optional[bytes],
        max_output_tokens: int,
        debug_errors: list[str],
    ) -> Optional[str]:

        provider_key = "openai"

        if (
            self.openai_client is None
            or not self._is_available(provider_key)
        ):
            return None

        model = (
            self.openai_vision_model
            if image_bytes is not None
            else self.openai_text_model
        )

        try:

            return self._call_provider(
                client=self.openai_client,
                model=model,
                chat_messages=chat_messages,
                max_output_tokens=max_output_tokens,
                provider_name="OpenAI",
                provider_key=provider_key,
            )

        except Exception as exc:

            self._register_failure(
                provider_key,
                exc,
            )

            debug_errors.append(
                f"OpenAI: {exc}"
            )

            return None

    def generate(
        self,
        instructions: str,
        messages: list[dict],
        image_bytes: Optional[bytes] = None,
        image_mime_type: str = "image/jpeg",
        max_output_tokens: int = 1400,
    ) -> str:

        max_output_tokens = max(
            256,
            min(int(max_output_tokens or 1400), 1400),
        )

        chat_messages = self._build_messages(
            instructions=instructions,
            messages=messages,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
        )

        debug_errors: list[str] = []

        handlers = {
            "gemini": lambda: self._try_gemini_keys(
                chat_messages=chat_messages,
                image_bytes=image_bytes,
                max_output_tokens=max_output_tokens,
                debug_errors=debug_errors,
            ),
            "openrouter": lambda: self._try_openrouter(
                chat_messages=chat_messages,
                image_bytes=image_bytes,
                max_output_tokens=max_output_tokens,
                debug_errors=debug_errors,
            ),
            "groq": lambda: self._try_groq(
                chat_messages=chat_messages,
                image_bytes=image_bytes,
                max_output_tokens=max_output_tokens,
                debug_errors=debug_errors,
            ),
            "openai": lambda: self._try_openai(
                chat_messages=chat_messages,
                image_bytes=image_bytes,
                max_output_tokens=max_output_tokens,
                debug_errors=debug_errors,
            ),
        }

        for provider in self.provider_order:

            handler = handlers.get(provider)

            if handler is None:
                continue

            result = handler()

            if result:
                return result

        if debug_errors:
            logger.error(
                "All AI providers failed. Errors: %s",
                " | ".join(debug_errors),
            )

        raise RuntimeError(
            "خدمة NABIL AI مشغولة أو غير متاحة مؤقتًا. "
            "يرجى إعادة المحاولة بعد قليل."
        )

    def health_snapshot(
        self,
    ) -> dict:

        now = time.monotonic()

        with self._state_lock:
            blocked = {
                key: max(
                    0,
                    round(until - now),
                )
                for key, until
                in self._blocked_until.items()
                if until > now
            }

            failures = dict(
                self._failure_count
            )

        return {
            "provider_order": list(
                self.provider_order
            ),
            "blocked_for_seconds": blocked,
            "failure_count": failures,
            "gemini_key_count": len(
                self.gemini_api_keys
            ),
            "gemini_global_blocked_for_seconds": max(
                0,
                round(
                    self._gemini_global_blocked_until
                    - time.monotonic()
                ),
            ),
            "openrouter_enabled": (
                self.openrouter_client
                is not None
            ),
            "groq_enabled": (
                self.groq_client
                is not None
            ),
            "openai_enabled": (
                self.openai_client
                is not None
            ),
        }

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "voice.webm",
    ) -> str:

        raise RuntimeError(
            "تحويل الصوت غير متاح حاليًا في هذا المسار."
        )
