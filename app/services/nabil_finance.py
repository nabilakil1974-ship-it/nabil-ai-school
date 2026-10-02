"""NABIL AI internal cost ledger and budget guard.
This is cost accounting, not a payment processor. Prices are configured only by env.
Unknown provider prices are never invented.
"""
from __future__ import annotations
import os, sqlite3, time, uuid
from pathlib import Path
from typing import Optional
from fastapi import HTTPException

DB_PATH = Path(os.getenv("NABIL_CONTROL_DB", "data/nabil_control.db"))
DAILY_AI_BUDGET_USD = float(os.getenv("NABIL_DAILY_AI_BUDGET_USD", "0"))  # 0 = no hard budget until owner configures one


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(DB_PATH, timeout=10)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("""CREATE TABLE IF NOT EXISTS cost_ledger(
        id TEXT PRIMARY KEY, ts INTEGER NOT NULL, student_hash TEXT,
        event_type TEXT NOT NULL, provider TEXT, model TEXT,
        input_tokens INTEGER NOT NULL DEFAULT 0, output_tokens INTEGER NOT NULL DEFAULT 0,
        cost_usd REAL NOT NULL DEFAULT 0, lesson_id TEXT, cache_hit INTEGER NOT NULL DEFAULT 0,
        metadata TEXT
    )""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_cost_ts ON cost_ledger(ts)")
    return c


def record_event(*, event_type: str, student_hash: str = "", provider: str = "", model: str = "",
                 input_tokens: int = 0, output_tokens: int = 0, cost_usd: float = 0.0,
                 lesson_id: str = "", cache_hit: bool = False, metadata: str = "") -> None:
    c = _conn()
    try:
        c.execute("INSERT INTO cost_ledger VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", (
            uuid.uuid4().hex, int(time.time()), student_hash, event_type, provider, model,
            max(0,int(input_tokens or 0)), max(0,int(output_tokens or 0)), max(0.0,float(cost_usd or 0)),
            lesson_id, 1 if cache_hit else 0, metadata[:2000]))
        c.commit()
    finally:
        c.close()


def today_cost_usd() -> float:
    now = int(time.time()); start = now - (now % 86400)
    c = _conn()
    try:
        return float(c.execute("SELECT COALESCE(SUM(cost_usd),0) FROM cost_ledger WHERE ts>=?", (start,)).fetchone()[0] or 0)
    finally:
        c.close()


def assert_ai_budget_available() -> None:
    if DAILY_AI_BUDGET_USD > 0 and today_cost_usd() >= DAILY_AI_BUDGET_USD:
        raise HTTPException(status_code=503, detail="تم بلوغ سقف كلفة الذكاء الاصطناعي اليومي. المحتوى الذهبي المحفوظ يبقى متاحًا.")
