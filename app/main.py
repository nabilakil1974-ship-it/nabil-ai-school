from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import text
from app.core.config import settings
from app.db.session import Base, engine
from app.api import routes_health, routes_chat, routes_admin


if settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
    with open("drive_service_account.json", "w", encoding="utf-8") as f:
        f.write(settings.GOOGLE_DRIVE_CREDENTIALS_JSON)

Base.metadata.create_all(bind=engine)

from app.services.rag_search import get_model
print("⏳ تحميل موديل الفهم اللغوي (مرة وحدة فقط)...", flush=True)
get_model()
print("✅ الموديل جاهز بالذاكرة.", flush=True)

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


@app.get("/")
def root():
    return FileResponse("app/static/chat.html")
