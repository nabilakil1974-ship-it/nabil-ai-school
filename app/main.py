import os
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from groq import Groq

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

def get_groq_client():
    if not settings.GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="مفتاح GROQ_API_KEY غير معرّف في النظام!")
    return Groq(api_key=settings.GROQ_API_KEY)

class ImageChatRequest(BaseModel):
    student_id: str
    conversation_id: Optional[str] = None
    message: str
    image: Optional[str] = None
    subject: Optional[str] = "رياضيات"
    grade: Optional[str] = "الصف السابع"
    language: Optional[str] = "العربية"
    curriculum: Optional[str] = "CRDP"

@app.post("/api/chat-with-image")
async def chat_with_image_endpoint(req: ImageChatRequest):
    try:
        client = get_groq_client()
        
        system_instruction = (
            "أنت الأستاذ نبيل، أستاذ لبناني خبير وودي، تشرح بوضوح وبدون تعقيد، "
            "وتلتزم حصرياً بالهيكلية المنهجية المعتمدة (المعطيات، القاعدة، الحل خطوة بخطوة، "
            "والمصطلحات الأجنبية) وفق المنهج اللبناني الرسمي (CRDP)."
        )

        prompt_text = f"""
        {system_instruction}
        
        الصف: {req.grade} | المادة: {req.subject} | لغة الشرح المطلوبة: {req.language}.
        
        يجب أن تلتزم التزاماً تاماً بالهيكلية التالية في إجابتك:
        1. المعطيات (Given / Données).
        2. القاعدة أو القانون (Formula / Formule).
        3. التطبيق والحل خطوة بخطوة (Step-by-Step Solution).
        4. المصطلحات والمفاتيح باللغة الأجنبية (Keywords).

        سؤال الطالب أو نص المسألة المرفقة:
        {req.message if req.message else "اشرح وحل هذه المسألة بالتفصيل المنهجي"}
        """

        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt_text}
        ]

        completion = client.chat.completions.create(
            model="meta-llama/llama-3.2-11b-vision-preview",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )

        reply_text = completion.choices[0].message.content

        return {
            "conversation_id": req.conversation_id or "conv_123",
            "reply": reply_text if reply_text else "عذراً، لم أستطع توليد الإجابة."
        }

    except Exception as e:
        err_str = str(e)
        print(f"Error encountered: {err_str}")
        return {
            "conversation_id": req.conversation_id or "conv_123",
            "reply": f"عذراً يا بطل، حدث خطأ تقني في المعالجة: {err_str}"
        }

@app.get("/")
def root():
    return FileResponse("app/static/chat.html")

@app.get("/admin")
def admin_page():
    return FileResponse("app/static/admin.html")
