from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
)

from app.db.session import Base


class AIUsageLog(Base):
    __tablename__ = "ai_usage_logs"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    student_id = Column(
        String(255),
        nullable=True,
        index=True,
    )

    grade = Column(
        String(100),
        nullable=True,
    )

    subject = Column(
        String(120),
        nullable=True,
    )

    lesson = Column(
        String(255),
        nullable=True,
    )

    provider = Column(
        String(80),
        nullable=True,
        index=True,
    )

    model = Column(
        String(150),
        nullable=True,
    )

    success = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
    )

    status_code = Column(
        Integer,
        nullable=False,
        default=200,
        index=True,
    )

    error_type = Column(
        String(100),
        nullable=True,
    )

    response_time_ms = Column(
        Float,
        nullable=True,
    )

    cache_hit = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    input_tokens = Column(
        Integer,
        nullable=True,
    )

    output_tokens = Column(
        Integer,
        nullable=True,
    )

    total_tokens = Column(
        Integer,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        index=True,
    )
