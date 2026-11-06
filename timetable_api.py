"""Lightweight standalone API for school timetable analysis."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
from app.api import routes_timetable

app = FastAPI(title="NABIL School Timetable Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes_timetable.router, prefix="/api")

@app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
def school_app():
    index = Path(__file__).parent / "timetable" / "index.html"
    if not index.is_file():
        return {"error": "NABIL school interface is not installed"}
    return FileResponse(index, media_type="text/html; charset=utf-8")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NABIL timetable analyzer", "nabil_engine_configured": bool(os.getenv("NABIL_EXECUTIVE_API_URL") and os.getenv("NABIL_EXECUTIVE_API_KEY"))}

# Anonymous, aggregate usage analytics for the timetable app.
# Render's free filesystem is ephemeral: set NABIL_ANALYTICS_DB to a persistent
# mounted path if one is configured later (for example /var/data/analytics.sqlite3).
import hashlib
import re
import sqlite3
from datetime import datetime, timezone

ANALYTICS_DB = os.getenv("NABIL_ANALYTICS_DB", "/tmp/nabil_timetable_analytics.sqlite3")

def _analytics_connection():
    conn = sqlite3.connect(ANALYTICS_DB, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=10000")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS analytics_visitors (
            visitor_hash TEXT PRIMARY KEY,
            first_seen TEXT NOT NULL,
            last_seen TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS analytics_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_hash TEXT NOT NULL,
            visited_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS analytics_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_hash TEXT NOT NULL,
            event_type TEXT NOT NULL,
            school_hash TEXT,
            created_at TEXT NOT NULL
        );
    """)
    return conn

def _visitor_hash(visitor_id: str) -> str:
    value = str(visitor_id or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9-]{16,80}", value):
        raise ValueError("معرّف الزائر غير صالح")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

@app.post("/api/analytics/visit")
def analytics_visit(payload: dict):
    try:
        visitor = _visitor_hash(payload.get("visitor_id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    now = datetime.now(timezone.utc).isoformat()
    with _analytics_connection() as conn:
        conn.execute(
            "INSERT INTO analytics_visitors(visitor_hash,first_seen,last_seen) VALUES(?,?,?) "
            "ON CONFLICT(visitor_hash) DO UPDATE SET last_seen=excluded.last_seen",
            (visitor, now, now),
        )
        conn.execute(
            "INSERT INTO analytics_visits(visitor_hash,visited_at) VALUES(?,?)",
            (visitor, now),
        )
    return {"ok": True}

@app.post("/api/analytics/event")
def analytics_event(payload: dict):
    try:
        visitor = _visitor_hash(payload.get("visitor_id"))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    event_type = str(payload.get("event_type") or "").strip()
    if event_type != "schedule_created":
        raise HTTPException(status_code=400, detail="نوع الحدث غير مدعوم")
    school_name = str(payload.get("school_name") or "").strip()[:200]
    school_hash = hashlib.sha256(school_name.casefold().encode("utf-8")).hexdigest() if school_name else None
    now = datetime.now(timezone.utc).isoformat()
    with _analytics_connection() as conn:
        conn.execute(
            "INSERT INTO analytics_visitors(visitor_hash,first_seen,last_seen) VALUES(?,?,?) "
            "ON CONFLICT(visitor_hash) DO UPDATE SET last_seen=excluded.last_seen",
            (visitor, now, now),
        )
        conn.execute(
            "INSERT INTO analytics_events(visitor_hash,event_type,school_hash,created_at) VALUES(?,?,?,?)",
            (visitor, event_type, school_hash, now),
        )
    return {"ok": True}

@app.get("/api/analytics/summary")
def analytics_summary():
    with _analytics_connection() as conn:
        visitors = conn.execute("SELECT COUNT(*) FROM analytics_visitors").fetchone()[0]
        visits = conn.execute("SELECT COUNT(*) FROM analytics_visits").fetchone()[0]
        schedules = conn.execute("SELECT COUNT(*) FROM analytics_events WHERE event_type='schedule_created'").fetchone()[0]
        schools = conn.execute("SELECT COUNT(DISTINCT school_hash) FROM analytics_events WHERE school_hash IS NOT NULL").fetchone()[0]
        updated = conn.execute("SELECT MAX(created_at) FROM analytics_events").fetchone()[0]
    return {
        "unique_visitors": visitors,
        "visits": visits,
        "schedules_created": schedules,
        "schools_used": schools,
        "updated_at": updated,
        "storage_note": "تُحفظ الإحصاءات على مساحة الخدمة الحالية وقد تُصفّر عند إعادة تشغيل/نشر الخدمة على الخطة المجانية."
    }


# Serve the school-facing web app from the same public Render URL.
# Keep this mount last so it cannot shadow the /api routes above.
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "timetable"), html=True), name="school-timetable")
