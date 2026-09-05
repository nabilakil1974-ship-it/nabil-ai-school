import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text

# استيراد مكتبة Gemini الرسمية google-genai
from google import genai
from google.genai import types

from app.core.config import settings
from app.db.session import Base, engine
from app.api import routes_health, routes_chat, routes_admin

# يفعّل امتداد pgvector بقاعدة البيانات
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

# يكتب ملف مفتاح Google Drive من المتغير السري (إذا موجود)
if settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
    with open("drive_service_account.json", "w", encoding="utf-8") as f:
        f.write(settings.GOOGLE_DRIVE_CREDENTIALS_JSON)

# ينشئ الجداول تلقائياً أول مرة
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

# تهيئة عميل Gemini مع تمرير مفتاح البيئة صراحةً
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
            
            mime_type = "image/jpeg"
            if "png" in header:
                mime_type = "image/png"
            elif "webp" in header:
                mime_type = "image/webp"

            contents.append(
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                )
            )

        prompt_text = f"""
        أنت "الأستاذ نبيل"، مدرس خبير في المنهج اللبناني الرسمي (CRDP).
        المادة: {req.subject}، الصف: {req.grade}.
        مهمتك هي قراءة المسألة من الصورة (أو النص) وحلها بأسلوب تربوي مبسط، خطوة بخطوة باللغة العربية:
        {req.message}
        """
        contents.append(prompt_text)

        # استخدام موديل الفلاش القياسي المدعوم للرؤية والنصوص
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction="أنت أستاذ لبناني ودي، تشرح بوضوح وبدون تعقيد، وتراعي المنهج اللبناني."
            )
        )

        return {
            "conversation_id": req.conversation_id or "conv_123",
            "reply": response.text
        }

    except Exception as e:
        print(f"Error handling image chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
def preload_embedding_model():
    print("⏳ تحميل موديل الفهم اللغوي (مرة وحدة فقط)...")
    try:
        from app.services.rag_search import get_model
        get_model()
        print("✅ الموديل جاهز بالذاكرة.")
    except Exception as e:
        print(f"⚠️ ملاحظة حول تحميل الموديل: {e}")

@app.get("/")
def root():
    return FileResponse("app/static/chat.html")

@app.get("/admin")
def admin_page():
    return FileResponse("app/static/admin.html")
