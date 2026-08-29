import uuid
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
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

    id = Column(String, primary_key=True, default=gen_uuid)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)          # مثال: "الصف السابع"
    preferred_language = Column(String, default="ar-LB")  # ar-LB / ar / fr / en
    created_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="student")


class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=gen_uuid)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)        # رياضيات / فيزياء / كيمياء
    grade = Column(String, nullable=False)
    curriculum = Column(String, nullable=False)      # CRDP-FR / CRDP-EN / Building Up
    drive_file_id = Column(String, nullable=False)   # معرّف الملف على Google Drive
    total_pages = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    pages = relationship("BookPage", back_populates="book")


class BookPage(Base):
    __tablename__ = "book_pages"

    id = Column(String, primary_key=True, default=gen_uuid)
    book_id = Column(String, ForeignKey("books.id"), nullable=False)
    printed_page_number = Column(Integer)   # الرقم المطبوع بالكتاب
    pdf_page_index = Column(Integer)        # رقم الصفحة الفعلي بملف الـ PDF
    text_content = Column(Text)             # النص المستخرج (OCR أو نص مباشر)

    book = relationship("Book", back_populates="pages")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=gen_uuid)
    student_id = Column(String, ForeignKey("students.id"), nullable=False)
    subject = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=gen_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)   # student / teacher
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")


class BookChunk(Base):
    """
    مقطع نصي من كتاب (عادة صفحة واحدة أو نصف صفحة) مع الـ embedding تبعه.
    هاد الجدول هو أساس البحث الدلالي (RAG) - كل صف مربوط بكتاب محدد
    ورقم صفحة مطبوع حقيقي، عشان لما نبحث ما نلخبط بين الكتب أو الصفحات.
    """
    __tablename__ = "book_chunks"

    id = Column(String, primary_key=True, default=gen_uuid)
    book_id = Column(String, ForeignKey("books.id"), nullable=False)

    # فهرسة صارمة - كل بحث لازم يمرّ من هاي الحقول الأربعة قبل المقارنة بالمعنى
    subject = Column(String, nullable=False)     # رياضيات / فيزياء ...
    grade = Column(String, nullable=False)        # الصف السابع ...
    curriculum = Column(String, nullable=False)   # CRDP-FR / CRDP-EN / Building Up

    printed_page_number = Column(Integer, nullable=False)  # الرقم المطبوع بالكتاب فعلياً
    chunk_index_in_page = Column(Integer, default=0)       # لو الصفحة انقسمت لأكثر من مقطع

    text_content = Column(Text, nullable=False)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book")

