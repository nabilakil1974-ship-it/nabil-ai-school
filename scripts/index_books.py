"""
سكربت فهرسة الكتب - يشتغل مرة وحدة (أو كل ما نضيف كتاب جديد) وليس أثناء
محادثة الطالب، عشان البحث اللحظي يضل سريع.

هالنسخة "قابلة للاستئناف" (resumable): إذا صار كراش أو Restart بمنتصف
الفهرسة، إعادة تشغيل نفس الأمر بترجع تكمل من آخر صفحة محفوظة، مش من الصفر.
"""

import argparse
import gc
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from pypdf import PdfReader

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models import Book, BookChunk
from app.services.rag_search import embed_text

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

MAX_CHUNK_CHARS = 1800


def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        "drive_service_account.json", scopes=SCOPES
    )
    return build("drive", "v3", credentials=creds)


def list_pdfs_in_folder(service, folder_id: str):
    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"
    files, page_token = [], None
    while True:
        resp = service.files().list(
            q=query, fields="nextPageToken, files(id, name)", pageToken=page_token
        ).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def download_pdf(service, file_id: str) -> bytes:
    request = service.files().get_media(fileId=file_id)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return buffer.getvalue()


def split_into_chunks(text: str) -> list[str]:
    text = text.strip()
    if len(text) <= MAX_CHUNK_CHARS:
        return [text] if text else []
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + MAX_CHUNK_CHARS])
        start += MAX_CHUNK_CHARS
    return chunks


def index_book(
    file_id: str,
    title: str,
    subject: str,
    grade: str,
    curriculum: str,
    printed_page_offset: int = 0,
):
    db = SessionLocal()

    # نتحقق: هل الكتاب هيدا اتفهرس (كلياً أو جزئياً) من قبل؟
    book = db.query(Book).filter(Book.drive_file_id == file_id).first()
    already_indexed_pdf_pages = 0

    if book:
        print(f"📚 الكتاب موجود أصلاً بالداتابيز (id={book.id}) - رح نتحقق وين وقفنا", flush=True)
        last_chunk = (
            db.query(BookChunk)
            .filter(BookChunk.book_id == book.id)
            .order_by(BookChunk.printed_page_number.desc())
            .first()
        )
        if last_chunk:
            already_indexed_pdf_pages = last_chunk.printed_page_number + printed_page_offset
            print(f"⏩ آخر صفحة محفوظة: {already_indexed_pdf_pages} - رح نكمل من بعدها", flush=True)

    # نحمّل الملف مرة وحدة بس (كان قبل عم يتحمّل مرتين - مرة لحساب عدد
    # الصفحات ومرة تانية للمعالجة - وهيدا كان يضاعف استهلاك الذاكرة بلا داعي)
    service = get_drive_service()
    print(f"⏳ تحميل ملف PDF: {title}", flush=True)
    pdf_bytes = download_pdf(service, file_id)
    reader = PdfReader(io.BytesIO(pdf_bytes))
    total_pages = len(reader.pages)
    print(f"📄 عدد صفحات الملف: {total_pages}", flush=True)
    del pdf_bytes  # ما عاد لازمنا البايتات الخام بعد ما صار عند reader نسخته الخاصة
    gc.collect()

    if not book:
        book = Book(
            title=title,
            subject=subject,
            grade=grade,
            curriculum=curriculum,
            drive_file_id=file_id,
            total_pages=total_pages,
        )
        db.add(book)
        db.commit()
        db.refresh(book)

    for pdf_index, page in enumerate(reader.pages):
        if pdf_index + 1 <= already_indexed_pdf_pages:
            continue  # هاي الصفحة اتفهرست بمحاولة سابقة - نتخطاها

        print(f"  🔎 معالجة صفحة PDF رقم {pdf_index + 1}...", flush=True)
        text = (page.extract_text() or "").strip()
        print(f"  📝 استخرج {len(text)} حرف من صفحة {pdf_index + 1}", flush=True)

        if not text:
            print(f"  ⏭️ صفحة {pdf_index + 1} فاضية أو صورة - تخطّيناها", flush=True)
            continue

        printed_page = pdf_index + 1 - printed_page_offset
        chunks = split_into_chunks(text)

        for i, chunk_text in enumerate(chunks):
            vector = embed_text(chunk_text)
            db.add(BookChunk(
                book_id=book.id,
                subject=subject,
                grade=grade,
                curriculum=curriculum,
                printed_page_number=printed_page,
                chunk_index_in_page=i,
                text_content=chunk_text,
                embedding=vector,
            ))

        db.commit()
        db.expire_all()  # يحرر ذاكرة الكائنات المخزّنة بجلسة SQLAlchemy
        print(f"  ✅ خزّنت صفحة {pdf_index + 1}/{total_pages}", flush=True)

        if pdf_index % 10 == 0:
            gc.collect()  # تنظيف دوري للذاكرة كل 10 صفحات

    db.close()
    print(f"✅ خلصت فهرسة: {title} ({total_pages} صفحة)", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--grade", required=True)
    parser.add_argument("--curriculum", required=True)
    parser.add_argument("--page-offset", type=int, default=0)
    args = parser.parse_args()

    index_book(
        file_id=args.file_id,
        title=args.title,
        subject=args.subject,
        grade=args.grade,
        curriculum=args.curriculum,
        printed_page_offset=args.page_offset,
    )
