"""HTTP surface of the exercise solver (all heavy lifting is in app.services.exercise_solver)."""
from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Deque, Dict, Optional

from fastapi import APIRouter, Depends, File, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services import exercise_solver as sv

router = APIRouter(prefix="/solver", tags=["exercise-solver"])
_HITS: Dict[str, Deque[float]] = defaultdict(deque)


def _limit(request: Request, per_minute: int = 12) -> None:
    ip = (request.client.host if request.client else "?")
    q, now = _HITS[ip], time.monotonic()
    while q and now - q[0] > 60:
        q.popleft()
    if len(q) >= per_minute:
        raise sv.SolverError("RATE_LIMIT", "طلبات كثيرة. انتظر قليلًا ثم أعد المحاولة.", 429)
    q.append(now)


def _err(e: sv.SolverError) -> JSONResponse:
    return JSONResponse({"status": "error", "code": e.code, "message": e.message}, status_code=e.http)


@router.get("/status")
def status():
    return sv.providers_status()


@router.post("/read")
async def read(request: Request, text: str = Form(""), lang: str = Form("ar"),
               file: Optional[UploadFile] = File(None)):
    try:
        _limit(request)
        data = await file.read(sv.MAX_UPLOAD_BYTES + 1) if file is not None else None
        return sv.read_statement(text=text, file_bytes=data or None,
                                 mime=(file.content_type if file else "") or "", lang=lang)
    except sv.SolverError as e:
        return _err(e)


class SolveIn(BaseModel):
    statement: str = Field(..., min_length=3, max_length=4000)
    confirmed: bool = False
    lang: str = "ar"
    grade: str = ""
    subject: str = ""


@router.post("/solve")
def solve(body: SolveIn, request: Request):
    try:
        _limit(request, 8)
        if not body.confirmed:
            raise sv.SolverError("NOT_CONFIRMED", "يجب أن يؤكد الطالب نص التمرين قبل الحل.")
        return sv.solve(statement=body.statement, lang=body.lang, grade=body.grade, subject=body.subject)
    except sv.SolverError as e:
        return _err(e)


@router.post("/book")
def book(request: Request, lesson_id: str = Form(...), number: str = Form(""), page: str = Form(""),
         db: Session = Depends(get_db)):
    """Find an exercise in the indexed book of this lesson (grade/subject/language come from the catalogue)."""
    try:
        _limit(request, 20)
        from app.services import golden_catalogue as gc
        entry = gc._entry(lesson_id)
        if not entry:
            raise sv.SolverError("LESSON_NOT_FOUND", "الدرس غير موجود.", 404)
        from app.api.routes_textbook_pages import exact_exercise_preview
        message = (f"exercise {number}" if number.strip() else "")
        res = exact_exercise_preview(grade=str(entry.get("grade") or ""), subject=str(entry.get("subject") or ""),
                                     curriculum=str(entry.get("branch") or ""), language=str(entry.get("language") or ""),
                                     message=message, book_page=page.strip(), pdf_page="", db=db)
        if res.get("status") != "indexed":
            return {"status": "unavailable", "message": res.get("message", "")}
        return {"status": "ok", "statement": res["source_text"][:4000], "printed_page": res.get("printed_page"),
                "page_image_url": res.get("page_image_url"), "heading_verified": res.get("exercise_heading_verified"),
                "book_title": res.get("book_title"), "source": "book_index", "message": res.get("message", "")}
    except sv.SolverError as e:
        return _err(e)
