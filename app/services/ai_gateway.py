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
        # Gemini fallback
        # =====================================================

        self.gemini_api_key = getattr(
            settings,
            "GEMINI_API_KEY",
            "",
        )

        self.gemini_client = None

        if self.gemini_api_key:
            self.gemini_client = OpenAI(
                base_url=(
                    "https://generativelanguage.googleapis.com/"
                    "v1beta/openai/"
                ),
                api_key=self.gemini_api_key,
            )

        self.gemini_text_model = getattr(
            settings,
            "GEMINI_TEXT_MODEL",
            "gemini-3.8-flash",
        )

        self.gemini_vision_model = getattr(
            settings,
            "GEMINI_VISION_MODEL",
            "gemini-3.8-flash",
        )

        # =====================================================
        # Groq optional third fallback
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
            and self.gemini_client is None
            and self.groq_client is None
        ):
            raise RuntimeError(
                "لا يوجد أي مفتاح AI مضبوط. "
                "أضف OPENROUTER_API_KEY أو GEMINI_API_KEY."
            )

    # =========================================================
    # استخراج النص من الرد
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

            role = msg.get(
                "role",
                "user",
            )

            content = msg.get(
                "content",
                "",
            )

            chat_messages.append(
                {
                    "role": role,
                    "content": content,
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
                                "حدد أولًا نوع المحتوى. "
                                "إذا كانت الصورة سؤالًا أو تمرينًا، "
                                "استخرج السؤال كما هو ثم حلّه "
                                "خطوة خطوة وفق مستوى الطالب. "
                                "إذا كانت الصورة صفحة درس، "
                                "استخرج الأفكار والمفاهيم الأساسية "
                                "واشرحها تدريجيًا. "
                                "إذا كانت تحتوي على رسم هندسي "
                                "أو منحنى أو جدول أو مخطط، "
                                "اقرأ عناصره واستعملها في الحل. "
                                "لا تخترع أي رقم أو رمز أو معلومة "
                                "غير واضحة في الصورة."
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
    # تنفيذ الطلب عند مزود محدد
    # =========================================================

    def _call_provider(
        self,
        client,
        model: str,
        chat_messages: list[dict],
        max_output_tokens: int,
        provider_name: str,
    ) -> str:

        if client is None:
            raise RuntimeError(
                f"{provider_name} غير مضبوط."
            )

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
    # تحديد هل الخطأ مناسب للانتقال إلى fallback
    # =========================================================

    def _is_retryable_error(
        self,
        error: Exception,
    ) -> bool:

        text = str(
            error
        ).lower()

        retryable_markers = [
            "429",
            "rate limit",
            "rate_limit",
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
            for marker in retryable_markers
        )

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
        # 1. OpenRouter
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

                # إذا الخطأ ليس rate limit أو provider error
                # ما زلنا نسمح بـ Gemini كاحتياط
                pass

        # =====================================================
        # 2. Gemini fallback
        # يدعم النص والصور
        # =====================================================

        if self.gemini_client is not None:

            try:

                model = (
                    self.gemini_vision_model
                    if image_bytes is not None
                    else self.gemini_text_model
                )

                return self._call_provider(
                    client=self.gemini_client,
                    model=model,
                    chat_messages=chat_messages,
                    max_output_tokens=max_output_tokens,
                    provider_name="Gemini",
                )

            except Exception as exc:

                errors.append(
                    f"Gemini: {exc}"
                )

        # =====================================================
        # 3. Groq fallback
        # حاليًا للنص فقط
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
        # فشل الجميع
        # =====================================================

        if errors:

            clean_errors = "\n".join(
                errors
            )

            raise RuntimeError(
                "تعذر الحصول على إجابة من مزودي الذكاء الاصطناعي.\n"
                f"{clean_errors}"
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
            "تحويل الصوت غير متاح حاليًا "
            "في هذا المسار."
        )
