from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.config import settings
from app.db.session import get_db
from scripts.index_books import index_book

router = APIRouter()


class IndexRequest(BaseModel):
    admin_key: str
    file_id: str
    title: str
    subject: str
    grade: str
    curriculum: str
    page_offset: int = 0


@router.post("/admin/index-book")
def trigger_index_book(req: IndexRequest, background_tasks: BackgroundTasks):
    """
    يبلّش فهرسة كتاب بالخلفية. لازم admin_key يطابق SECRET_KEY تبع
    السيرفر عشان محدا غريب يقدر يستخدمها.

    بيتنادى من أي أداة بترسل POST request (متل موقع httpie.io/app
    أو إضافة REST Client بالمتصفح) - رح نشرحلك بالخطوة الجاية أسهل طريقة.
    """
    if req.admin_key != settings.SECRET_KEY:
        raise HTTPException(403, "admin_key غلط")

    background_tasks.add_task(
        index_book,
        file_id=req.file_id,
        title=req.title,
        subject=req.subject,
        grade=req.grade,
        curriculum=req.curriculum,
        printed_page_offset=req.page_offset,
    )
    return {"status": "بلّشت الفهرسة بالخلفية - راقب اللوغز (Logs) بـ Railway لتتابع التقدم"}
