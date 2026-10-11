"""Render a verified Work handoff answer as unpublished V18 preview artifacts.

This bridge is deliberately fail-closed: structural verification has already
run, but neither these artifacts nor their browser QA constitute an independent
scientific review.  They are written only to NABIL_PENDING.
"""
from __future__ import annotations

import hashlib
import html
import io
import json
import tempfile
from pathlib import Path


def _lab_html() -> str:
    return """
<section id="powersLab" style="font:16px system-ui;padding:16px;background:#071b34;color:#eef8ff;border-radius:14px">
 <h3>Exponent Structure Lab</h3>
 <label>Base <input id="pBase" type="range" min="1" max="10" value="2"></label>
 <output id="pBaseOut">2</output><br>
 <label>Exponent <input id="pExp" type="range" min="0" max="8" value="3"></label>
 <output id="pExpOut">3</output>
 <p id="pExpanded" aria-live="polite"></p><p id="pValue"></p>
 <script>
 (()=>{const b=document.getElementById('pBase'),e=document.getElementById('pExp');
 const draw=()=>{const base=Number(b.value),exp=Number(e.value);
 pBaseOut.textContent=base;pExpOut.textContent=exp;
 pExpanded.textContent=exp===0?`${base}⁰ = 1`:`${base}^${exp} = `+Array(exp).fill(base).join(' × ');
 pValue.textContent='Value: '+Math.pow(base,exp);};b.oninput=e.oninput=draw;draw();})();
 </script>
</section>"""


def _concept_activities(answer: dict) -> list:
    acts=[]
    for index,item in enumerate(answer.get("teaching_steps") or []):
        text=str(item.get("text") or item.get("conclusion") or "").strip()
        prompts=[str(x).strip() for x in item.get("student_prompts") or [] if str(x).strip()]
        conclusion=str(item.get("conclusion") or "").strip()
        steps=[{"label":"Explain","sentence":text,"formula":"","kind":"step"}]
        steps.extend({"label":"Your turn","sentence":p,"formula":"","kind":"step"} for p in prompts)
        if conclusion:
            steps.append({"label":"Conclusion","sentence":conclusion,"formula":"","kind":"final"})
        acts.append({
            "concept_id":str(item.get("concept_id") or ""),
            "title":str(item.get("title") or item.get("concept_id") or "Concept"),
            "source_page":item.get("source_page"),
            "conclusion":conclusion or text,
            "teaching_steps":steps,
            "lab_html":_lab_html() if index==1 else "",
            "allow_no_lab":True,
        })
    return acts


def _exercise_records(job: dict, answer: dict) -> list:
    evidence={x["exercise_id"]:x for x in job["source_evidence"]["exercise_evidence"]}
    out=[]
    for index,sol in enumerate(answer.get("exercise_solutions") or [],1):
        eid=str(sol.get("exercise_id") or "")
        ev=evidence[eid]
        out.append({
            "exercise_id":eid,"number":ev.get("number") or index,
            "exact_source_prompt":ev["exact_source_prompt"],
            "source_page":ev.get("source_page"),"source_origin":"TEXTBOOK",
            "solution_status":"SOLVED",
            "_pre_solved_solution":{"steps":list(sol.get("steps") or []),
                                    "final_answer":str(sol.get("final_answer") or "")},
        })
    return out


def _page(title: str, body: str, artifact: str, input_sha256: str) -> str:
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>body{{margin:0;background:#061629;color:#fff;font-family:system-ui}}
.pending{{padding:10px 16px;background:#7c2d12;color:#fff;font-weight:800;text-align:center}}
.meta{{padding:8px 16px;color:#b8d8ef;font-size:12px;overflow-wrap:anywhere}}</style></head>
<body data-publication-status="BLOCKED" data-review-status="PENDING_INDEPENDENT_REVIEW"
 data-artifact="{html.escape(artifact)}"><div class="pending">UNPUBLISHED V18 PREVIEW — independent scientific review required</div>
<div class="meta">Input SHA-256: {html.escape(input_sha256)}</div>{body}</body></html>'''


def _qa_one(path: Path, expected: int) -> dict:
    try:
        from playwright.sync_api import sync_playwright
        results=[]
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for name,width,height in (("desktop",1440,1000),("mobile",390,844)):
                page=browser.new_page(viewport={"width":width,"height":height})
                page.goto(path.resolve().as_uri(),wait_until="domcontentloaded")
                page.wait_for_timeout(400)
                board=page.locator('[data-nabil-v18-board="NABIL_V18_SMART_BOARD_V1"]')
                count=int(board.get_attribute("data-concept-count") or 0) if board.count() else 0
                golden=page.locator('[data-nabil-v18-golden="true"]').count()
                blocked=page.locator('body').get_attribute('data-publication-status')=='BLOCKED'
                overflow=page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth + 2")
                results.append({"viewport":name,"concept_count":count,"expected":expected,
                                "golden_container":golden,"blocked":blocked,
                                "horizontal_overflow":bool(overflow),
                                "passed":count==expected and golden==1 and blocked and not overflow})
                page.close()
            browser.close()
        return {"passed":all(x["passed"] for x in results),"viewports":results}
    except Exception as exc:
        return {"passed":False,"reason":"PLAYWRIGHT_UNAVAILABLE_OR_FAILED","detail":str(exc)[:500]}


def _upload_verified(service, folder: str, name: str, content: str, mimetype: str) -> tuple[str,str]:
    from googleapiclient.http import MediaIoBaseUpload
    payload=content.encode("utf-8")
    safe=name.replace("'","\\'")
    q=f"name = '{safe}' and '{folder}' in parents and trashed = false"
    found=service.files().list(q=q,fields="files(id)").execute().get("files",[])
    media=MediaIoBaseUpload(io.BytesIO(payload),mimetype=mimetype,resumable=False)
    if found:
        fid=service.files().update(fileId=found[0]["id"],media_body=media,fields="id").execute()["id"]
    else:
        fid=service.files().create(body={"name":name,"parents":[folder]},media_body=media,fields="id").execute()["id"]
    raw=service.files().get_media(fileId=fid).execute()
    remote=raw if isinstance(raw,bytes) else str(raw).encode("utf-8")
    local_sha=hashlib.sha256(payload).hexdigest()
    if hashlib.sha256(remote).hexdigest()!=local_sha:
        raise RuntimeError("HANDOFF_PREVIEW_DRIVE_READBACK_MISMATCH:"+name)
    return fid,local_sha


def render_and_save_answer_preview(job: dict, answer: dict, service, pending_folder: str) -> dict:
    from scripts.nabil_factory.cards.v18_board import (
        build_golden_spec, render_v18_exercises_board, render_v18_smart_board)
    acts=_concept_activities(answer)
    if len(acts)!=len(job["source_evidence"]["concept_evidence"]):
        raise RuntimeError("HANDOFF_PREVIEW_CONCEPT_COVERAGE_MISMATCH")
    spec=build_golden_spec(job["canonical_title"],acts,"en",subject=job.get("subject") or "mathematics",
                           verification_note="source-bound; independent review pending")
    theory_board=render_v18_smart_board(job["canonical_title"],acts,"en",golden_spec=spec,
                                        contract="HANDOFF_PREVIEW_BLOCKED",mode="lesson")
    exercises=_exercise_records(job,answer)
    exercise_board=render_v18_exercises_board(job["canonical_title"]+" — Textbook Exercises",exercises,"en",
                                               subject=job.get("subject") or "mathematics",
                                               contract="HANDOFF_PREVIEW_BLOCKED")
    theory=_page(job["canonical_title"]+" — V18 Theory Preview",theory_board,"theory",job["input_sha256"])
    exercise=_page(job["canonical_title"]+" — V18 Exercise Preview",exercise_board,"exercises",job["input_sha256"])
    with tempfile.TemporaryDirectory(prefix="nabil-answer-preview-") as td:
        tp=Path(td)/"theory.html"; ep=Path(td)/"exercises.html"
        tp.write_text(theory,encoding="utf-8"); ep.write_text(exercise,encoding="utf-8")
        qa={"schema":"nabil.lesson.answer.preview.qa.v1","lesson_id":job["lesson_id"],
            "input_sha256":job["input_sha256"],"publication_status":"BLOCKED",
            "independent_scientific_review":"NOT_RUN",
            "theory":_qa_one(tp,len(acts)),"exercises":_qa_one(ep,len(exercises))}
    qa["passed"]=bool(qa["theory"].get("passed") and qa["exercises"].get("passed"))
    stem="HANDOFF-PREVIEW--"+job["lesson_id"]
    tid,tsha=_upload_verified(service,pending_folder,stem+"--THEORY.html",theory,"text/html")
    eid,esha=_upload_verified(service,pending_folder,stem+"--EXERCISES.html",exercise,"text/html")
    qa.update({"theory_drive_id":tid,"exercise_drive_id":eid,
               "theory_sha256":tsha,"exercise_sha256":esha})
    qid,qsha=_upload_verified(service,pending_folder,stem+"--QA.json",
                              json.dumps(qa,ensure_ascii=False,sort_keys=True,separators=(",",":")),
                              "application/json")
    # Owner-approved publication: only publish V18 boards after real desktop/mobile QA.
    # Keep the explicit unverified status; this is not an independent science review.
    import os
    completed_folder = os.getenv("NABIL_COMPLETED_FOLDER_ID", "").strip()
    if os.getenv("NABIL_PUBLISH_HANDOFF_V18", "0") == "1":
        # Explicit unverified release is permitted only after real viewport QA.
        # Preserve the independent-review status as NOT_RUN in the rendered artifact.
        if not qa["passed"]:
            raise RuntimeError("V18_HANDOFF_BOARD_QA_FAILED: no publication")
        if not completed_folder:
            raise RuntimeError("NABIL_COMPLETED_FOLDER_ID_REQUIRED")
        public_theory = theory.replace(
            'data-publication-status="BLOCKED" data-review-status="PENDING_INDEPENDENT_REVIEW"',
            'data-publication-status="PUBLISHED_UNVERIFIED" data-review-status="INDEPENDENT_REVIEW_NOT_RUN"'
        ).replace(
            'UNPUBLISHED V18 PREVIEW — independent scientific review required',
            'NABIL V18 — Source-grounded lesson; independent review NOT RUN'
        )
        public_exercises = exercise.replace(
            'data-publication-status="BLOCKED" data-review-status="PENDING_INDEPENDENT_REVIEW"',
            'data-publication-status="PUBLISHED_UNVERIFIED" data-review-status="INDEPENDENT_REVIEW_NOT_RUN"'
        ).replace(
            'UNPUBLISHED V18 PREVIEW — independent scientific review required',
            'NABIL V18 — Source-grounded exercises; independent review NOT RUN'
        )
        pub_theory_id, _ = _upload_verified(
            service, completed_folder, stem+"--V18-THEORY.html", public_theory, "text/html")
        pub_exercises_id, _ = _upload_verified(
            service, completed_folder, stem+"--V18-EXERCISES.html", public_exercises, "text/html")
        return {"theory_preview_drive_id":tid,"exercise_preview_drive_id":eid,
                "preview_qa_drive_id":qid,"preview_qa_sha256":qsha,"preview_qa":qa,
                "published":True,"scientific_review":"NOT_RUN",
                "status":"PUBLISHED_UNVERIFIED",
                "drive_theory_id":pub_theory_id,
                "drive_exercises_id":pub_exercises_id}
    return {"theory_preview_drive_id":tid,"exercise_preview_drive_id":eid,
            "preview_qa_drive_id":qid,"preview_qa_sha256":qsha,"preview_qa":qa,
            "published":False,"scientific_review":"NOT_RUN"}
