"""Source-only EB09 physics reader. Never use the generated lesson as evidence."""
import re
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Book, BookPage, BookChunk
from app.core.textbook_page_citations import resolve_book_printed_page

router = APIRouter()
SOURCE_DRIVE_ID = "11dqVqafG9zhr1sQzsjD3kxc5thA2DvZC"
SOURCE_URL = "https://drive.google.com/file/d/" + SOURCE_DRIVE_ID + "/view"

def _book(db):
    book = db.query(Book).filter(Book.drive_file_id == SOURCE_DRIVE_ID).first()
    if not book:
        raise HTTPException(503, "EB 09.pdf has not been indexed in this deployment. No generated lesson fallback.")
    return book

def _page(db, book, printed):
    matches = []
    for page in db.query(BookPage).filter(BookPage.book_id == book.id).all():
        resolved = resolve_book_printed_page({"book_title":book.title,"page":page.printed_page_number,"pdf_page":page.pdf_page_index,"text":page.text_content or ""})
        if resolved == printed:
            matches.append(page)
    if len(matches) != 1:
        raise HTTPException(404 if not matches else 409, "Printed page not uniquely verified in the original indexed EB 09.pdf.")
    p=matches[0]
    chunks=db.query(BookChunk).filter(BookChunk.book_id==book.id,BookChunk.printed_page_number==p.printed_page_number).order_by(BookChunk.chunk_index_in_page.asc()).all()
    content="\\n".join(c.text_content for c in chunks if c.text_content).strip() or (p.text_content or "").strip()
    return p,content

@router.get("/eb9-ohm/source")
def source(mode: str=Query("lesson",pattern="^(lesson|page|exercise)$"), page: int | None=Query(None,ge=1,le=999), exercise: int | None=Query(None,ge=1,le=999),db:Session=Depends(get_db)):
    book=_book(db)
    if mode=="page" and page is None or mode=="exercise" and exercise is None:
        raise HTTPException(400,"Specify the printed page or exercise number.")
    if mode=="lesson":
        numbers=range(93,101)
    elif mode=="page":
        numbers=[page]
    else:
        numbers=[page] if page else range(101,104)
    results=[]
    for printed in numbers:
        try:
            p,body=_page(db,book,printed)
        except HTTPException:
            if mode=="exercise" and page is None: continue
            raise
        if mode=="exercise":
            # Match only an explicit exercise heading, never a bare number in a formula.
            pat=rf"(?im)^\s*(?:exercice|exercise|ex\.?|n[°o]?)\s*[:.\-#]?\s*{exercise}\s*(?:[.)\-:]|$)"
            if not re.search(pat,body):continue
        results.append({"printed_page":printed,"pdf_page":p.pdf_page_index,"text":body,"page_image":f"/api/textbooks/{book.id}/pages/{printed}/image"})
    if not results:
        raise HTTPException(404,"Requested exercise/page not confirmed in the indexed original. Do not invent it.")
    if mode=="exercise" and len(results)>1 and page is None:
        raise HTTPException(409,"Exercise number appears on multiple pages. Supply the printed page.")
    return {"book":book.title,"drive_source":SOURCE_URL,"mode":mode,"exercise":exercise,"pages":results,"grounded_in":"indexed original Google Drive PDF, not the static HTML lesson"}
