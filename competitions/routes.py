from __future__ import annotations

import io
import json
import re
from typing import Literal

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from competitions.offline_generator import build_offline_assessment

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

@router.post("/generate")
def generate(req: GenerateRequest):
    _validate_selection(req)
    try:
        data = build_offline_assessment(req)
        # Hard quality gate: every selected lesson gets a question, solution and rubric.
        if len(data["questions"]) != len(req.lessons):
            raise ValueError("Not every selected lesson received a question.")
        if len(data["questions"]) != len(data["solutions"]) or len(data["questions"]) != len(data["rubric"]):
            raise ValueError("Question, solution and rubric counts do not match.")
        marks = round(sum(float(q.get("marks", 0)) for q in data["questions"]), 2)
        if marks != float(req.total_marks):
            raise ValueError(f"Question marks total {marks}, expected {req.total_marks}.")
        return data
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(500, f"Offline competition generation failed: {str(exc)[:240]}")

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
