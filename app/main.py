from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine
from app.api import routes_health, routes_chat

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


@app.get("/")
def root():
    return {"message": "NabilAI backend يعمل بنجاح 🎓"}
