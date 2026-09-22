import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from starlette.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.core.config import settings
from app.db.session import Base, engine

# ==========================================================
# Logging configuration
# ==========================================================
#
# Without this, custom loggers such as "nabil_ai.lesson" (used for the
# LESSON_TIMING diagnostic line that reports rag_ms/primary_ai_ms/
# practice_repair_ai_ms/total_ms per request) have NO handler attached and
# INFO-level messages are silently dropped - Uvicorn's default logging setup
# (started with no log_config in scripts/start_server.py) only configures
# its OWN loggers (uvicorn, uvicorn.access, uvicorn.error), not the root
# logger or any app-defined logger. This meant the per-phase timing
# instrumentation that already existed in the code was almost certainly
# never actually reaching Railway's log viewer at all - there was no way to
# see WHICH phase (book retrieval, the AI call itself, or a repair pass) was
# responsible for an unusually long request, only the end-user-visible total
# wait. Configuring the root logger here makes every existing
# logger.info(...) call in the app (not just this one) actually show up in
# Railway logs, searchable by prefix (e.g. "LESSON_TIMING").
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


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
    routes_textbook_pages,
    routes_research,
    routes_worksheet,
    routes_interactive_lessons,
    routes_lesson_export,
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

# The large legacy lesson HTML is several MB: compress the delivered page and
# JSON lessons on capable browsers without changing their semantics.
app.add_middleware(GZipMiddleware, minimum_size=4096, compresslevel=4)


# ==========================================================
# API routers
# ==========================================================

app.include_router(
    routes_health.router,
    prefix="/api",
    tags=["health"],
)

app.include_router(routes_textbook_pages.router, prefix="/api", tags=["textbook-pages"])

app.include_router(
    routes_chat.router,
    prefix="/api",
    tags=["chat"],
)

app.include_router(routes_research.router, prefix="/api")
app.include_router(routes_worksheet.router, prefix="/api")
app.include_router(routes_interactive_lessons.router, prefix="/api")
app.include_router(routes_lesson_export.router, prefix="/api")

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

def _build_root_html() -> str:
    """Read app/static/chat.html and apply the fixed set of server-side
    patches (retiring legacy scripts, injecting theme CSS/JS, speech-pace
    patches) that used to run on EVERY request to "/". chat.html is a
    static file only ever changed by a new deploy (nothing in this codebase
    writes to it at runtime), so this transform's result is identical for
    the lifetime of the process - computing it once here at import time and
    caching the result removes a real per-request cost (multiple .find/
    .replace/.lower passes over a ~5.6 MB string) that was previously paid
    on every single page load, including the two full-string .lower() calls
    used only to locate </head> and </body> case-insensitively.

    Inject ONLY at the real final closing body tag. Never use str.replace:
    the large legacy HTML embeds literal "</body>" in JavaScript templates;
    replacing all of them splits <script> blocks and displays raw JS to users.
    """
    html = Path("app/static/chat.html").read_text(encoding="utf-8")
    # Retire the previous client-only XP/mastery simulation. Its old click-
    # counters and text heuristics were not learning assessments and must not
    # keep running alongside the evidence-based learning dock.
    legacy_start = html.find('<script id="nabilV130Script">')
    if legacy_start >= 0:
        legacy_end = html.find("</script>", legacy_start)
        if legacy_end < 0:
            raise RuntimeError("Legacy learning script is incomplete")
        html = html[:legacy_start] + html[legacy_end + len("</script>"):]
    # The owner retired BOTH introductory screens. Keep all lesson controls,
    # chat, image upload, avatar and microphone, but enter the real lesson page
    # directly. The obsolete gateway is an isolated ~2 MB inline script with
    # an embedded base64 avatar; removing it also reduces HTML transfer.
    gateway_marker = '<script id="nabil-v105-startup-script">'
    gateway_start = html.find(gateway_marker)
    if gateway_start >= 0:
        gateway_end = html.find("</script>", gateway_start)
        if gateway_end < 0:
            raise RuntimeError("Obsolete welcome gateway script is incomplete")
        html = html[:gateway_start] + html[gateway_end + len("</script>"):]

    # Retire the giant robot/grade-picker splash without deleting the actual
    # lesson DOM: legacy lesson controls still refer to nabilHome internally.
    # The guard prevents its onload/bootstrap from relocking page scroll.
    home_bootstrap = "function bootstrapNabilHome(){"
    if home_bootstrap not in html:
        raise RuntimeError("NABIL legacy splash bootstrap not found")
    html = html.replace(
        home_bootstrap,
        "function bootstrapNabilHome(){ return; // splash retired\n",
        1,
    )

    # In open exercise mode detect the language of the actual question,
    # not the currently selected lesson dropdown. Keep lesson-mode untouched.
    send_start = html.find("async function sendToAI(")
    if send_start < 0:
        raise RuntimeError("Legacy chat sendToAI was not found")
    language_old = (
        '    const language =\n'
        '        languageSelect.value || "العربية";'
    )
    language_new = (
        '    const language =\n'
        '        generalExercisesMode\n'
        '        ? (detectMessageRenderLanguage(showStudentMessage ? message : (nabilCurrentQuestionText || message)) || "العربية")\n'
        '        : (languageSelect.value || "العربية");'
    )
    before_send, after_send = html[:send_start], html[send_start:]
    if language_old not in after_send:
        raise RuntimeError("Open tutor language selector anchor was not found")
    html = before_send + after_send.replace(language_old, language_new, 1)

    # Use a single student-configurable speech pace in the lesson AND landing
    # tutor. This patches the two legacy speech engines at response time,
    # without loading the 5.6 MB legacy HTML in another GitHub commit.
    pace_browser = '    u.rate = 0.90;'
    pace_browser_new = ('    u.rate = Math.max(0.70, Math.min(1.15, '
                        'Number(window.nabilVoicePace || 0.90)));')
    if pace_browser not in html:
        raise RuntimeError("NABIL browser TTS pace anchor is missing")
    html = html.replace(pace_browser, pace_browser_new, 1)
    pace_neural = '        nabilNeuralAudio = audio;'
    pace_neural_new = (pace_neural + '\n        audio.playbackRate = Math.max(0.70, Math.min(1.15, '
                   'Number(window.nabilVoicePace || 0.90)));')
    if pace_neural not in html:
        raise RuntimeError("NABIL neural TTS pace anchor is missing")
    html = html.replace(pace_neural, pace_neural_new, 1)

    # Preserve the blue robot as the only home; hide the separate welcome gateway.
    direct_entry_css = (
        "<style id='nabil-direct-lesson-entry'>"
        "#nabilProfessorGateway{display:none!important}"
        "body.nabil-home-lock{overflow:hidden!important}"
        "</style>"
    )
    head_boundary = html.lower().find("</head>")
    if head_boundary < 0:
        raise RuntimeError("NABIL chat page has no closing head tag")
    theme_css = '<link rel="stylesheet" href="/static/nabil_reference_theme.css?v=19">'
    html = html[:head_boundary] + direct_entry_css + theme_css + html[head_boundary:]

    scripts = (
        '<script src="/static/curriculum_strict.js?v=138"></script>\n'
        '<script src="/static/nabil_learning_v132.js?v=138"></script>\n'
        '<script src="/static/nabil_worksheet_v1.js?v=5"></script>\n'
        '<script src="/static/nabil_lesson_worksheet_card_v1.js?v=1"></script>\n'
        '<script src="/static/nabil_drive_prepared_lesson_v1.js?v=3"></script>\n'
        '<script src="/static/nabil_voice_v133.js?v=133"></script>\n'
        '<script src="/static/nabil_open_tutor_v1.js?v=18"></script>\n'
        '<script src="/static/nabil_ionic_diagram_fix.js?v=1"></script>\n'
        '<script src="/static/nabil_research_v1.js?v=2"></script>\n'
        '<script src="/static/nabil_book_first_preview_v1.js?v=8"></script>\n'
        '<script src="/static/nabil_universal_language_v1.js?v=1"></script>\n'
        '<script src="/static/nabil_drive_home_requests_v1.js?v=5"></script>\n'
        '<script src="/static/nabil_universal_lesson_actions_v1.js?v=1"></script>\n'
    )
    boundary = html.lower().rfind("</body>")
    if boundary < 0:
        raise RuntimeError("NABIL chat page has no closing body tag")
    # Experimental virtual laboratories stay on /labs, not on the main student platform.
    html = html[:boundary] + scripts + html[boundary:]
    return html


# Computed once per process at import time, not per request. chat.html is
# static (see _build_root_html's docstring), so every request can safely
# share this one cached string instead of re-running ~7 full-file string
# scans on every page load.
_CACHED_ROOT_HTML = _build_root_html()


@app.get("/")
def root():
    return HTMLResponse(_CACHED_ROOT_HTML, headers={"Cache-Control": "no-store"})


@app.get("/dashboard")
def student_dashboard_page():
    return FileResponse(
        "app/static/student_dashboard.html"
    )


@app.get("/labs")
def nabil_virtual_labs_page():
    """Standalone, shareable multilingual math, chemistry and optics labs."""
    return FileResponse("app/static/nabil_labs.html", media_type="text/html")


@app.get("/labs/secondary-physics")
def nabil_secondary_physics_lab():
    """Public experimental physics prototype, separate from the student platform."""
    return FileResponse(
        "app/static/nabil_secondary_physics_lab.html",
        media_type="text/html",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/labs/chemistry")
def nabil_full_chemistry_lab():
    """Full original chemistry virtual lab; independent student demo."""
    return FileResponse("app/static/nabil_lab_chemistry_full.html",
                        media_type="text/html", headers={"Cache-Control": "no-store"})


@app.get("/labs/light")
def nabil_full_light_lab():
    """Full original light and lenses virtual lab."""
    return FileResponse("app/static/nabil_lab_light_full.html",
                        media_type="text/html", headers={"Cache-Control": "no-store"})


@app.get("/labs/math")
def nabil_full_math_lab():
    """Full original three-language vector and line virtual lab."""
    return FileResponse("app/static/nabil_lab_math_full.html",
                        media_type="text/html", headers={"Cache-Control": "no-store"})

