"""Deterministic cache identities and persistence for NABIL AI lessons.

Published Golden packages are served before RAG/embeddings/AI. Source signatures
remain available for strict verification when source chunks are already loaded.
"""
from __future__ import annotations
import hashlib, json, re
from typing import Any, Optional

DEFAULT_LESSON_LANGUAGE="en"
DEFAULT_PACKAGE_VERSION="0.01"
DEFAULT_TEACHING_MODE="full_lesson"
DEFAULT_LAB_ENGINE_VERSION="nabil-interactive-lab-v1"
PUBLISHED_STATUS="published"
_LESSON_ID_RE=re.compile(r"^[A-Z0-9][A-Z0-9._-]{2,127}$")

def _normalize(value:Any)->str: return str(value or "").strip().casefold()
def normalize_lesson_id(lesson_id:str)->str:
    value=str(lesson_id or "").strip().upper()
    if not value: raise ValueError("lesson_id is required")
    if not _LESSON_ID_RE.fullmatch(value): raise ValueError("Invalid lesson_id. Expected a stable identifier such as 'G12-MATH-GS-002'.")
    return value

def normalize_language(language:str|None)->str:
    value=str(language or DEFAULT_LESSON_LANGUAGE).strip().casefold().replace("_","-") or DEFAULT_LESSON_LANGUAGE
    aliases={"english":"en","anglais":"en","الإنجليزية":"en","الانجليزية":"en","français":"fr","francais":"fr","french":"fr","الفرنسية":"fr","arabic":"ar","العربية":"ar"}
    value=aliases.get(value,value)
    if len(value)>32: raise ValueError("Invalid language identifier")
    return value

def normalize_package_version(version:str|None)->str:
    value=str(version or DEFAULT_PACKAGE_VERSION).strip() or DEFAULT_PACKAGE_VERSION
    if len(value)>64 or not re.fullmatch(r"[A-Za-z0-9._-]+",value): raise ValueError("Invalid package version")
    return value

def lesson_package_identity(lesson_id:str,language:str=DEFAULT_LESSON_LANGUAGE,version:str=DEFAULT_PACKAGE_VERSION)->str:
    return "|".join((normalize_lesson_id(lesson_id),normalize_language(language),normalize_package_version(version)))

def lesson_package_key(lesson_id:str,language:str=DEFAULT_LESSON_LANGUAGE,version:str=DEFAULT_PACKAGE_VERSION)->str:
    return hashlib.sha256(lesson_package_identity(lesson_id,language,version).encode()).hexdigest()

def lesson_cache_key(grade:str,branch:str,subject:str,curriculum:str,language:str,lesson:str,teaching_mode:str)->str:
    raw="|".join(_normalize(x) for x in (grade,branch,subject,curriculum,language,lesson,teaching_mode))
    return hashlib.sha256(raw.encode()).hexdigest()

def source_signature(source_chunks:list[dict])->str:
    rows=[]
    for item in source_chunks or []:
        if isinstance(item,dict): rows.append((str(item.get("book_id") or ""),str(item.get("page") or ""),str(item.get("pdf_page") or ""),str(item.get("text") or "")[:240]))
    rows.sort()
    return hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()

def _json(value, fallback):
    try:
        parsed=json.loads(value or "")
        return parsed if isinstance(parsed,type(fallback)) else fallback
    except Exception:
        return fallback

def _package_to_dict(row)->dict[str,Any]:
    return {
        "cache_key":getattr(row,"cache_key",None), "signature":getattr(row,"source_signature",None) or getattr(row,"signature",None),
        "grade":getattr(row,"grade",None), "branch":getattr(row,"branch",None), "subject":getattr(row,"subject",None),
        "curriculum":getattr(row,"curriculum",None), "language":getattr(row,"language",None), "lesson":getattr(row,"lesson",None),
        "reply":getattr(row,"reply","") or "", "drawings":_json(getattr(row,"drawings_json",None),[]), "sources":_json(getattr(row,"sources_json",None),[]),
        "lesson_id":getattr(row,"lesson_id",None), "version":getattr(row,"version",None), "drive_file_id":getattr(row,"drive_file_id",None),
        "drive_url":getattr(row,"drive_url",None), "package_status":getattr(row,"package_status",None),
        "lab_html":getattr(row,"lab_html",None), "lab_spec":_json(getattr(row,"lab_spec_json",None),{}),
        "lab_engine_version":getattr(row,"lab_engine_version",None), "lesson_html":getattr(row,"lesson_html",None),
    }

def get_published_lesson(db,*,cache_key:str)->Optional[dict[str,Any]]:
    if not cache_key:return None
    from app.db.models import LessonPackage
    row=db.query(LessonPackage).filter(LessonPackage.cache_key==cache_key).first()
    if row is None:return None
    status=getattr(row,"package_status",None)
    if status and str(status).lower() not in {PUBLISHED_STATUS,"published_verified","golden"}:return None
    return _package_to_dict(row)

def get_cached_lesson(db,cache_key:str,signature:str)->Optional[dict[str,Any]]:
    item=get_published_lesson(db,cache_key=cache_key)
    if not item or not signature:return None
    return item if str(item.get("signature") or "")==str(signature) else None

def save_cached_lesson(db,*,cache_key:str,signature:str,grade:str,branch:str,subject:str,curriculum:str,language:str,lesson:str,reply:str,drawings:list,sources:list,
                       teaching_mode:str=DEFAULT_TEACHING_MODE,lesson_id:str|None=None,version:str|None=None,drive_file_id:str|None=None,drive_url:str|None=None,
                       package_status:str=PUBLISHED_STATUS,lab_html:str|None=None,lab_spec:dict|None=None,lab_engine_version:str=DEFAULT_LAB_ENGINE_VERSION,
                       lesson_html:str|None=None):
    """Upsert LessonPackage while remaining compatible with older deployed DB schemas."""
    from app.db.models import LessonPackage
    row=db.query(LessonPackage).filter(LessonPackage.cache_key==cache_key).first()
    if row is None: row=LessonPackage(cache_key=cache_key);db.add(row)
    values={"source_signature":signature,"signature":signature,"grade":grade,"branch":branch,"subject":subject,"curriculum":curriculum,"language":language,
            "lesson":lesson,"teaching_mode":teaching_mode,"reply":reply,"drawings_json":json.dumps(drawings or [],ensure_ascii=False),
            "sources_json":json.dumps(sources or [],ensure_ascii=False),"lesson_id":lesson_id,"version":version,"drive_file_id":drive_file_id,"drive_url":drive_url,
            "package_status":package_status,"lab_html":lab_html,"lab_spec_json":json.dumps(lab_spec or {},ensure_ascii=False) if lab_spec is not None else None,
            "lab_engine_version":lab_engine_version,"lesson_html":lesson_html}
    for key,value in values.items():
        if value is not None and hasattr(row,key):setattr(row,key,value)
    db.commit();db.refresh(row);return row
