import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.db.session import Base


# طول متجه الـ embeddings - يجب أن يطابق نموذج التضمين المحلي المستخدم
# paraphrase-multilingual-MiniLM-L12-v2 = 384 بعد
EMBEDDING_DIM = 384


def gen_uuid():
    return str(uuid.uuid4())


class Student(Base):
    __tablename__ = "students"

    id = Column(
        String,
        primary_key=True,
        default=gen_uuid,
    )
    name = Column(
        String,
        nullable=False,
    )
    grade = Column(
        String,
        nullable=False,
    )
    preferred_language = Column(
        String,
        default="ar-LB",
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    conversations = relationship(
        "Conversation",
        back_populates="student",
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(
        String,
        primary_key=True,
        default=gen_uuid,
    )
    title = Column(
        String,
        nullable=False,
    )
    subject = Column(
        String,
        nullable=False,
    )
    grade = Column(
        String,
        nullable=False,
    )
    curriculum = Column(
        String,
        nullable=False,
    )
    drive_file_id = Column(
        String,
        nullable=False,
    )
    total_pages = Column(
        Integer,
        default=0,
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    pages = relationship(
        "BookPage",
        back_populates="book",
    )


class BookPage(Base):
    __tablename__ = "book_pages"

    id = Column(
        String,
        primary_key=True,
        default=gen_uuid,
    )
    book_id = Column(
        String,
        ForeignKey("books.id"),
        nullable=False,
    )
    printed_page_number = Column(Integer)
    pdf_page_index = Column(Integer)
    text_content = Column(Text)

    book = relationship(
        "Book",
        back_populates="pages",
    )


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(
        String,
        primary_key=True,
        default=gen_uuid,
    )
    student_id = Column(
        String,
        ForeignKey("students.id"),
        nullable=False,
    )
    subject = Column(String)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    student = relationship(
        "Student",
        back_populates="conversations",
    )
    messages = relationship(
        "Message",
        back_populates="conversation",
    )


class Message(Base):
    __tablename__ = "messages"

    id = Column(
        String,
        primary_key=True,
        default=gen_uuid,
    )
    conversation_id = Column(
        String,
        ForeignKey("conversations.id"),
        nullable=False,
    )
    role = Column(
        String,
        nullable=False,
    )
    content = Column(
        Text,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )


class LessonPackage(Base):
    """
    حزمة درس منشورة وقابلة لإعادة الاستخدام.

    الهدف:
    - الدرس الجاهز لا يعاد توليده.
    - المختبر الجاهز لا يعاد توليده.
    - الطالب لا يمر عبر RAG/embeddings/AI
      عندما تكون الحزمة المنشورة موجودة.
    - source_signature يبقى محفوظاً للتحقق
      من نسخة المصدر عند الحاجة.
    """

    __tablename__ = "lesson_packages"

    # المفتاح الداخلي للحزمة.
    cache_key = Column(
        String,
        primary_key=True,
    )

    # توقيع المصدر الذي بُنيت منه الحزمة.
    source_signature = Column(
        String,
        nullable=False,
    )

    # هوية الدرس.
    grade = Column(
        String,
        nullable=False,
    )
    branch = Column(
        String,
        nullable=False,
        default="",
    )
    subject = Column(
        String,
        nullable=False,
    )
    curriculum = Column(
        String,
        nullable=False,
    )
    language = Column(
        String,
        nullable=False,
    )
    lesson = Column(
        String,
        nullable=False,
    )

    # نمط التدريس جزء من هوية الحزمة.
    teaching_mode = Column(
        String,
        nullable=False,
        default="default",
    )

    # محتوى الدرس الجاهز.
    reply = Column(
        Text,
        nullable=False,
    )

    # الرسومات والمصادر الجاهزة.
    drawings_json = Column(
        Text,
        nullable=False,
        default="[]",
    )
    sources_json = Column(
        Text,
        nullable=False,
        default="[]",
    )

    # المختبر المتحقق منه والمُرندر مسبقاً.
    # لا يُنشأ من جديد عند طلب الطالب.
    lab_html = Column(
        Text,
        nullable=True,
    )

    # النسخة الأصلية المنظمة للمختبر، إن كانت محفوظة.
    lab_spec_json = Column(
        Text,
        nullable=True,
    )

    # نسخة محرك المختبر.
    # عند تغيير المحرك يمكن للمصنع إعادة بناء المختبرات
    # بصورة مقصودة، لا من طلب الطالب.
    lab_engine_version = Column(
        String,
        nullable=False,
        default="1",
    )

    # مرجع اختياري للنسخة المنشورة على Drive.
    # لا نجعل وجوده إلزامياً حتى لا نكسر الحزم القديمة.
    drive_file_id = Column(
        String,
        nullable=True,
    )

    drive_url = Column(
        Text,
        nullable=True,
    )

    # حالة النشر.
    # published = مسموح للطالب استخدام الحزمة مباشرة.
    package_status = Column(
        String,
        nullable=False,
        default="published",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class BookChunk(Base):
    """
    مقطع نصي من كتاب مع embedding.

    هذا الجدول يبقى لمسار RAG عندما:
    - لا توجد حزمة درس منشورة جاهزة.
    - الطالب يسأل سؤالاً يحتاج الرجوع للمصدر.
    - الطالب يطلب حل تمرين غير موجود في الحزمة.

    لا ينبغي الوصول إليه لمجرد عرض درس Golden
    محفوظ ومُعتمد.
    """

    __tablename__ = "book_chunks"

    id = Column(
        String,
        primary_key=True,
        default=gen_uuid,
    )

    book_id = Column(
        String,
        ForeignKey("books.id"),
        nullable=False,
    )

    subject = Column(
        String,
        nullable=False,
    )
    grade = Column(
        String,
        nullable=False,
    )
    curriculum = Column(
        String,
        nullable=False,
    )

    printed_page_number = Column(
        Integer,
        nullable=False,
    )

    chunk_index_in_page = Column(
        Integer,
        default=0,
    )

    text_content = Column(
        Text,
        nullable=False,
    )

    embedding = Column(
        Vector(EMBEDDING_DIM),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    book = relationship("Book")
