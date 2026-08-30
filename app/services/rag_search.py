"""
خدمة البحث الدلالي بالكتب (RAG).
البصمات الرقمية (embeddings) تتولّد محلياً على السيرفر نفسه (مكتبة
sentence-transformers) - بدون أي اتصال بأي API خارجي. هيك النظام:
- مجاني 100% وبدون أي حدود يومية
- ما بيتعطل بسبب مشاكل خارجية (انقطاع خدمة، حصص استخدام، إلخ)
- أبطأ شوي من خدمة سحابية، بس مقبول جداً لحجم الاستخدام هون
القواعد الصارمة يلي بتضمن الدقة وعدم اللخبطة:
1. أي بحث لازم يكون "محصور" مسبقاً بمادة + صف + منهج محددين (فلترة SQL).
2. البحث بالمعنى بيصير بس جوّا هالنطاق المحصور، يعني سريع.
3. كل نتيجة مرجعة معها رقم الصفحة المطبوع الحقيقي.
"""
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from sqlalchemy.orm import Session
from app.db.models import Book, BookChunk

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"  # يدعم العربي والفرنسي والإنكليزي


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    # يتحمّل مرة وحدة بس ويضل بالذاكرة (lru_cache) بدل ما يعاد تحميله كل استدعاء
    return SentenceTransformer(MODEL_NAME)


def embed_text(text: str, task_type: str = "retrieval_document") -> list[float]:
    model = get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()


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
    print(f"🔍 بحث: subject={subject!r} grade={grade!r} curriculum={curriculum!r}", flush=True)

    matching_count = (
        db.query(BookChunk)
        .filter(
            BookChunk.subject == subject,
            BookChunk.grade == grade,
            BookChunk.curriculum == curriculum,
        )
        .count()
    )
    print(f"🔍 عدد المقاطع المطابقة للفلترة (قبل البحث الدلالي): {matching_count}", flush=True)

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
    print(f"🔍 عدد النتائج بعد البحث الدلالي: {len(results)}", flush=True)

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
