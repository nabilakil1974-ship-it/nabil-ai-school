"""Universal lesson-package registry for NABIL batch production.

This module is deliberately zero-AI. The factory/batch worker produces package
manifests and artifacts; the platform only validates, indexes and serves them.

Package layout (default):
  data/lesson_packages/<LESSON_ID>/manifest.json
  data/lesson_packages/<LESSON_ID>/<artifact files>

The manifest may contain:
{
  "schema_version": "1.0",
  "lesson_id": "G12-MATH-GS-001",
  "title": "Irrational Functions",
  "grade": "12",
  "subject": "Mathematics",
  "subject_code": "MATH",
  "branch": "GS",
  "language": "en",
  "status": "READY",
  "source_identity": "...",
  "p1_identity": "...",
  "p2_scientific_identity": "...",
  "p3_status": "candidate",
  "artifacts": {
    "lesson_html": "lesson.html",
    "exercise_html": "exercises.html",
    "teacher_docx": "teacher/...docx",
    "teacher_json": "teacher/...json",
    "faq_bank": "faq_bank.json",
    "exercise_bank": "exercise_bank.json",
    "p3_manifest": "p3/manifest.json"
  }
}

Only status=READY packages are runtime-ready. Paths are resolved fail-closed
inside the package directory; no path traversal or fuzzy lesson fallback.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CATALOGUE_PATH = Path(
    os.getenv("NABIL_GOLDEN_CATALOGUE_PATH", str(ROOT / "data" / "NABIL_GOLDEN_CATALOGUE.json"))
)
PACKAGE_ROOT = Path(
    os.getenv("NABIL_LESSON_PACKAGES_DIR", str(ROOT / "data" / "lesson_packages"))
).resolve()

READY = "READY"
KNOWN_STATUSES = {"READY", "FAILED", "PROCESSING", "QUEUED", "CATALOGUED", "NEEDS_AUDIT"}

_SUBJECT_ALIASES = {
    "MATH": {"math", "maths", "mathematics", "mathematiques", "mathématiques", "رياضيات"},
    "PHYSICS": {"physics", "physique", "فيزياء"},
    "CHEMISTRY": {"chemistry", "chimie", "كيمياء"},
    "BIOLOGY": {"biology", "biologie", "علوم الحياة", "علومالحياة", "أحياء", "احياء"},
    "SCIENCE": {"science", "sciences", "علوم", "general science"},
    "ARABIC": {"arabic", "arabe", "لغة عربية", "اللغة العربية", "عربي"},
    "ENGLISH": {"english", "anglais", "لغة إنكليزية", "لغة انجليزية", "انكليزي", "إنكليزي"},
    "FRENCH": {"french", "francais", "français", "لغة فرنسية", "فرنسي"},
    "HISTORY": {"history", "histoire", "تاريخ"},
    "GEOGRAPHY": {"geography", "geographie", "géographie", "جغرافيا"},
    "CIVICS": {"civics", "civic education", "education civique", "تربية وطنية", "تربية مدنية", "وطنية"},
    "PHILOSOPHY": {"philosophy", "philosophie", "فلسفة"},
    "SOCIOLOGY": {"sociology", "sociologie", "اجتماع", "علم الاجتماع"},
    "ECONOMICS": {"economics", "economie", "économie", "اقتصاد"},
    "COMPUTER": {"computer", "informatics", "informatique", "computer science", "معلوماتية", "حاسوب"},
    "ART": {"art", "arts", "تربية فنية", "فنون"},
    "MUSIC": {"music", "musique", "موسيقى"},
    "PHYSICAL_ED": {"physical education", "sports", "sport", "تربية رياضية", "رياضة"},
}


def _norm(value: Any) -> str:
    return re.sub(r"[^a-z0-9\u0600-\u06ff]+", "", str(value or "").casefold())


def canonical_subject(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    upper = raw.upper().replace("-", "_").replace(" ", "_")
    if upper in _SUBJECT_ALIASES:
        return upper
    normalized = _norm(raw)
    for code, aliases in _SUBJECT_ALIASES.items():
        if normalized == _norm(code):
            return code
        if any(normalized == _norm(alias) for alias in aliases):
            return code
    # Stable subject codes embedded in lesson_id remain valid even when a
    # human-readable alias is not yet listed. Do not invent a new code from prose.
    if re.fullmatch(r"[A-Z][A-Z0-9_]{1,31}", upper):
        return upper
    return ""


def canonical_language(value: Any) -> str:
    raw = str(value or "").strip().casefold()
    if raw.startswith("fr") or raw in {"french", "francais", "français"}:
        return "fr"
    if raw.startswith("en") or raw in {"english", "anglais"}:
        return "en"
    if raw.startswith("ar") or raw in {"arabic", "arabe", "العربية", "عربي"}:
        return "ar"
    return ""


def lesson_meta(lesson_id: Any) -> dict[str, str]:
    lid = str(lesson_id or "").strip().upper()
    parts = [p for p in lid.split("-") if p]
    if len(parts) < 3 or not re.fullmatch(r"G\d{2}", parts[0]) or not re.fullmatch(r"\d{3}", parts[-1]):
        return {}
    grade = str(int(parts[0][1:]))
    subject = canonical_subject(parts[1])
    language = ""
    branch = ""
    for token in parts[2:-1]:
        if token in {"AR", "EN", "FR"}:
            language = token.lower()
        elif token in {"GS", "LS", "SV", "SE", "ES", "LH", "HUM"}:
            branch = {"SV": "LS", "ES": "SE", "HUM": "LH"}.get(token, token)
    return {
        "lesson_id": lid,
        "grade": grade,
        "subject_code": subject,
        "language": language,
        "branch": branch,
        "sequence": parts[-1],
    }


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return None


def catalogue_rows() -> list[dict[str, Any]]:
    data = _load_json(CATALOGUE_PATH)
    if not isinstance(data, dict):
        return []
    raw = data.get("lessons", [])
    if isinstance(raw, dict):
        raw = list(raw.values())
    if not isinstance(raw, list):
        return []
    rows: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        lid = str(item.get("lesson_id") or "").strip().upper()
        meta = lesson_meta(lid)
        if not meta:
            continue
        subject_code = canonical_subject(item.get("subject_code") or item.get("subject") or meta["subject_code"])
        language = canonical_language(item.get("language")) or meta["language"]
        rows.append({
            **item,
            **meta,
            "lesson_id": lid,
            "title": str(item.get("title") or item.get("canonical_title") or lid),
            "subject_code": subject_code or meta["subject_code"],
            "language": language,
            "status": str(item.get("package_status") or item.get("status") or "CATALOGUED").upper(),
            "catalogued": True,
            "runtime_ready": False,
            "registry_source": "canonical_catalogue",
        })
    return rows


def _artifact_map(package_dir: Path, manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw = manifest.get("artifacts") or {}
    if not isinstance(raw, dict):
        return {}
    out: dict[str, dict[str, Any]] = {}
    for kind, rel_value in raw.items():
        kind = str(kind or "").strip()
        rel = str(rel_value or "").strip()
        if not kind or not rel:
            continue
        candidate = (package_dir / rel).resolve()
        try:
            candidate.relative_to(package_dir.resolve())
        except ValueError:
            continue
        if not candidate.is_file():
            continue
        out[kind] = {
            "kind": kind,
            "relative_path": candidate.relative_to(package_dir).as_posix(),
            "path": str(candidate),
            "bytes": candidate.stat().st_size,
        }
    return out


def package_rows() -> list[dict[str, Any]]:
    if not PACKAGE_ROOT.is_dir():
        return []
    rows: list[dict[str, Any]] = []
    for manifest_path in sorted(PACKAGE_ROOT.glob("*/manifest.json")):
        manifest = _load_json(manifest_path)
        if not isinstance(manifest, dict):
            continue
        package_dir = manifest_path.parent.resolve()
        lid = str(manifest.get("lesson_id") or package_dir.name).strip().upper()
        meta = lesson_meta(lid)
        if not meta or package_dir.name.upper() != lid:
            continue
        status = str(manifest.get("status") or "").strip().upper()
        if status not in KNOWN_STATUSES:
            status = "NEEDS_AUDIT"
        artifacts = _artifact_map(package_dir, manifest)
        lesson_html = artifacts.get("lesson_html")
        runtime_ready = status == READY and bool(lesson_html)
        rows.append({
            **manifest,
            **meta,
            "lesson_id": lid,
            "title": str(manifest.get("title") or manifest.get("canonical_title") or lid),
            "subject_code": canonical_subject(
                manifest.get("subject_code") or manifest.get("subject") or meta["subject_code"]
            ) or meta["subject_code"],
            "language": canonical_language(manifest.get("language")) or meta["language"],
            "status": status,
            "catalogued": True,
            "runtime_ready": runtime_ready,
            "registry_source": "lesson_package",
            "package_dir": str(package_dir),
            "artifacts": artifacts,
        })
    return rows


def combined_rows() -> list[dict[str, Any]]:
    merged = {row["lesson_id"]: row for row in catalogue_rows()}
    for pkg in package_rows():
        base = dict(merged.get(pkg["lesson_id"], {}))
        base.update(pkg)
        merged[pkg["lesson_id"]] = base
    return [merged[k] for k in sorted(merged)]


def get_lesson(lesson_id: str) -> dict[str, Any] | None:
    lid = str(lesson_id or "").strip().upper()
    return next((row for row in combined_rows() if row["lesson_id"] == lid), None)


def get_artifact(lesson_id: str, artifact_kind: str) -> Path | None:
    item = get_lesson(lesson_id)
    if not item or item.get("runtime_ready") is not True:
        return None
    artifacts = item.get("artifacts")
    if not isinstance(artifacts, dict):
        return None
    record = artifacts.get(str(artifact_kind or "").strip())
    if not isinstance(record, dict):
        return None
    raw = str(record.get("path") or "").strip()
    if not raw:
        return None
    path = Path(raw).resolve()
    package_dir = Path(str(item.get("package_dir") or "")).resolve()
    try:
        path.relative_to(package_dir)
    except ValueError:
        return None
    return path if path.is_file() else None


def filter_rows(
    *, grade: str = "", subject: str = "", language: str = "",
    branch: str = "", status: str = "", runtime_ready: bool | None = None,
) -> list[dict[str, Any]]:
    wanted_grade = str(grade or "").strip().lstrip("Gg0") or str(grade or "").strip()
    wanted_subject = canonical_subject(subject)
    wanted_language = canonical_language(language)
    wanted_branch = str(branch or "").strip().upper()
    wanted_status = str(status or "").strip().upper()
    out = []
    for row in combined_rows():
        if wanted_grade and str(row.get("grade") or "") != str(int(wanted_grade)) if wanted_grade.isdigit() else False:
            continue
        if wanted_subject and row.get("subject_code") != wanted_subject:
            continue
        if wanted_language and row.get("language") != wanted_language:
            continue
        if wanted_branch and str(row.get("branch") or "").upper() != wanted_branch:
            continue
        if wanted_status and str(row.get("status") or "").upper() != wanted_status:
            continue
        if runtime_ready is not None and bool(row.get("runtime_ready")) is not runtime_ready:
            continue
        out.append(row)
    return out


def public_row(row: dict[str, Any]) -> dict[str, Any]:
    artifacts = row.get("artifacts") if isinstance(row.get("artifacts"), dict) else {}
    return {
        "lesson_id": row.get("lesson_id"),
        "title": row.get("title"),
        "grade": row.get("grade"),
        "subject_code": row.get("subject_code"),
        "language": row.get("language"),
        "branch": row.get("branch"),
        "status": row.get("status"),
        "runtime_ready": bool(row.get("runtime_ready")),
        "registry_source": row.get("registry_source"),
        "artifact_kinds": sorted(artifacts),
        "source_identity": row.get("source_identity"),
        "p1_identity": row.get("p1_identity"),
        "p2_scientific_identity": row.get("p2_scientific_identity"),
        "p3_status": row.get("p3_status"),
    }


def readiness_summary() -> dict[str, Any]:
    rows = combined_rows()
    counts: dict[str, int] = {}
    subject_counts: dict[str, dict[str, int]] = {}
    grade_counts: dict[str, dict[str, int]] = {}
    for row in rows:
        status = str(row.get("status") or "UNKNOWN").upper()
        counts[status] = counts.get(status, 0) + 1
        sc = str(row.get("subject_code") or "UNKNOWN")
        subject_counts.setdefault(sc, {"total": 0, "ready": 0})
        subject_counts[sc]["total"] += 1
        subject_counts[sc]["ready"] += int(bool(row.get("runtime_ready")))
        gr = str(row.get("grade") or "UNKNOWN")
        grade_counts.setdefault(gr, {"total": 0, "ready": 0})
        grade_counts[gr]["total"] += 1
        grade_counts[gr]["ready"] += int(bool(row.get("runtime_ready")))
    ready = sum(1 for r in rows if r.get("runtime_ready"))
    return {
        "schema_version": "1.0",
        "total_lessons": len(rows),
        "runtime_ready": ready,
        "not_runtime_ready": len(rows) - ready,
        "status_counts": counts,
        "subjects": subject_counts,
        "grades": grade_counts,
        "package_root": str(PACKAGE_ROOT),
        "zero_ai_runtime": True,
    }
