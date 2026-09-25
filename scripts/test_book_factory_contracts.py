"""Fast offline contract tests for the source-driven book factory.

No API keys, Drive downloads, AI calls, or copyrighted PDF contents required.
Run: python -m scripts.test_book_factory_contracts
"""
import json
import unittest
from unittest.mock import MagicMock, patch

from scripts import nabil_book_factory as book


class BookFactoryContracts(unittest.TestCase):
    def test_unknown_book_requires_classification_not_filename_guess(self):
        with patch.object(book, "MANIFESTS", ()):
            with self.assertRaisesRegex(RuntimeError, "NEW_BOOK_METADATA_REQUIRED"):
                book.registered_book("new-drive-id", drive_service=MagicMock())

    def test_new_pdf_accepted_with_explicit_classification(self):
        service = MagicMock()
        service.files.return_value.get.return_value.execute.return_value = {
            "id": "fresh-id", "name": "Unindexed.pdf",
            "mimeType": "application/pdf", "trashed": False
        }
        with patch.object(book, "MANIFESTS", ()):
            item = book.registered_book(
                "fresh-id", drive_service=service, grade="7",
                subject="physics", language="en")
        self.assertEqual(item["drive_file_id"], "fresh-id")
        self.assertEqual(item["registration"], "SOURCE_DRIVE_PDF_CLASSIFIED_BY_OWNER")

    def test_unsafe_non_pdf_cannot_enter_factory(self):
        service = MagicMock()
        service.files.return_value.get.return_value.execute.return_value = {
            "id": "not-a-pdf", "name": "Fake.pdf",
            "mimeType": "text/plain", "trashed": False
        }
        with patch.object(book, "MANIFESTS", ()):
            with self.assertRaisesRegex(RuntimeError, "SOURCE_IS_NOT_ORIGINAL_DRIVE_PDF"):
                book.registered_book("not-a-pdf", drive_service=service,
                                     grade="7", subject="physics", language="en")

    def test_missing_chapter_numbers_rejected(self):
        rows = [{"chapter_number": 1, "title": "Matter"},
                {"chapter_number": 3, "title": "Energy"}]
        with self.assertRaisesRegex(RuntimeError, "TOC_NOT_FOUND_OR_AMBIGUOUS"):
            book.validate_sequence(rows)

    def test_bookmark_alone_does_not_verify_source_opener(self):
        class FakeDoc:
            def __len__(self):
                return 5
            def __getitem__(self, index):
                return object()
        rows = [{"chapter_number": 1, "title": "Solids",
                 "pdf_start_page": 2, "toc_pdf_page": None},
                {"chapter_number": 2, "title": "Liquids",
                 "pdf_start_page": 4, "toc_pdf_page": None}]
        with patch.object(book, "_best_header_match", return_value=(0.1, "other chapter")):
            with self.assertRaisesRegex(RuntimeError, "BOOKMARK_OPENING_UNVERIFIED"):
                book.verify_openers(FakeDoc(), rows)

    def test_real_source_discovery_not_existing_pilot_catalog(self):
        book_info = {"grade": "7", "subject": "physics",
                     "language": "en", "title": "NEW SOURCE.pdf"}
        original = [
            {"chapter_number": 1, "title": "First source chapter",
             "pdf_start_page": 3, "pdf_end_page": 7, "toc_pdf_page": 2},
            {"chapter_number": 2, "title": "Second source chapter",
             "pdf_start_page": 8, "pdf_end_page": 12, "toc_pdf_page": 2},
        ]
        with patch.object(book, "scan_original_toc", return_value=original), patch.object(
            book, "verify_openers", return_value=original
        ):
            index = book.build_index([None] * 12, book_info, book_id="brand-new-pdf",
                                     pdf_hash="original-hash")
        self.assertEqual([x["canonical_title"] for x in index["lessons"]],
                         ["First source chapter", "Second source chapter"])
        self.assertNotEqual(index["lessons"][0]["lesson_id"], "G07-PHYSICS-001")
        self.assertEqual(index["lessons"][0]["pdf_start_page"], 3)
        self.assertEqual(index["lessons"][1]["pdf_end_page"], 12)
        self.assertEqual(index["index_method"],
                         "ACTUAL_TOC_PLUS_PHYSICAL_OPENING_LOCAL_OCR")

    def test_watch_requires_one_minute_poll_floor(self):
        with self.assertRaisesRegex(RuntimeError, "WATCH_POLL_INTERVAL_TOO_SHORT"):
            book.run_folder("folder", watch=True, poll_seconds=5)

    def test_drive_folder_pagination_and_pdf_filter(self):
        service = MagicMock()
        service.files.return_value.list.return_value.execute.side_effect = [
            {"files": [{"id": "first", "mimeType": "application/pdf"}],
             "nextPageToken": "page-2"},
            {"files": [{"id": "second", "mimeType": "application/pdf"},
                       {"id": "notpdf", "mimeType": "text/plain"}]},
        ]
        self.assertEqual(book.folder_pdf_ids(service, "folder"), ["first", "second"])


if __name__ == "__main__":
    unittest.main()
