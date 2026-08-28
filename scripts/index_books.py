"""
سكربت فهرسة الكتب - يشتغل مرة وحدة (أو كل ما نضيف كتاب جديد) وليس أثناء
محادثة الطالب، عشان البحث اللحظي يضل سريع.

طريقة التشغيل (من Railway، تبويب "Console" بخدمة web):
    python -m scripts.index_books --drive-folder-id <ID> --subject "رياضيات" \
        --grade "الصف السابع" --curriculum "CRDP-FR"

كل كتاب لازم يتفهرس لحاله (مادة/صف/منهج محددين بوضوح بسطر الأوامر)
عشان ما يصير خلط تلقائي - هيدا قرار مقصود لضمان الدقة.
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

# طول المقطع الأقصى بالحروف قبل ما نقسم الصفحة لأكثر من مقطع
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
    """
    printed_page_offset: الفرق بين رقم صفحة الـ PDF ورقم الصفحة المطبوع
    بالكتاب (مثلاً إذا الغلاف والفهرس ياخدو 3 صفحات قبل ما تبلش الصفحة "1"
    المطبوعة، بيصير printed_page_offset = 3).
    """
    db = SessionLocal()
    service = get_drive_service()

    print(f"⏳ تحميل الكتاب: {title}")
    pdf_bytes = download_pdf(service, file_id)
    reader = PdfReader(io.BytesIO(pdf_bytes))
    total_pages = len(reader.pages)

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
        text = (page.extract_text() or "").strip()
        if not text:
            continue  # صفحة صور/فارغة - رح نضيف OCR لاحقاً لهالحالة

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

        if pdf_index % 20 == 0:
            db.commit()
            print(f"  ...صفحة {pdf_index + 1}/{total_pages}")

    db.commit()
    db.close()
    print(f"✅ خلصت فهرسة: {title} ({total_pages} صفحة)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-id", required=True, help="Google Drive file ID للكتاب")
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
