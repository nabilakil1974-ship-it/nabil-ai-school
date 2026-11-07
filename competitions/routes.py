from __future__ import annotations

import io
import json
import os
import re
from typing import Literal

from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from competitions.offline_generator import build_offline_assessment
from competitions import exam_archive

router = APIRouter(prefix="/competitions", tags=["competitions"])

GRADE_TOPICS = {
    "g7": ["Powers", "Prime Numbers", "Congruent Triangles", "Signed Numbers (+ and -)", "Signed Numbers (× and ÷)", "Angles and Lines", "Reduce Fractions", "Decimal Fractions", "Locating a Point", "Algebraic Expressions", "Perpendicular Bisectors", "Locus", "Proportion", "Statistics", "Equations"],
    "g8": ["Powers", "The Circle", "The Square", "Powers of 10", "The Rectangle", "Literal Fractions", "The Rhombus", "Square Roots", "The Parallelogram", "Remarkable Identities", "Midpoint Theorem", "Arcs and Angles", "Pythagoras' Theorem", "Equations", "Rational Fractions", "Right Triangle", "Inequalities", "Plotting in a System", "Statistics"],
    "g9": ["Real Numbers", "Algebraic Expressions", "Lines and Circles", "Proportion", "Lines and Coordinate System", "Thales' Theorem", "Analytic Geometry", "Trigonometry", "System of Equations", "Vectors", "Statistics", "Similar Triangles"],
    "g10": ["Statistical Vocabulary", "Statistical Indicators", "Sets", "Powers of Real Numbers", "Order", "Absolute Value", "Trigonometry", "Vectors", "Coordinate Systems", "Lines in Coordinate Planes", "Scalar Product", "Analytic Form of Scalar Product", "Linear Equations", "Linear Inequalities", "Functions", "Basic Functions", "Plane Geometry", "Graphical Solution"],
    "g11_lh": ["Quadratic Equations", "Quadratic Functions", "Limit Concept", "Operations on Limits", "Continuity", "Derivatives", "Applications of Derivatives", "Variation of Functions", "Permutations", "Events", "Notion of Probability", "Rules of Probability", "Arithmetic Sequences", "Geometric Sequences", "Antiderivatives", "Statistics"],
    "terminal_gs": ["Quadratic Equations", "Signs of Quadratic Functions", "Limits of Functions at Infinity", "Limits of a Function at a Point", "Derivatives", "Functions", "Permutations", "Probability I", "Probability II", "Orthogonality", "Vectors and Coordinate Systems", "Sequences", "Trigonometric Equations", "Trigonometric Formulas", "Circle", "Scalar Product", "Antiderivatives", "Complex Numbers", "Statistics"],
    "terminal_ls": ["Continuous Functions on an Interval", "Inverse Function", "Second and Higher-Order Derivatives", "Logarithm", "Exponential Function", "Combinations", "Conditional Probability", "Random Variable", "Integral", "Methods of Integration", "Applications of Integral Calculus", "Components of the Vector Product", "Planes and Lines", "Parallelism and Orthogonality", "Differential Equations"],
    "terminal_se": ["Distribution of Two Variables", "Rational Functions", "Derivatives", "Functions of Economics", "Logarithm", "Exponential Functions", "Combinations", "Conditional Probability and Total Probability", "Sequences", "Interest", "Compound Interest", "Annuity", "Random Variables"],
    "terminal_lh": ["Position Measures of Statistical Data", "Rational Functions", "Conditional Probability", "Dispersion", "Graphical Interpretation", "Equations and Inequalities"],
}

class GenerateRequest(BaseModel):
    grade: str
    lessons: list[str] = Field(min_length=1, max_length=30)
    language: Literal["en", "fr"]
    exam_type: str = "Training competition"
    duration_minutes: int = Field(default=90, ge=15, le=240)
    total_marks: int = Field(default=20, ge=5, le=100)
    difficulty: Literal["balanced", "easy", "challenging"] = "balanced"
    curriculum_evidence: str = Field(default="", max_length=12000)

class ExportRequest(BaseModel):
    title: str
    grade_label: str
    language: Literal["en", "fr"]
    duration_minutes: int
    total_marks: int
    questions: list[dict]
    solutions: list[dict]
    rubric: list[dict]
    curriculum_note: str = ""

def _validate_selection(req: GenerateRequest):
    allowed = GRADE_TOPICS.get(req.grade)
    if not allowed:
        raise HTTPException(422, "Unknown grade or branch.")
    if any(x not in allowed for x in req.lessons):
        raise HTTPException(422, "A selected lesson does not belong to this grade/branch.")
    if req.grade == "g9" and any("probab" in x.lower() for x in req.lessons):
        raise HTTPException(422, "Probability is not in the supplied Grade 9 lesson map.")

def _instructions(req: GenerateRequest) -> str:
    lang = "English" if req.language == "en" else "French"
    step = ("We write → We substitute → We calculate → We conclude" if req.language == "en"
            else "On écrit → On remplace → On calcule → On conclut")
    return f"""You are NABIL AI, an expert Lebanese school mathematics assessment author.
Write the entire assessment in {lang}, at exactly grade/branch {req.grade}.
Selected lessons only: {json.dumps(req.lessons, ensure_ascii=False)}.
Exam type: {req.exam_type}; duration {req.duration_minutes} minutes; total {req.total_marks} marks; difficulty {req.difficulty}.
CURRICULUM EVIDENCE supplied by teacher: {req.curriculum_evidence or "NONE"}.
CRITICAL: the supplied lesson map is a teacher-provided preliminary map, NOT official proof.
Do not claim CRDP/Ministry/official curriculum verification unless a specific source excerpt is supplied above.
If no source evidence is supplied, mark curriculum_status as "teacher_review_required"; still create a careful training draft based ONLY on selected lesson names and familiar prerequisite skills, avoid uncertain subtopics and explicitly state that teacher validation is required.
Never include content from a higher grade or a lesson not selected. Every question must be tagged with its selected lesson.
Never fabricate citations, source titles, URLs or page numbers. If evidence is supplied, quote its source label exactly.
Create a high-quality progressive exam with clear marks; total question marks must add exactly to {req.total_marks}.
Include real mathematical expressions, numerical data and precise geometry construction descriptions when needed; avoid decorative fake diagrams.
For calculation questions use the language-specific sequence: {step}, with steps appropriate to the problem.
Return ONLY valid JSON with this exact schema:
{{"title":"...","grade_label":"...","curriculum_status":"verified_from_supplied_evidence OR teacher_review_required","curriculum_note":"honest concise note","sources":[{{"label":"...","evidence":"...","lesson":"..."}}],"questions":[{{"number":1,"lesson":"...","title":"...","statement":"...","marks":4,"parts":[{{"label":"a","statement":"...","marks":2}}]}}],"solutions":[{{"number":1,"steps":["..."],"final_answer":"..."}}],"rubric":[{{"number":1,"criteria":[{{"criterion":"...","marks":1}}],"total":4}}]}}.
Make questions varied and progressively harder. Include enough working space indicators only as instructions, not huge blank strings. Solutions must correspond to every question and show all reasoning. Rubric must award partial credit and sum consistently. Do not include markdown fences."""
 
@router.get("/catalogue")
def catalogue():
    return {"grades": GRADE_TOPICS}

@router.get("/benchmark/terminal-gs")
def terminal_gs_benchmark(language: Literal["en", "fr"] = "en"):
    """Reproducible public QA fixture: same lessons, time and mark total for NABIL comparison."""
    req = GenerateRequest(
        grade="terminal_gs",
        lessons=["Derivatives", "Probability I", "Vectors and Coordinate Systems", "Statistics"],
        language=language,
        exam_type="Training competition",
        duration_minutes=90,
        total_marks=20,
        difficulty="balanced",
        curriculum_evidence=""
    )
    return generate(req)

def _archive_context(req: GenerateRequest):
    query = " ".join(req.lessons)
    grade_alias = {"terminal_gs": "Terminale GS", "terminal_ls": "Terminale LS",
                   "terminal_se": "Terminale SE", "terminal_lh": "Terminale LH",
                   "g9": "Brevet"}
    # Never feed a certificate exam from another grade into a non-certificate assessment.
    if req.grade not in grade_alias:
        return []
    grade = grade_alias[req.grade]
    hits = exam_archive.search_archive(query, grade=grade, limit=10)
    return hits


def _validate_generated(data: dict, req: GenerateRequest):
    questions = data.get("questions") or []
    solutions = data.get("solutions") or []
    rubrics = data.get("rubric") or []
    if len(questions) != len(req.lessons):
        raise ValueError("The AI did not create exactly one question for each selected lesson.")
    if len(solutions) != len(questions) or len(rubrics) != len(questions):
        raise ValueError("Question, solution and marking-scheme counts do not match.")
    if [q.get("lesson") for q in questions] != req.lessons:
        raise ValueError("The AI changed, omitted or added a selected lesson.")
    total = round(sum(float(q.get("marks", 0)) for q in questions), 2)
    if total != float(req.total_marks):
        raise ValueError(f"Question marks total {total}, expected {req.total_marks}.")
    solution_numbers = {str(x.get("number")) for x in solutions}
    rubric_numbers = {str(x.get("number")) for x in rubrics}
    question_numbers = {str(x.get("number")) for x in questions}
    if solution_numbers != question_numbers or rubric_numbers != question_numbers:
        raise ValueError("Every question must have exactly one matching solution and rubric.")
    for q in questions:
        number = str(q.get("number"))
        mark = round(float(q.get("marks", 0)), 2)
        parts = q.get("parts") or []
        if parts and round(sum(float(p.get("marks", 0)) for p in parts), 2) != mark:
            raise ValueError(f"Question {number}: part marks do not add to the question total.")
        rubric = next(x for x in rubrics if str(x.get("number")) == number)
        if round(sum(float(x.get("marks", 0)) for x in rubric.get("criteria", [])), 2) != round(float(rubric.get("total", -1)), 2):
            raise ValueError(f"Question {number}: marking criteria do not add to the rubric total.")
        if round(float(rubric.get("total", -1)), 2) != mark:
            raise ValueError(f"Question {number}: rubric total does not match question marks.")
        solution = next(x for x in solutions if str(x.get("number")) == number)
        if len(solution.get("steps") or []) < 2 or not solution.get("final_answer"):
            raise ValueError(f"Question {number}: the model solution is incomplete.")
        if not q.get("statement") or not q.get("title"):
            raise ValueError(f"Question {number}: statement or title is missing.")
        lesson_name = str(q.get("lesson", "")).strip().lower()
        statement_text = str(q.get("statement", "")).strip().lower()
        if "antiderivative" in lesson_name or "primitive" in lesson_name:
            if not any(term in statement_text for term in ("antiderivative", "primitive", "find a function f", "déterminer une primitive")):
                raise ValueError(f"Question {number}: the selected antiderivatives lesson is not actually assessed.")
            if "f′(x)" in statement_text and "antiderivative" not in statement_text and "primitive" not in statement_text:
                raise ValueError(f"Question {number}: derivative calculation was incorrectly substituted for antiderivatives.")


def _generate_with_ai(req: GenerateRequest, archive_hits: list[dict]):
    api_key = (os.getenv("NABIL_LLM_API_KEY") or os.getenv("GEMINI_API_KEY")
               or os.getenv("OPENAI_API_KEY") or "").strip()
    if not api_key:
        return None
    from openai import OpenAI
    base_url = os.getenv("NABIL_LLM_BASE_URL", "").strip()
    if not base_url and os.getenv("GEMINI_API_KEY") and not os.getenv("NABIL_LLM_API_KEY"):
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    model = os.getenv("NABIL_LLM_MODEL") or os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"
    client = OpenAI(api_key=api_key, base_url=base_url or None, timeout=90.0, max_retries=1)
    archive_excerpt = []
    for hit in archive_hits:
        archive_excerpt.append({
            "title": hit.get("title"), "year": hit.get("year"),
            "session": hit.get("session"), "branch": hit.get("grade"),
            "language": hit.get("language"), "source_url": hit.get("source_url"),
            "official_exam_excerpt": hit.get("excerpt", "")[:1200]
        })
    evidence = json.dumps(archive_excerpt, ensure_ascii=False)
    prompt = _instructions(req) + """
OFFICIAL EXAM KNOWLEDGE RETRIEVAL:
Use the following excerpts only to learn the official Lebanese examination style, question sequencing,
expected reasoning depth and marking approach. Do not copy any full question. Create original questions.
An archive item is evidence of past exam style, NOT proof that its topic is in the current curriculum.
If the archive has no relevant excerpt, say so honestly and use only the teacher-selected lesson names.
Retrieved official archive records:
""" + evidence + """
QUALITY REQUIREMENTS:
- Produce genuinely progressive, multi-part questions appropriate to this branch and certificate level.
- Each question must test the named selected lesson, not merely mention its name.
- Show full derivations and calculations in the model solution; do not repeat the final answer as filler.
- Marking criteria must describe observable mathematical steps and allocate partial credit.
- Use a real data table structure in the JSON when statistics data are required: add a table object with headers and rows.
- For coordinate geometry, provide exact plotted points, axes range and scale in a diagram object.
- Do not invent diagrams or claim a visual is to scale unless coordinates and scale are supplied.
- Return JSON only, with no markdown.
"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "You are a rigorous Lebanese official-exam assessment designer and independent mathematics checker. Return valid JSON only."},
                  {"role": "user", "content": prompt}],
        temperature=0.25,
        response_format={"type": "json_object"}
    )
    data = json.loads(response.choices[0].message.content or "{}")
    _validate_generated(data, req)
    source_records = [{"label": h.get("title", "CRDP official exam"), "url": h.get("source_url"),
                       "year": h.get("year"), "grade": h.get("grade"),
                       "evidence": h.get("excerpt", "")[:900]} for h in archive_hits]
    data["sources"] = source_records
    data["quality_gate"] = {
        "question_solution_rubric_alignment": True,
        "marks_total": float(req.total_marks),
        "selected_lessons_exact_match": True,
        "official_archive_records_retrieved": len(archive_hits),
        "generator": "retrieval-augmented-ai",
        "curriculum_verified": False
    }
    data["curriculum_status"] = "teacher_review_required"
    data["curriculum_note"] = ("Past official exam papers were retrieved to inform examination style. They do not certify the current curriculum; verify against the latest CRDP/Ministry scope before use."
                               if req.language == "en" else "Des sujets officiels antérieurs ont été consultés pour guider le style d'examen. Ils ne certifient pas le programme actuel ; vérifier le programme CRDP/Ministère en vigueur.")
    data["request"] = req.model_dump()
    return data


@router.get("/archive/status")
def official_archive_status():
    return exam_archive.get_status()


@router.get("/archive/documents")
def official_archive_catalogue(grade: str | None = None, year: int | None = None,
                               session_name: str | None = None,
                               limit: int = 30, offset: int = 0):
    """Browse the public mathematics archive and download original CRDP PDFs."""
    return exam_archive.list_archive(grade=grade, year=year,
                                     session_name=session_name, limit=limit, offset=offset)


@router.get("/archive/search")
def official_archive_search(q: str, grade: str | None = None, limit: int = 8):
    results = exam_archive.search_archive(q, grade=grade, limit=limit)
    public_results = []
    for item in results:
        item = dict(item)
        item.pop("local_pdf", None)
        item.pop("local_text", None)
        item["download_url"] = f"/api/competitions/archive/documents/{item['id']}"
        public_results.append(item)
    return {"query": q, "results": public_results}


@router.get("/archive/documents/{document_id}")
def official_archive_document(document_id: str):
    try:
        found = exam_archive.get_document(document_id)
    except Exception as exc:
        raise HTTPException(502, f"Could not retrieve the original CRDP PDF: {str(exc)[:180]}")
    if not found:
        raise HTTPException(404, "The requested PDF is not in the current in-memory catalogue. Run CRDP archive sync first.")
    content, metadata = found
    filename = re.sub(r"[^A-Za-z0-9._-]+", "_", metadata.get("title", "official-exam"))[:100] + ".pdf"
    return StreamingResponse(
        io.BytesIO(content),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.post("/archive/sync")
def official_archive_sync(background: bool = True, max_pages: int = 300,
                          x_archive_admin_token: str | None = Header(default=None, alias="X-Archive-Admin-Token")):
    expected = os.getenv("NABIL_ARCHIVE_ADMIN_TOKEN", "").strip()
    if not expected:
        raise HTTPException(503, "Set NABIL_ARCHIVE_ADMIN_TOKEN before starting an archive sync.")
    if not x_archive_admin_token or not __import__("hmac").compare_digest(x_archive_admin_token, expected):
        raise HTTPException(403, "Archive administrator token is missing or invalid.")
    if max_pages < 1 or max_pages > 400:
        raise HTTPException(422, "max_pages must be between 1 and 400.")
    if background:
        return exam_archive.start_sync(max_pages=max_pages)
    return exam_archive.sync_archive(max_pages=max_pages, mathematics_only=True)


@router.post("/generate")
def generate(req: GenerateRequest):
    _validate_selection(req)
    try:
        archive_hits = _archive_context(req)
        data = _generate_with_ai(req, archive_hits)
        if data is None:
            data = build_offline_assessment(req)
            data["quality_gate"]["generator"] = "offline-deterministic-no-llm-configured"
            data["quality_gate"]["official_archive_records_available"] = len(archive_hits)
            data["quality_gate"]["archive_used_for_generation"] = False
            data["curriculum_note"] = (
                "Offline fallback only: no AI model key is configured, so official archive material was NOT used to generate these questions. Configure NABIL_LLM_API_KEY or GEMINI_API_KEY to enable retrieval-augmented generation. Teacher review is required."
                if req.language == "en" else
                "Mode hors ligne uniquement : aucune clé de modèle IA n'est configurée ; les archives officielles n'ont donc PAS été utilisées pour générer ces questions. Configurez NABIL_LLM_API_KEY ou GEMINI_API_KEY. Validation par l'enseignant requise."
            )
            data["sources"] = [{"label": h.get("title"), "url": h.get("source_url"),
                                "year": h.get("year"), "grade": h.get("grade")}
                               for h in archive_hits]
            _validate_generated(data, req)
        return data
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(422, f"Assessment rejected by the lesson/quality gate: {str(exc)[:300]}")
    except Exception as exc:
        raise HTTPException(500, f"Competition quality gate failed: {str(exc)[:300]}")

@router.post("/export/docx")
def export_docx(req: ExportRequest):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Cm, Pt
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn

    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2.0)
    sec.left_margin = sec.right_margin = Cm(2.2)
    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(12)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.25

    def para(text, style=None, bold=False):
        p = doc.add_paragraph(style=style)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(str(text))
        r.bold = bold
        return p

    para("NABIL AI | MATHEMATICS COMPETITION", "Title")
    para(req.title, "Heading 1")
    para(f"{req.grade_label}   |   Duration: {req.duration_minutes} min   |   Total: {req.total_marks} marks")
    para("Prepared by NABIL AI — Training paper; teacher review required.")
    para("PART I — QUESTION PAPER", "Heading 1")
    for q in req.questions:
        para(f"Question {q.get('number')}: {q.get('title','')} ({q.get('marks',0)} marks)", "Heading 2")
        para(q.get("statement", ""))
        table_data = q.get("table") or {}
        headers = table_data.get("headers") or []
        rows = table_data.get("rows") or []
        if headers and rows:
            data_table = doc.add_table(rows=1, cols=len(headers))
            data_table.style = "Table Grid"
            for index, heading in enumerate(headers):
                data_table.rows[0].cells[index].text = str(heading)
            for row in rows:
                cells = data_table.add_row().cells
                for index, value in enumerate(row[:len(headers)]):
                    cells[index].text = str(value)
        diagram = q.get("diagram")
        if diagram:
            from PIL import Image, ImageDraw
            image = Image.new("RGB", (720, 300), "white")
            draw = ImageDraw.Draw(image)
            navy = (24, 55, 78)
            if diagram.get("type") == "triangle":
                draw.line([(180, 245), (360, 35), (550, 245), (180, 245)], fill=navy, width=5)
                draw.text((160, 250), "A", fill=navy); draw.text((350, 12), "B", fill=navy); draw.text((555, 250), "C", fill=navy)
            elif diagram.get("type") == "circle":
                draw.ellipse((240, 25, 480, 265), outline=navy, width=5)
                draw.line((360, 145, 480, 145), fill=navy, width=4)
                draw.ellipse((354, 139, 366, 151), fill=navy)
                draw.text((340, 150), "O", fill=navy); draw.text((485, 135), "A", fill=navy)
            elif diagram.get("type") == "coordinate_plane":
                xmin=float(diagram.get("x_min",-5)); xmax=float(diagram.get("x_max",5))
                ymin=float(diagram.get("y_min",-5)); ymax=float(diagram.get("y_max",5))
                def plot_xy(x,y):
                    return (70+(float(x)-xmin)/(xmax-xmin)*580, 245-(float(y)-ymin)/(ymax-ymin)*220)
                ox,oy=plot_xy(0,0)
                draw.line((70, oy, 650, oy), fill=navy, width=3)
                draw.line((ox, 265, ox, 25), fill=navy, width=3)
                draw.polygon([(650,oy),(635,oy-8),(635,oy+8)], fill=navy)
                draw.polygon([(ox,25),(ox-8,40),(ox+8,40)], fill=navy)
                draw.text((660,oy-10), "x", fill=navy); draw.text((ox+8,12), "y", fill=navy); draw.text((ox+7,oy+5), "O", fill=navy)
                points=diagram.get("points") or []
                plotted=[plot_xy(point.get("x",0),point.get("y",0)) for point in points]
                if len(plotted)>1:
                    draw.line((plotted[0][0],plotted[0][1],plotted[1][0],plotted[1][1]), fill=(190,80,45), width=4)
                for point, (px,py) in zip(points,plotted):
                    draw.ellipse((px-7,py-7,px+7,py+7), fill=(190,80,45))
                    draw.text((px+10,py-18), f"{point.get('label','P')}({point.get('x')},{point.get('y')})", fill=navy)
            else:
                draw.line((100,150,620,150), fill=navy, width=4)
                draw.line((360,150,520,45), fill=navy, width=4)
                draw.arc((300,90,430,220), start=0, end=35, fill=(190,80,45), width=5)
                draw.text((350,165), "O", fill=navy); draw.text((80,125), "A", fill=navy); draw.text((625,125), "B", fill=navy)
            picture = io.BytesIO()
            image.save(picture, format="PNG")
            picture.seek(0)
            doc.add_picture(picture, width=Cm(13.5))
            para(diagram.get("caption", "Schematic diagram"))
        for part in q.get("parts", []):
            para(f"{part.get('label','')} ) {part.get('statement','')} [{part.get('marks',0)} marks]")
        para("________________________________________________________________________")
    doc.add_page_break()
    para("PART II — MODEL SOLUTIONS", "Heading 1")
    solmap = {str(x.get("number")): x for x in req.solutions}
    for q in req.questions:
        sol = solmap.get(str(q.get("number")), {})
        para(f"Question {q.get('number')}", "Heading 2")
        for step in sol.get("steps", []):
            para(step)
        para(f"Final answer: {sol.get('final_answer','')}", bold=True)
    doc.add_page_break()
    para("PART III — DETAILED MARKING SCHEME", "Heading 1")
    rubmap = {str(x.get("number")): x for x in req.rubric}
    for q in req.questions:
        rub = rubmap.get(str(q.get("number")), {})
        para(f"Question {q.get('number')} — {rub.get('total', q.get('marks',0))} marks", "Heading 2")
        for c in rub.get("criteria", []):
            para(f"• {c.get('criterion','')} — {c.get('marks',0)} marks")
    if req.curriculum_note:
        doc.add_page_break()
        para("CURRICULUM AND SOURCE NOTE", "Heading 1")
        para(req.curriculum_note)
    stream = io.BytesIO()
    doc.save(stream)
    return StreamingResponse(io.BytesIO(stream.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="NABIL-mathematics-competition.docx"',
                 "Cache-Control": "no-store"})


@router.post("/analytics/visit")
def record_visit(payload: dict, db: Session = Depends(get_db)):
    """Count one page view per browser load and retain anonymous unique visitors."""
    visitor_id = str(payload.get("visitor_id", "")).strip()
    if not visitor_id or len(visitor_id) > 100:
        raise HTTPException(422, "Invalid anonymous visitor identifier.")
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS nabil_competition_analytics (
            visitor_id VARCHAR(100) PRIMARY KEY,
            visits INTEGER NOT NULL DEFAULT 0,
            first_seen VARCHAR(40) NOT NULL,
            last_seen VARCHAR(40) NOT NULL
        )
    """))
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc).isoformat()
    db.execute(text("""
        INSERT INTO nabil_competition_analytics (visitor_id, visits, first_seen, last_seen)
        VALUES (:visitor_id, 1, :now, :now)
        ON CONFLICT (visitor_id) DO UPDATE SET
            visits = nabil_competition_analytics.visits + 1,
            last_seen = :now
    """), {"visitor_id": visitor_id, "now": now})
    db.commit()
    return {"ok": True}


@router.get("/analytics/summary")
def competition_analytics_summary(db: Session = Depends(get_db)):
    db.execute(text("""
        CREATE TABLE IF NOT EXISTS nabil_competition_analytics (
            visitor_id VARCHAR(100) PRIMARY KEY,
            visits INTEGER NOT NULL DEFAULT 0,
            first_seen VARCHAR(40) NOT NULL,
            last_seen VARCHAR(40) NOT NULL
        )
    """))
    row = db.execute(text("""
        SELECT COUNT(*) AS unique_visitors, COALESCE(SUM(visits), 0) AS visits,
               MAX(last_seen) AS updated_at
        FROM nabil_competition_analytics
    """)).mappings().one()
    return {
        "unique_visitors": int(row["unique_visitors"] or 0),
        "visits": int(row["visits"] or 0),
        "updated_at": row["updated_at"],
        "storage_note": "Anonymous browser IDs only; no names or personal details are collected."
    }
