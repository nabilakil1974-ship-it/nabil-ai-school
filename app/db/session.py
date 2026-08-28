from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# ملاحظة: connect_args خاص فقط بـ SQLite (للتجربة المحلية بدون قاعدة بيانات حقيقية)
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """يُستخدم كـ dependency في كل endpoint يحتاج الوصول لقاعدة البيانات."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
