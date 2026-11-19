"""Archive index import test: reads a manifest like Drive's archive-index.json through the real
restore_index_from_drive() path (fake Drive service), then checks /api/documents and /api/search.
Run: ARCHIVE_TEST_MANIFEST=path.json DATA_DIR=/tmp/x python3 -m pytest -q test_archive_index.py"""
import os, sys, json, tempfile
from pathlib import Path
os.environ.setdefault("DATA_DIR", tempfile.mkdtemp())
sys.path.insert(0, str(Path(__file__).parent))
import types
for _m in ("fitz","pytesseract","docx","google_auth_oauthlib","google_auth_oauthlib.flow","google.oauth2","google.oauth2.credentials","googleapiclient","googleapiclient.discovery","googleapiclient.http"):
    try: __import__(_m)
    except Exception:
        mod=types.ModuleType(_m); sys.modules[_m]=mod
        for n in ("Document","Flow","Credentials","build","MediaFileUpload","MediaIoBaseDownload"): setattr(mod,n,object)
try: import gemini_service
except Exception:
    g=types.ModuleType("gemini_service"); g.analyze_document_images=lambda *a,**k:None
    g.GeminiError=type("GeminiError",(Exception,),{}); g.GeminiNotConfigured=type("GeminiNotConfigured",(Exception,),{}); sys.modules["gemini_service"]=g
import app as A
from fastapi.testclient import TestClient

MANIFEST = Path(os.environ.get("ARCHIVE_TEST_MANIFEST", Path(__file__).parent / "fixtures" / "archive-drive-manifest.json"))

class _Req:
    def __init__(s, v): s.v = v
    def execute(s): return s.v
class _Files:
    def __init__(s, raw, idx): s.raw = raw; s.idx = idx
    def list(s, **k):
        if "manifest" in k.get("q", ""): return _Req({"files": [{"id": "m1", "name": "archive-drive-manifest.json"}]})
        return _Req({"files": [{"id": "idx1", "name": "archive-index.json"}]}) if not getattr(s, "no_index", False) else _Req({"files": []})
    def get(s, **k): return _Req(s.raw if k.get("fileId") != "idx1" else s.idx)
class _Svc:
    def __init__(s, raw, idx): s._f = _Files(raw, idx)
    def files(s): return s._f

def load(monkeypatch, data):
    raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
    idx = (Path(__file__).parent / "fixtures" / "archive-index-pending.json").read_bytes()
    monkeypatch.setattr(A, "drive_service", lambda: _Svc(raw, idx))
    monkeypatch.setattr(A, "ensure_drive_folder", lambda s: "folder")
    A.DRIVE_INDEX_CACHE.update({"items": [], "loaded_at": -1e9})

def test_import_20_style_manifest(monkeypatch):
    data = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    load(monkeypatch, data + data[:3])  # re-import with duplicates must not duplicate
    c = TestClient(A.app)
    docs = c.get("/api/documents").json()
    assert len(docs) == len(data) + 1  # manifest docs + the one pending doc from archive-index.json
    assert len({d["id"] for d in docs}) == len(docs)
    ids = {x["document_id"] for x in data}
    mdocs = [d for d in docs if d["id"] in ids]
    assert len(mdocs) == len(data)
    for src, d in zip(sorted(data, key=lambda x: x["document_id"]), sorted(mdocs, key=lambda x: x["id"])):
        assert d["id"] == src["document_id"]
        assert d["title"] == src["original_title"] and d["filename"] == src["original_title"]
        assert d["original_link"] == src["original_url"] == d["original_url"]
        assert d["text"] == src["full_text"] and len(d["text"]) > 300
        assert d["ocr_id"] == src["ocr_id"] and d["ocr_title"] == src["ocr_title"] and d["ocr_url"] == src["ocr_url"]
        assert d["document_number"] == src["document_number"] and d["document_date"] == src["document_date"] and d["issuer"] == src["issuer"]
    forms = [d for d in docs if d["category"] == "نماذج وإفادات"]
    assert len(forms) == sum(1 for x in data if x["document_type"] in ("نموذج إداري رسمي", "إفادة رسمية"))

def test_search_full_text_and_category(monkeypatch):
    data = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    load(monkeypatch, data)
    c = TestClient(A.app)
    # a word taken from deep inside a full text (not title/summary) must be found
    probe = data[0]["full_text"].split("\n")[4].split()[3]
    r = c.get("/api/search", params={"q": probe}).json()
    assert r["count"] >= 1 and any(x["id"] == data[0]["document_id"] for x in r["results"])
    r = c.get("/api/search", params={"q": "", "category": "نماذج وإفادات"}).json()
    assert r["count"] == sum(1 for x in data if x["document_type"] in ("نموذج إداري رسمي", "إفادة رسمية"))
    assert c.get("/api/search", params={"q": "كلمةغيرموجودةإطلاقاً"}).json()["count"] == 0

def test_ebook_category():
    assert A.category_from_type("كتاب إلكتروني") == "كتب إلكترونية"
    assert A.category_from_type("نموذج إداري رسمي") == "نماذج وإفادات"
    assert A.category_from_type("إفادة رسمية") == "نماذج وإفادات"
