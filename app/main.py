from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import text

from app.core.config import settings
from app.db.session import Base, engine
from app.api import routes_health, routes_chat, routes_admin

# يفعّل امتداد pgvector بقاعدة البيانات (لازم يصير قبل إنشاء جدول book_chunks)
with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()

# يكتب ملف مفتاح Google Drive من المتغير السري (إذا موجود) عشان سكربت
# الفهرسة يقدر يستخدمه - هيك ما بنرفع الملف السري نفسه عGitHub
if settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
    with open("drive_service_account.json", "w", encoding="utf-8") as f:
        f.write(settings.GOOGLE_DRIVE_CREDENTIALS_JSON)

# ينشئ الجداول تلقائياً أول مرة (لاحقاً رح نستبدلها بـ Alembic migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # لاحقاً رح نحصرها بدومين الموقع فقط
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_health.router, prefix="/api", tags=["health"])
app.include_router(routes_chat.router, prefix="/api", tags=["chat"])
app.include_router(routes_admin.router, prefix="/api", tags=["admin"])

@app.on_event("startup")
def preload_embedding_model():
    print("⏳ تحميل موديل الفهم اللغوي (مرة وحدة فقط)...")
    from app.services.rag_search import get_model
    get_model()
    print("✅ الموديل جاهز بالذاكرة.")


@app.get("/")
def root():
    return {"message": "NabilAI backend يعمل بنجاح 🎓"}


@app.get("/admin")
def admin_page():
    return FileResponse("app/static/admin.html")
