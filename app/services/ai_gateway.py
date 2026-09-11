import base64
from typing import Optional

from openai import OpenAI

from app.core.config import settings


class NabilAIGateway:
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise RuntimeError(
                "OPENAI_API_KEY غير مضبوط في إعدادات السيرفر"
            )

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.text_model = "gpt-5.6"
        self.vision_model = "gpt-5.6"
        self.transcription_model = "gpt-4o-transcribe"

    def generate(
        self,
        instructions: str,
        messages: list[dict],
        image_bytes: Optional[bytes] = None,
        image_mime_type: str = "image/jpeg",
        max_output_tokens: int = 2000,
    ) -> str:

        input_items = []

        for msg in messages:
            input_items.append(
                {
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                }
            )

        if image_bytes:
            encoded = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            input_items.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "اقرأ الصورة بدقة، واستخرج "
                                "المسألة أو السؤال الموجود فيها "
                                "ثم ساعد الطالب في حله."
                            ),
                        },
                        {
                            "type": "input_image",
                            "image_url": (
                                f"data:{image_mime_type};base64,{encoded}"
                            ),
                        },
                    ],
                }
            )

        response = self.client.responses.create(
            model=(
                self.vision_model
                if image_bytes
                else self.text_model
            ),
            instructions=instructions,
            input=input_items,
            max_output_tokens=max_output_tokens,
        )

        return (response.output_text or "").strip()

    def transcribe(
        self,
        audio_bytes: bytes,
        filename: str = "voice.webm",
    ) -> str:

        result = self.client.audio.transcriptions.create(
            model=self.transcription_model,
            file=(filename, audio_bytes),
        )

        return str(result.text).strip()
