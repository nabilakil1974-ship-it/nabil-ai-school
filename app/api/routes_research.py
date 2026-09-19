"""Opt-in postgraduate research workspace; sources and empirical data stay attributable."""
from __future__ import annotations

import csv
import io
import json
import re
from typing import Literal

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.services.ai_gateway import NabilAIGateway
from app.services.research_survey_analysis import (MAX_UPLOAD, SurveyDataError,
    summarize_survey, report_markdown, tables_csv, spss_syntax)
from app.services.research_docx_notes import attach_researcher_footnotes

router = APIRouter(prefix="/research", tags=["research"])
DEGREE = Literal["masters", "doctorate"]
STAGE = Literal["proposal", "theoretical", "questionnaire", "sampling",
                "practical", "results", "conclusion", "summary", "revision"]
MAX_MANUSCRIPT = 120_000


class ResearchRequest(BaseModel):
    degree: DEGREE
    title: str = Field(min_length=8, max_length=500)
    outline: str = Field(min_length=5, max_length=12_000)
    stage: STAGE = "proposal"
    language: Literal["ar", "en", "fr"] = "ar"
    previous_text: str = Field(default="", max_length=35_000)
    sources: str = Field(default="", max_length=15_000)
    guidance: str = Field(default="", max_length=4000)
    research_questions: str = Field(default="", max_length=12000)
    observed_aggregates: str = Field(default="", max_length=18000)


class ResearchExport(BaseModel):
    degree: DEGREE
    title: str = Field(min_length=8, max_length=500)
    language: Literal["ar", "en", "fr"] = "ar"
    manuscript: str = Field(min_length=1, max_length=MAX_MANUSCRIPT)
    sources: str = Field(default="", max_length=15_000)


class SurveyRequest(BaseModel):
    title: str = Field(min_length=8, max_length=500)
    axes: list[str] = Field(min_length=1, max_length=12)
    language: Literal["ar", "en", "fr"] = "ar"
    questions_per_axis: int = Field(default=4, ge=2, le=10)


def research_instructions(request: ResearchRequest) -> str:
    language = {"ar": "Modern Standard Arabic", "en": "English", "fr": "French"}[request.language]
    return f"""NABIL ACADEMIC RESEARCH MODE V1. Degree: {request.degree}. Stage: {request.stage}.
Write in {language}, professionally and naturally, respecting the researcher's original ideas.
Doctoral-level proposals require an explicit original contribution and rigorous methodological justification;
master's-level work needs a feasible, coherent scope. Title/outline are constraints, not evidence.
Structure: research problem, objectives, questions, hypotheses only when appropriate, conceptual
framework, methods, participants/sampling, instruments, analysis, limitations, ethics, and work plan;
for the theoretical stage provide coherent sections and critical synthesis; after theoretical stage,\nfor questionnaire stage propose validated axes/items; for sampling stage distinguish target population,\nsampling frame, actual recruitment and observed valid responses, never invented N; for practical stage
provide research DESIGN only, with blank placeholders for REAL data/results, never invented findings.\nFor results and conclusion stages, use ONLY actual aggregates explicitly provided; when no real verified\ndata are included, prepare fillable interpretation headings instead of invented tables, statistics or claims.\nFor the final summary, distinguish supported findings, limitations and future research.
For questionnaire, create clearly grouped axes, non-leading items and an explicit response scale.
For revision, improve the provided draft while retaining the researcher's claims.
NEVER fabricate publications, authors, quotations, DOI, page numbers, citations, URLs, fieldwork,
participant consent, survey responses, statistics or empirical outcomes. Only attribute a citation
when a provided excerpt genuinely establishes it; otherwise write [SOURCE NEEDED] at the exact claim.
The user's source list is unverified metadata, not proof that a work says anything. Do not assert
you searched the web or downloaded a reference. Never claim the text is solely human-authored or
promise evasion of AI detection; leave authorship and disclosure decisions to university rules.
Be substantial for the requested STAGE, not a fake promise that an entire doctorate fits one reply.
Return only the requested stage, with useful headings and substantive draft text."""


@router.post("/draft")
def draft_research(request: ResearchRequest):
    if request.stage in ("results", "conclusion", "summary") and not request.observed_aggregates.strip():
        raise HTTPException(status_code=422, detail="Upload and analyze actual questionnaire responses before empirical findings and final conclusions.")
    question = (
        f"Research title:\n{request.title}\n\nOwner's outline:\n{request.outline}"
        f"\n\nResearcher guidance:\n{request.guidance or '(none)'}"
        f"\n\nResearcher-supplied bibliographic notes (UNVERIFIED):\n{request.sources or '(none)'}"
        f"\n\nPrevious draft to continue or revise:\n{request.previous_text or '(none)'}"
        f"\n\nVERIFIED AGGREGATES FROM UPLOADED RESPONSES (if any):\n{request.observed_aggregates or 'NONE'}"
        f"\n\nWrite stage: {request.stage}."
    )
    try:
        result = NabilAIGateway().generate(
            instructions=research_instructions(request),
            messages=[{"role": "user", "content": question}],
            max_output_tokens=5200 if request.stage in ("theoretical", "practical", "results") else 3400,
        )
    except Exception:
        raise HTTPException(status_code=503, detail="Research generation is unavailable; retry without losing your draft.")
    if not isinstance(result, str) or not result.strip():
        raise HTTPException(status_code=503, detail="No academic draft was returned; please retry.")
    return {"degree": request.degree, "stage": request.stage, "title": request.title,
            "text": result.strip(), "sources_verified": False, "complete_thesis": False}


def build_research_docx(request: ResearchExport) -> bytes:
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt

    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = sec.bottom_margin = Cm(2.5)
    sec.left_margin = sec.right_margin = Cm(2.6)
    style = doc.styles["Normal"]
    style.font.name = "Arial"
    style.font.size = Pt(12)
    style.paragraph_format.space_after = Pt(7)

    def add(text: str, kind: str = ""):
        paragraph = doc.add_paragraph(style=kind or None)
        if request.language == "ar":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            prop = paragraph._p.get_or_add_pPr()
            bidi = OxmlElement("w:bidi")
            bidi.set(qn("w:val"), "1")
            prop.append(bidi)
        run = paragraph.add_run(text)
        if request.language == "ar":
            rtl = OxmlElement("w:rtl")
            rtl.set(qn("w:val"), "1")
            run._r.get_or_add_rPr().append(rtl)
        return paragraph

    add(request.title, "Title")
    add("Doctoral research draft" if request.degree == "doctorate" else "Master's research draft")
    add("Researcher review required: validate source claims, methods, data and university requirements.")
    for raw in request.manuscript.splitlines():
        line = raw.strip()
        if not line:
            doc.add_paragraph()
        elif line.startswith(("### ", "## ", "# ")):
            level = 3 if line.startswith("### ") else 2 if line.startswith("## ") else 1
            title = line.lstrip("#").strip()
            add(title, f"Heading {level}")
        else:
            add(line)
    if request.sources.strip():
        add("المراجع المقدّمة من الباحث (تحتاج إلى تحقق)" if request.language == "ar"
            else "Researcher-supplied references (verification required)", "Heading 1")
        for source in request.sources.splitlines():
            if source.strip():
                add(source.strip())
    stream = io.BytesIO()
    doc.save(stream)
    return attach_researcher_footnotes(stream.getvalue(), request.sources)


@router.post("/export/docx")
def export_research_docx(request: ResearchExport):
    data = build_research_docx(request)
    filename = "nabil-doctorate-draft.docx" if request.degree == "doctorate" else "nabil-masters-draft.docx"
    return StreamingResponse(io.BytesIO(data),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{filename}"',
                 "Cache-Control": "no-store"})


def build_survey_rows(request: SurveyRequest) -> list[dict[str, str]]:
    labels = {
        "ar": ("المحور", "العبارة", "مقياس الموافقة الخماسي"),
        "en": ("Axis", "Item", "Five-point agreement scale"),
        "fr": ("Axe", "Question", "Échelle d'accord à cinq points"),
    }
    axis_label, item_label, scale = labels[request.language]
    return [
        {"axis": axis.strip(), "item": f"[{axis_label}: {axis.strip()}] {item_label} {number}: "
         "[RESEARCHER TO WRITE AND VALIDATE QUESTION]", "response_scale": scale}
        for axis in request.axes for number in range(1, request.questions_per_axis + 1)
    ]


@router.post("/survey/template")
def survey_template(request: SurveyRequest):
    if any(not item.strip() or len(item) > 160 for item in request.axes):
        raise HTTPException(status_code=422, detail="Each survey axis needs a short, non-empty name.")
    return {"title": request.title, "axes": request.axes,
            "items": build_survey_rows(request), "google_form_created": False,
            "note": "Editable survey template only. Actual Google Forms creation requires user-authorized OAuth."}


@router.post("/survey/csv")
def survey_csv(request: SurveyRequest):
    if any(not item.strip() or len(item) > 160 for item in request.axes):
        raise HTTPException(status_code=422, detail="Each survey axis needs a short, non-empty name.")
    stream = io.StringIO()
    stream.write("\ufeff")
    writer = csv.DictWriter(stream, fieldnames=["axis", "item", "response_scale"])
    writer.writeheader()
    writer.writerows(build_survey_rows(request))
    return StreamingResponse(iter([stream.getvalue().encode("utf-8")]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="nabil-survey-template.csv"',
                 "Cache-Control": "no-store"})


class GoogleFormScriptRequest(BaseModel):
    title: str = Field(min_length=8, max_length=500)
    language: Literal["ar", "en", "fr"] = "ar"
    questions: list[dict[str, str]] = Field(min_length=1, max_length=120)


def build_google_form_script(request: GoogleFormScriptRequest) -> str:
    """Generate a script the owner MUST run and authorize in their Google account.

    No Google Forms is claimed to exist from this API request alone.
    """
    cleaned = []
    for entry in request.questions:
        axis = str(entry.get("axis", "")).strip()
        item = str(entry.get("item", "")).strip()
        if not axis or not item or len(axis) > 160 or len(item) > 600:
            raise HTTPException(status_code=422, detail="Each question requires a short axis and item.")
        if "[RESEARCHER TO WRITE" in item.upper():
            raise HTTPException(status_code=422, detail="Replace placeholder items with real questions first.")
        cleaned.append({"axis": axis, "item": item})
    scales = {
        "ar": ["لا أوافق بشدة", "لا أوافق", "محايد", "أوافق", "أوافق بشدة"],
        "en": ["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"],
        "fr": ["Pas du tout d’accord", "Pas d’accord", "Neutre", "D’accord", "Tout à fait d’accord"],
    }
    # JSON string literals are valid Google Apps Script (JavaScript). Escape HTML
    # metacharacters to ensure pasted user research titles cannot break the code.
    payload = json.dumps(
        {"title": request.title, "items": cleaned, "scale": scales[request.language]},
        ensure_ascii=True,
    ).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return (
        "// NABIL AI — run createNabilResearchForm in your OWN Google Apps Script account.\n"
        "// Google will request authorization; no Form is created by downloading this file.\n"
        "function createNabilResearchForm() {\n"
        "  const spec = " + payload + ";\n"
        "  const form = FormApp.create(spec.title);\n"
        "  let currentAxis = null;\n"
        "  for (const entry of spec.items) {\n"
        "    if (entry.axis !== currentAxis) {\n"
        "      currentAxis = entry.axis;\n"
        "      form.addSectionHeaderItem().setTitle(currentAxis);\n"
        "    }\n"
        "    form.addMultipleChoiceItem().setTitle(entry.item)\n"
        "      .setChoiceValues(spec.scale).setRequired(true);\n"
        "  }\n"
        "  Logger.log('Edit URL: ' + form.getEditUrl());\n"
        "  Logger.log('Response URL: ' + form.getPublishedUrl());\n"
        "}\n"
    )


@router.post("/survey/google-forms-script")
def google_forms_script(request: GoogleFormScriptRequest):
    data = build_google_form_script(request).encode("utf-8")
    return StreamingResponse(iter([data]), media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="nabil-create-google-form.gs"',
                 "Cache-Control": "no-store"})


# Verified provider landing pages, NOT extracted theses or verified citations.
RESEARCH_PORTALS = [
    {"name": "OATD", "url": "https://www.oatd.org/", "access": "open-access discovery index"},
    {"name": "White Rose eTheses", "url": "https://etheses.whiterose.ac.uk/",
     "access": "open institutional theses; each record may have its own conditions"},
    {"name": "AUC Knowledge Fountain", "url": "https://fount.aucegypt.edu/",
     "access": "institutional repository; some items embargoed or restricted"},
    {"name": "Saudi Digital Library", "url": "https://sdl.edu.sa/",
     "access": "access may depend on institutional credentials"},
    {"name": "ProQuest Dissertations & Theses", "url": "https://www.proquest.com/",
     "access": "institutional subscription or purchase may be required"},
]


@router.get("/source-portals")
def source_portals():
    return {"portals": RESEARCH_PORTALS, "retrieved_theses": [],
            "note": "Discovery links only; verify the original record/full text and citation before quoting."}


def _axis_columns(text_value: str) -> dict[str, list[str]]:
    try:
        value = json.loads(text_value)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail="Axes must be a JSON object mapping axis names to CSV item columns.") from exc
    if not isinstance(value, dict) or any(not isinstance(k, str)
       or not isinstance(v, list) or any(not isinstance(c, str) for c in v)
       for k, v in value.items()):
        raise HTTPException(status_code=422, detail="Invalid axis-to-column mapping.")
    return value


async def _uploaded_analysis(file: UploadFile, axes_json: str):
    axes = _axis_columns(axes_json)
    data = await file.read(MAX_UPLOAD + 1)
    try:
        return summarize_survey(data, axes)
    except SurveyDataError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/survey/analyze")
async def analyze_uploaded_survey(file: UploadFile = File(...),
                                  axes_json: str = Form(...),
                                  language: Literal["ar", "en", "fr"] = Form("ar")):
    report = await _uploaded_analysis(file, axes_json)
    return {"summary": report, "markdown": report_markdown(report, language),
            "actual_data_analyzed": True, "spss_executed": False}


@router.post("/survey/analysis-tables.csv")
async def download_analysis_tables(file: UploadFile = File(...),
                                   axes_json: str = Form(...)):
    report = await _uploaded_analysis(file, axes_json)
    return StreamingResponse(iter([tables_csv(report)]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="nabil-survey-tables.csv"',
                 "Cache-Control": "no-store"})


@router.post("/survey/analysis.sps")
async def download_spss_syntax(file: UploadFile = File(...),
                               axes_json: str = Form(...)):
    report = await _uploaded_analysis(file, axes_json)
    return StreamingResponse(iter([spss_syntax(report).encode("utf-8")]),
        media_type="text/plain; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="nabil-survey-analysis.sps"',
                 "Cache-Control": "no-store"})
