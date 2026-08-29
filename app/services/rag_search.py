"""
خدمة البحث الدلالي بالكتب (RAG) - تستخدم Gemini المجاني من Google لتوليد
البصمات الرقمية (embeddings)، وليس OpenAI (عشان ما يحتاج بطاقة دفع).

القواعد الصارمة يلي بتضمن الدقة وعدم اللخبطة:
1. أي بحث لازم يكون "محصور" مسبقاً بمادة + صف + منهج محددين (فلترة SQL عادية)
   قبل ما نستخدم البحث بالمعنى (vector search).
2. البحث بالمعنى بيصير بس جوّا هالنطاق المحصور، يعني سريع.
3. كل نتيجة مرجعة معها رقم الصفحة المطبوع الحقيقي.
"""

import google.generativeai as genai
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Book, BookChunk

genai.configure(api_key=settings.GEMINI_API_KEY)

EMBEDDING_MODEL = "models/gemini-embedding-001"  # الموديل الحالي المدعوم
EMBEDDING_OUTPUT_DIM = 768  # نطلب 768 بعد عشان يطابق قاعدة البيانات


def embed_text(text: str, task_type: str = "retrieval_document") -> list[float]:
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type=task_type,
        output_dimensionality=EMBEDDING_OUTPUT_DIM,
    )
    return result["embedding"]


def search_book_pages(
    db: Session,
    query: str,
    subject: str,
    grade: str,
    curriculum: str,
    top_k: int = 4,
):
    """
    يرجّع أفضل top_k مقاطع مرتبطة بسؤال الطالب، محصورة حصراً بمادة/صف/منهج
    محددين، مرتبة بالصفحة الأقرب دلالياً لسؤاله.
    """
    query_vector = embed_text(query, task_type="retrieval_query")

    results = (
        db.query(BookChunk)
        .join(Book, Book.id == BookChunk.book_id)
        .filter(
            BookChunk.subject == subject,
            BookChunk.grade == grade,
            BookChunk.curriculum == curriculum,
        )
        .order_by(BookChunk.embedding.cosine_distance(query_vector))
        .limit(top_k)
        .all()
    )

    return [
        {
            "book_title": r.book.title,
            "page": r.printed_page_number,
            "text": r.text_content,
        }
        for r in results
    ]


def build_context_block(chunks: list[dict]) -> str:
    if not chunks:
        return ""

    lines = ["مقاطع من الكتاب المرجعي (استخدمها للشرح واذكر رقم الصفحة بالضبط):"]
    for c in chunks:
        lines.append(f"\n[{c['book_title']} - صفحة {c['page']}]\n{c['text']}")
    return "\n".join(lines)
