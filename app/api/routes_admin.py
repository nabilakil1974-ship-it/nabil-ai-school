from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.config import settings
from app.db.session import get_db, SessionLocal
from app.db.models import Book
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


class BookItem(BaseModel):
    file_id: str
    title: str
    subject: str
    grade: str
    curriculum: str
    page_offset: int = 0


class BatchIndexRequest(BaseModel):
    admin_key: str
    books: list[BookItem]


def run_batch(books: list[BookItem]):
    for i, b in enumerate(books):
        print(f"📚 [{i + 1}/{len(books)}] بدء فهرسة: {b.title}", flush=True)
        try:
            db = SessionLocal()
            already = db.query(Book).filter(Book.drive_file_id == b.file_id).first()
            db.close()
            if already:
                print(f"⏭️ [{i + 1}/{len(books)}] {b.title} موجود أصلاً - تخطّي", flush=True)
                continue
            index_book(
                file_id=b.file_id,
                title=b.title,
                subject=b.subject,
                grade=b.grade,
                curriculum=b.curriculum,
                printed_page_offset=b.page_offset,
            )
        except Exception as e:
            print(f"❌ [{i + 1}/{len(books)}] فشلت فهرسة {b.title}: {e}", flush=True)
            continue
    print(f"🎉 خلصت الدفعة الكاملة ({len(books)} كتاب)", flush=True)


@router.post("/admin/index-books-batch")
def trigger_index_books_batch(req: BatchIndexRequest, background_tasks: BackgroundTasks):
    if req.admin_key != settings.SECRET_KEY:
        raise HTTPException(403, "admin_key غلط")
    background_tasks.add_task(run_batch, req.books)
    return {"status": f"بلّشت فهرسة دفعة من {len(req.books)} كتاب بالخلفية - راقب اللوغز بـ Railway"}


@router.get("/admin/books")
def list_books(admin_key: str = Query(...), db: Session = Depends(get_db)):
    if admin_key != settings.SECRET_KEY:
        raise HTTPException(403, "admin_key غلط")
    from app.db.models import BookChunk
    books = db.query(Book).all()
    result = []
    for b in books:
        chunk_count = db.query(BookChunk).filter(BookChunk.book_id == b.id).count()
        result.append({
            "title": b.title,
            "subject": b.subject,
            "grade": b.grade,
            "curriculum": b.curriculum,
            "total_pages": b.total_pages,
            "chunks_indexed": chunk_count,
        })
    return result
