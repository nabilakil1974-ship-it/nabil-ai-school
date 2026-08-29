"""
سكربت فهرسة الكتب - يشتغل مرة وحدة (أو كل ما نضيف كتاب جديد) وليس أثناء
محادثة الطالب، عشان البحث اللحظي يضل سريع.
"""

import argparse
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
    service = get_drive_service()

    print(f"⏳ تحميل الكتاب: {title}")
    pdf_bytes = download_pdf(service, file_id)
    reader = PdfReader(io.BytesIO(pdf_bytes))
    total_pages = len(reader.pages)
    print(f"📄 عدد صفحات الملف: {total_pages}")

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
        print(f"  🔎 معالجة صفحة PDF رقم {pdf_index + 1}...", flush=True)
        text = (page.extract_text() or "").strip()
        print(f"  📝 استخرج {len(text)} حرف من صفحة {pdf_index + 1}", flush=True)

        if not text:
            print(f"  ⏭️ صفحة {pdf_index + 1} فاضية أو صورة - تخطّيناها", flush=True)
            continue

        printed_page = pdf_index + 1 - printed_page_offset
        chunks = split_into_chunks(text)

        for i, chunk_text in enumerate(chunks):
            print(f"    🧮 حساب embedding للمقطع {i + 1}/{len(chunks)}...", flush=True)
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
        print(f"  ✅ خزّنت صفحة {pdf_index + 1}/{total_pages}", flush=True)

    db.close()
    print(f"✅ خلصت فهرسة: {title} ({total_pages} صفحة)")


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
