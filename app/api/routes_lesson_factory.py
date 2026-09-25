"""Owner-triggered, evidence-gated lesson preparation within NABIL.

The pilot generates locally and is viewable through NABIL after QA. It does
NOT silently publish to Drive or claim a lesson was reviewed by the owner.
Preparation requires a separate server-side owner token, never an AI API key.
"""
from __future__ import annotations

import hmac
import json
import os
import re
import secrets
import subprocess
import sys
import threading
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import FileResponse

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "data" / "nabil_canonical_lesson_catalog.json"
OUT = ROOT / "output"
LOGS = ROOT / "data" / "factory_jobs"
router = APIRouter(prefix="/interactive-lessons/factory", tags=["lesson-factory"])

_guard = threading.Lock()
_jobs: dict[str, dict] = {}


def _authorized(token: str | None) -> None:
    expected = os.getenv("NABIL_FACTORY_OWNER_TOKEN", "").strip()
    if not expected:
        raise HTTPException(503, "FACTORY_OWNER_TOKEN_NOT_CONFIGURED")
    if not token or not hmac.compare_digest(token, expected):
        raise HTTPException(403, "FACTORY_OWNER_AUTH_REQUIRED")


def _entries() -> list[dict]:
    if not CATALOG.is_file():
        raise HTTPException(503, "CANONICAL_CATALOG_NOT_FOUND")
    try:
        entries = json.loads(CATALOG.read_text(encoding="utf-8"))["lessons"]
        if not isinstance(entries, list):
            raise ValueError("invalid catalog list")
    except (KeyError, ValueError, json.JSONDecodeError):
        raise HTTPException(503, "CANONICAL_CATALOG_INVALID")
    # No speculative titles or filenames: only source-locked actual lessons.
    return [e for e in entries if isinstance(e, dict)
            and all(e.get(k) is not None for k in (
                "lesson_id", "canonical_title", "book_id", "grade",
                "subject", "language", "pdf_start_page", "pdf_end_page"))]


def _entry(lesson_id: str) -> dict:
    matches = [e for e in _entries() if e["lesson_id"] == lesson_id]
    if len(matches) != 1:
        raise HTTPException(404, "LESSON_NOT_FOUND_IN_CATALOG")
    return matches[0]


def _public(job: dict) -> dict:
    result = {
        "lesson_id": job["lesson_id"],
        "title": job["title"],
        "status": job["status"],
        "stage": job["stage"],
        "message": job.get("message", ""),
    }
    if job["status"] == "QA_PASSED_LOCAL":
        access = quote(job["access"], safe="")
        lid = quote(job["lesson_id"], safe="")
        result["url"] = f"/api/interactive-lessons/factory/view?lesson_id={lid}&access={access}"
        result["source"] = "nabil_factory_local_qa"
    return result


def _worker(lesson_id: str) -> None:
    with _guard:
        job = _jobs[lesson_id]
    try:
        LOGS.mkdir(parents=True, exist_ok=True)
        log_path = LOGS / f"{lesson_id}.log"
        cmd = [sys.executable, "-u", "-m", "scripts.nabil_lesson_factory",
               "--lesson-id", lesson_id]
        with log_path.open("w", encoding="utf-8") as stream:
            process = subprocess.Popen(
                cmd, cwd=str(ROOT), stdout=stream, stderr=subprocess.STDOUT,
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )
            try:
                exit_code = process.wait(timeout=1200)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
                exit_code = -1
                stream.write("\nFACTORY_TIMEOUT_AFTER_1200_SECONDS\n")
        text = log_path.read_text(encoding="utf-8", errors="replace")
        found = re.search(r'"status"\s*:\s*"QA_PASSED_LOCAL"', text)
        files = [
            OUT / job["filename_a"], OUT / job["filename_b"]
        ]
        verified_files = all(
            path.is_file()
            and path.stat().st_size > 1000
            and f'name="nabil-lesson-id" content="{lesson_id}"'
            in path.read_text(encoding="utf-8", errors="replace")
            for path in files
        )
        with _guard:
            if exit_code == 0 and found and verified_files:
                job.update(status="QA_PASSED_LOCAL", stage="READY",
                           message="Local quality gates passed. Owner scientific and classroom review pending.")
            else:
                tail = text[-2000:].strip()
                job.update(status="FAILED", stage="FAILED",
                           message=tail or f"Factory exited with code {exit_code}")
    except Exception as exc:
        with _guard:
            job.update(status="FAILED", stage="FAILED",
                       message=f"{type(exc).__name__}: {exc}")


@router.get("/catalog")
def factory_catalog(grade: str = "", subject: str = ""):
    """Discover actual preparable lessons, distinct from published Drive lessons."""
    entries = _entries()
    if grade:
        entries = [e for e in entries if str(e["grade"]) == str(grade)]
    if subject:
        from app.api.routes_interactive_lessons import _subject
        entries = [e for e in entries if _subject(e["subject"]) == _subject(subject)]
    return {"lessons": [
        {"lesson_id": e["lesson_id"], "title": e["canonical_title"],
         "grade": e["grade"], "subject": e["subject"],
         "language": e["language"]} for e in entries
    ]}


@router.post("/prepare")
def prepare(payload: dict, x_nabil_factory_token: str | None = Header(default=None)):
    _authorized(x_nabil_factory_token)
    lesson_id = str(payload.get("lesson_id") or "").strip()
    if not re.fullmatch(r"[A-Z0-9_-]{3,90}", lesson_id):
        raise HTTPException(400, "INVALID_LESSON_ID")
    entry = _entry(lesson_id)
    if os.getenv("NABIL_FACTORY_ENABLED", "0") != "1":
        raise HTTPException(503, "FACTORY_NOT_ENABLED")
    # Prevent concurrent expensive jobs in a public-facing web service.
    with _guard:
        if lesson_id in _jobs:
            return _public(_jobs[lesson_id])
        if any(j["status"] == "RUNNING" for j in _jobs.values()):
            raise HTTPException(409, "FACTORY_BUSY")
        grade = f"G{int(entry['grade']):02d}"
        subject = re.sub(r"[^\w]+", "-", entry["subject"]).upper()
        title = re.sub(r"[^\w]+", "-", entry["canonical_title"]).upper()
        match = re.search(r"-(\d{3})$", lesson_id)
        if not match:
            raise HTTPException(422, "INVALID_CANONICAL_LESSON_ID")
        base = f"{grade}-{subject}--{match.group(1)}--{title}"
        _jobs[lesson_id] = {
            "lesson_id": lesson_id, "title": entry["canonical_title"],
            "status": "RUNNING", "stage": "STARTING", "message": "",
            "access": secrets.token_urlsafe(32),
            "filename_a": base + ".html",
            "filename_b": base + "--EXERCISES.html",
        }
        result = _public(_jobs[lesson_id])
    threading.Thread(target=_worker, args=(lesson_id,),
                     daemon=True, name=f"factory-{lesson_id}").start()
    return result


@router.get("/status")
def preparation_status(lesson_id: str,
                       x_nabil_factory_token: str | None = Header(default=None)):
    _authorized(x_nabil_factory_token)
    _entry(lesson_id)
    with _guard:
        job = _jobs.get(lesson_id)
        if not job:
            return {"lesson_id": lesson_id, "status": "NOT_STARTED"}
        result = _public(job)
    if result["status"] == "RUNNING":
        log_path = LOGS / f"{lesson_id}.log"
        if log_path.exists():
            try:
                lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()
                stages = []
                for line in lines[-80:]:
                    try:
                        data = json.loads(line)
                        if data.get("stage"):
                            stages.append(str(data["stage"]))
                    except (ValueError, TypeError):
                        pass
                if stages:
                    result["stage"] = stages[-1]
            except OSError:
                pass
    return result


@router.get("/view")
def view_local_lesson(lesson_id: str, access: str, view: str = ""):
    if view not in ("", "exercises"):
        raise HTTPException(400, "INVALID_LESSON_VIEW")
    with _guard:
        job = _jobs.get(lesson_id)
        if (not job or job["status"] != "QA_PASSED_LOCAL"
                or not hmac.compare_digest(str(access), job["access"])):
            raise HTTPException(404, "VERIFIED_LESSON_NOT_AVAILABLE")
        filename = job["filename_b" if view == "exercises" else "filename_a"]
    path = OUT / filename
    if not path.is_file():
        raise HTTPException(404, "LESSON_ARTIFACT_MISSING")
    return FileResponse(path, media_type="text/html",
                        headers={"Cache-Control": "private, no-store",
                                 "Content-Security-Policy": "default-src 'self' data: blob: https:; script-src 'unsafe-inline' 'self' https:; style-src 'unsafe-inline' 'self' https:; frame-ancestors 'self'"})
