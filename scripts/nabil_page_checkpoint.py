"""Durable, source-locked per-page evidence cache for the NABIL lesson factory.

Use the owner's Drive OAuth service. Every page is independent: a Railway
restart loses no completed vision calls. NO AI calls in this module.
Only metadata is persisted; figure and exercise images are regenerated
from the original PDF and checked against the original SHA-256.
"""
import hashlib
import io
import json
import re
from pathlib import Path

from googleapiclient.http import MediaIoBaseUpload

CACHE_SCHEMA = "PAGE_EVIDENCE_V1_SOURCE_LOCKED"
_FOLDER_CACHE = {}


def _escape(value):
    return str(value).replace("\\", "\\\\").replace("'", "\\'")


def _children(service, parent, name, *, mime=None):
    clause = (
        "name = '%s' and '%s' in parents and trashed = false"
        % (_escape(name), _escape(parent))
    )
    if mime:
        clause += " and mimeType = '%s'" % _escape(mime)
    files = service.files().list(
        q=clause, fields="nextPageToken,files(id,name,mimeType)",
        pageSize=100, supportsAllDrives=True, includeItemsFromAllDrives=True,
    ).execute()
    out = list(files.get("files", []))
    token = files.get("nextPageToken")
    while token:
        files = service.files().list(
            q=clause, fields="nextPageToken,files(id,name,mimeType)",
            pageSize=100, pageToken=token, supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        out.extend(files.get("files", []))
        token = files.get("nextPageToken")
    if len(out) > 1:
        raise RuntimeError("PAGE_CHECKPOINT_DUPLICATE: " + name)
    return out[0]["id"] if out else None


def _folder(service, root_id, entry, create):
    key = (id(service), root_id, entry["book_id"], entry["lesson_id"])
    if key in _FOLDER_CACHE:
        return _FOLDER_CACHE[key]
    checkpoints = _children(
        service, root_id, "NABIL Factory Checkpoints",
        mime="application/vnd.google-apps.folder")
    if not checkpoints and create:
        checkpoints = service.files().create(body={
            "name": "NABIL Factory Checkpoints",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [root_id],
        }, fields="id").execute()["id"]
    if not checkpoints:
        return None
    name = "PAGE_EVIDENCE_%s_%s" % (
        entry["book_id"], entry["lesson_id"])
    folder = _children(service, checkpoints, name,
                       mime="application/vnd.google-apps.folder")
    if not folder and create:
        folder = service.files().create(body={
            "name": name, "mimeType": "application/vnd.google-apps.folder",
            "parents": [checkpoints],
        }, fields="id").execute()["id"]
    if folder:
        _FOLDER_CACHE[key] = folder
    return folder


def _filename(page_num, kind):
    if kind not in ("PAGE", "EXERCISES"):
        raise ValueError("Invalid page cache kind")
    return "%s_%04d.json" % (kind, page_num)


def _source_signature(doc, page_num):
    page = doc[page_num - 1]
    return hashlib.sha256(page.get_pixmap(dpi=72).samples).hexdigest()


def _model_signature(provider, vision_model):
    return {"provider": provider, "vision_model": vision_model}


def _load_record(service, root_id, doc, entry, page_num, kind,
                 provider, vision_model):
    folder = _folder(service, root_id, entry, create=False)
    if not folder:
        return None
    fid = _children(service, folder, _filename(page_num, kind))
    if not fid:
        return None
    raw = service.files().get_media(fileId=fid).execute()
    record = json.loads(raw.decode("utf-8") if isinstance(raw, bytes)
                        else raw)
    expected = {
        "schema": CACHE_SCHEMA,
        "book_id": entry["book_id"],
        "lesson_id": entry["lesson_id"],
        "source_pdf_sha256": entry.get("source_pdf_sha256")
                              or entry.get("source_book_sha256"),
        "page_num": page_num,
        "source_page_sha256": _source_signature(doc, page_num),
        **_model_signature(provider, vision_model),
    }
    if not isinstance(record, dict) or any(
        record.get(key) != val for key, val in expected.items()):
        return None
    if not isinstance(record.get("data"), (list, dict)):
        raise RuntimeError(
            "PAGE_CHECKPOINT_CORRUPT: invalid data " + _filename(page_num, kind))
    return record["data"]


def _save_record(service, root_id, doc, entry, page_num, kind,
                 provider, vision_model, data):
    folder = _folder(service, root_id, entry, create=True)
    filename = _filename(page_num, kind)
    body = {
        "schema": CACHE_SCHEMA,
        "book_id": entry["book_id"],
        "lesson_id": entry["lesson_id"],
        "source_pdf_sha256": entry.get("source_pdf_sha256")
                              or entry.get("source_book_sha256"),
        "page_num": page_num,
        "source_page_sha256": _source_signature(doc, page_num),
        **_model_signature(provider, vision_model),
        "data": data,
    }
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    media = MediaIoBaseUpload(io.BytesIO(payload),
                              mimetype="application/json",
                              resumable=False)
    old = _children(service, folder, filename)
    if old:
        service.files().update(fileId=old, media_body=media,
                               fields="id").execute()
    else:
        service.files().create(body={
            "name": filename, "parents": [folder],
        }, media_body=media, fields="id").execute()


def _source_crop(doc, page_num, row, kind):
    import fitz
    from PIL import Image

    bbox = row.get("bbox") if kind == "PAGE" else row.get("source_bbox")
    if not isinstance(bbox, list) or len(bbox) != 4:
        raise ValueError("Missing original PDF figure/exercise bbox")
    area = fitz.Rect(*[float(v) for v in bbox])
    if area.is_empty or not doc[page_num - 1].rect.contains(area):
        raise ValueError("Source bbox outside physical textbook page")
    if kind == "EXERCISES":
        return doc[page_num - 1].get_pixmap(clip=area, dpi=200).tobytes("png")
    if row.get("evidence_method") == "EMBEDDED_IMAGE_WITH_SOURCE_BBOX":
        found = re.search(r"_E(\d+)$", row.get("figure_id", ""))
        if not found:
            raise ValueError("Embedded source image xref index missing")
        embeds = doc[page_num - 1].get_images(full=True)
        index = int(found.group(1)) - 1
        if index < 0 or index >= len(embeds):
            raise ValueError("Embedded source image index changed")
        original = doc.extract_image(embeds[index][0])
        with Image.open(io.BytesIO(original["image"])) as picture:
            buffer = io.BytesIO()
            picture.convert("RGB").save(buffer, format="PNG")
            return buffer.getvalue()
    if row.get("evidence_method") not in (
        "PDF_VECTOR_CROP",
        "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF",
    ):
        raise ValueError("Unexpected source image method")
    return doc[page_num - 1].get_pixmap(clip=area, dpi=180).tobytes("png")


def load_page(service, root_id, doc, entry, page_num, cache_dir,
              provider, vision_model):
    data = _load_record(service, root_id, doc, entry, page_num, "PAGE",
                        provider, vision_model)
    if data is None:
        return None
    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        raise RuntimeError("PAGE_CHECKPOINT_CORRUPT: source text missing")
    if not isinstance(data.get("figures"), list):
        raise RuntimeError("PAGE_CHECKPOINT_CORRUPT: source figures missing")
    figures = []
    for figure in data["figures"]:
        original = _source_crop(doc, page_num, figure, "PAGE")
        if hashlib.sha256(original).hexdigest() != figure.get("image_sha256"):
            raise RuntimeError(
                "PAGE_CHECKPOINT_IMAGE_MISMATCH: do not reuse page %d"
                % page_num)
        restored = dict(figure)
        path = Path(cache_dir) / (
            "cached_%s.png" % re.sub(
                r"[^A-Za-z0-9_-]", "_", figure["figure_id"]))
        path.write_bytes(original)
        restored["image_path"] = str(path)
        figures.append(restored)
    return {"page_num": page_num, "text": data["text"],
            "text_hash": hashlib.sha256(
                data["text"].encode("utf-8")).hexdigest()[:16],
            "figures": figures}


def save_page(service, root_id, doc, entry, page, provider, vision_model):
    data = {
        "text": page["text"],
        "figures": [
            {k: v for k, v in fig.items() if k != "image_path"}
            for fig in page["figures"]
        ],
    }
    _save_record(service, root_id, doc, entry, page["page_num"],
                 "PAGE", provider, vision_model, data)


def load_exercises(service, root_id, doc, entry, page_num, cache_dir,
                   provider, vision_model):
    data = _load_record(service, root_id, doc, entry, page_num, "EXERCISES",
                        provider, vision_model)
    if data is None:
        return None
    if not isinstance(data, list):
        raise RuntimeError("EXERCISE_CHECKPOINT_CORRUPT: not an array")
    rows = []
    for item in data:
        row = dict(item)
        if row.get("source_region_sha256"):
            original = _source_crop(doc, page_num, row, "EXERCISES")
            if (hashlib.sha256(original).hexdigest() !=
                    row["source_region_sha256"]):
                raise RuntimeError(
                    "EXERCISE_CHECKPOINT_REGION_MISMATCH: page %d" % page_num)
            path = Path(cache_dir) / (
                "cached_exercise_p%d_%d.png"
                % (page_num, int(row["number"])))
            path.write_bytes(original)
            row["source_region_image_ref"] = str(path)
        rows.append(row)
    return rows


def save_exercises(service, root_id, doc, entry, page_num, rows,
                   provider, vision_model):
    data = [
        {k: v for k, v in row.items() if k != "source_region_image_ref"}
        for row in rows
    ]
    _save_record(service, root_id, doc, entry, page_num, "EXERCISES",
                 provider, vision_model, data)


def invalidate_page(service, root_id, entry, page_num):
    folder = _folder(service, root_id, entry, create=False)
    if not folder:
        return
    fid = _children(service, folder, _filename(page_num, "PAGE"))
    if fid:
        service.files().delete(fileId=fid).execute()
