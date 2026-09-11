from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.core.config import settings
from app.db.session import Base, engine
from app.api import routes_health, routes_chat, routes_admin


# =========================================================
# Database
# =========================================================

with engine.connect() as conn:
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()


# =========================================================
# Google Drive credentials
# =========================================================

if settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
    with open(
        "drive_service_account.json",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(settings.GOOGLE_DRIVE_CREDENTIALS_JSON)


# =========================================================
# Create database tables
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# FastAPI application
# =========================================================

app = FastAPI(
    title=settings.PROJECT_NAME
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Static files
# مهم جداً:
# هذا يجعل الصور والملفات الموجودة داخل app/static
# متاحة من خلال /static
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# =========================================================
# API Routes
# =========================================================

app.include_router(
    routes_health.router,
    prefix="/api",
    tags=["health"]
)

app.include_router(
    routes_chat.router,
    prefix="/api",
    tags=["chat"]
)

app.include_router(
    routes_admin.router,
    prefix="/api",
    tags=["admin"]
)


# =========================================================
# Main page
# =========================================================

@app.get("/")
def root():
    return FileResponse("app/static/chat.html")
