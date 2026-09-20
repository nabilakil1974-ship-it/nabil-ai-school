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
from sqlalchemy import or_
from app.db.models import Book, BookChunk, BookPage

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

    # BookChunk has printed page numbers, but visual verification needs the
    # separate 1-based PDF position recorded by the indexer in BookPage.
    # Only return a PDF page reference when an exact BookPage row exists.
    output = []
    page_lookup = {}
    for chunk in results:
        lookup_key = (chunk.book_id, chunk.printed_page_number)
        if lookup_key not in page_lookup:
            page_lookup[lookup_key] = (
                db.query(BookPage.pdf_page_index)
                .filter(
                    BookPage.book_id == chunk.book_id,
                    BookPage.printed_page_number == chunk.printed_page_number,
                )
                .order_by(BookPage.pdf_page_index.asc())
                .first()
            )
        matched = page_lookup[lookup_key]
        pdf_page = int(matched[0]) if matched and matched[0] is not None else None
        output.append({
            "book_title": chunk.book.title,
            "book_id": chunk.book_id,
            "page": chunk.printed_page_number,
            "pdf_page": pdf_page,
            "text": chunk.text_content,
        })
    return output


def build_context_block(chunks: list[dict]) -> str:
    if not chunks:
        return ""
    lines = ["مقاطع من الكتاب المرجعي (استخدمها للشرح واذكر رقم الصفحة بالضبط):"]
    for c in chunks:
        lines.append(f"\n[{c['book_title']} - صفحة {c['page']}]\n{c['text']}")
    return "\n".join(lines)


def find_nearest_book_exercises(
    db: Session,
    source_chunks: list[dict],
    subject: str,
    grade: str,
    curriculum: str,
    max_distance_pages: int = 18,
    max_chunks: int = 9,
) -> list[dict]:
    """Retrieve REAL nearby chapter exercise pages from the same indexed book.

    Semantic lesson search often finds concept pages but misses the question
    pages at the end of the chapter. This separate scoped lookup never generates
    exercises, never uses a different book/grade/curriculum, and includes PDF
    position only when BookPage was actually indexed.
    """
    anchor = next((
        item for item in source_chunks or []
        if item.get("book_id") and isinstance(item.get("page"), int)
    ), None)
    if not anchor:
        return []
    book_id = anchor["book_id"]
    first_page = int(anchor["page"])
    terms = (
        "%questions and exercises%",
        "%answer the following questions%",
        "%exercises and questions%",
        "%exercices et questions%",
        "%questions et exercices%",
        "%أسئلة وتمارين%",
        "%الأسئلة والتمارين%",
    )
    scoped = db.query(BookChunk).filter(
        BookChunk.book_id == book_id,
        BookChunk.subject == subject,
        BookChunk.grade == grade,
        BookChunk.curriculum == curriculum,
        BookChunk.printed_page_number >= first_page,
        BookChunk.printed_page_number <= first_page + max_distance_pages,
    )
    heading = (
        scoped.filter(or_(*[BookChunk.text_content.ilike(term) for term in terms]))
        .order_by(BookChunk.printed_page_number.asc())
        .first()
    )
    if heading is None:
        return []
    start_page = heading.printed_page_number
    rows = (
        scoped.filter(
            BookChunk.printed_page_number >= start_page,
            BookChunk.printed_page_number <= start_page + 3,
        )
        .order_by(
            BookChunk.printed_page_number.asc(),
            BookChunk.chunk_index_in_page.asc(),
        )
        .limit(max_chunks).all()
    )
    out = []
    for row in rows:
        indexed = db.query(BookPage.pdf_page_index).filter(
            BookPage.book_id == row.book_id,
            BookPage.printed_page_number == row.printed_page_number,
        ).first()
        out.append({
            "book_title": row.book.title,
            "book_id": row.book_id,
            "page": row.printed_page_number,
            "pdf_page": int(indexed[0]) if indexed and indexed[0] else None,
            "text": row.text_content,
            "is_verified_book_exercise_source": True,
        })
    return out
