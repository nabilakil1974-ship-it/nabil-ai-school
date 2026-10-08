"""Read-only API for batch-produced NABIL lesson packages."""
from __future__ import annotations

import mimetypes
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.lesson_package_registry import (
    filter_rows,
    get_artifact,
    get_lesson,
    public_row,
    readiness_summary,
)

router = APIRouter(prefix="/content-registry", tags=["content-registry"])


@router.get("/readiness")
def readiness():
    return readiness_summary()


@router.get("/lessons")
def lessons(
    grade: str = "",
    subject: str = "",
    language: str = "",
    branch: str = "",
    status: str = "",
    runtime_ready: bool | None = None,
):
    rows = filter_rows(
        grade=grade,
        subject=subject,
        language=language,
        branch=branch,
        status=status,
        runtime_ready=runtime_ready,
    )
    return {
        "count": len(rows),
        "zero_ai_runtime": True,
        "lessons": [public_row(row) for row in rows],
    }


@router.get("/lessons/{lesson_id}")
def lesson(lesson_id: str):
    item = get_lesson(lesson_id)
    if not item:
        raise HTTPException(404, "LESSON_NOT_IN_CONTENT_REGISTRY")
    return public_row(item)


@router.get("/artifact/{lesson_id}/{artifact_kind}")
def artifact(lesson_id: str, artifact_kind: str):
    path = get_artifact(lesson_id, artifact_kind)
    if path is None:
        raise HTTPException(404, "READY_ARTIFACT_NOT_AVAILABLE")
    media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    headers = {
        "Cache-Control": "public, max-age=300",
        "X-NABIL-Lesson-ID": str(lesson_id).strip().upper(),
        "X-NABIL-Artifact-Kind": artifact_kind,
        "X-NABIL-Runtime-AI": "false",
    }
    if media_type == "text/html":
        headers["Content-Security-Policy"] = (
            "default-src 'self' data: blob: https:; "
            "script-src 'unsafe-inline' 'self' https:; "
            "style-src 'unsafe-inline' 'self' https:; "
            "img-src 'self' data: blob: https:; "
            "media-src 'self' data: blob: https:; "
            "frame-ancestors 'self'"
        )
    return FileResponse(path, media_type=media_type, headers=headers)
