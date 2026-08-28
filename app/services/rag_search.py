"""
خدمة البحث الدلالي بالكتب (RAG).

القواعد الصارمة يلي بتضمن الدقة وعدم اللخبطة:
1. أي بحث لازم يكون "محصور" مسبقاً بمادة + صف + منهج محددين (فلترة SQL عادية)
   قبل ما نستخدم البحث بالمعنى (vector search) - هيك ما بيصير خلط بين كتاب
   رياضيات صف سابع وكتاب فيزياء صف تاسع مثلاً، حتى لو تشابهت الكلمات.
2. البحث بالمعنى بيصير بس جوّا هالنطاق المحصور (WHERE ثم ORDER BY المسافة)،
   يعني سريع لأنو ما بيقارن مع كل كتب المكتبة، بس مع صفحات الكتاب المطلوب.
3. كل نتيجة مرجعة معها رقم الصفحة المطبوع الحقيقي، فالأستاذ نبيل دائماً
   بقدر يقول "هاد موجود صفحة كذا بالكتاب" بدقة.
"""

from openai import OpenAI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models import Book, BookChunk

client = OpenAI(api_key=settings.OPENAI_API_KEY)

EMBEDDING_MODEL = "text-embedding-3-small"


def embed_text(text: str) -> list[float]:
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return resp.data[0].embedding


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
    query_vector = embed_text(query)

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
    """
    يحوّل نتائج البحث لنص واحد جاهز يُضاف لبرومبت الأستاذ نبيل، مع ذكر
    اسم الكتاب ورقم الصفحة بوضوح لكل مقطع - عشان يقدر يستشهد فيها بدقة
    وما يخترع صفحات غير موجودة.
    """
    if not chunks:
        return ""

    lines = ["مقاطع من الكتاب المرجعي (استخدمها للشرح واذكر رقم الصفحة بالضبط):"]
    for c in chunks:
        lines.append(f"\n[{c['book_title']} - صفحة {c['page']}]\n{c['text']}")
    return "\n".join(lines)
