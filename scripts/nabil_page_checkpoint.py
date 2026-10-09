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

from scripts.nabil_transient_resilience_v1781 import CheckpointWriteError

CACHE_SCHEMA = "PAGE_EVIDENCE_V1_SOURCE_LOCKED"
FACTORY_STATE_SCHEMA = "NABIL_FACTORY_RECOVERY_STATE_V1782"
SOLUTION_PROMPT_VERSION = "NABIL_GROUNDED_SOLUTION_V1782"
PAID_UNIT_SCHEMA = "NABIL_PAID_UNIT_V1783"
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


def _write_json_verified(service, folder, filename, body):
    """Write one Drive checkpoint atomically enough for recovery and verify bytes.

    Google Drive create/update is followed by a full read-back.  The factory
    must never continue after an unverified checkpoint write.
    """
    payload = json.dumps(
        body, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    media = MediaIoBaseUpload(
        io.BytesIO(payload), mimetype="application/json", resumable=False)
    old = _children(service, folder, filename)
    try:
        if old:
            fid = service.files().update(
                fileId=old, media_body=media, fields="id").execute()["id"]
        else:
            fid = service.files().create(
                body={"name": filename, "parents": [folder]},
                media_body=media, fields="id").execute()["id"]
        raw = service.files().get_media(fileId=fid).execute()
        remote = raw if isinstance(raw, bytes) else str(raw).encode("utf-8")
        # Parse and canonicalize on both sides so harmless JSON whitespace/order
        # changes cannot create a false mismatch.
        remote_obj = json.loads(remote.decode("utf-8"))
        remote_canon = json.dumps(
            remote_obj, ensure_ascii=False, sort_keys=True,
            separators=(",", ":")).encode("utf-8")
        if hashlib.sha256(remote_canon).hexdigest() != hashlib.sha256(payload).hexdigest():
            raise CheckpointWriteError(
                "CHECKPOINT_READBACK_MISMATCH:" + filename)
        return fid
    except CheckpointWriteError:
        raise
    except Exception as exc:
        raise CheckpointWriteError(
            "CHECKPOINT_WRITE_OR_READBACK_FAILED:%s:%s"
            % (filename, exc)) from exc


def _filename(page_num, kind):
    if kind not in ("PAGE", "EXERCISES"):
        raise ValueError("Invalid page cache kind")
    return "%s_%04d.json" % (kind, page_num)


def _source_signature(doc, page_num):
    page = doc[page_num - 1]
    return hashlib.sha256(page.get_pixmap(dpi=72).samples).hexdigest()


def _model_signature(provider, vision_model):
    # Compatibility key for deciding whether an old checkpoint belongs to the
    # same requested primary run configuration. This is NOT evidence origin.
    return {"provider": provider, "vision_model": vision_model}


def _collect_actual_provenance(value):
    """Collect actual provider/model metadata embedded in evidence objects."""
    found = []

    def walk(node):
        if isinstance(node, dict):
            if (
                "provider" in node
                and "model" in node
                and ("used_failover" in node or "completed_at" in node)
            ):
                item = {
                    "provider": node.get("provider"),
                    "model": node.get("model"),
                    "primary_provider": node.get("primary_provider"),
                    "used_failover": bool(node.get("used_failover", False)),
                    "completed_at": node.get("completed_at"),
                }
                if item not in found:
                    found.append(item)
            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(value)
    return found


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
        "provider_fields_role": "CHECKPOINT_COMPATIBILITY_KEY_NOT_EVIDENCE_ORIGIN",
        "actual_provenance": _collect_actual_provenance(data),
        "data": data,
    }
    _write_json_verified(service, folder, filename, body)


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
    method = row.get("evidence_method")
    if method not in (
        "PDF_VECTOR_CROP",
        "APPROVED_VISION_BOX_CROPPED_FROM_SOURCE_PDF",
        "TARGETED_HIGHRES_VISION_PLUS_LOCAL_CAPTION_OCR",
    ):
        raise ValueError("Unexpected source image method")
    dpi = 220 if method == "TARGETED_HIGHRES_VISION_PLUS_LOCAL_CAPTION_OCR" else 180
    return doc[page_num - 1].get_pixmap(
        clip=area, dpi=dpi).tobytes("png")


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


def _solution_filename(exercise):
    safe = re.sub(r"[^A-Za-z0-9_-]", "_",
                  str(exercise.get("exercise_id") or "exercise"))
    return "SOLUTION_%s.json" % safe


def load_solution(service, root_id, entry, exercise,
                  prompt_version=SOLUTION_PROMPT_VERSION,
                  operation="exercise_solution"):
    """Restore a verified solved exercise independently of page extraction."""
    folder = _folder(service, root_id, entry, create=False)
    if not folder:
        return None
    filename = _solution_filename(exercise)
    fid = _children(service, folder, filename)
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
        "exercise_id": exercise.get("exercise_id"),
        "source_prompt_hash": exercise.get("source_prompt_hash"),
        "source_origin": exercise.get("source_origin"),
        "source_page": exercise.get("source_page"),
        "figure_hashes": list(exercise.get("figure_hashes") or []),
        "scope_concept_ids": list(exercise.get("scope_concept_ids") or []),
        "prompt_version": prompt_version,
        "operation": operation,
    }
    if not isinstance(record, dict) or any(
            record.get(k) != v for k, v in expected.items()):
        return None
    solution = record.get("solution")
    if (not isinstance(solution, dict)
            or not isinstance(solution.get("steps"), list)
            or not solution.get("final_answer")):
        raise RuntimeError(
            "SOLUTION_CHECKPOINT_CORRUPT: " + filename)
    return solution


def save_solution(service, root_id, entry, exercise, solution,
                  prompt_version=SOLUTION_PROMPT_VERSION,
                  operation="exercise_solution"):
    """Persist one independently verified exercise solution."""
    if (not isinstance(solution, dict)
            or not isinstance(solution.get("steps"), list)
            or not solution.get("final_answer")):
        raise RuntimeError("SOLUTION_CHECKPOINT_INVALID")
    folder = _folder(service, root_id, entry, create=True)
    filename = _solution_filename(exercise)
    body = {
        "schema": CACHE_SCHEMA,
        "book_id": entry["book_id"],
        "lesson_id": entry["lesson_id"],
        "source_pdf_sha256": entry.get("source_pdf_sha256")
                              or entry.get("source_book_sha256"),
        "exercise_id": exercise.get("exercise_id"),
        "source_prompt_hash": exercise.get("source_prompt_hash"),
        "source_origin": exercise.get("source_origin"),
        "source_page": exercise.get("source_page"),
        "figure_hashes": list(exercise.get("figure_hashes") or []),
        "scope_concept_ids": list(exercise.get("scope_concept_ids") or []),
        "prompt_version": prompt_version,
        "operation": operation,
        "actual_provenance": _collect_actual_provenance(solution),
        "solution": solution,
    }
    _write_json_verified(service, folder, filename, body)



def _paid_unit_filename(operation, unit_id):
    safe_op = re.sub(r"[^A-Za-z0-9_-]", "_", str(operation or "operation"))
    safe_unit = re.sub(r"[^A-Za-z0-9_-]", "_", str(unit_id or "unit"))
    return "PAID_%s_%s.json" % (safe_op[:70], safe_unit[:90])


def load_paid_unit(service, root_id, entry, *, operation, unit_id,
                   source_hash, prompt_version):
    """Restore one verified paid-stage result only for the exact source/prompt."""
    folder = _folder(service, root_id, entry, create=False)
    if not folder:
        return None
    filename = _paid_unit_filename(operation, unit_id)
    fid = _children(service, folder, filename)
    if not fid:
        return None
    raw = service.files().get_media(fileId=fid).execute()
    record = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
    expected = {
        "schema": PAID_UNIT_SCHEMA,
        "book_id": entry.get("book_id"),
        "lesson_id": entry.get("lesson_id"),
        "source_pdf_sha256": (
            entry.get("source_pdf_sha256") or entry.get("source_book_sha256")),
        "operation": str(operation),
        "unit_id": str(unit_id),
        "source_hash": str(source_hash),
        "prompt_version": str(prompt_version),
    }
    if not isinstance(record, dict) or any(
            record.get(k) != v for k, v in expected.items()):
        return None
    payload = record.get("payload")
    if payload is None:
        raise RuntimeError("PAID_UNIT_CHECKPOINT_CORRUPT:" + filename)
    return payload


def save_paid_unit(service, root_id, entry, *, operation, unit_id,
                   source_hash, prompt_version, payload, provenance=None):
    """Persist and read-back verify one paid-stage result."""
    folder = _folder(service, root_id, entry, create=True)
    body = {
        "schema": PAID_UNIT_SCHEMA,
        "book_id": entry.get("book_id"),
        "lesson_id": entry.get("lesson_id"),
        "source_pdf_sha256": (
            entry.get("source_pdf_sha256") or entry.get("source_book_sha256")),
        "operation": str(operation),
        "unit_id": str(unit_id),
        "source_hash": str(source_hash),
        "prompt_version": str(prompt_version),
        "actual_provenance": dict(provenance or {}),
        "payload": payload,
    }
    _write_json_verified(
        service, folder, _paid_unit_filename(operation, unit_id), body)
    return payload


def _factory_state_filename():
    return "FACTORY_STATE.json"


def load_factory_state(service, root_id, entry):
    folder = _folder(service, root_id, entry, create=False)
    if not folder:
        return None
    fid = _children(service, folder, _factory_state_filename())
    if not fid:
        return None
    raw = service.files().get_media(fileId=fid).execute()
    data = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
    if not isinstance(data, dict):
        raise RuntimeError("FACTORY_STATE_CORRUPT")
    if data.get("schema") != FACTORY_STATE_SCHEMA:
        return None
    if data.get("book_id") != entry.get("book_id"):
        return None
    if data.get("lesson_id") != entry.get("lesson_id"):
        return None
    expected_source = (
        entry.get("source_pdf_sha256") or entry.get("source_book_sha256"))
    if data.get("source_pdf_sha256") != expected_source:
        return None
    return data


def save_factory_state(service, root_id, entry, state):
    """Persist recovery/pause status next to page/solution checkpoints."""
    if not isinstance(state, dict) or not str(state.get("status") or "").strip():
        raise RuntimeError("FACTORY_STATE_INVALID")
    folder = _folder(service, root_id, entry, create=True)
    body = {
        "schema": FACTORY_STATE_SCHEMA,
        "book_id": entry.get("book_id"),
        "lesson_id": entry.get("lesson_id"),
        "source_pdf_sha256": (
            entry.get("source_pdf_sha256") or entry.get("source_book_sha256")),
        **state,
    }
    _write_json_verified(
        service, folder, _factory_state_filename(), body)
    return body


def invalidate_page(service, root_id, entry, page_num):
    folder = _folder(service, root_id, entry, create=False)
    if not folder:
        return
    fid = _children(service, folder, _filename(page_num, "PAGE"))
    if fid:
        service.files().delete(fileId=fid).execute()
