from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.core.config import settings
from app.db.session import Base, engine


# ==========================================================
# Import database models before create_all
# ==========================================================

from app.db import models  # noqa: F401
from app.db import student_learning  # noqa: F401
from app.db import subscription  # noqa: F401
from app.db import ai_usage  # noqa: F401


# ==========================================================
# API routers
# ==========================================================

from app.api import (
    routes_health,
    routes_chat,
    routes_admin,
    routes_student,
    routes_platform_admin,
    routes_parent,
)


# ==========================================================
# PostgreSQL extensions
# ==========================================================

with engine.connect() as conn:
    try:
        conn.execute(
            text(
                "CREATE EXTENSION IF NOT EXISTS vector"
            )
        )
        conn.commit()

    except Exception:
        # SQLite/local development does not support pgvector.
        pass


# ==========================================================
# Google Drive credentials
# ==========================================================

if settings.GOOGLE_DRIVE_CREDENTIALS_JSON:
    with open(
        "drive_service_account.json",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(
            settings.GOOGLE_DRIVE_CREDENTIALS_JSON
        )


# ==========================================================
# Safe database migration
# student_learning_profiles
# ==========================================================

def migrate_student_learning_profiles():
    """
    Add missing columns to the existing student learning table.

    This migration:
    - does NOT delete the table
    - does NOT delete student data
    - adds only missing columns
    """

    if engine.dialect.name != "postgresql":
        return

    statements = [
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS current_grade VARCHAR(100)
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS current_branch VARCHAR(100)
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS current_subject VARCHAR(120)
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS current_lesson VARCHAR(255)
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS lessons_studied_json TEXT
        NOT NULL DEFAULT '[]'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS lesson_mastery_json TEXT
        NOT NULL DEFAULT '[]'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS strengths_json TEXT
        NOT NULL DEFAULT '[]'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS weaknesses_json TEXT
        NOT NULL DEFAULT '[]'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS frequent_mistakes_json TEXT
        NOT NULL DEFAULT '[]'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS concepts_to_review_json TEXT
        NOT NULL DEFAULT '[]'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS test_results_json TEXT
        NOT NULL DEFAULT '[]'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS overall_progress_percent
        DOUBLE PRECISION NOT NULL DEFAULT 0.0
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS mastered_lessons_count
        INTEGER NOT NULL DEFAULT 0
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS total_learning_minutes
        INTEGER NOT NULL DEFAULT 0
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS interaction_count
        INTEGER NOT NULL DEFAULT 0
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS last_active_activity VARCHAR(500)
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS trial_started_at
        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS trial_ends_at TIMESTAMP
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS subscription_status
        VARCHAR(40) NOT NULL DEFAULT 'trial'
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS subscription_started_at TIMESTAMP
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS subscription_ends_at TIMESTAMP
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS created_at
        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        """,
        """
        ALTER TABLE student_learning_profiles
        ADD COLUMN IF NOT EXISTS updated_at
        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        """,
    ]

    with engine.begin() as conn:

        # Check whether the table already exists.
        table_exists = conn.execute(
            text(
                """
                SELECT to_regclass(
                    'public.student_learning_profiles'
                )
                """
            )
        ).scalar()

        # Fresh database:
        # create_all below will create the complete table.
        if not table_exists:
            return

        # Add only missing columns.
        for statement in statements:
            conn.execute(
                text(statement)
            )

        # Existing students without a trial end date
        # receive a 30-day trial period.
        conn.execute(
            text(
                """
                UPDATE student_learning_profiles
                SET trial_ends_at =
                    COALESCE(
                        trial_ends_at,
                        trial_started_at
                        + INTERVAL '30 days'
                    )
                WHERE trial_ends_at IS NULL
                """
            )
        )


migrate_student_learning_profiles()


# ==========================================================
# Create database tables
# ==========================================================

# SQLAlchemy now knows:
# - existing application models
# - student_learning
# - subscription
# - ai_usage

Base.metadata.create_all(
    bind=engine
)


# ==========================================================
# FastAPI application
# ==========================================================

app = FastAPI(
    title=settings.PROJECT_NAME
)


# ==========================================================
# Static files
# ==========================================================

app.mount(
    "/static",
    StaticFiles(
        directory="app/static"
    ),
    name="static",
)


# ==========================================================
# CORS
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================================
# API routers
# ==========================================================

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

# routes_admin already contains:
# /admin
# /api/admin/summary
#
# Therefore DO NOT add another /api prefix.
app.include_router(
    routes_admin.router,
)

app.include_router(
    routes_student.router,
    prefix="/api",
    tags=["student"],
)

# Parent / guardian educational monitoring API.
# routes_parent contains:
# /parent/student
# /parent/progress
#
# Final endpoints become:
# /api/parent/student
# /api/parent/progress
app.include_router(
    routes_parent.router,
    prefix="/api",
    tags=["parent"],
)

app.include_router(
    routes_platform_admin.router,
    prefix="/api/admin",
    tags=["platform-admin"],
)


# ==========================================================
# Web pages
# ==========================================================

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
