"""Low-cost abuse protection for NABIL AI student endpoints.
No external service required. No raw IP addresses are persisted.
"""
from __future__ import annotations
import hashlib, os, sqlite3, threading, time
from pathlib import Path
from fastapi import HTTPException, Request

DB_PATH = Path(os.getenv("NABIL_CONTROL_DB", "data/nabil_control.db"))
MAX_MESSAGES_PER_MINUTE = int(os.getenv("NABIL_MESSAGES_PER_MINUTE", "12"))
MAX_MESSAGE_CHARS = int(os.getenv("NABIL_MAX_MESSAGE_CHARS", "4000"))
MAX_UPLOAD_BYTES = int(os.getenv("NABIL_MAX_UPLOAD_BYTES", str(12 * 1024 * 1024)))
_LOCK = threading.Lock()


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=10)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("CREATE TABLE IF NOT EXISTS rate_events (bucket TEXT NOT NULL, ts INTEGER NOT NULL)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_rate_bucket_ts ON rate_events(bucket,ts)")
    return c


def _fingerprint(request: Request, student_id: str) -> str:
    forwarded = request.headers.get("x-forwarded-for", "").split(",")[0].strip()
    peer = forwarded or (request.client.host if request.client else "unknown")
    salt = os.getenv("NABIL_SECURITY_SALT", "nabil-ai-runtime")
    return hashlib.sha256(f"{salt}|{student_id}|{peer}".encode()).hexdigest()


def enforce_student_request(request: Request, student_id: str, message: str | None) -> str:
    text = str(message or "")
    if len(text) > MAX_MESSAGE_CHARS:
        raise HTTPException(status_code=413, detail=f"الرسالة طويلة جدًا. الحد الأقصى {MAX_MESSAGE_CHARS} حرفًا.")
    bucket = _fingerprint(request, str(student_id or "anonymous"))
    now = int(time.time()); cutoff = now - 60
    with _LOCK:
        c = _conn()
        try:
            c.execute("DELETE FROM rate_events WHERE ts < ?", (now - 3600,))
            count = c.execute("SELECT COUNT(*) FROM rate_events WHERE bucket=? AND ts>=?", (bucket, cutoff)).fetchone()[0]
            if count >= MAX_MESSAGES_PER_MINUTE:
                raise HTTPException(status_code=429, detail="عدد الطلبات مرتفع. انتظر قليلًا ثم أعد المحاولة.", headers={"Retry-After":"10"})
            c.execute("INSERT INTO rate_events(bucket,ts) VALUES(?,?)", (bucket, now)); c.commit()
        finally:
            c.close()
    return bucket


def enforce_upload_size(size: int | None) -> None:
    if size is not None and size > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="حجم الملف أكبر من الحد المسموح.")
