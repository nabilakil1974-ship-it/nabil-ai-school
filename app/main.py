from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import text

from app.core.config import settings
from app.db.session import Base, engine

# Import models before create_all so SQLAlchemy knows all tables.
from app.db import models  # noqa: F401
from app.db import student_learning  # noqa: F401
from app.db import subscription  # noqa: F401

from app.api import (
    routes_health,
    routes_chat,
    routes_admin,
    routes_student,
    routes_platform_admin,
)


with engine.connect() as conn:
    try:
        conn.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )
        )
        conn.commit()
    except Exception:
        # SQLite/local development does not support pgvector extension.
        pass


if settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
    with open(
        "drive_service_account.json",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            settings.GOOGLE_DRIVE_CREDENTIALS_JSON
        )


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title=settings.PROJECT_NAME
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    routes_health.router,
    prefix="/api",
    tags=["health"],
)

app.include_router(
    routes_chat.router,
    prefix="/api",
    tags=["chat"],
)

# IMPORTANT:
# routes_admin v9 already contains /admin and /api/admin/summary.
# Therefore it must NOT receive an additional /api prefix here.
app.include_router(
    routes_admin.router,
)

app.include_router(
    routes_student.router,
    prefix="/api",
    tags=["student"],
)

app.include_router(
    routes_platform_admin.router,
    prefix="/api/admin",
    tags=["platform-admin"],
)


@app.get("/")
def root():
    return FileResponse(
        "app/static/chat.html"
    )


@app.get("/dashboard")
def student_dashboard_page():
    return FileResponse(
        "app/static/student_dashboard.html"
    )
