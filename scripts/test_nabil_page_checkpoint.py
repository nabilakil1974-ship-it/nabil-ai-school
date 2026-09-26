"""Offline acceptance tests for durable per-page NABIL checkpointing.

No API keys, no real Drive, no Groq calls, no user textbook transfer.
Run on Railway: python -m unittest scripts.test_nabil_page_checkpoint -v
"""
import hashlib
import io
import json
import re
import tempfile
import unittest
from pathlib import Path

try:
    import fitz
    from scripts import nabil_page_checkpoint as cp
except ImportError:
    fitz = None
    cp = None


class _Request:
    def __init__(self, execute):
        self._execute = execute

    def execute(self):
        return self._execute()


class _MemoryDrive:
    def __init__(self):
        self.items = {}
        self.last_id = 0
        self.api = self
        self._add("root", "root", "", "application/vnd.google-apps.folder")

    def _add(self, fid, name, parent, mime, data=b""):
        self.items[fid] = {
            "id": fid, "name": name, "parent": parent,
            "mimeType": mime, "data": data,
        }

    def files(self):
        return self.api

    def list(self, q, **kw):
        names = re.search(r"name = '([^']+)'", q)
        parents = re.search(r"and '([^']+)' in parents", q)
        if not names or not parents:
            raise AssertionError("Invalid Drive list query " + q)
        rows = [
            {"id": item["id"], "name": item["name"],
             "mimeType": item["mimeType"]}
            for item in self.items.values()
            if item["name"] == names.group(1)
            and item["parent"] == parents.group(1)
        ]
        return _Request(lambda: {"files": rows})

    def create(self, body, media_body=None, **kw):
        def apply():
            self.last_id += 1
            fid = "mem_" + str(self.last_id)
            data = media_body.getbytes(0, media_body.size()) if media_body else b""
            self._add(fid, body["name"], body["parents"][0],
                      body.get("mimeType", "application/json"), data)
            return {"id": fid}
        return _Request(apply)

    def update(self, fileId, media_body, **kw):
        def apply():
            self.items[fileId]["data"] = media_body.getbytes(0, media_body.size())
            return {"id": fileId}
        return _Request(apply)

    def get_media(self, fileId, **kw):
        return _Request(lambda: self.items[fileId]["data"])

    def delete(self, fileId, **kw):
        return _Request(lambda: self.items.pop(fileId, None))


@unittest.skipIf(fitz is None or cp is None, "Railway PDF/Drive dependencies unavailable")
class CheckpointTest(unittest.TestCase):
    def setUp(self):
        self.drive = _MemoryDrive()
        cp._FOLDER_CACHE.clear()
        self.doc = fitz.open()
        self.page = self.doc.new_page(width=600, height=800)
        self.page.draw_rect(fitz.Rect(50, 50, 280, 220), color=(0, 0, 0))
        self.entry = {
            "book_id": "book_123",
            "lesson_id": "G07-PHYSICS-001",
            "source_pdf_sha256": "s" * 64,
        }
        self.temp = tempfile.TemporaryDirectory()
        self.cache = Path(self.temp.name)
        self.area = [50.0, 50.0, 280.0, 220.0]
        self.image = self.page.get_pixmap(
            clip=fitz.Rect(*self.area), dpi=180).tobytes("png")

    def tearDown(self):
        self.doc.close()
        self.temp.cleanup()

    def test_save_and_resume_without_reinvoking_vision(self):
        source_path = self.cache / "fig_p1_scanned_1.png"
        source_path.write_bytes(self.image)
        figures = [{
            "figure_id": "FIG_P1_SCAN_1",
            "printed_label": "1",
            "printed_number": 1,
            "source_page": 1,
            "bbox": self.area,
            "image_path": str(source_path),
            "image_sha256": hashlib.sha256(self.image).hexdigest(),
            "evidence_method": "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF",
        }]
        page = {"page_num": 1, "text": "Fig. 1",
                "figures": figures}
        cp.save_page(self.drive, "root", self.doc, self.entry,
                     page, "groq", "qwen/qwen3.8-27b")
        resumed = cp.load_page(self.drive, "root", self.doc, self.entry,
                               1, self.cache, "groq", "qwen/qwen3.8-27b")
        self.assertEqual(resumed["text"], "Fig. 1")
        self.assertEqual(resumed["figures"][0]["image_sha256"],
                         hashlib.sha256(self.image).hexdigest())
        self.assertTrue(Path(resumed["figures"][0]["image_path"]).is_file())
        self.assertIsNone(cp.load_page(
            self.drive, "root", self.doc, self.entry, 1, self.cache,
            "openai", "gpt-4o-mini"))
        cp.invalidate_page(self.drive, "root", self.entry, 1)
        self.assertIsNone(cp.load_page(
            self.drive, "root", self.doc, self.entry, 1, self.cache,
            "groq", "qwen/qwen3.8-27b"))

    def test_targeted_rescue_roundtrip_and_provenance(self):
        targeted = self.page.get_pixmap(
            clip=fitz.Rect(*self.area), dpi=220).tobytes("png")
        source_path = self.cache / "fig_p1_targeted_1.png"
        source_path.write_bytes(targeted)
        figure = {
            "figure_id": "FIG_P1_TARGET_1",
            "printed_label": "1",
            "printed_number": 1,
            "source_page": 1,
            "bbox": self.area,
            "image_path": str(source_path),
            "image_sha256": hashlib.sha256(targeted).hexdigest(),
            "ai_provenance": {
                "provider": "openrouter",
                "model": "vision-model",
                "primary_provider": "groq",
                "used_failover": True,
                "completed_at": "2026-09-26T00:00:00+00:00",
            },
            "evidence_method":
                "TARGETED_HIGHRES_VISION_PLUS_LOCAL_CAPTION_OCR",
        }
        cp.save_page(
            self.drive, "root", self.doc, self.entry,
            {"page_num": 1, "text": "Fig. 1", "figures": [figure]},
            "groq", "qwen/qwen3.8-27b")
        resumed = cp.load_page(
            self.drive, "root", self.doc, self.entry,
            1, self.cache, "groq", "qwen/qwen3.8-27b")
        self.assertEqual(
            resumed["figures"][0]["image_sha256"],
            hashlib.sha256(targeted).hexdigest())
        self.assertEqual(
            resumed["figures"][0]["ai_provenance"]["provider"],
            "openrouter")

        # Inspect the stored JSON record: top-level provider/model are clearly
        # labelled as compatibility keys, while actual provenance is explicit.
        folder = cp._folder(
            self.drive, "root", self.entry, create=False)
        fid = cp._children(
            self.drive, folder, "PAGE_0001.json")
        record = json.loads(
            self.drive.items[fid]["data"].decode("utf-8"))
        self.assertEqual(
            record["provider_fields_role"],
            "CHECKPOINT_COMPATIBILITY_KEY_NOT_EVIDENCE_ORIGIN")
        self.assertEqual(
            record["actual_provenance"][0]["provider"],
            "openrouter")

    def test_source_hash_blocks_reuse(self):
        cp.save_page(self.drive, "root", self.doc, self.entry,
                     {"page_num": 1, "text": "text", "figures": []},
                     "groq", "vision")
        changed = dict(self.entry, source_pdf_sha256="z" * 64)
        self.assertIsNone(cp.load_page(
            self.drive, "root", self.doc, changed, 1,
            self.cache, "groq", "vision"))

    def test_exercise_region_roundtrip(self):
        region = self.page.get_pixmap(
            clip=fitz.Rect(*self.area), dpi=200).tobytes("png")
        row = {
            "number": 1, "section_type": "EXERCISE",
            "exact_source_prompt": "Compare the pictured objects.",
            "source_bbox": self.area,
            "source_region_sha256": hashlib.sha256(region).hexdigest(),
            "source_region_image_ref": str(self.cache / "exercise_source.png"),
            "verified_against_source": True,
        }
        cp.save_exercises(self.drive, "root", self.doc, self.entry,
                          1, [row], "groq", "vision")
        rows = cp.load_exercises(self.drive, "root", self.doc,
                                 self.entry, 1, self.cache,
                                 "groq", "vision")
        self.assertEqual(len(rows), 1)
        self.assertEqual(Path(rows[0]["source_region_image_ref"]).read_bytes(),
                         region)


if __name__ == "__main__":
    unittest.main()
