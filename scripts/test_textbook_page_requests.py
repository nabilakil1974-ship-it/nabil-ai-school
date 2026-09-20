"""Exact textbook-page routing regression tests, no provider calls."""
import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock
# CI's lightweight UI job deliberately does not install SQLAlchemy. Use
# model-name doubles for this pure routing test; Railway uses actual ORM models.
import sys
import types

class _Column:
    def __eq__(self, other):
        return self
    def asc(self):
        return self

class Book:
    grade = subject = curriculum = title = _Column()

class BookPage:
    book_id = pdf_page_index = _Column()

class BookChunk:
    book_id = printed_page_number = chunk_index_in_page = _Column()

fake_models = types.ModuleType("app.db.models")
fake_models.Book = Book
fake_models.BookPage = BookPage
fake_models.BookChunk = BookChunk
sys.modules["app.db.models"] = fake_models
from app.services.textbook_page_request import (
    parse_textbook_page_request, indexed_textbook_page_context,
)


class ExactPageTests(unittest.TestCase):
    def test_student_request_languages_and_modes(self):
        self.assertEqual(parse_textbook_page_request("اشرحلي الصفحة 55"), (55, "page"))
        self.assertEqual(parse_textbook_page_request("اشرح الدرس من صفحة 55"), (55, "lesson"))
        self.assertEqual(parse_textbook_page_request("Explain page 15"), (15, "page"))
        self.assertEqual(parse_textbook_page_request("Start the lesson from page 55"), (55, "lesson"))
        self.assertEqual(parse_textbook_page_request("Begin the selected lesson", "55"), (55, "lesson"))
        self.assertIsNone(parse_textbook_page_request("Exercise 5: factorize"))
        self.assertIsNone(parse_textbook_page_request("Study the function f(x)=ln(x)"))
        with self.assertRaises(ValueError):
            parse_textbook_page_request("اشرح الصفحة 0")
        with self.assertRaises(ValueError):
            parse_textbook_page_request("Begin the selected lesson", "3b")

    def test_pdf_page_differs_from_printed_page(self):
        book = SimpleNamespace(
            id="b1", title="chemistry - grade 9.pdf",
            grade="الصف التاسع", subject="كيمياء", curriculum="CRDP-EN",
        )
        pages = [
            SimpleNamespace(
                printed_page_number=n, pdf_page_index=n,
                text_content=f"Book text on printed page {n+2}",
            )
            for n in (53, 54, 55, 56)
        ]
        pages[-1].text_content = "Chapter 3 Next chapter"
        db = MagicMock()
        def query(model):
            q = MagicMock()
            q.filter.return_value = q
            q.order_by.return_value = q
            if model is Book:
                q.all.return_value = [book]
            elif model is BookPage:
                q.all.return_value = pages
            elif model is BookChunk:
                q.all.return_value = []
            return q
        db.query.side_effect = query
        one = indexed_textbook_page_context(
            db, grade=book.grade, subject=book.subject,
            curriculum=book.curriculum, printed_page=55,
            mode="page",
        )
        self.assertEqual(len(one), 1)
        self.assertEqual(one[0]["page"], 53)  # legacy indexed value
        self.assertEqual(one[0]["printed_page"], 55)
        self.assertEqual(one[0]["pdf_page"], 53)
        self.assertIn("55", one[0]["text"])

        lesson = indexed_textbook_page_context(
            db, grade=book.grade, subject=book.subject,
            curriculum=book.curriculum, printed_page=55,
            mode="lesson",
        )
        self.assertEqual([p["printed_page"] for p in lesson], [55, 56, 57])
        with self.assertRaises(LookupError):
            indexed_textbook_page_context(
                db, grade=book.grade, subject=book.subject,
                curriculum=book.curriculum, printed_page=99,
            )

    def test_ambiguous_books_do_not_silently_choose_wrong_file(self):
        books = [SimpleNamespace(id=str(n), title=f"Chemistry {n}.pdf")
                 for n in (1, 2)]
        page = SimpleNamespace(
            printed_page_number=55, pdf_page_index=55,
            text_content="Sample verified page"
        )
        db = MagicMock()
        def query(model):
            q = MagicMock()
            q.filter.return_value = q
            q.order_by.return_value = q
            q.all.return_value = books if model is Book else (
                [page] if model is BookPage else []
            )
            return q
        db.query.side_effect = query
        with self.assertRaises(ValueError):
            indexed_textbook_page_context(
                db, grade="Grade 9", subject="Chemistry",
                curriculum="CRDP-EN", printed_page=55,
            )


if __name__ == "__main__":
    unittest.main()
