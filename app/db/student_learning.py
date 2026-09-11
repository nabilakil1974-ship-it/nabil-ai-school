import json
from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.db.session import Base


class StudentLearningProfile(Base):
    __tablename__ = "student_learning_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(255), unique=True, nullable=False, index=True)

    current_grade = Column(String(100), nullable=True)
    current_branch = Column(String(100), nullable=True)
    current_subject = Column(String(120), nullable=True)
    current_lesson = Column(String(255), nullable=True)

    lessons_studied_json = Column(Text, nullable=False, default="[]")
    strengths_json = Column(Text, nullable=False, default="[]")
    weaknesses_json = Column(Text, nullable=False, default="[]")
    frequent_mistakes_json = Column(Text, nullable=False, default="[]")
    concepts_to_review_json = Column(Text, nullable=False, default="[]")
    test_results_json = Column(Text, nullable=False, default="[]")

    overall_progress_percent = Column(Float, nullable=False, default=0.0)
    mastered_lessons_count = Column(Integer, nullable=False, default=0)
    total_learning_minutes = Column(Integer, nullable=False, default=0)
    interaction_count = Column(Integer, nullable=False, default=0)

    last_active_activity = Column(String(500), nullable=True)

    trial_started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    trial_ends_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(days=30),
    )

    subscription_status = Column(String(40), nullable=False, default="trial")
    subscription_started_at = Column(DateTime, nullable=True)
    subscription_ends_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    @staticmethod
    def loads_list(value):
        if not value:
            return []

        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except Exception:
            return []

    @staticmethod
    def dumps_list(value):
        safe = value if isinstance(value, list) else []
        return json.dumps(safe, ensure_ascii=False)
