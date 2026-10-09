from __future__ import annotations

# ============================================================================== 
# PUBLISHED LAB ARTIFACT STORE — BUILD ONCE, SERVE MANY
# ============================================================================== 
# Only factory-produced, quality-gated lab HTML is written here. Runtime/student
# requests must read these static artifacts; they must not invoke AI/RAG to rebuild
# an already published lab.
PUBLISHED_LABS_DIR = ROOT / "data" / "published_labs"
PUBLISHED_LABS_INDEX = PUBLISHED_LABS_DIR / "index.json"
PUBLISHED_LABS_DIR.mkdir(parents=True, exist_ok=True)


def _published_lab_safe_part(value: str) -> str:
    value = str(value or "").strip()
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-.")
    return value or "unknown"


def _published_lab_artifact_key(
        lesson_id: str, lab_key: str, language: str,
        engine_version: str = REFERENCE_RENDERER_CONTRACT) -> str:
    raw = "|".join(str(x or "").strip().casefold() for x in (
        lesson_id, lab_key, language, engine_version,
    ))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _atomic_write_text(path: Path, content: str) -> None:
    """Replace a static artifact atomically; never expose a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def _load_published_labs_index() -> dict:
    if not PUBLISHED_LABS_INDEX.exists():
        return {"schema": "nabil-published-labs/v1", "labs": {}, "lessons": {}}
    try:
        data = json.loads(PUBLISHED_LABS_INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"PUBLISHED_LABS_INDEX_INVALID:{exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError("PUBLISHED_LABS_INDEX_INVALID:ROOT_NOT_OBJECT")
    if not isinstance(data.get("labs", {}), dict):
        raise RuntimeError("PUBLISHED_LABS_INDEX_INVALID:LABS_NOT_OBJECT")
    if not isinstance(data.get("lessons", {}), dict):
        raise RuntimeError("PUBLISHED_LABS_INDEX_INVALID:LESSONS_NOT_OBJECT")
    data.setdefault("schema", "nabil-published-labs/v1")
    data.setdefault("labs", {})
    data.setdefault("lessons", {})
    return data


def _persist_one_verified_lab(
        *, lesson_id: str, lab_key: str, language: str, html_text: str,
        kind: str, spec: Optional[dict] = None) -> dict:
    """Persist HTML already built by the factory; validate spec again when present."""
    lesson_id = str(lesson_id or "").strip()
    lab_key = str(lab_key or "").strip()
    language = resolve_lang_code(language or "en")
    html_text = str(html_text or "")
    if not lesson_id or not lab_key:
        raise RuntimeError("PUBLISHED_LAB_IDENTITY_REQUIRED")
    if not html_text.strip():
        raise RuntimeError(f"PUBLISHED_LAB_HTML_EMPTY:{lesson_id}:{lab_key}")
    if spec is not None:
        if not isinstance(spec, dict):
            raise RuntimeError(f"PUBLISHED_LAB_SPEC_INVALID:{lesson_id}:{lab_key}")
        # Preserve the existing fail-closed scientific/evidence validation.
        validate_lab_spec(spec)

    artifact_key = _published_lab_artifact_key(lesson_id, lab_key, language)
    rel = (Path(_published_lab_safe_part(lesson_id)) /
           _published_lab_safe_part(language) /
           _published_lab_safe_part(REFERENCE_RENDERER_CONTRACT) /
           f"{artifact_key}.html")
    out = PUBLISHED_LABS_DIR / rel
    payload = html_text.encode("utf-8")
    sha = hashlib.sha256(payload).hexdigest()
    if not out.exists() or hashlib.sha256(out.read_bytes()).hexdigest() != sha:
        _atomic_write_text(out, html_text)
    return {
        "artifact_key": artifact_key,
        "lesson_id": lesson_id,
        "lab_key": lab_key,
        "language": language,
        "kind": str(kind or "lab"),
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "path": rel.as_posix(),
        "sha256": sha,
        "bytes": len(payload),
    }


def persist_quality_gated_labs(entry: dict, theory: dict, exercises: list) -> dict:
    """Publish all prebuilt labs only AFTER lesson QA + scientific review succeed."""
    lesson_id = str(entry.get("lesson_id") or "").strip()
    language = resolve_lang_code(entry.get("language", "en"))
    records = []

    for act in theory.get("activities") or []:
        lab_html = str(act.get("lab_html") or "")
        if not lab_html.strip():
            continue
        concept_id = str(act.get("concept_id") or "").strip()
        records.append(_persist_one_verified_lab(
            lesson_id=lesson_id,
            lab_key=f"concept:{concept_id}",
            language=language,
            html_text=lab_html,
            kind=str((act.get("lab_spec") or {}).get("kind") or "concept"),
            spec=act.get("lab_spec"),
        ))

    for ex in exercises or []:
        lab_html = str(ex.get("_prebuilt_lab_html") or "")
        lab_key = str(ex.get("_prebuilt_lab_key") or "").strip()
        if not lab_html.strip() or not lab_key:
            continue
        records.append(_persist_one_verified_lab(
            lesson_id=lesson_id,
            lab_key=lab_key,
            language=language,
            html_text=lab_html,
            kind=str((ex.get("_prebuilt_lab_spec") or {}).get("kind") or "exercise"),
            spec=ex.get("_prebuilt_lab_spec"),
        ))

    # This is the complete autonomous teacher-led lesson lab assembled from the
    # already verified concept labs/teaching steps. Persist the exact generated HTML.
    whole_html = str(theory.get("whole_lesson_lab_html") or "")
    if whole_html.strip():
        records.append(_persist_one_verified_lab(
            lesson_id=lesson_id,
            lab_key="lesson:whole",
            language=language,
            html_text=whole_html,
            kind="whole_lesson_teacher",
            spec=None,
        ))

    index = _load_published_labs_index()
    lesson_record_keys = []
    for record in records:
        key = record["artifact_key"]
        index["labs"][key] = record
        lesson_record_keys.append(key)
    index["lessons"][lesson_id] = {
        "lesson_id": lesson_id,
        "language": language,
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "artifact_keys": lesson_record_keys,
        "runtime_ai_required": False,
        "updated_at": now(),
    }
    index["updated_at"] = now()
    _atomic_write_text(
        PUBLISHED_LABS_INDEX,
        json.dumps(index, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    progress(
        "PUBLISHED_STATIC_LABS_READY",
        lesson_id=lesson_id,
        artifacts=len(records),
        index=str(PUBLISHED_LABS_INDEX),
    )
    return {
        "lesson_id": lesson_id,
        "artifacts": records,
        "index": str(PUBLISHED_LABS_INDEX),
    }

_ARABIC_COLLOQUIAL_TOKENS = (
    "هلق", "شو", "بدك", "بدي", "فيك", "هيك", "هيدا", "هيدي",
    "هني", "ليش", "يلا", "خلينا", "رح ", "عم ", "منشوف", "منعمل",
)


def _assert_formal_arabic_text(value: str, *, purpose: str) -> None:
    """Reject generated/translated Arabic dialect in student teaching text.

    Never run this against raw textbook evidence; only NABIL-authored teaching
    or translation output is checked.
    """
    text = " " + re.sub(r"\s+", " ", str(value or "")).strip() + " "
    found = [tok.strip() for tok in _ARABIC_COLLOQUIAL_TOKENS
             if tok in text]
    if found:
        raise RuntimeError(
            f"FORMAL_ARABIC_REQUIRED:{purpose}:"
            + ",".join(sorted(set(found))))


def reference_renderer_css() -> str:
    """Shared lesson/exercise presentation contract for every subject/grade."""
    return r"""
:root{
 --nabil-ref-page:#05172d;--nabil-ref-header:#002973;
 --nabil-ref-panel:#081e33;--nabil-ref-card:#062039;
 --nabil-ref-deep:#0b1c36;--nabil-ref-control:#0d223d;
 --nabil-ref-border:#13618f;--nabil-ref-cyan:#14c8f5;
 --nabil-ref-cyan-text:#65dfff;--nabil-ref-text:#eef8ff;
 --nabil-ref-muted:#b9d7ea;--nabil-ref-green:#009e48;
 --nabil-ref-red:#ea202c;--nabil-ref-blue:#0874e8;
 --nabil-ref-purple:#5a35ca;--nabil-ref-yellow:#ffd447;
}
*{box-sizing:border-box}
html{color-scheme:dark;background:var(--nabil-ref-page)}
body{
 margin:0!important;padding:14px!important;max-width:100vw!important;
 overflow-x:hidden!important;background:var(--nabil-ref-page)!important;
 color:var(--nabil-ref-text)!important;
 font-family:system-ui,-apple-system,"Segoe UI",Arial,sans-serif!important;
}
.container{width:100%!important;max-width:1180px!important;margin:0 auto!important;min-width:0!important}
.header{
 display:flex!important;justify-content:space-between!important;align-items:center!important;
 gap:10px!important;flex-wrap:wrap!important;padding:12px 14px!important;
 background:linear-gradient(90deg,#05172d,var(--nabil-ref-header),#05172d)!important;
 border:1px solid #0b4d7f!important;border-radius:16px!important;
 position:sticky;top:4px;z-index:30;
}
.header h1{color:var(--nabil-ref-cyan-text)!important;overflow-wrap:anywhere}
.header-actions{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;align-items:center}
.card,.nabil-concept-card,.nabil-exercise-card,.ws-item,
#goldenReferenceCard,.lesson-final-card,.nabil-sci-card{
 background:linear-gradient(180deg,#08243d,#061d33)!important;
 color:var(--nabil-ref-text)!important;
 border:1px solid var(--nabil-ref-border)!important;
 border-radius:16px!important;box-shadow:0 12px 28px rgba(0,0,0,.28)!important;
 min-width:0!important;max-width:100%!important;
}
.card{padding:16px!important}
.nabil-concept-card h3,.nabil-exercise-card h3,#goldenReferenceCard h2,
.nabil-reference-concept>div>span:first-child{
 color:var(--nabil-ref-cyan-text)!important;
}
.nabil-teacher-step{
 background:#0b2a45!important;color:var(--nabil-ref-text)!important;
 border-inline-start-color:var(--nabil-ref-cyan)!important;
}
.nav-btn,.q-opt,.nabil-smart-lab-action{
 min-height:44px!important;border-radius:10px!important;
 border:1px solid #1f77aa!important;color:#fff!important;
 background:#0f3655!important;padding:9px 12px!important;
 font:inherit!important;font-weight:800!important;cursor:pointer;
 max-width:100%;
}
.q-opt{background:#0d2b45!important}
.nav-btn[style*="#0f766e"],.nabil-explain-lab-btn{background:#0f766e!important;border-color:#39c7b0!important}
.nav-btn[style*="#7c3aed"]{background:var(--nabil-ref-purple)!important;border-color:#9b7af1!important}
.nabil-prebuilt-exercise-lab,.interactive-lab{
 width:100%!important;max-width:100%!important;min-width:0!important;
 overflow:hidden!important;
}
.interactive-lab svg,.nabil-prebuilt-exercise-lab svg,
.nabil-explanatory-visual svg,.nabil-sci-visual-stage svg{
 display:block!important;width:100%!important;max-width:100%!important;height:auto!important;
}
.nabil-reference-concept{
 background:linear-gradient(160deg,#0f3151,#0a2239)!important;
 color:var(--nabil-ref-text)!important;border:1px solid #2f5f86!important;
 border-radius:14px!important;padding:12px!important;min-width:0!important;
}
.nabil-reference-concept *{color:inherit}

/* APPROVED NABIL SCIENTIFIC CARD — concept + final */
.nabil-sci-card{--bg:#07192d;--panel:#0d2945;--panel2:#0a2239;--line:#2f5f86;--cyan:#6ce7ff;--gold:#ffd36a;--green:#7ce6b8;--red:#ff8b98;--txt:#f4fbff;--muted:#bed4e5;background:radial-gradient(circle at 50% -20%,#153f68,#07192d 70%)!important;color:var(--txt)!important;border:1px solid #2d638d!important;border-radius:22px!important;padding:14px!important;box-shadow:0 16px 44px rgba(0,0,0,.24)!important;margin:14px 0!important;overflow:hidden!important;width:100%!important;box-sizing:border-box!important}
.nabil-sci-top{display:flex;gap:12px;align-items:center;justify-content:space-between;border-bottom:1px solid #2a5479;padding:2px 4px 11px;flex-wrap:wrap}
.nabil-sci-brand{font-weight:900;color:var(--cyan);letter-spacing:.7px}.nabil-sci-badge{font-size:.75rem;border:1px solid #46789e;border-radius:999px;padding:4px 10px;color:#d8efff}
.nabil-sci-title{margin:9px 0 2px;font-size:clamp(1.15rem,3vw,1.65rem);line-height:1.25;overflow-wrap:anywhere;color:#f4fbff!important}
.nabil-sci-grid{display:grid;grid-template-columns:minmax(250px,.92fr) minmax(390px,1.55fr) minmax(190px,.64fr);gap:12px;margin-top:12px;align-items:stretch}
.nabil-sci-panel{background:linear-gradient(160deg,#0f3151,#0a2239)!important;border:1px solid var(--line)!important;border-radius:17px!important;padding:13px!important;min-width:0}
.nabil-sci-panel h3{margin:0 0 9px;color:#9eeeff!important;font-size:1rem}.nabil-sci-section{border-top:1px solid #284e6f;padding-top:9px;margin-top:9px}.nabil-sci-label{font-weight:800;color:#8fe8ff}.nabil-sci-value{color:#fff;white-space:pre-wrap;overflow-wrap:anywhere}
.nabil-sci-visual{min-height:310px;display:flex;flex-direction:column;gap:10px}.nabil-sci-visual-stage{flex:1;display:block;background:#061827;border:1px solid #274d6d;border-radius:14px;padding:10px;overflow:auto}.nabil-sci-visual-stage svg,.nabil-sci-visual-stage canvas,.nabil-sci-visual-stage img{display:block;max-width:100%;height:auto;max-height:480px}
.nabil-sci-teacher{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;min-height:100%}.nabil-sci-avatar{width:min(100%,180px);max-height:230px;object-fit:contain;filter:drop-shadow(0 12px 22px rgba(0,0,0,.25))}.nabil-sci-teacher strong{color:var(--cyan);font-size:1.05rem}.nabil-sci-teacher p{margin:0;color:#d7e9f6;line-height:1.5}
.nabil-sci-final{margin-top:12px;background:linear-gradient(145deg,#0e3547,#0b2939);border:1px solid #3b8b8a;border-radius:16px;padding:12px}.nabil-sci-final h3{margin:0 0 7px;color:#8ff3d7!important}.nabil-sci-results{display:flex;gap:8px;flex-wrap:wrap}.nabil-sci-chip{border:1px solid #41769a;background:#0c2a45;border-radius:999px;padding:5px 9px;font-size:.84rem;overflow-wrap:anywhere}.nabil-sci-verify{margin-top:9px;border-inline-start:4px solid var(--green);background:#0d2d36;border-radius:9px;padding:9px 10px}.nabil-sci-list{margin:0;padding-inline-start:18px;line-height:1.65}.nabil-sci-list li{margin:5px 0;overflow-wrap:anywhere}
.nabil-sci-tools{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}.nabil-sci-tools button{border:1px solid #4d80a5;background:#123d60;color:white;border-radius:10px;padding:8px 11px;cursor:pointer;font:inherit}.nabil-flow-row{margin:8px 0;padding:9px 11px;border-radius:10px;background:#0b2a45;border-inline-start:4px solid #14c8f5;line-height:1.55}.nabil-flow-row b{color:#8fe8ff}.nabil-flow-row.nabil-conclude{border-inline-start-color:#7ce6b8;background:#0d2d36}.nabil-flow-row.nabil-apply{border-inline-start-color:#ffd36a;background:#302b18}
@media(max-width:1080px){.nabil-sci-grid{grid-template-columns:minmax(250px,.9fr) minmax(360px,1.5fr)}.nabil-sci-teacher-panel{grid-column:1/-1}.nabil-sci-teacher{flex-direction:row;text-align:start;justify-content:flex-start}.nabil-sci-avatar{width:110px}}
@media(max-width:760px){.nabil-sci-card{padding:10px!important;border-radius:16px!important}.nabil-sci-grid{grid-template-columns:1fr!important}.nabil-sci-panel{padding:11px!important}.nabil-sci-teacher-panel{grid-column:auto}.nabil-sci-teacher{flex-direction:row;text-align:start}.nabil-sci-avatar{width:84px;max-height:112px}.nabil-sci-visual{min-height:250px}}

#goldenReferenceCard{
 background:radial-gradient(circle at 50% -20%,#153f68,#07192d 70%)!important;
 border:1px solid #2d638d!important;padding:16px!important;
}
#goldenReferenceCard>div:first-child{border-bottom-color:#2d638d!important}
#goldenReferenceCard [style*="#334155"],
#goldenReferenceCard [style*="#64748b"]{color:#d7e9f6!important}
#goldenReferenceCard [style*="#0369a1"]{color:var(--nabil-ref-cyan-text)!important}
#goldenReferenceCard [style*="#eff6ff"]{
 background:#0b2943!important;border-color:#315f82!important;color:#dff5ff!important;
}
img[data-source-scan],.source-page-scan,.textbook-page-scan{display:none!important}
mjx-container{max-width:100%!important;overflow-x:auto;overflow-y:hidden}
table{max-width:100%}
@media(max-width:430px){
 body{padding:6px!important}
 .container{max-width:100%!important;margin:0!important}
 .header{position:relative!important;display:block!important;padding:10px!important}
 .header h1{font-size:20px!important;margin:0 0 9px!important}
 .header-actions,.header>div{width:100%!important}
 .header-actions{display:grid!important;grid-template-columns:1fr!important}
 .header button,.header select,.nav-btn{width:100%!important;justify-content:center!important}
 .card,.nabil-concept-card,.nabil-exercise-card,#goldenReferenceCard{padding:10px!important;border-radius:13px!important}
 .nabil-teacher-step{padding:9px!important;margin:7px 0!important}
 .nabil-reference-concept{padding:10px!important}
 .nabil-prebuilt-exercise-lab,.interactive-lab{margin-inline:0!important}
 .nabil-sci-grid{grid-template-columns:1fr!important}
 .nabil-sci-panel{min-width:0!important}
 .nabil-sci-table-wrap{max-width:100%!important;overflow-x:auto!important}
 button,input,select,textarea{font-size:16px!important}
}
"""



# ==============================================================================
# 5. PREFLIGHT & DRIVE SERVICE (PURE PLAIN-TEXT SCOPES)
# ==============================================================================
def execute_preflight_checks(require_drive: bool = False) -> Dict[str, Any]:
    progress("PREFLIGHT: Executing universal runtime verification...")
    report = {"status": "PASS", "dependencies": {}}

    required = [("pypdf", "pypdf"), ("PIL", "Pillow"), ("googleapiclient", "google-api-python-client"), ("google.auth", "google-auth"), ("playwright", "playwright")]
    for mod, pkg in required:
        try:
            __import__(mod)
            report["dependencies"][pkg] = True
        except ImportError:
            report["dependencies"][pkg] = False
            raise RuntimeError(f"DEPENDENCY_MISSING:{pkg}")

    try:
        import fitz
        report["dependencies"]["PyMuPDF"] = True
    except ImportError:
        report["dependencies"]["PyMuPDF"] = False
        raise RuntimeError("DEPENDENCY_MISSING:PyMuPDF")

    if require_drive:
        root_id = resolve_drive_root_id()
        try:
            service = get_drive_service()
            about = service.about().get(fields="user(emailAddress)").execute()
            report["drive_user"] = about.get("user", {}).get("emailAddress")
        except Exception as e:
            raise RuntimeError(f"DRIVE_AUTH_FAILED:{e}")

    for d in [PERM_EVIDENCE_DIR, CACHE_DIR, OUT_DIR, ARTIFACTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
        if not os.access(d, os.W_OK):
            raise RuntimeError(f"CANNOT_WRITE_DIR:{d}")

    progress("PREFLIGHT: Universal environment verified.")
    return report


def get_drive_service():
    """Use the owner's OAuth credentials for uploads to their personal My Drive.

    A service account can read shared source PDFs but cannot own uploaded files
    in personal Drive, even if shared as Editor. Keep tokens in Railway secrets;
    never commit them to the repository.
    """
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request

    scopes = ["https://www.googleapis.com/auth/drive"]

    # Prefer the complete owner OAuth JSON generated by authorize_drive_owner.py.
    # This is the canonical credential after an explicit re-authorization and
    # must take precedence over legacy split variables that may contain a
    # revoked refresh token.
    raw_oauth = os.getenv("NABIL_DRIVE_OAUTH_TOKEN_JSON", "").strip()
    if raw_oauth:
        try:
            info = json.loads(raw_oauth)
            creds = Credentials.from_authorized_user_info(info, scopes=scopes)
            if not creds.valid and creds.refresh_token:
                creds.refresh(Request())
            if not creds.valid:
                raise RuntimeError("NABIL_DRIVE_OAUTH_REFRESH_REQUIRED")
        except (ValueError, KeyError, TypeError) as exc:
            raise RuntimeError("NABIL_DRIVE_OAUTH_TOKEN_INVALID: check Railway secret JSON") from exc
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    # Legacy three-variable OAuth remains as a fallback only.
    owner_keys = (
        "GOOGLE_DRIVE_OAUTH_CLIENT_ID",
        "GOOGLE_DRIVE_OAUTH_CLIENT_SECRET",
        "GOOGLE_DRIVE_OAUTH_REFRESH_TOKEN",
    )
    owner_values = [os.getenv(name, "").strip() for name in owner_keys]
    if all(owner_values):
        credentials = Credentials(
            token=None,
            refresh_token=owner_values[2],
            token_uri="https://oauth2.googleapis.com/token",
            client_id=owner_values[0],
            client_secret=owner_values[1],
            scopes=scopes,
        )
        credentials.refresh(Request())
        return build("drive", "v3", credentials=credentials,
                     cache_discovery=False)

    if any(owner_values):
        missing = [name for name, value in zip(owner_keys, owner_values) if not value]
        raise RuntimeError("OWNER_DRIVE_OAUTH_INCOMPLETE: missing " + ",".join(missing))

    # Keep existing read-only source access for index-only operations.
    try:
        from scripts.index_books import get_drive_service as base_get_drive
        return base_get_drive()
    except Exception:
        pass

    paths = [
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "").strip(),
        str(ROOT / "drive_service_account.json"),
        str(ROOT / "credentials.json"),
    ]
    path = next((p for p in paths if p and Path(p).is_file()), None)
    if path:
        creds = service_account.Credentials.from_service_account_file(
            path, scopes=scopes)
    else:
        import google.auth
        creds, _ = google.auth.default(scopes=scopes)
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def resolve_drive_root_id() -> str:
    root_id = os.getenv("NABIL_CURRICULUM_ROOT_ID",
                        os.getenv("NABIL_INTERACTIVE_CURRICULUM_ROOT_ID",
                                  os.getenv("NABIL_LESSON_DRIVE_ROOT", ""))).strip()
    if not root_id:
        raise RuntimeError("NABIL_CURRICULUM_ROOT_ID_NOT_CONFIGURED: Set NABIL_CURRICULUM_ROOT_ID in environment.")
    return root_id


def resolve_source_book_pdf(book_id: str, drive_service=None) -> Path:
    cache_dir = Path("/tmp/nabil_source_books")
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / f"{book_id}.pdf"

    if target.exists() and target.stat().st_size > 20000:
        try:
            import fitz
            doc = fitz.open(str(target))
            if len(doc) >= 1:
                doc.close()
                return target
            doc.close()
        except Exception:
            target.unlink(missing_ok=True)

    candidates = [Path(f"/app/data/books/{book_id}.pdf"), Path(f"/app/books/{book_id}.pdf"), Path(f"data/books/{book_id}.pdf"), Path(f"{book_id}.pdf")]
    for c in candidates:
        if c.exists() and c.stat().st_size > 20000:
            try:
                import fitz
                doc = fitz.open(str(c))
                if len(doc) >= 1:
                    doc.close()
                    shutil.copy2(c, target)
                    return target
                doc.close()
            except Exception:
                pass

    if not drive_service:
        drive_service = get_drive_service()

    progress("DOWNLOADING_SOURCE_PDF", file_id=book_id)
    from googleapiclient.http import MediaIoBaseDownload
    with target.open("wb") as fh:
        loader = MediaIoBaseDownload(fh, drive_service.files().get_media(fileId=book_id))
        done = False
        while not done:
            _, done = loader.next_chunk()

    try:
        import fitz
        doc = fitz.open(str(target))
        if len(doc) < 1:
            doc.close()
            target.unlink(missing_ok=True)
            raise ValueError("Zero-page PDF")
        doc.close()
    except Exception as e:
        target.unlink(missing_ok=True)
        raise RuntimeError(f"SOURCE_PDF_NOT_FOUND: PDF is corrupted or unreadable ({e})")

    return target


# ==============================================================================
# 12. ATOMIC PROMOTION & POST-UPLOAD SHA-256 VERIFICATION
# ==============================================================================
def rollback_lesson_drive(drive_service, lesson_id: str, target_version: int):
    root_id = resolve_drive_root_id()
    ver_file = VERSIONS_DIR / f"{lesson_id}.json"
    if not ver_file.exists():
        raise RuntimeError("ROLLBACK_VERSION_NOT_FOUND")

    meta = json.loads(ver_file.read_text(encoding="utf-8"))
    old_a = ARTIFACTS_DIR / f"{lesson_id}_v{target_version}_A.html"
    old_b = ARTIFACTS_DIR / f"{lesson_id}_v{target_version}_B.html"
    old_labs = ARTIFACTS_DIR / f"{lesson_id}_v{target_version}_LABS.json"

    if not (old_a.exists() and old_b.exists()):
        raise RuntimeError(f"ROLLBACK_ARTIFACTS_MISSING: Version v{target_version} files not found")

    content_a = old_a.read_text(encoding="utf-8")
    content_b = old_b.read_text(encoding="utf-8")
    content_labs = (
        old_labs.read_text(encoding="utf-8")
        if old_labs.exists() else None
    )

    from googleapiclient.http import MediaIoBaseUpload
    if meta.get("drive_theory_id"):
        media_a = MediaIoBaseUpload(io.BytesIO(content_a.encode("utf-8")), mimetype="text/html", resumable=True)
        drive_service.files().update(fileId=meta["drive_theory_id"], media_body=media_a).execute()

    if meta.get("drive_exercises_id"):
        media_b = MediaIoBaseUpload(io.BytesIO(content_b.encode("utf-8")), mimetype="text/html", resumable=True)
        drive_service.files().update(fileId=meta["drive_exercises_id"], media_body=media_b).execute()

    if meta.get("drive_labs_id") and content_labs is not None:
        media_labs = MediaIoBaseUpload(
            io.BytesIO(content_labs.encode("utf-8")),
            mimetype="application/json",
            resumable=True)
        drive_service.files().update(
            fileId=meta["drive_labs_id"], media_body=media_labs).execute()

    meta["published_version"] = target_version
    meta["status"] = "ROLLED_BACK"
    meta["history"].append({"action": "ROLLBACK", "target": target_version, "time": now()})
    ver_file.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    progress("ROLLBACK_DRIVE_EXECUTING_SUCCESS", lesson_id=lesson_id, target_version=target_version)



def _update_golden_registry(entry: dict, *, version: str, theory_id: str,
                            exercises_id: str | None = None, labs_id: str | None = None) -> None:
    """Atomically register a successfully verified Drive publication."""
    try:
        data = json.loads(GOLDEN_REGISTRY_PATH.read_text(encoding="utf-8")) if GOLDEN_REGISTRY_PATH.exists() else {}
    except Exception as exc:
        raise RuntimeError(f"GOLDEN_REGISTRY_INVALID:{exc}") from exc
    if not isinstance(data, dict):
        data = {}
    lessons = data.setdefault("lessons", {})
    lesson_id = str(entry.get("lesson_id") or "").strip().upper()
    if not lesson_id:
        raise RuntimeError("GOLDEN_REGISTRY_LESSON_ID_REQUIRED")
    language = resolve_lang_code(entry.get("language") or "en")
    lessons[lesson_id] = {
        "lesson_id": lesson_id,
        "title": str(entry.get("canonical_title") or lesson_id),
        "grade": str(entry.get("grade") or ""),
        "branch": str(entry.get("branch") or ""),
        "subject": str(entry.get("subject") or ""),
        "curriculum": str(entry.get("curriculum") or "Lebanese"),
        "language": language,
        "version": str(version),
        "drive_file_id": theory_id,
        "drive_theory_id": theory_id,
        "drive_exercises_id": exercises_id,
        "drive_labs_id": labs_id,
        "drive_url": f"https://drive.google.com/file/d/{theory_id}/view",
        "runtime_ai_required": False,
        "updated_at": now(),
    }
    data["schema"] = "nabil-golden-lessons/v1"
    data["updated_at"] = now()
    _atomic_write_text(GOLDEN_REGISTRY_PATH, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\\n")


def promote_candidate(candidate: dict, entry: dict, drive_service) -> Tuple[str, str, str]:
    """Atomic Promotion with Post-Upload SHA-256 Verification & Safe Revert Backup."""
    root_id = resolve_drive_root_id()
    from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload

    def get_or_create_folder(name: str, parent: str) -> str:
        q = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and '{parent}' in parents and trashed = false"
        res = drive_service.files().list(q=q, fields="files(id)").execute().get("files", [])
        if len(res) > 1:
            raise RuntimeError(f"DRIVE_FOLDER_DUPLICATE_FAILED: Multiple folders named '{name}' under {parent}")
        if res:
            return res[0]["id"]
        meta = {"name": name, "mimeType": "application/vnd.google-apps.folder", "parents": [parent]}
        return drive_service.files().create(body=meta, fields="id").execute()["id"]

    grade_fid = get_or_create_folder(f"Grade {entry['grade']}", root_id)
    subject_folder_names = {
        "physics": "Physics - فيزياء",
        "mathematics": "Mathematics - رياضيات",
        "chemistry": "Chemistry - كيمياء",
        "biology": "Biology - علوم الحياة",
        "general_science": "General Science - علوم عامة",
    }
    subject_fid = get_or_create_folder(subject_folder_names.get(entry['subject'], entry['subject']), grade_fid)

    def get_existing_file(fname: str) -> Optional[dict]:
        q = f"name = '{fname}' and '{subject_fid}' in parents and trashed = false"
        files = drive_service.files().list(q=q, fields="files(id, name)").execute().get("files", [])
        return files[0] if files else None

    existing_a = get_existing_file(candidate["filename_a"])
    existing_b = get_existing_file(candidate["filename_b"])
    existing_labs = get_existing_file(candidate["filename_labs"])
    backup_data_a = None
    backup_data_b = None
    backup_data_labs = None
    if existing_a:
        backup_data_a = drive_service.files().get_media(fileId=existing_a["id"]).execute()
    if existing_b:
        backup_data_b = drive_service.files().get_media(fileId=existing_b["id"]).execute()
    if existing_labs:
        backup_data_labs = drive_service.files().get_media(
            fileId=existing_labs["id"]).execute()

    def upload_or_update(fname: str, content: str, existing: Optional[dict],
                         mimetype: str = "text/html", artifact: str = "theory") -> str:
        media = MediaIoBaseUpload(io.BytesIO(content.encode("utf-8")), mimetype=mimetype, resumable=True)
        props = {
            "nabil_lesson_id": str(entry.get("lesson_id") or "").strip().upper(),
            "nabil_language": resolve_lang_code(entry.get("language") or "en"),
            "nabil_version": str(candidate.get("version") or candidate.get("candidate_version") or "0.01"),
            "nabil_artifact": artifact,
            "nabil_golden": "true",
        }
        body={"name": fname, "appProperties": props}
        if existing:
            drive_service.files().update(fileId=existing["id"], body=body, media_body=media).execute()
            return existing["id"]
        body["parents"]=[subject_fid]
        return drive_service.files().create(body=body, media_body=media, fields="id").execute()["id"]

    tid = None
    eid = None
    lid = None
    try:
        tid = upload_or_update(
            candidate["filename_a"], candidate["page_a_html"], existing_a)
        eid = upload_or_update(
            candidate["filename_b"], candidate["page_b_html"], existing_b, artifact="exercises")
        lid = upload_or_update(
            candidate["filename_labs"], candidate["lab_index_json"],
            existing_labs, mimetype="application/json", artifact="labs")

        def verify_remote_sha256(file_id: str, local_content: str):
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, drive_service.files().get_media(fileId=file_id))
            done = False
            while not done:
                _, done = downloader.next_chunk()
            remote_sha = hashlib.sha256(fh.getvalue()).hexdigest()
            local_sha = hashlib.sha256(local_content.encode("utf-8")).hexdigest()
            if remote_sha != local_sha:
                raise RuntimeError(f"POST_UPLOAD_VERIFICATION_FAILED: SHA256 mismatch for file id {file_id}")

        verify_remote_sha256(tid, candidate["page_a_html"])
        verify_remote_sha256(eid, candidate["page_b_html"])
        verify_remote_sha256(lid, candidate["lab_index_json"])

    except Exception as e:
        if tid and existing_a and backup_data_a:
            revert_media_a = MediaIoBaseUpload(io.BytesIO(backup_data_a), mimetype="text/html", resumable=True)
            drive_service.files().update(fileId=tid, media_body=revert_media_a).execute()
        elif tid and not existing_a:
            drive_service.files().delete(fileId=tid).execute()

        if eid and existing_b and backup_data_b:
            revert_media_b = MediaIoBaseUpload(io.BytesIO(backup_data_b), mimetype="text/html", resumable=True)
            drive_service.files().update(fileId=eid, media_body=revert_media_b).execute()
        elif eid and not existing_b:
            drive_service.files().delete(fileId=eid).execute()

        if lid and existing_labs and backup_data_labs:
            revert_media_labs = MediaIoBaseUpload(
                io.BytesIO(backup_data_labs),
                mimetype="application/json",
                resumable=True)
            drive_service.files().update(
                fileId=lid, media_body=revert_media_labs).execute()
        elif lid and not existing_labs:
            drive_service.files().delete(fileId=lid).execute()

        raise RuntimeError(f"ATOMIC_PROMOTION_FAILED: Transaction rolled back safely ({e})")

    return tid, eid, lid
