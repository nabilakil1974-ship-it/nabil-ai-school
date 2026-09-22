import base64
import io
import unittest
from zipfile import ZipFile

from app.api.routes_worksheet import WorksheetExport, WorksheetSection, _docx_bytes, _pdf_bytes, _plain_markdown


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

    def test_hidden_web_solutions_have_clean_print_headings(self):
        text = "Question 1\\n[SOLUTION 1]x < 3 & x > 1[/SOLUTION 1]"
        result = _plain_markdown(text)
        self.assertIn("Solution 1:", result)
        self.assertIn("x < 3 & x > 1", result)
        self.assertNotIn("[SOLUTION", result)
        self.assertNotIn("[/SOLUTION", result)

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

    def test_lesson_pptx_contains_real_figures_and_transitions(self):
        from app.api.routes_lesson_export import Cards, _pptx, _source_image
        from fastapi.responses import StreamingResponse
        from bs4 import BeautifulSoup
        svg = BeautifulSoup(
            '<svg xmlns="http://www.w3.org/2000/svg" width="160" height="90">'
            '<rect width="160" height="90" fill="#35aeea"/></svg>', "html.parser"
        ).find("svg")
        image = _source_image(svg)
        self.assertIsNotNone(image, "SVG figures must render, not disappear")
        response = _pptx(Cards(title="Physics", cards=["Water stays level"],
                               images=[[image]]))
        self.assertIsInstance(response, StreamingResponse)
        import asyncio

        async def collect_stream():
            chunks = []
            async for chunk in response.body_iterator:
                chunks.append(chunk if isinstance(chunk, bytes) else chunk.encode("utf-8"))
            return b"".join(chunks)

        data = asyncio.run(collect_stream())
        self.assertTrue(data.startswith(b"PK"), "PowerPoint must be a ZIP package")
        with ZipFile(io.BytesIO(data)) as archive:
            self.assertTrue(any(n.startswith("ppt/media/") for n in archive.namelist()))
            slides = [n for n in archive.namelist()
                      if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            self.assertTrue(any(b"<p:fade" in archive.read(n) for n in slides))

    def test_pdf_is_real_pdf(self):
        data = _pdf_bytes(self.request)
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertGreater(len(data), 1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
