import base64
import os
import time
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

# تجمع المفاتيح الذكي لتجاوز حظر الـ 429 تلقائياً
api_keys_pool = []
if settings.GEMINI_API_KEY:
    api_keys_pool.append(settings.GEMINI_API_KEY)

# جلب أي مفاتيح احتياطية إضافية إن وجدت في المتغيرات (مثل GEMINI_API_KEY_2, GEMINI_API_KEY_3)
for i in range(2, 6):
    extra_key = os.environ.get(f"GEMINI_API_KEY_{i}")
    if extra_key:
        api_keys_pool.append(extra_key)

current_key_index = 0

def get_gemini_client():
    global current_key_index
    if not api_keys_pool:
        return genai.Client(api_key=settings.GEMINI_API_KEY)
    key = api_keys_pool[current_key_index]
    return genai.Client(api_key=key)

def rotate_key():
    global current_key_index
    if len(api_keys_pool) > 1:
        current_key_index = (current_key_index + 1) % len(api_keys_pool)
        print(f"🔄 Switched to backup Gemini API Key index: {current_key_index}")

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
    global api_keys_pool
    max_attempts = max(1, len(api_keys_pool) * 2)
    attempt = 0
    
    while attempt < max_attempts:
        try:
            client = get_gemini_client()
            contents = []
            if req.image:
                header, encoded = req.image.split(",", 1) if "," in req.image else ("", req.image)
                image_bytes = base64.b64decode(encoded)
                mime_type = "image/png" if "png" in header else "image/webp" if "webp" in header else "image/jpeg"
                contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

            prompt_text = f"""
            أنت "الأستاذ نبيل"، مدرس خبير ومعتمد في المنهج اللبناني الرسمي (CRDP).
            الصف: {req.grade} | المادة: {req.subject} | لغة الشرح المطلوبة: {req.language}.
            
            يجب أن تلتزم التزاماً تاماً بالهيكلية التالية في إجابتك:
            1. المعطيات (Given / Données).
            2. القاعدة أو القانون (Formula / Formule).
            3. التطبيق والحل خطوة بخطوة (Step-by-Step Solution).
            4. المصطلحات والمفاتيح باللغة الأجنبية (Keywords).

            سؤال الطالب أو نص المسألة المرفقة:
            {req.message if req.message else "اشرح وحل هذه المسألة بالتفصيل المنهجي"}
            """
            contents.append(prompt_text)

            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction="أنت الأستاذ نبيل، أستاذ لبناني خبير وودي، تشرح بوضوح وبدون تعقيد، وتلتزم حصرياً بالهيكلية المنهجية المعتمدة (المعطيات، القاعدة، الحل خطوة بخطوة، والمصطلحات الأجنبية) وفق المنهج اللبناني الرسمي (CRDP)."
                )
            )

            return {
                "conversation_id": req.conversation_id or "conv_123",
                "reply": response.text if response.text else "عذراً، لم أستطع توليد الإجابة."
            }

        except Exception as e:
            err_str = str(e)
            print(f"Error encountered: {err_str}")
            # إذا ظهر خطأ نفاد الحصة (429)، نقوم بتبديل المفتاح أو المحاولة بذكاء لتجاوز العطل
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                rotate_key()
                attempt += 1
                time.sleep(1) # استراحة ثانية قبل إعادة المحاولة بالمفتاح الجديد
                continue
            else:
                return {
                    "conversation_id": req.conversation_id or "conv_123",
                    "reply": f"عذراً يا بطل، حدث خطأ تقني في المعالجة: {err_str}"
                }
                
    return {
        "conversation_id": req.conversation_id or "conv_123",
        "reply": "عذراً يا بطل، لقد استنفدنا الحصة المؤقتة للطلبات. يرجى الانتظار ثوانٍ معدودة والمحاولة مرة أخرى."
    }

@app.get("/")
def root():
    return FileResponse("app/static/chat.html")

@app.get("/admin")
def admin_page():
    return FileResponse("app/static/admin.html")
