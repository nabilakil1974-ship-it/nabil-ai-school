import os
import base64
from typing import Optional

from openai import OpenAI

from app.core.config import settings


class NabilAIGateway:

    def __init__(self):

        # =====================================================
        # OpenRouter
        # =====================================================

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

        # =====================================================
        # Gemini key pool
        # =====================================================

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
                self.gemini_api_keys.append(
                    value
                )

        # Gemini model is fixed here intentionally.
        # This avoids an old/stale setting overriding the deployed model.
        self.gemini_text_model = "gemini-3.6-flash"
        self.gemini_vision_model = "gemini-3.6-flash"

        # =====================================================
        # OpenAI fallback
        # =====================================================

        self.openai_api_key = (
            os.getenv(
                "OPENAI_API_KEY",
                "",
            )
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
            )

        self.openai_text_model = (
            os.getenv(
                "OPENAI_TEXT_MODEL",
                "",
            )
            or getattr(
                settings,
                "OPENAI_TEXT_MODEL",
                "gpt-5.5",
            )
            or "gpt-5.5"
        )

        self.openai_vision_model = (
            os.getenv(
                "OPENAI_VISION_MODEL",
                "",
            )
            or getattr(
                settings,
                "OPENAI_VISION_MODEL",
                self.openai_text_model,
            )
            or self.openai_text_model
        )

        # =====================================================
        # Groq
        # =====================================================

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
            )

        self.groq_text_model = getattr(
            settings,
            "GROQ_TEXT_MODEL",
            "openai/gpt-oss-120b",
        )

        # =====================================================
        # تأكد أن لدينا مزودًا واحدًا على الأقل
        # =====================================================

        if (
            self.openrouter_client is None
            and not self.gemini_api_keys
            and self.groq_client is None
            and self.openai_client is None
        ):
            raise RuntimeError(
                "لا يوجد أي مفتاح AI مضبوط في إعدادات السيرفر."
            )

    # =========================================================
    # استخراج النص
    # =========================================================

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

        if isinstance(
            content,
            str,
        ):
            return content.strip()

        if isinstance(
            content,
            list,
        ):

            parts = []

            for item in content:

                if isinstance(
                    item,
                    str,
                ):
                    parts.append(item)

                elif isinstance(
                    item,
                    dict,
                ):

                    text = item.get(
                        "text"
                    )

                    if text:
                        parts.append(
                            str(text)
                        )

                else:

                    text = getattr(
                        item,
                        "text",
                        None,
                    )

                    if text:
                        parts.append(
                            str(text)
                        )

            return "\n".join(
                parts
            ).strip()

        return ""

    # =========================================================
    # بناء الرسائل
    # =========================================================

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
            ).decode(
                "utf-8"
            )

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

    # =========================================================
    # تنفيذ طلب لمزود واحد
    # =========================================================

    def _call_provider(
        self,
        client,
        model: str,
        chat_messages: list[dict],
        max_output_tokens: int,
        provider_name: str,
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

        content = self._extract_content(
            response
        )

        if not content:
            raise RuntimeError(
                f"{provider_name} لم يُرجع إجابة نصية."
            )

        return content

    # =========================================================
    # هل الخطأ يستحق الانتقال للمفتاح التالي؟
    # =========================================================

    def _is_retryable_error(
        self,
        error: Exception,
    ) -> bool:

        text = str(
            error
        ).lower()

        markers = [
            "429",
            "rate limit",
            "rate_limit",
            "quota",
            "resource exhausted",
            "temporarily",
            "timeout",
            "timed out",
            "provider returned error",
            "overloaded",
            "503",
            "502",
            "500",
            "upstream",
            "connection",
            "server error",
        ]

        return any(
            marker in text
            for marker in markers
        )

    # =========================================================
    # Gemini key rotation
    # =========================================================

    def _try_gemini_keys(
        self,
        chat_messages: list[dict],
        image_bytes: Optional[bytes],
        max_output_tokens: int,
        errors: list[str],
    ) -> Optional[str]:

        model = (
            self.gemini_vision_model
            if image_bytes is not None
            else self.gemini_text_model
        )

        for index, api_key in enumerate(
            self.gemini_api_keys,
            start=1,
        ):

            client = OpenAI(
                base_url=(
                    "https://generativelanguage.googleapis.com/"
                    "v1beta/openai/"
                ),
                api_key=api_key,
            )

            try:

                return self._call_provider(
                    client=client,
                    model=model,
                    chat_messages=chat_messages,
                    max_output_tokens=max_output_tokens,
                    provider_name=f"Gemini #{index}",
                )

            except Exception as exc:

                errors.append(
                    f"Gemini #{index}: {exc}"
                )

                continue

        return None

    # =========================================================
    # generate
    # =========================================================

    def generate(
        self,
        instructions: str,
        messages: list[dict],
        image_bytes: Optional[bytes] = None,
        image_mime_type: str = "image/jpeg",
        max_output_tokens: int = 2500,
    ) -> str:

        chat_messages = self._build_messages(
            instructions=instructions,
            messages=messages,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
        )

        errors = []

        # =====================================================
        # 1) OpenRouter
        # =====================================================

        if self.openrouter_client is not None:

            try:

                model = (
                    self.openrouter_vision_model
                    if image_bytes is not None
                    else self.openrouter_text_model
                )

                return self._call_provider(
                    client=self.openrouter_client,
                    model=model,
                    chat_messages=chat_messages,
                    max_output_tokens=max_output_tokens,
                    provider_name="OpenRouter",
                )

            except Exception as exc:

                errors.append(
                    f"OpenRouter: {exc}"
                )

        # =====================================================
        # 2) Gemini key rotation
        # =====================================================

        if self.gemini_api_keys:

            result = self._try_gemini_keys(
                chat_messages=chat_messages,
                image_bytes=image_bytes,
                max_output_tokens=max_output_tokens,
                errors=errors,
            )

            if result:
                return result

        # =====================================================
        # 3) Groq
        # النص فقط
        # =====================================================

        if (
            image_bytes is None
            and self.groq_client is not None
        ):

            try:

                return self._call_provider(
                    client=self.groq_client,
                    model=self.groq_text_model,
                    chat_messages=chat_messages,
                    max_output_tokens=max_output_tokens,
                    provider_name="Groq",
                )

            except Exception as exc:

                errors.append(
                    f"Groq: {exc}"
                )

        # =====================================================
        # 4) OpenAI fallback
        # =====================================================

        if self.openai_client is not None:

            try:

                model = (
                    self.openai_vision_model
                    if image_bytes is not None
                    else self.openai_text_model
                )

                return self._call_provider(
                    client=self.openai_client,
                    model=model,
                    chat_messages=chat_messages,
                    max_output_tokens=max_output_tokens,
                    provider_name="OpenAI",
                )

            except Exception as exc:

                errors.append(
                    f"OpenAI: {exc}"
                )

        # =====================================================
        # فشل الجميع
        # =====================================================

        if errors:

            raise RuntimeError(
                "تعذر الحصول على إجابة من جميع مزودي الذكاء الاصطناعي.\n"
                +
                "\n".join(
                    errors
                )
            )

        raise RuntimeError(
            "لا يوجد مزود ذكاء اصطناعي متاح."
        )

    # =========================================================
    # الصوت
    # =========================================================

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "voice.webm",
    ) -> str:

        raise RuntimeError(
            "تحويل الصوت غير متاح حاليًا في هذا المسار."
        )
