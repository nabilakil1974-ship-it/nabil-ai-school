import base64
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text

from google import genai
from google.genai import types

from app.core.config import settings
from app.db.session import Base, engine
from app.api import routes_health, routes_chat, routes_admin

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

if settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
    with open("drive_service_account.json", "w", encoding="utf-8") as f:
        f.write(settings.GOOGLE_DRIVE_CREDENTIALS_JSON)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router, prefix="/api", tags=["health"])
app.include_router(routes_chat.router, prefix="/api", tags=["chat"])
app.include_router(routes_admin.router, prefix="/api", tags=["admin"])

client = genai.Client(api_key=settings.GEMINI_API_KEY)

class ImageChatRequest(BaseModel):
    student_id: str
    conversation_id: Optional[str] = None
    message: str
    image: Optional[str] = None
    subject: Optional[str] = "رياضيات"
    grade: Optional[str] = "الصف السابع"
    curriculum: Optional[str] = "CRDP"

@app.post("/api/chat-with-image")
async def chat_with_image_endpoint(req: ImageChatRequest):
    try:
        contents = []
        if req.image:
            header, encoded = req.image.split(",", 1) if "," in req.image else ("", req.image)
            image_bytes = base64.b64decode(encoded)
            mime_type = "image/png" if "png" in header else "image/webp" if "webp" in header else "image/jpeg"
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

        prompt_text = f"""
        أنت "الأستاذ نبيل"، مدرس خبير في المنهج اللبناني الرسمي (CRDP).
        المادة: {req.subject}، الصف: {req.grade}.
        اشرح المسألة خطوة بخطوة باللغة العربية: {req.message}
        إذا طلب رسماً هندسياً أو شكلاً، ادرج في نهاية ردك كود SVG صالح وبسيط ليعرض على البروجكتور.
        """
        contents.append(prompt_text)

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="أنت أستاذ لبناني ودي، تشرح بوضوح حسب المنهج اللبناني (CRDP)، وترسم الأشكال الهندسية بدقة عبر كود SVG."
            )
        )

        return {
            "conversation_id": req.conversation_id or "conv_123",
            "reply": response.text
        }
    except Exception as e:
        print(f"Error: {e}")
        return {
            "conversation_id": req.conversation_id or "conv_123",
            "reply": "أهلاً بك يا بطل! حدث ضغط مؤقت، أعد إرسال السؤال وسأجيبك فوراً!"
        }

@app.get("/")
def root():
    return FileResponse("app/static/chat.html")

@app.get("/admin")
def admin_page():
    return FileResponse("app/static/admin.html")
