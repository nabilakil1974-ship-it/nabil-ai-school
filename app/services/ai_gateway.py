import base64
from typing import Optional

from openai import OpenAI

from app.core.config import settings


class NabilAIGateway:

    def __init__(self):

        api_key = getattr(
            settings,
            "OPENROUTER_API_KEY",
            "",
        )

        if not api_key:

            raise RuntimeError(
                "OPENROUTER_API_KEY غير مضبوط في إعدادات السيرفر"
            )

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

        self.text_model = "openrouter/free"
        self.vision_model = "google/gemma-4-26b-a4b-it:free"


    def _extract_content(
        self,
        response
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

            return "\n".join(
                parts
            ).strip()

        return ""


    def generate(
        self,
        instructions: str,
        messages: list[dict],
        image_bytes: Optional[bytes] = None,
        image_mime_type: str = "image/jpeg",
        max_output_tokens: int = 2500,
    ) -> str:

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
                                "حدد أولًا نوع المحتوى. "
                                "إذا كانت الصورة سؤالًا أو تمرينًا، "
                                "استخرج السؤال كما هو ثم حلّه "
                                "خطوة خطوة. "
                                "إذا كانت الصورة صفحة درس أو شرحًا، "
                                "استخرج الأفكار والمفاهيم الأساسية "
                                "واشرح الدرس للطالب تدريجيًا. "
                                "إذا كانت الصورة تحتوي على رسم "
                                "أو جدول أو مخطط، اقرأه واشرحه "
                                "بدقة. "
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


        try:

            response = (
                self.client
                .chat
                .completions
                .create(
                    model=(
                        self.vision_model
                        if image_bytes is not None
                        else self.text_model
                    ),
                    messages=chat_messages,
                    max_tokens=max_output_tokens,
                )
            )

        except Exception as exc:

            raise RuntimeError(
                f"خطأ في الاتصال بـ OpenRouter: {exc}"
            ) from exc


        content = self._extract_content(
            response
        )


        if content:

            return content


        raise RuntimeError(
            "NABIL AI لم يُرجع إجابة نصية."
        )


    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "voice.webm",
    ) -> str:

        raise RuntimeError(
            "تحويل الصوت غير متاح حاليًا "
            "في المسار المجاني."
        )
