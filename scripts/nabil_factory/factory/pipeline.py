from __future__ import annotations

# ==============================================================================
# PRODUCTION PIPELINE ENTRY (LAZY DRIVE RESOLUTION)
# ==============================================================================
def _produce_lesson_for_entry_impl(entry: dict, drive_service=None, publish: bool = False) -> dict:
    # Protected engineering safety layer; independent of the V18 display engine.
    from scripts.nabil_factory.factory.locked_v18_safety import (
        assert_safe_factory_boundaries, assert_source_identity,
    )
    assert_safe_factory_boundaries()
    lesson_id = entry["lesson_id"]
    book_id = entry["book_id"]
    assert_source_identity(entry, book_id)
    progress("PRODUCTION_PIPELINE_START", lesson_id=lesson_id)
    assert_renderer_family_contract()

    ver_file = VERSIONS_DIR / f"{lesson_id}.json"
    if ver_file.exists():
        ver_meta = json.loads(ver_file.read_text(encoding="utf-8"))
        candidate_v = ver_meta.get("published_version", 0) + 1
    else:
        ver_meta = {"lesson_id": lesson_id, "published_version": 0, "history": []}
        candidate_v = 1

    profile = resolve_pedagogy_profile(entry)
    
    if drive_service is None and (publish or not Path(f"/app/data/books/{book_id}.pdf").exists()):
        drive_service = get_drive_service()
    elif drive_service is None:
        # Best-effort recovery channel. A local-book dry run remains valid if
        # Drive auth is unavailable; publication still requires Drive normally.
        try:
            drive_service = get_drive_service()
            progress("RECOVERY_CHECKPOINT_DRIVE_READY", lesson_id=lesson_id)
        except Exception as exc:
            progress(
                "RECOVERY_CHECKPOINT_DRIVE_UNAVAILABLE_CONTINUING_LOCAL",
                lesson_id=lesson_id, reason=str(exc)[:240])
            drive_service = None

    pdf_path = resolve_source_book_pdf(book_id, drive_service)
    import fitz
    doc = fitz.open(str(pdf_path))
    try:
        # Checkpointing is recovery infrastructure, not publication.
        # If Drive is already available, persist verified page evidence even in
        # dry-run mode so a transient provider/process failure can resume work.
        ev_map = build_evidence_map(
            doc, entry,
            drive_service=drive_service,
            persist_pages=(drive_service is not None))
    finally:
        doc.close()

    theory = synthesize_universal_pedagogy(
        entry, ev_map, profile, drive_service=drive_service)

    # 1) Attempt EVERY verified textbook exercise first.
    textbook_exercises = [dict(ex) for ex in ev_map["exercise_evidence"]]
    prepare_verified_solutions(
        entry, textbook_exercises, profile, ev_map,
        drive_service=drive_service, persist=(drive_service is not None))
    verified_textbook = retain_only_verified_solved_exercises(
        textbook_exercises, origin="TEXTBOOK")
    progress(
        "TEXTBOOK_EXERCISE_SOLVE_SUMMARY",
        extracted=len(textbook_exercises),
        verified_solved=len(verified_textbook),
        dropped=len(textbook_exercises) - len(verified_textbook))

    # 2) If only 0, 1, or 2 textbook exercises survived, ask AI for >=3
    #    ADDITIONAL exercises. Every candidate must pass the strict lesson-scope
    #    scientific gate; invented/out-of-scope exercises are discarded alone.
    generated_practice = generate_ai_practice_for_insufficient_book_exercises(
        entry, ev_map, profile,
        verified_textbook_count=len(verified_textbook))
    if generated_practice:
        prepare_verified_solutions(
            entry, generated_practice, profile, ev_map,
            drive_service=drive_service, persist=(drive_service is not None))
    verified_ai = retain_only_verified_solved_exercises(
        generated_practice, origin="AI_ADDITIONAL_PRACTICE")

    # The lesson survives exercise-level rejection. Only scientifically verified
    # solved exercises become student-facing.
    exercises = verified_textbook + verified_ai

    # 3) Build exercise labs individually. A bad exercise/lab is dropped, not
    #    the whole lesson.
    prepare_prebuilt_exercise_labs(entry, exercises, profile, ev_map)
    exercises = [
        ex for ex in exercises
        if not ex.get("_exercise_render_rejected")
        and ex.get("_prebuilt_lab_key")
        and ex.get("_pre_solved_solution")
        and ex.get("solution_status") == "SOLVED"
    ]
    progress(
        "FINAL_STUDENT_EXERCISE_SET",
        textbook=sum(1 for ex in exercises
                     if ex.get("source_origin", "TEXTBOOK") == "TEXTBOOK"),
        ai=sum(1 for ex in exercises
               if ex.get("source_origin") == "AI_ADDITIONAL_PRACTICE"),
        total=len(exercises))

    # Factory-default pedagogical self-healing: if source-scope auditing removed
    # a generated quiz/apply item, bind that concept to a verified textbook
    # exercise BEFORE rendering/translation so all languages and caches contain
    # the repaired Apply step.
    theory = ensure_verified_apply_steps(
        theory, exercises, ev_map,
        resolve_lang_code(entry.get("language", "en")))

    lab_index = build_prebuilt_lab_index(entry, theory, exercises)
    page_a_raw = render_lesson_page_a(
        entry, theory, ev_map, lab_index=lab_index)
    page_b_raw = render_lesson_page_b(
        entry, exercises, profile, ev_map, lab_index=lab_index)

    # Source/book raster pixels are NEVER student-facing. They may be used only
    # internally as hidden scientific evidence for OCR/vision/audit/redraw.
    page_a_raw = strip_source_rasters_from_student_html(
        page_a_raw, ev_map, "LESSON")
    page_b_raw = strip_source_rasters_from_student_html(
        page_b_raw, ev_map, "EXERCISES")

    source_lang_code = resolve_lang_code(entry.get("language", "en"))

    def _translate_page_cached(raw_html: str, unit_id: str, purpose: str):
        # Paid translation is keyed by translatable content, not by the
        # JavaScript escaping form of the MathJax delimiter config. Canonicalize
        # this renderer-only difference so the corrected renderer can reuse the
        # already-paid translation checkpoint with zero provider calls.
        hash_html = raw_html.replace(
            "tex: { inlineMath: [['\\\\(', '\\\\)']], "
            "displayMath: [['\\\\[', '\\\\]']], processEscapes: true },",
            "tex: { inlineMath: [['\\(', '\\)']], "
            "displayMath: [['\\[', '\\]']], processEscapes: true },",
        )
        source_hash = hashlib.sha256(
            hash_html.encode("utf-8")).hexdigest()
        # Paid translation cache must depend on translation semantics,
        # not on unrelated renderer/QA code. This key matches the already
        # verified V7 translation policy; bump it ONLY when translation logic,
        # locking, numeric preservation, or Arabic normalization changes.
        prompt_version = (
            "TRILINGUAL_PAGE_TRANSLATION_V7_SELFHEAL_6037750d2063fb4f"
        )
        checkpoint_root = str(
            os.getenv("NABIL_CURRICULUM_ROOT_ID") or "").strip() or None
        checkpoint_api = None
        if drive_service is not None and checkpoint_root:
            from scripts import nabil_page_checkpoint as checkpoint_api
            saved = checkpoint_api.load_paid_unit(
                drive_service, checkpoint_root, entry,
                operation="page_translation",
                unit_id=unit_id,
                source_hash=source_hash,
                prompt_version=prompt_version,
            )
            if (
                isinstance(saved, dict)
                and isinstance(saved.get("html"), str)
                and isinstance(saved.get("report"), dict)
            ):
                cached_html, normalized_count = (
                    normalize_cached_trilingual_translation_html(saved["html"])
                )
                if normalized_count:
                    checkpoint_api.save_paid_unit(
                        drive_service, checkpoint_root, entry,
                        operation="page_translation",
                        unit_id=unit_id,
                        source_hash=source_hash,
                        prompt_version=prompt_version,
                        payload={
                            "html": cached_html,
                            "report": saved["report"],
                        },
                        provenance={
                            "policy": "LOCAL_FORMAL_ARABIC_NORMALIZATION",
                        },
                    )
                    progress(
                        "PAGE_TRANSLATION_CACHED_ARABIC_NORMALIZED",
                        lesson_id=lesson_id,
                        unit_id=unit_id,
                        normalized_count=normalized_count,
                    )
                progress(
                    "PAGE_TRANSLATION_RESTORED_FROM_DRIVE",
                    lesson_id=lesson_id,
                    unit_id=unit_id,
                )
                return cached_html, saved["report"]

        translated_html, report = build_trilingual_page_translation(
            raw_html, source_lang_code, purpose=purpose)

        if checkpoint_api is not None:
            checkpoint_api.save_paid_unit(
                drive_service, checkpoint_root, entry,
                operation="page_translation",
                unit_id=unit_id,
                source_hash=source_hash,
                prompt_version=prompt_version,
                payload={"html": translated_html, "report": report},
                provenance=dict(get_last_llm_provenance()),
            )
            progress(
                "PAGE_TRANSLATION_SAVED_TO_DRIVE",
                lesson_id=lesson_id,
                unit_id=unit_id,
            )
        return translated_html, report

    page_a, translation_a = _translate_page_cached(
        page_a_raw, "theory",
        purpose=f"lesson_page_translation_{lesson_id}")
    page_b, translation_b = _translate_page_cached(
        page_b_raw, "exercises",
        purpose=f"exercise_page_translation_{lesson_id}")

    # Legacy bridge toward the typed text/math contract. Run AFTER translation
    # cache restore so this costs zero provider calls and also heals cached
    # language dictionaries. Genuine math remains delimited; prose accidentally
    # wrapped as math is deterministically demoted before Playwright/MathJax.
    page_a, mixed_a = normalize_legacy_mixed_math_html(
        page_a, context=f"{lesson_id}:theory")
    page_b, mixed_b = normalize_legacy_mixed_math_html(
        page_b, context=f"{lesson_id}:exercises")
    if mixed_a or mixed_b:
        progress(
            "MIXED_MATH_CONTRACT_APPLIED",
            lesson_id=lesson_id,
            theory_demoted=mixed_a,
            exercises_demoted=mixed_b,
        )

    slug_subj = re.sub(r'[^\w]+', '-', entry.get("subject", "PHYSICS")).upper()
    slug_title = re.sub(r'[^\w]+', '-', entry["canonical_title"]).upper()
    seq_match = re.search(r'-(\d{3})$', lesson_id)
    seq_str = seq_match.group(1) if seq_match else "001"
    grade_str = f"G{int(entry.get('grade', 7)):02d}"

    # Two source PDFs may share grade/subject/title. Never overwrite a French
    # edition or revised textbook because its chapter number happens to match.
    source_key = re.sub(r"[^A-Za-z0-9]", "", entry.get("source_key", "")).upper()
    stem = f"{grade_str}-{slug_subj}--{source_key}--{seq_str}--{slug_title}" if source_key else f"{grade_str}-{slug_subj}--{seq_str}--{slug_title}"
    filename_a = stem + ".html"
    filename_b = stem + "--EXERCISES.html"
    filename_labs = stem + "--LABS.json"
    lab_index_json = json.dumps(
        lab_index, ensure_ascii=False, indent=2, sort_keys=True)

    candidate = {
        "lesson_id": lesson_id,
        "candidate_version": candidate_v,
        "filename_a": filename_a,
        "filename_b": filename_b,
        "filename_labs": filename_labs,
        "page_a_html": page_a,
        "page_b_html": page_b,
        "lab_index_json": lab_index_json,
        "evidence_map": ev_map,
        "theory": theory,
        "exercises": exercises,
        "lab_index": lab_index,
        "translation_report": {
            "page_a": translation_a,
            "page_b": translation_b,
        },
        "hashes": {
            "page_a": hashlib.sha256(page_a.encode("utf-8")).hexdigest(),
            "page_b": hashlib.sha256(page_b.encode("utf-8")).hexdigest(),
            "labs": hashlib.sha256(lab_index_json.encode("utf-8")).hexdigest(),
            "evidence": hashlib.sha256(json.dumps(ev_map).encode("utf-8")).hexdigest()
        }
    }

    gates_res = run_all_quality_gates(candidate)

    # QA middleware may deterministically repair presentation/layout. Freeze the
    # exact reviewed HTML for local artifacts and Drive publish.
    page_a = candidate["page_a_html"]
    page_b = candidate["page_b_html"]

    review_res = independent_scientific_review(entry, candidate)

    title_review = dict(ev_map.get("title_verification") or {})
    candidate["review_status"] = str(
        review_res.get("review_status") or "UNREVIEWED")
    candidate["needs_review"] = bool(
        title_review.get("needs_review")
        or review_res.get("needs_review")
        or candidate["review_status"] != "REVIEWED"
    )
    candidate["review_reasons"] = {
        "title": title_review,
        "scientific_review": review_res,
    }

    # QA and independent scientific review have passed or were explicitly
    # classified as non-blocking review debt. Only now freeze the
    # already-rendered labs as static reusable artifacts for every student.
    published_labs = persist_quality_gated_labs(entry, theory, exercises)

    path_a = OUT_DIR / filename_a
    path_b = OUT_DIR / filename_b
    path_labs = OUT_DIR / filename_labs

    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_A.html").write_text(page_a, encoding="utf-8")
    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_B.html").write_text(page_b, encoding="utf-8")
    (ARTIFACTS_DIR / f"{lesson_id}_v{candidate_v}_LABS.json").write_text(
        lab_index_json, encoding="utf-8")

    path_a.write_text(page_a, encoding="utf-8")
    path_b.write_text(page_b, encoding="utf-8")
    path_labs.write_text(lab_index_json, encoding="utf-8")
    progress(
        "LOCAL_ARTIFACTS_COMPILED",
        file_a=filename_a,
        file_b=filename_b,
        file_labs=filename_labs)

    drive_theory_id = None
    drive_exercises_id = None
    drive_labs_id = None
    status_str = "QA_PASSED_LOCAL"
    if publish:
        if drive_service is None:
            drive_service = get_drive_service()
        drive_theory_id, drive_exercises_id, drive_labs_id = promote_candidate(
            candidate, entry, drive_service)
        ver_meta["published_version"] = candidate_v
        ver_meta["drive_theory_id"] = drive_theory_id
        ver_meta["drive_exercises_id"] = drive_exercises_id
        ver_meta["drive_labs_id"] = drive_labs_id
        ver_meta["history"].append({"action": "PUBLISH", "version": candidate_v, "time": now()})
        if candidate.get("needs_review"):
            status_str = "PUBLISHED_UNVERIFIED"
            progress(
                "ATOMIC_PUBLISHED_UNVERIFIED_TO_DRIVE",
                theory_id=drive_theory_id,
                exercises_id=drive_exercises_id,
                labs_id=drive_labs_id,
                review_status=candidate.get("review_status"),
                review_reasons=candidate.get("review_reasons"),
            )
        else:
            _update_golden_registry(
                entry, version=str(candidate_v), theory_id=drive_theory_id,
                exercises_id=drive_exercises_id, labs_id=drive_labs_id,
            )
            status_str = "PUBLISHED_VERIFIED"
            progress(
                "ATOMIC_PUBLISHED_AND_VERIFIED_TO_DRIVE",
                theory_id=drive_theory_id,
                exercises_id=drive_exercises_id,
                labs_id=drive_labs_id)
        ver_file.write_text(json.dumps(ver_meta, indent=2), encoding="utf-8")

    rep = {
        "status": status_str,
        "lesson_id": lesson_id,
        "candidate_version": candidate_v,
        "canonical_title": entry["canonical_title"],
        "source_book_id": entry["book_id"],
        "source_pages": f"{entry['pdf_start_page']}..{entry['pdf_end_page']}",
        "evidence_hash": candidate["hashes"]["evidence"][:16],
        "activities_count": len(theory["activities"]),
        "exercises_count": len(exercises),
        "prebuilt_concept_labs": len(lab_index.get("concept_labs") or []),
        "prebuilt_exercise_labs": len(lab_index.get("exercise_labs") or []),
        "runtime_ai_required_for_indexed_labs": False,
        "published_static_labs": len(published_labs.get("artifacts") or []),
        "published_labs_index": published_labs.get("index"),
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "mobile_reference_viewport": {"width": 390, "height": 844},
        "source_raster_student_facing": False,
        "source_completeness_status": (
            (ev_map.get("source_completeness") or {}).get("status")
        ),
        "pending_source_count": int(
            (ev_map.get("source_backlog") or {}).get("pending_count") or 0
        ),
        "pending_source_items": list(
            (ev_map.get("source_backlog") or {}).get("pending") or []
        ),
        "pending_source_retry_after_epoch": (
            (ev_map.get("source_backlog") or {}).get("next_retry_epoch")
        ),
        "voice_engine": "SpeechSynthesis",
        "voice_paid_endpoint": False,
        "male_voice_preferred": True,
        "male_voice_guaranteed": False,
        "autonomous_teaching_engine": True,
        "whole_lesson_smart_lab": bool(theory.get("whole_lesson_lab_active")),
        "translation_report": candidate.get("translation_report"),
        "drive_theory_id": drive_theory_id,
        "drive_exercises_id": drive_exercises_id,
        "drive_labs_id": drive_labs_id,
        "gates_report": gates_res["gates"],
        "scientific_review": review_res,
        "review_status": candidate.get("review_status"),
        "needs_review": bool(candidate.get("needs_review")),
        "review_reasons": candidate.get("review_reasons"),
        "local_files": [str(path_a), str(path_b), str(path_labs)]
    }
    return rep


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

def produce_lesson_for_entry(entry: dict, drive_service=None, publish: bool = False) -> dict:
    """Single recovery boundary for every provider-dependent production stage."""
    try:
        return _produce_lesson_for_entry_impl(
            entry, drive_service=drive_service, publish=publish)
    except (ProviderDailyQuotaError, ProviderTransientError) as exc:
        retry = max(1, int(getattr(exc, "retry_after_seconds", None) or 60))
        operation = str(getattr(exc, "operation", None) or "provider_operation")
        unit_id = str(getattr(exc, "unit_id", None) or operation)
        checkpoint_drive = drive_service
        if checkpoint_drive is None:
            try:
                checkpoint_drive = get_drive_service()
            except Exception:
                checkpoint_drive = None
        state = _persist_factory_recovery_state(
            entry, checkpoint_drive,
            status=STATUS_PAUSED_TRANSIENT,
            reason=str(getattr(exc, "reason", None) or exc),
            unit_id=unit_id,
            operation=operation,
            retry_seconds=retry,
        )
        if state.get("status") == STATUS_NEEDS_ATTENTION:
            capped = NeedsAttentionError(
                state.get("reason") or "PAUSE_RESUME_CYCLE_CAP_EXCEEDED",
                operation=operation,
                unit_id=unit_id,
                reason=state.get("reason"),
            )
            capped.state = state
            raise capped from exc
        exc.state = state
        raise
    except ProviderUnavailableError as exc:
        operation = str(getattr(exc, "operation", None) or "provider_operation")
        unit_id = str(getattr(exc, "unit_id", None) or operation)
        checkpoint_drive = drive_service
        if checkpoint_drive is None:
            try:
                checkpoint_drive = get_drive_service()
            except Exception:
                checkpoint_drive = None
        state = _persist_factory_recovery_state(
            entry, checkpoint_drive,
            status=STATUS_PROVIDER_UNAVAILABLE,
            reason=str(getattr(exc, "reason", None) or exc),
            unit_id=unit_id,
            operation=operation,
        )
        if state.get("status") == STATUS_NEEDS_ATTENTION:
            capped = NeedsAttentionError(
                state.get("reason") or "PAUSE_RESUME_CYCLE_CAP_EXCEEDED",
                operation=operation,
                unit_id=unit_id,
                reason=state.get("reason"),
            )
            capped.state = state
            raise capped from exc
        exc.state = state
        raise
    except NeedsAttentionError as exc:
        operation = str(getattr(exc, "operation", None) or "provider_operation")
        unit_id = str(getattr(exc, "unit_id", None) or operation)
        checkpoint_drive = drive_service
        if checkpoint_drive is None:
            try:
                checkpoint_drive = get_drive_service()
            except Exception:
                checkpoint_drive = None
        state = _persist_factory_recovery_state(
            entry, checkpoint_drive,
            status=STATUS_NEEDS_ATTENTION,
            reason=str(getattr(exc, "reason", None) or exc),
            unit_id=unit_id,
            operation=operation,
        )
        exc.state = state
        raise

def main():
    global PROGRESS_STARTED
    PROGRESS_STARTED = time.monotonic()

    modular_root = ROOT / "scripts" / "nabil_factory"
    modular_files = sorted(modular_root.rglob("*.py"))
    source_code = "\n".join(
        p.read_text(encoding="utf-8") for p in modular_files)
    assert_no_lesson_specific_hardcode(source_code)
    assert_no_markdown_urls_in_runtime_code(source_code)
    for source_file in modular_files:
        py_compile.compile(str(source_file), doraise=True)

    parser = argparse.ArgumentParser(description="NABIL AI Universal Production Factory")
    parser.add_argument("--lesson-id", type=str, default=None, help="Exact canonical/discovered lesson ID")
    parser.add_argument("--grade", type=str, default=None, help="Grade selector, e.g. 7, G07, EB7, 9")
    parser.add_argument("--subject", type=str, default=None, help="Subject selector, e.g. physics, mathematics, فيزياء, رياضيات")
    parser.add_argument("--lesson", type=str, default=None, help="Lesson title/name inside the selected grade/subject")
    parser.add_argument("--index-book", type=str, default=None, help="Google Drive book file ID: index its TOC, lessons and works")
    parser.add_argument("--index-all-books", action="store_true", help="Discover and index every curriculum PDF under the configured Google Drive root")
    parser.add_argument("--force-book-index", action="store_true", help="Rebuild book indexes even when a valid cached index exists")
    parser.add_argument("--check-ai", action="store_true", help="Probe vision with generated blank image; no textbook page or Drive access")
    parser.add_argument("--publish", action="store_true", help="Publish produced lesson directly to Google Drive")
    parser.add_argument("--rollback", type=int, default=None, help="Target version to rollback; requires --lesson-id")
    args = parser.parse_args()

    if args.rollback is not None:
        if not args.lesson_id:
            raise RuntimeError("ROLLBACK_REQUIRES_LESSON_ID")
        drive_service = get_drive_service()
        rollback_lesson_drive(drive_service, args.lesson_id, args.rollback)
        return 0

    if args.check_ai:
        execute_preflight_checks(require_drive=False)
        from PIL import Image
        sample = io.BytesIO()
        Image.new("RGB", (64, 64), "white").save(sample, format="PNG")
        progress("AI_VISION_PROBE_START", image="generated_blank_64x64")
        response = execute_llm_completion(
            'Return only valid JSON: {"ok":true}', json_mode=True,
            image_base64=base64.b64encode(sample.getvalue()).decode("ascii"),
            operation="ai_vision_probe",
            unit_id="ai_vision_probe")
        json.loads(response)
        progress("AI_VISION_PROBE_PASS")
        return 0

    # No target means the universal action: discover and index the whole Drive curriculum.
    if not any((args.lesson_id, args.grade, args.subject, args.lesson, args.index_book, args.index_all_books)):
        args.index_all_books = True

    if args.index_all_books:
        drive_service = get_drive_service()
        report = build_all_registered_book_indexes(
            drive_service=drive_service,
            force=args.force_book_index,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["failed_count"] == 0 else 2

    if args.index_book:
        drive_service = get_drive_service()
        book_index = build_book_lesson_index(
            args.index_book,
            drive_service=drive_service,
            force=args.force_book_index,
        )
        print(json.dumps(book_index, ensure_ascii=False, indent=2))
        return 0

    # Grade and/or subject without a lesson means: index that complete scope.
    if (args.grade or args.subject) and not (args.lesson or args.lesson_id):
        drive_service = get_drive_service()
        report = build_scoped_book_indexes(
            drive_service=drive_service,
            force=args.force_book_index,
            grade=args.grade,
            subject=args.subject,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["failed_count"] == 0 else 2

    # A lesson title is dynamic: first ensure its grade/subject books are indexed,
    # then resolve the real discovered lesson and feed the unchanged production pipeline.
    if args.lesson:
        if not args.grade or not args.subject:
            raise RuntimeError("LESSON_SELECTOR_REQUIRES_GRADE_AND_SUBJECT")
        drive_service = get_drive_service()
        scope_report = build_scoped_book_indexes(
            drive_service=drive_service,
            force=args.force_book_index,
            grade=args.grade,
            subject=args.subject,
        )
        if scope_report["failed_count"]:
            raise RuntimeError(
                f"LESSON_SCOPE_INDEX_INCOMPLETE: failed_books={scope_report['failed_count']}")
        entry = resolve_lesson_selector(
            args.lesson, grade=args.grade, subject=args.subject)
    elif args.lesson_id:
        entry = resolve_canonical_entry(args.lesson_id)
    else:
        raise RuntimeError("TARGET_REQUIRED: use --index-all-books, --index-book, --grade/--subject, --lesson, or --lesson-id")

    execute_preflight_checks(require_drive=args.publish)
    drive_service = get_drive_service() if args.publish else None
    report = produce_lesson_for_entry(
        entry, drive_service=drive_service, publish=args.publish)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def _cli_entry() -> int:
    try:
        return int(main() or 0)
    except ProviderDailyQuotaError as exc:
        state = getattr(exc, "state", None) or {
            "status": STATUS_PAUSED_TRANSIENT,
            "reason": str(exc),
            "retry_after_seconds": getattr(exc, "retry_after_seconds", None),
        }
        print(json.dumps(state, ensure_ascii=False), flush=True)
        return EXIT_PAUSED_TRANSIENT
    except ProviderTransientError as exc:
        state = getattr(exc, "state", None) or {
            "status": STATUS_PAUSED_TRANSIENT,
            "reason": str(exc),
            "retry_after_seconds": getattr(exc, "retry_after_seconds", None),
        }
        print(json.dumps(state, ensure_ascii=False), flush=True)
        return EXIT_PAUSED_TRANSIENT
    except ProviderUnavailableError as exc:
        state = getattr(exc, "state", None) or {
            "status": STATUS_PROVIDER_UNAVAILABLE,
            "reason": str(exc),
        }
        print(json.dumps(state, ensure_ascii=False), flush=True)
        return EXIT_PROVIDER_UNAVAILABLE
    except (NeedsAttentionError, CheckpointWriteError) as exc:
        state = getattr(exc, "state", None) or {
            "status": STATUS_NEEDS_ATTENTION,
            "reason": str(exc),
        }
        print(json.dumps(state, ensure_ascii=False), flush=True)
        return EXIT_NEEDS_ATTENTION
    except ScientificGateBlocked as exc:
        state = {
            "status": "BLOCKED",
            "reason": str(exc),
            "blocked": True,
        }
        print(json.dumps(state, ensure_ascii=False), flush=True)
        return 1
    except Exception as exc:
        state = {
            "status": STATUS_NEEDS_ATTENTION,
            "reason": f"UNEXPECTED_INTERNAL_ERROR:{type(exc).__name__}:{exc}",
        }
        print(json.dumps(state, ensure_ascii=False), flush=True)
        return EXIT_NEEDS_ATTENTION


