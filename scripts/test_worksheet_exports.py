import base64
import io
import unittest
from zipfile import ZipFile

from app.api.routes_worksheet import WorksheetExport, WorksheetSection, _docx_bytes, _pdf_bytes


class WorksheetExportTests(unittest.TestCase):
    def setUp(self):
        self.request = WorksheetExport(
            title="ورقة عمل تفاعلية — محيط الدائرة",
            grade="الصف السادس",
            subject="الرياضيات",
            lesson="محيط الدائرة",
            language="العربية",
            source_label="مبنية على مقاطع مسترجعة من كتاب موثق — ص. 12",
            sections=[
                WorksheetSection(phase="لاحظ", content="لاحظ نصف القطر.", figures=[
                    "data:image/png;base64," + base64.b64encode(
                        base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=")
                    ).decode("ascii")
                ]),
                WorksheetSection(phase="طبّق", content="إذا كان r=5 فإن C=31.4 cm عند π≈3.14."),
            ],
        )

    def test_docx_is_real_editable_document(self):
        data = _docx_bytes(self.request)
        self.assertTrue(data.startswith(b"PK"))
        with ZipFile(io.BytesIO(data)) as archive:
            xml = archive.read("word/document.xml").decode("utf-8")
        self.assertIn("31.4 cm", xml)
        self.assertIn("محيط الدائرة", xml)

    def test_math_inequalities_are_not_stripped_from_docx(self):
        request = self.request.model_copy(update={
            "sections": [WorksheetSection(phase="قارن", content="x < 3 and x > 2; A & B")]
        })
        data = _docx_bytes(request)
        with ZipFile(io.BytesIO(data)) as archive:
            xml = archive.read("word/document.xml").decode("utf-8")
        self.assertIn("x &lt; 3", xml)
        self.assertIn("x &gt; 2", xml)
        self.assertIn("A &amp; B", xml)

    def test_pdf_handles_inequalities_in_every_field(self):
        request = self.request.model_copy(update={
            "title": "x < 3 & x > 2",
            "source_label": "صفحات < 10 & > 2",
            "sections": [WorksheetSection(phase="x < 3", content="2 < x < 3 & x > 1")]
        })
        data = _pdf_bytes(request)
        self.assertTrue(data.startswith(b"%PDF"))

    def test_pdf_is_real_pdf(self):
        data = _pdf_bytes(self.request)
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertGreater(len(data), 1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
