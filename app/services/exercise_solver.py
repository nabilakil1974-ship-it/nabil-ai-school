"""Exercise solver: read a question (typed / image / PDF), then produce a step-by-step solution
that the Golden V6 board writes with the animated pen.

Safety rules (all enforced here, not in the browser):
- uses the project's existing AI gateway (providers + keys stay server-side; nothing is logged);
- the reader may never guess: unclear parts are returned as `unclear`, and the browser must make
  the student confirm/fix the statement before solving;
- a solution is only normalised data (no HTML); figures are numbers + labels drawn by the engine;
- when a machine check (sympy) is possible it is reported as verified / mismatch, else not_checked.
"""
from __future__ import annotations

import json
import logging
import math
import os
import re
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("nabil_ai.solver")

MAX_UPLOAD_BYTES = 8 * 1024 * 1024
MAX_PDF_PAGES = 3
IMAGE_MIMES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
LANGS = {"ar": "Arabic", "fr": "French", "en": "English"}

PROVIDER_ENV = {
    "gemini": ("GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3", "GEMINI_API_KEY_4", "GEMINI_API_KEY_5"),
    "openrouter": ("OPENROUTER_API_KEY",),
    "groq": ("GROQ_API_KEY",),
    "openai": ("OPENAI_API_KEY",),
}


class SolverError(Exception):
    def __init__(self, code: str, message: str, http: int = 400):
        super().__init__(message)
        self.code, self.message, self.http = code, message, http


def providers_status() -> Dict[str, Any]:
    """Which providers are configured. Booleans only: key values are never exposed."""
    configured = {name: any(os.getenv(k, "").strip() for k in keys) for name, keys in PROVIDER_ENV.items()}
    return {"providers": configured, "any": any(configured.values()),
            "vision_models": {"openrouter": bool(os.getenv("OPENROUTER_VISION_MODEL", "").strip()),
                              "gemini": bool(os.getenv("GEMINI_VISION_MODEL", "").strip()),
                              "openai": bool(os.getenv("OPENAI_VISION_MODEL", "").strip())},
            "pdftotext": bool(shutil.which("pdftotext")), "pdftoppm": bool(shutil.which("pdftoppm"))}


def _gateway():
    if not providers_status()["any"]:
        raise SolverError("PROVIDER_NOT_CONFIGURED",
                          "لا يوجد مزوّد ذكاء اصطناعي مضبوط على الخادم، لذلك لا يمكن قراءة أو حل تمرين جديد الآن.", 503)
    from app.services.ai_gateway import get_ai_gateway
    return get_ai_gateway()


def extract_json(raw: str) -> Dict[str, Any]:
    t = str(raw or "").strip()
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.I)
    try:
        v = json.loads(t)
    except Exception:
        a, b = t.find("{"), t.rfind("}")
        if a < 0 or b <= a:
            raise SolverError("BAD_MODEL_OUTPUT", "تعذّر فهم ردّ النموذج. حاول مرة أخرى.", 502)
        try:
            v = json.loads(t[a:b + 1])
        except Exception:
            raise SolverError("BAD_MODEL_OUTPUT", "تعذّر فهم ردّ النموذج. حاول مرة أخرى.", 502)
    if not isinstance(v, dict):
        raise SolverError("BAD_MODEL_OUTPUT", "ردّ النموذج ليس بالصيغة المطلوبة.", 502)
    return v


def _s(v: Any, n: int = 600) -> str:
    return re.sub(r"\s+", " ", str(v if v is not None else "")).strip()[:n]


# ----------------------------------------------------------------------------- reading
READ_PROMPT = """You transcribe a school exercise from a photo or a page. Reply with ONLY JSON:
{"statement": "<the exact text of the exercise, formulas in plain text such as x^2 - 5x + 6 = 0, sqrt(x), a/b>",
 "unclear": ["<each part that is hard to read, cut off, or missing, with where it is>"],
 "has_figure": true|false,
 "figure_description": "<only what is visibly drawn: shapes, labelled points, given lengths/angles; empty if none>"}
Rules: transcribe, do not solve. NEVER guess a number, a sign, an exponent or a label that is not clearly visible:
put it in "unclear" instead. Keep the original language of the exercise. If the image is not an exercise or is unreadable,
return an empty statement and explain in "unclear"."""


def _pdf_to_text_or_image(data: bytes) -> Tuple[str, Optional[bytes]]:
    if not data.startswith(b"%PDF"):
        raise SolverError("NOT_A_PDF", "الملف ليس PDF صالحًا.")
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "in.pdf")
        with open(src, "wb") as f:
            f.write(data)
        text = ""
        if shutil.which("pdftotext"):
            try:
                text = subprocess.run(["pdftotext", "-f", "1", "-l", str(MAX_PDF_PAGES), "-layout", src, "-"],
                                      capture_output=True, text=True, timeout=30, check=False).stdout
            except Exception:
                text = ""
        if len(re.sub(r"\s+", "", text)) >= 40:
            return text.strip()[:6000], None
        if not shutil.which("pdftoppm"):
            raise SolverError("PDF_SCANNED_NO_RASTER", "ملف PDF ممسوح ضوئيًا ولا توجد أداة تحويله إلى صورة على الخادم.", 503)
        out = os.path.join(d, "p")
        subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "130", "-jpeg", src, out], timeout=60, check=False)
        pages = sorted(x for x in os.listdir(d) if x.startswith("p") and x.endswith(".jpg"))
        if not pages:
            raise SolverError("PDF_RENDER_FAILED", "تعذّر تحويل صفحة PDF إلى صورة.", 422)
        with open(os.path.join(d, pages[0]), "rb") as f:
            return "", f.read()


def read_statement(*, text: str = "", file_bytes: Optional[bytes] = None, mime: str = "",
                   lang: str = "ar") -> Dict[str, Any]:
    """-> {status: 'ok'|'needs_clarification'|'unreadable', statement, unclear[], has_figure, figure_description, source}"""
    typed = _s(text, 4000)
    if typed and not file_bytes:
        return {"status": "ok", "statement": typed, "unclear": [], "has_figure": False,
                "figure_description": "", "source": "typed"}
    if not file_bytes:
        raise SolverError("EMPTY", "اكتب التمرين أو ارفع صورة/ملف PDF.")
    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise SolverError("TOO_LARGE", "الملف أكبر من 8 ميغابايت.", 413)
    mime = (mime or "").lower()
    source, image = "image", None
    if mime == "application/pdf" or file_bytes.startswith(b"%PDF"):
        source = "pdf"
        pdf_text, image = _pdf_to_text_or_image(file_bytes)
        if pdf_text:
            return {"status": "ok", "statement": pdf_text, "unclear": [], "has_figure": False,
                    "figure_description": "", "source": "pdf_text"}
        mime = "image/jpeg"
    elif mime in IMAGE_MIMES:
        image = file_bytes
    else:
        raise SolverError("UNSUPPORTED", "الأنواع المدعومة: صورة JPG/PNG/WEBP أو PDF.", 415)
    gw = _gateway()
    try:
        raw = gw.generate(READ_PROMPT, [{"role": "user", "content": "Transcribe the exercise in the image."}],
                          image_bytes=image, image_mime_type=mime if mime != "image/jpg" else "image/jpeg",
                          max_output_tokens=1400)
    except SolverError:
        raise
    except Exception as exc:
        logger.warning("SOLVER_READ_PROVIDER_FAILED %s", type(exc).__name__)
        raise SolverError("PROVIDER_FAILED", "تعذّرت قراءة الصورة الآن (المزوّد غير متاح). يمكنك كتابة التمرين يدويًا.", 502)
    data = extract_json(raw)
    statement = _s(data.get("statement"), 4000)
    unclear = [_s(u, 240) for u in (data.get("unclear") or []) if _s(u, 240)][:8] if isinstance(data.get("unclear"), list) else []
    out = {"statement": statement, "unclear": unclear, "has_figure": bool(data.get("has_figure")),
           "figure_description": _s(data.get("figure_description"), 800), "source": source}
    out["status"] = "unreadable" if not statement else ("needs_clarification" if unclear else "ok")
    return out


# ----------------------------------------------------------------------------- solving
SOLVE_PROMPT = """You are Ustaz NABIL, a school maths/science tutor. Solve the exercise like a teacher at the board.
Write EVERYTHING (labels, say, text, justification) in {language}. Reply with ONLY JSON:
{{"needs_clarification": false, "questions": [],
  "title": "<short title>",
  "given": ["<datum taken from the statement>"], "required": ["<what must be found/proved>"],
  "figure": null | {{"points": {{"A":[0,0],"B":[4,0],"C":[0,3]}}, "segments": [["A","B","4 cm"],["B","C"],["A","C","dash"]],
                    "circles": [{{"center":"O","r":2}}], "marks": [{{"type":"right_angle","at":"A","between":["B","C"]}}, {{"type":"equal","segs":[["A","B"],["A","C"]],"n":1}}, {{"type":"equal_angle","at":"B","between":["A","C"],"n":1}}, {{"type":"parallel","segs":[["A","B"],["D","E"]],"n":1}}]}},
  (mark ONLY properties stated or proved: equal = congruent segments, same n = same length; equal_angle = equal angles; parallel = parallel lines)
  "steps": [{{"say": "<2-5 word spoken lead-in such as: We substitute now>",
             "text": "<one clear sentence explaining the move>", "formula": "<optional, plain text like 2x + 3 = 7>",
             "justification": "<rule/theorem/property used, optional>"}}],
  "answer": "<final answer sentence>",
  "machine_check": null | {{"equation": "x**2-5*x+6=0", "variable": "x", "solutions": ["2","3"]}}}}
Rules:
- Use ONLY data present in the statement. If something needed is missing or ambiguous, set needs_clarification=true,
  list precise questions, and leave steps empty. Never invent numbers.
- 4 to 14 steps. Each step is one school-level move (substitute, simplify, divide both sides, factor, apply a theorem, conclude).
  Show every calculation; never jump to the result. The last step concludes the answer.
- A figure is optional: only for geometry, with coordinates consistent with the given lengths/angles (maths coordinates, y up).
- machine_check only for equations/inequalities in one variable that python/sympy can solve (use ** for powers); else null.
- Plain text only, no markdown, no HTML, no LaTeX commands."""


def _num(v: Any) -> Optional[float]:
    try:
        f = float(v)
        return f if math.isfinite(f) and abs(f) < 1e6 else None
    except Exception:
        return None


def _clean_figure(fig: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(fig, dict) or not isinstance(fig.get("points"), dict):
        return None
    pts: Dict[str, List[float]] = {}
    for name, xy in list(fig["points"].items())[:26]:
        if isinstance(xy, (list, tuple)) and len(xy) == 2 and _num(xy[0]) is not None and _num(xy[1]) is not None:
            pts[_s(name, 4)] = [float(xy[0]), float(xy[1])]
    if len(pts) < 1:
        return None
    segs = []
    for sg in (fig.get("segments") or [])[:40]:
        if isinstance(sg, (list, tuple)) and len(sg) >= 2 and _s(sg[0], 4) in pts and _s(sg[1], 4) in pts:
            extra = [_s(x, 24) for x in sg[2:4]]
            segs.append([_s(sg[0], 4), _s(sg[1], 4)] + extra)
    circles = [{"center": _s(c.get("center"), 4), "r": float(c["r"])} for c in (fig.get("circles") or [])[:6]
               if isinstance(c, dict) and _s(c.get("center"), 4) in pts and _num(c.get("r")) and float(c["r"]) > 0]
    marks = []
    for m in (fig.get("marks") or [])[:8]:
        if isinstance(m, dict) and m.get("type") == "right_angle" and _s(m.get("at"), 4) in pts \
                and isinstance(m.get("between"), list) and len(m["between"]) == 2 \
                and all(_s(b, 4) in pts for b in m["between"]):
            marks.append({"type": "right_angle", "at": _s(m["at"], 4), "between": [_s(b, 4) for b in m["between"]]})
    for m in (fig.get("marks") or [])[:12]:
        if isinstance(m, dict) and m.get("type") == "angle" and _s(m.get("at"), 4) in pts and _s(m.get("text"), 8):
            marks.append({"type": "angle", "at": _s(m["at"], 4), "text": _s(m["text"], 8)})
    for m in (fig.get("marks") or [])[:12]:
        if not isinstance(m, dict):
            continue
        n = int(m["n"]) if isinstance(m.get("n"), (int, float)) and 1 <= int(m["n"]) <= 4 else 1
        if m.get("type") in ("equal", "parallel") and isinstance(m.get("segs"), list):
            segs_ok = [[_s(x, 4) for x in sg] for sg in m["segs"][:6]
                       if isinstance(sg, list) and len(sg) == 2 and all(_s(x, 4) in pts for x in sg)]
            if segs_ok:
                marks.append({"type": m["type"], "segs": segs_ok, "n": n, **({"g": int(m["g"])} if isinstance(m.get("g"), int) and 0 <= m["g"] < 5 else {})})
        elif m.get("type") == "equal_angle" and _s(m.get("at"), 4) in pts \
                and isinstance(m.get("between"), list) and len(m["between"]) == 2 \
                and all(_s(b, 4) in pts for b in m["between"]):
            marks.append({"type": "equal_angle", "at": _s(m["at"], 4), "between": [_s(b, 4) for b in m["between"]], "n": n, **({"g": int(m["g"])} if isinstance(m.get("g"), int) and 0 <= m["g"] < 5 else {})})
    out = {"points": pts, "segments": segs, "circles": circles, "marks": marks}
    if isinstance(fig.get("show"), list):
        out["show"] = [_s(n, 4) for n in fig["show"] if _s(n, 4) in pts]
    return out


_SAFE_EXPR = re.compile(r"^[0-9a-zA-Z_+\-*/^().,=<>\s]*$")


def machine_check(mc: Any) -> Dict[str, str]:
    """Independent sympy check of the stated solution set. Never raises."""
    if not isinstance(mc, dict):
        return {"status": "not_checked", "detail": ""}
    try:
        import sympy as sp
        eq, var = _s(mc.get("equation"), 200), _s(mc.get("variable"), 4) or "x"
        sols = [_s(x, 40) for x in (mc.get("solutions") or [])][:10]
        if not eq or "__" in eq or not _SAFE_EXPR.match(eq) or not re.match(r"^[A-Za-z]$", var) \
                or any(not _SAFE_EXPR.match(x) or "__" in x for x in sols):
            return {"status": "not_checked", "detail": ""}
        eq = eq.replace("^", "**")
        x = sp.Symbol(var, real=True)
        local = {var: x, "sqrt": sp.sqrt, "pi": sp.pi, "Abs": sp.Abs}
        if "=" in eq:
            left, right = eq.split("=", 1)
            expr = sp.sympify(left.replace("**", "**"), locals=local) - sp.sympify(right, locals=local)
        else:
            return {"status": "not_checked", "detail": ""}
        real = sp.solveset(expr, x, domain=sp.S.Reals)
        if not isinstance(real, sp.FiniteSet):
            return {"status": "not_checked", "detail": ""}
        want = {sp.nsimplify(sp.sympify(s.replace("^", "**"), locals=local)) for s in sols}
        have = {sp.nsimplify(v) for v in real}
        ok = len(want) == len(have) and all(any(abs(complex(sp.N(a - b))) < 1e-9 for b in have) for a in want)
        return {"status": "verified" if ok else "mismatch",
                "detail": ", ".join(str(v) for v in sorted(have, key=lambda q: float(q)))}
    except Exception:
        return {"status": "not_checked", "detail": ""}


def normalise_solution(data: Dict[str, Any]) -> Dict[str, Any]:
    if data.get("needs_clarification"):
        qs = [_s(q, 240) for q in (data.get("questions") or []) if _s(q, 240)][:6]
        return {"status": "needs_clarification", "questions": qs or ["البيانات غير كافية لحل التمرين."]}
    steps = []
    for st in (data.get("steps") or [])[:20]:
        if not isinstance(st, dict):
            continue
        item = {"say": _s(st.get("say"), 90), "text": _s(st.get("text"), 500),
                "formula": _s(st.get("formula"), 200), "justification": _s(st.get("justification"), 220)}
        main_pts = (_clean_figure(data.get("figure")) or {}).get("points") if isinstance(data.get("figure"), dict) else None
        if main_pts and isinstance(st.get("figure_step"), dict):
            fs = dict(st["figure_step"]); fs["points"] = main_pts
            cf = _clean_figure(fs)
            if cf and (cf["segments"] or cf["marks"] or cf.get("show")):
                item["figure_step"] = {k: cf[k] for k in ("segments", "marks", "circles", "show") if k in cf}
        if item["text"] or item["formula"]:
            steps.append(item)
    if len(steps) < 2 or not _s(data.get("answer")):
        raise SolverError("INCOMPLETE_SOLUTION", "لم يُنتج النموذج حلًا كاملًا بخطوات. حاول مرة أخرى.", 502)
    return {"status": "ok", "title": _s(data.get("title"), 120),
            "given": [_s(x, 300) for x in (data.get("given") or [])][:10],
            "required": [_s(x, 300) for x in (data.get("required") or [])][:6],
            "figure": _clean_figure(data.get("figure")), "steps": steps,
            "answer": _s(data.get("answer"), 400),
            "verification": machine_check(data.get("machine_check"))}


def solve(*, statement: str, lang: str = "ar", grade: str = "", subject: str = "") -> Dict[str, Any]:
    st = _s(statement, 4000)
    if len(st) < 3:
        raise SolverError("EMPTY", "نص التمرين فارغ.")
    gw = _gateway()
    language = LANGS.get(lang, "Arabic")
    ctx = f"Grade: {_s(grade, 40) or 'unknown'}. Subject: {_s(subject, 60) or 'unknown'}.\nExercise (confirmed by the student):\n{st}"
    try:
        raw = gw.generate(SOLVE_PROMPT.format(language=language), [{"role": "user", "content": ctx}],
                          max_output_tokens=3200)
    except Exception as exc:
        logger.warning("SOLVER_SOLVE_PROVIDER_FAILED %s", type(exc).__name__)
        raise SolverError("PROVIDER_FAILED", "تعذّر الحل الآن (المزوّد غير متاح). أعد المحاولة بعد قليل.", 502)
    out = normalise_solution(extract_json(raw))
    out["statement"], out["lang"] = st, lang
    return out
