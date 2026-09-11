import base64
from typing import Optional

from openai import OpenAI

from app.core.config import settings


class NabilAIGateway:

    def __init__(self):

        api_key = getattr(
            settings,
            "OPENROUTER_API_KEY",
            ""
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
        self.vision_model = "openrouter/free"


    def _extract_content(self, response) -> str:

        if not response:
            return ""

        if not getattr(
            response,
            "choices",
            None
        ):
            return ""

        choice = response.choices[0]

        message = getattr(
            choice,
            "message",
            None
        )

        if message is None:
            return ""

        content = getattr(
            message,
            "content",
            None
        )

        if isinstance(
            content,
            str
        ):

            return content.strip()

        if isinstance(
            content,
            list
        ):

            parts = []

            for item in content:

                if isinstance(
                    item,
                    str
                ):

                    parts.append(item)

                elif isinstance(
                    item,
                    dict
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
        max_output_tokens: int = 2000,
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
                        "user"
                    ),
                    "content": msg.get(
                        "content",
                        ""
                    ),
                }
            )


        if image_bytes:

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
                                "اقرأ الصورة بدقة. "
                                "إذا كانت سؤالًا أو تمرينًا، "
                                "استخرج السؤال وحلّه خطوة خطوة. "
                                "إذا كانت صفحة درس أو شرحًا، "
                                "اشرح محتواها للطالب بطريقة "
                                "واضحة وتفاعلية. "
                                "لا تخترع أي معلومة غير ظاهرة."
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

            response = self.client.chat.completions.create(
                model=(
                    self.vision_model
                    if image_bytes
                    else self.text_model
                ),
                messages=chat_messages,
                max_tokens=max_output_tokens,
            )

        except Exception as e:

            raise RuntimeError(
                f"خطأ في الاتصال بـ OpenRouter: {str(e)}"
            ) from e


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
