"""NABIL AI Golden V6 board — renderer for structured lesson data.

The approved V6 design (photorealistic hand, one pen, written-word reveal, English
voice, 0.7x default speed, SINGLE / DUAL board) lives in ONE static engine:

    assets/golden_v6_engine.js   behaviour
    assets/golden_v6.css         look
    assets/golden_v6_hand_png_b64.txt   the hand, extracted byte-for-byte from the
                                 approved NABIL_G07_CUBE_GOLDEN_V6_APPROVED_VOICE_ON_SIDES.html
    assets/golden_v6_reference/  untouched copy of the approved template

The factory only produces *lesson data* (scenes). It never writes board code.
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any, Dict, List

V6_BOARD_CONTRACT = "NABIL_GOLDEN_V6_BOARD_V1"
_ASSETS = Path(__file__).resolve().parent / "assets"
HAND_SHA256 = "1271c28aa0015773c34dc54ee15e024d6974d98ab7d88115865e98514a0df8d4"
DEFAULT_SPEED = 0.7

UI_ALL: Dict[str, Dict[str, str]] = {
    "ar": {"play": "▶ ابدأ", "pause": "⏸ إيقاف", "resume": "▶ تابع", "prev": "السابق", "next": "التالي",
           "replay": "↻ إعادة", "voice_on": "🔊 الصوت مفعّل", "voice_off": "🔇 تفعيل الصوت",
           "lost": "لم أفهم", "understood": "فهمت، أكمل من هنا", "repeat_scene": "أعد هذه الفكرة",
           "lost_help": "لا بأس. أعد الفكرة من أولها، أو أكمل عندما تفهم.", "check": "تحقّق",
           "try_again": "حاول مرة أخرى وراجع الخطوات.", "start": "ابدأ الدرس", "brand": "منصة الأستاذ النبيل",
           "paused": "متوقف مؤقتًا", "playing": "", "fullscreen": "ملء الشاشة", "exit": "خروج",
           "voice_hint": "الصوت إنجليزي. فعّله بنقرة إن منعه المتصفح.", "enable_voice": "فعّل الصوت",
           "novoice": "لا يوجد صوت إنجليزي مثبّت على هذا الجهاز؛ يستمر الشرح مكتوبًا.",
           "ar_voice": "🔈 اقرأ بالعربية أيضًا", "ar_voice_on": "🔊 القراءة بالعربية مفعّلة", "exercise": "التمرين",
           "pick_exercise": "اختر التمرين", "tools": "⚙ أدوات", "repeat_step": "↻ كرّر الخطوة", "back_to_lesson": "↩ العودة إلى الدرس", "solve_done": "✓ اكتمل الحل. يمكنك تكرار خطوة أو العودة إلى الدرس.", "no_solution": "حلّ هذا التمرين غير متوفر بعد.", "ar_missing": "الترجمة العربية غير متوفرة لهذه الخطوة."},
    "fr": {"play": "▶ Démarrer", "pause": "⏸ Pause", "resume": "▶ Reprendre", "prev": "Précédent",
           "next": "Suivant", "replay": "↻ Rejouer", "voice_on": "🔊 Voix activée", "voice_off": "🔇 Activer la voix",
           "lost": "Je n'ai pas compris", "understood": "J'ai compris, continuer ici", "repeat_scene": "Répéter cette idée",
           "lost_help": "Pas de souci. Répète l'idée depuis le début, ou continue quand tu as compris.", "check": "Vérifier",
           "try_again": "Réessaie en relisant les étapes.", "start": "Commencer la leçon", "brand": "Plateforme d'Ustaz Nabil",
           "paused": "En pause", "playing": "", "fullscreen": "Plein écran", "exit": "Quitter",
           "voice_hint": "La voix est en anglais. Active-la d'un clic si le navigateur la bloque.", "enable_voice": "Activer la voix",
           "novoice": "Aucune voix anglaise installée sur cet appareil ; l'explication continue par écrit.",
           "ar_voice": "🔈 Lire aussi en arabe", "ar_voice_on": "🔊 Lecture arabe activée", "exercise": "Exercice",
           "pick_exercise": "Choisir l'exercice", "tools": "⚙ Outils", "repeat_step": "↻ Répéter l'étape", "back_to_lesson": "↩ Retour à la leçon", "solve_done": "✓ Solution terminée. Tu peux répéter une étape ou revenir à la leçon.", "no_solution": "La solution de cet exercice n'est pas encore disponible.", "ar_missing": "Traduction arabe indisponible pour cette étape."},
    "en": {"play": "▶ Start", "pause": "⏸ Pause", "resume": "▶ Resume", "prev": "Previous", "next": "Next",
           "replay": "↻ Replay", "voice_on": "🔊 Voice on", "voice_off": "🔇 Enable voice",
           "lost": "I did not understand", "understood": "I understand, continue here", "repeat_scene": "Repeat this idea",
           "lost_help": "No problem. Repeat the idea from its start, or continue when you are ready.", "check": "Check",
           "try_again": "Try again and review the steps.", "start": "Start lesson", "brand": "Ustaz Nabil Platform",
           "paused": "Paused", "playing": "", "fullscreen": "Fullscreen", "exit": "Exit",
           "voice_hint": "Voice is English. Tap to enable it if the browser blocked it.", "enable_voice": "Enable voice",
           "novoice": "No English voice is installed on this device; the explanation continues in writing.",
           "ar_voice": "🔈 Also read in Arabic", "ar_voice_on": "🔊 Arabic reading on", "exercise": "Exercise",
           "pick_exercise": "Choose exercise", "tools": "⚙ Tools", "repeat_step": "↻ Repeat step", "back_to_lesson": "↩ Back to the lesson", "solve_done": "✓ Solution finished. You can repeat a step or go back to the lesson.", "no_solution": "The solution for this exercise is not available yet.", "ar_missing": "No Arabic translation for this step."},
}

# ----------------------------------------------------------------- terminology
_SOLID_TITLE = re.compile(r"\b(cube|cuboid|prism|pyramid|solid|polyhedr\w*)\b|مكعب|متوازي المستطيلات|منشور|مجسم|cube|solide", re.I)


def is_solids_lesson(title: str) -> bool:
    return bool(_SOLID_TITLE.search(str(title or "")))


def apply_terminology(text: str, lesson_title: str) -> str:
    """Approved Cube terminology: Sides / أضلاع / Side length (not Edges / أحرف).
    Applied only inside solids lessons, so other subjects keep their exact terms."""
    if not is_solids_lesson(lesson_title):
        return text
    t = str(text or "")
    t = re.sub(r"\bEdge length\b", "Side length", t)
    t = re.sub(r"\bedge length\b", "side length", t)
    t = re.sub(r"\bEdges\b", "Sides", t)
    t = re.sub(r"\bedges\b", "sides", t)
    t = re.sub(r"\bEdge\b", "Side", t)
    t = re.sub(r"\bedge\b", "side", t)
    t = re.sub(r"أحرف", "أضلاع", t)
    t = re.sub(r"حرف المكعب", "ضلع المكعب", t)
    return t


# ------------------------------------------------------------------ scene data
_SUPD = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}


def _sup(n: int) -> str:
    return "".join(_SUPD.get(c, c) for c in str(n))


def power_draw_step(spec: dict) -> dict | None:
    """Pen drawing for a POWER_EXPLORER lab: the factors of the power, one box each."""
    from scripts.nabil_power_lab import _SAMPLE
    law = str(spec.get("law") or "definition")
    v = _SAMPLE.get(law)
    if not v:
        return None
    try:
        if law == "definition":
            base, exp = int(v["a"]), int(v["n"])
        elif law == "product_same_base":
            base, exp = int(v["a"]), int(v["m"]) + int(v["n"])
        elif law == "quotient_same_base":
            base, exp = int(v["a"]), int(v["m"]) - int(v["n"])
        elif law == "power_of_power":
            base, exp = int(v["a"]), int(v["m"]) * int(v["n"])
        elif law in ("product_same_exponent", "quotient_same_exponent"):
            base, exp = int(v["a"]) * int(v["b"]) if law == "product_same_exponent" else int(v["a"]) // int(v["b"]), int(v["m"])
        else:
            return None
    except (KeyError, ValueError, ZeroDivisionError):
        return None
    if exp < 1 or exp > 12:
        return None
    return {"t": "draw", "draw": "powerFactors",
            "args": {"base": base, "exp": exp, "value": str(base ** exp),
                     "title": f"{base}{_sup(exp)}"}}


def _clean(s: Any) -> str:
    from scripts.nabil_factory.cards.mathtext import canonical_math
    return canonical_math(re.sub(r"\s+", " ", str(s or "")).strip())


def build_scenes(activities: List[dict], lang: str, lesson_title: str = "") -> List[dict]:
    """Verified activities -> V6 scenes. Pure data; no HTML, no invented content."""
    scenes: List[dict] = []
    for act in activities:
        raw_steps = [s for s in (act.get("teaching_steps") or []) if isinstance(s, dict)]
        steps: List[dict] = []
        for st in raw_steps:
            text = apply_terminology(_clean(st.get("sentence")), lesson_title)
            if not text:
                continue
            speech_en = str(st.get("speech_en") or "").strip()
            entry = {"t": "text", "text": text,
                     "label": apply_terminology(str(st.get("label") or ""), lesson_title),
                     "speech": (text if lang == "en" else speech_en)}
            ar = str(st.get("speech_ar") or "").strip() or (text if lang == "ar" else "")
            if ar:
                entry["ar"] = ar
            hint = step_hint(text, lang)
            if hint and str(st.get("kind") or "") in ("step", "final", "problem"):
                entry["hint"] = hint
            if st.get("student_check") and isinstance(st["student_check"], dict):
                entry["_check"] = st["student_check"]
            steps.append(entry)
            formula = _clean(st.get("formula"))
            if formula:
                steps.append({"t": "formula", "text": formula})
            if entry.get("_check"):
                steps.append({"t": "check", "check": entry.pop("_check")})
        if not steps:
            for key in ("phenomenon", "investigation", "observation", "interpretation", "conclusion"):
                v = _clean(act.get(key))
                if v:
                    steps.append({"t": "text", "text": v, "label": "", "speech": v if lang == "en" else ""})
        if not steps:
            continue
        spec = act.get("lab_spec") if isinstance(act.get("lab_spec"), dict) else {}
        if spec.get("kind") == "POWER_EXPLORER":
            d = power_draw_step(spec)
            if d:
                steps.insert(min(1, len(steps)), d)
        explicit = act.get("draw_steps")
        if isinstance(explicit, list):   # solids/geometry lessons supply their own pen actions
            for k, d in enumerate(explicit):
                if isinstance(d, dict) and d.get("draw"):
                    steps.insert(min(1 + k, len(steps)), {"t": "draw", **d})
        page = act.get("source_page")
        scenes.append({"id": str(act.get("concept_id") or ""), "page": str(page or ""),
                       "title": apply_terminology(_clean(act.get("title")), lesson_title),
                       "start_mode": "single", "steps": steps})
    return scenes


def scene_board_modes(scene: dict) -> List[str]:
    """Board mode sequence implied by the actions (single until a drawing is needed)."""
    out, mode = [], scene.get("start_mode", "single")
    out.append(mode)
    for s in scene.get("steps", []):
        if s.get("t") == "draw" and mode != "dual":
            mode = "dual"
            out.append(mode)
        elif s.get("t") == "mode" and s.get("mode") != mode:
            mode = s["mode"]
            out.append(mode)
    return out


# ---------------------------------------------------------- solution hints
# Short "how to" words that help a student see what the step is doing. They name the
# operation that is already in the verified step; they never add mathematics.
_HINT_RULES = [
    ("substitute", r"substitut|replac|plug|remplac|substitu|عوّ?ض|تعويض|نعوض|بدل", {
        "en": "Substitute: put the values in place of the letters.",
        "fr": "Remplace : mets les valeurs à la place des lettres.",
        "ar": "عوّض: ضع القيم مكان الرموز."}),
    ("add_exp", r"add the exponents|add exponents|\badd\b.*exponent|additionn\w* les exposants|نجمع الأسس|جمع الأسس|أضف الأسس", {
        "en": "Same base: keep the base and add the exponents.",
        "fr": "Même base : garde la base et additionne les exposants.",
        "ar": "الأساس نفسه: نُبقي الأساس ونجمع الأسس."}),
    ("sub_exp", r"subtract the exponents|subtract exponents|soustr\w* les exposants|نطرح الأسس|طرح الأسس", {
        "en": "Same base: keep the base and subtract the exponents.",
        "fr": "Même base : garde la base et soustrais les exposants.",
        "ar": "الأساس نفسه: نُبقي الأساس ونطرح الأسس."}),
    ("mul_exp", r"multiply the exponents|multiply exponents|multipli\w* les exposants|نضرب الأسس|ضرب الأسس", {
        "en": "Power of a power: multiply the exponents.",
        "fr": "Puissance d'une puissance : multiplie les exposants.",
        "ar": "قوة قوة: نضرب الأسس."}),
    ("divide", r"\bdivid|\bquotient|\bdivis|نقسم|قسمة|اقسم", {
        "en": "Divide: split the first number by the second.",
        "fr": "Divise : partage le premier nombre par le second.",
        "ar": "اقسم: قسّم العدد الأول على الثاني."}),
    ("multiply", r"\bmultipl|\bproduct\b|\bproduit|نضرب|ضرب|اضرب", {
        "en": "Multiply the numbers one after another.",
        "fr": "Multiplie les nombres l'un après l'autre.",
        "ar": "اضرب الأعداد واحدًا بعد الآخر."}),
    ("simplify", r"simplif|reduce|calculate|compute|calcul|نبسّ?ط|تبسيط|نحسب|احسب", {
        "en": "Calculate: do the operations to get one number.",
        "fr": "Calcule : effectue les opérations pour obtenir un seul nombre.",
        "ar": "احسب: نفّذ العمليات لنحصل على عدد واحد."}),
    ("verify", r"verif|check|vérif|نتحقق|تحقق", {
        "en": "Check: put the answer back and see that it works.",
        "fr": "Vérifie : remets le résultat et regarde si ça marche.",
        "ar": "تحقّق: أعد وضع الجواب وتأكد أنه صحيح."}),
]
_TAG_LABEL = {
    "given": {"en": "Given", "fr": "Données", "ar": "المعطيات"},
    "required": {"en": "Required", "fr": "À trouver", "ar": "المطلوب"},
    "rule": {"en": "Rule", "fr": "Règle", "ar": "القاعدة"},
    "substitution": {"en": "Substitution", "fr": "Substitution", "ar": "التعويض"},
    "calculation": {"en": "Calculation", "fr": "Calcul", "ar": "الحساب"},
    "verification": {"en": "Verification", "fr": "Vérification", "ar": "التحقق"},
}


def step_hint(text: str, lang: str) -> str:
    t = str(text or "")
    for _name, rx, by_lang in _HINT_RULES:
        if re.search(rx, t, re.I):
            return by_lang.get(lang) or by_lang["en"]
    return ""


def build_exercise_scenes(exercises: List[dict], lang: str, lesson_title: str = "") -> List[dict]:
    """Every exercise becomes one scene: the statement, then the worked solution step by
    step (tag as label + a short how-to hint), then the final answer. An exercise whose
    verified solution is not available shows its statement and says so — it is never
    filled with an invented solution."""
    from scripts.nabil_factory.factory.pedagogical_gate import solution_tags
    ui = UI_ALL.get(lang, UI_ALL["en"])
    scenes: List[dict] = []
    for ex in exercises or []:
        num = str(ex.get("number") or "").strip()
        problem = apply_terminology(_clean(ex.get("exact_source_prompt")), lesson_title)
        if not (num and problem):
            continue
        steps: List[dict] = [{"t": "text", "text": problem,
                              "label": {"ar": "المسألة", "fr": "Énoncé", "en": "Problem"}.get(lang, "Problem"),
                              "speech": problem if lang == "en" else ""}]
        sol = ex.get("_pre_solved_solution")
        if ex.get("solution_status") == "SOLVED" and isinstance(sol, dict):
            for i, raw in enumerate(sol.get("steps") or [], 1):
                text = apply_terminology(_clean(raw), lesson_title)
                if not text:
                    continue
                tag = solution_tags(str(raw))
                label = _TAG_LABEL[tag][lang] if tag in _TAG_LABEL else f"{ {'ar': 'الخطوة', 'fr': 'Étape'}.get(lang, 'Step') } {i}"
                entry = {"t": "text", "text": text, "label": label, "speech": text if lang == "en" else ""}
                hint = step_hint(text, lang)
                if hint:
                    entry["hint"] = hint
                steps.append(entry)
            final = apply_terminology(_clean(sol.get("final_answer")), lesson_title)
            if final:
                steps.append({"t": "text", "text": final,
                              "label": {"ar": "الجواب النهائي", "fr": "Réponse finale", "en": "Final answer"}.get(lang, "Final answer"),
                              "speech": final if lang == "en" else ""})
        else:
            steps.append({"t": "text", "text": ui["no_solution"], "label": "", "speech": ""})
        scenes.append({"id": f"EX-{num}", "page": str(ex.get("source_page") or ex.get("page") or ""), "title": f"{ui['exercise']} {num}", "exercise": num,
                       "solved": ex.get("solution_status") == "SOLVED", "start_mode": "single", "steps": steps})
    return scenes


# ------------------------------------------------------------------- rendering
def _read(name: str) -> str:
    return (_ASSETS / name).read_text(encoding="utf-8")


def hand_payload() -> str:
    b64 = _read("golden_v6_hand_png_b64.txt").strip()
    if hashlib.sha256(b64.encode()).hexdigest() != HAND_SHA256:
        raise RuntimeError("GOLDEN_V6_HAND_ASSET_MODIFIED")
    return b64


def render_golden_v6_board(title: str, scenes: List[dict], lang_code: str,
                           golden_spec: dict | None = None, contract: str = "",
                           mode: str = "lesson", titles: Dict[str, str] | None = None,
                           meta: Dict[str, Any] | None = None) -> str:
    lang = lang_code if lang_code in UI_ALL else "en"
    if not scenes:
        return ""
    from scripts.nabil_factory.factory.student_clean_gate import audit_student_text
    _sc = audit_student_text(scenes)
    if _sc["verdict"] != "PASS":
        raise RuntimeError("STUDENT_TEXT_DIRTY: " + repr(_sc["hits"][:3]))
    if (not golden_spec or not golden_spec.get("sections")) and mode != "exercises":
        raise RuntimeError("V18_GOLDEN_CARD_SPEC_EMPTY")
    golden_spec = golden_spec or {}
    titles = dict(titles or {})
    titles.setdefault(lang, title)
    titles.setdefault("en", title)
    ui = UI_ALL[lang]
    data = {
        "contract": V6_BOARD_CONTRACT, "lang": lang, "title": title, "mode": mode,
        "titles": titles, "scenes": scenes,
        "exercises": [{"n": sc["exercise"], "scene": i, "solved": bool(sc.get("solved"))}
                      for i, sc in enumerate(scenes) if sc.get("exercise")], "default_speed": DEFAULT_SPEED,
        "ui_all": UI_ALL, "golden": dict(golden_spec, avatar_src=""),
        "avatar_base64": _read("nabil_avatar_b64.txt").strip(),
        "meta": {k: str(v)[:(400 if k == "status_text" else 80)] for k, v in (meta or {}).items()
                 if k in ("lesson_id", "grade", "subject", "language", "completeness", "status_text")},
    }
    from scripts.nabil_factory.cards.lesson_plan import build_plan_data
    data["plan"] = build_plan_data(title, scenes, golden_spec, mode, meta)
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\u0021--")
    engine_b64 = base64.b64encode(_read("v18_golden_cards_engine.js").encode("utf-8")).decode("ascii")
    h = html.escape
    t_en = h(titles.get("en") or title)
    t_fr = h(titles.get("fr") or "")
    # The factory's own page text normalisation must not rewrite engine JS.
    return f'''
<section id="nabilWholeLessonSmartLab" class="nabil-whole-lesson-smart-lab"
 data-whole-lesson-smart-lab="true" data-renderer-contract="{h(contract)}"
 data-nabil-v18-board="{V6_BOARD_CONTRACT}" data-nabil-golden-v6="true" data-v18-mode="{h(mode)}"
 data-concept-count="{len(scenes)}" data-board-mode="single" lang="{lang}">
<style>{_read("golden_v6.css")}</style>
<div class="nb-open" id="nbOpen">
 <img id="nbAvatarOpen" alt="NABIL AI" role="button" tabindex="0">
 <div class="nb-brand" dir="rtl">منصة الأستاذ النبيل</div>
 <div class="nb-title-en" dir="ltr" id="nbOpenTitleEn">{t_en}</div>
 {f'<div class="nb-title-fr" dir="ltr" id="nbOpenTitleFr">{t_fr}</div>' if t_fr and t_fr != t_en else ''}
 <button type="button" class="nb-start" id="nbStart" data-nb-l="start">{h(ui["start"])}</button>
 <div class="nb-hint" data-nb-l="voice_hint">{h(ui["voice_hint"])}</div>
</div>
<div class="nb-stage" id="nbStage">
 <div class="nb-head"><h2 id="nbHeadTitle"></h2><span class="nb-prog" id="nbProg"></span>
  <span><span id="nbLangs"><button type="button" class="nb-hbtn nb-lg" data-l="ar">عربي</button><button type="button" class="nb-hbtn nb-lg" data-l="en">English</button><button type="button" class="nb-hbtn nb-lg" data-l="fr">Français</button></span> <button type="button" id="nbSolveBtn" class="nb-solvebtn" aria-haspopup="dialog">🧮 حل التمارين | Solve Exercise</button><button type="button" id="nbFullscreen" data-nb-l="fullscreen" class="nb-hbtn">{h(ui["fullscreen"])}</button>
  <button type="button" id="nbExit" data-nb-l="exit" class="nb-hbtn">{h(ui["exit"])}</button></span></div>
 <div class="nb-badge" id="nbBadge" role="note" hidden></div>
 <div class="nb-voice-note" id="nbVoiceNote"><span>{h(ui["voice_hint"])}</span><button type="button" data-nb-l="enable_voice">{h(ui["enable_voice"])}</button></div>
 <section class="nb-workspace" id="nbWorkspace" data-board-mode="single">
  <aside class="nb-diagram" id="nbDiagram"><svg id="nbBoard" viewBox="170 105 610 540" preserveAspectRatio="xMidYMid meet"><g id="nbInk"></g></svg></aside>
  <article class="nb-writing" id="nbWriting" aria-live="polite"></article>
 </section>
 <div class="nb-golden" id="nbGolden" data-v18-final-stage="true"></div>
 <nav class="nb-ctl" aria-label="lesson controls">
  <button type="button" id="nabilWholePrev" data-nb-l="prev">{h(ui["prev"])}</button>
  <button type="button" id="nabilWholePlay" data-nb-l="play">{h(ui["play"])}</button>
  <button type="button" id="nabilWholeNext" data-nb-l="next">{h(ui["next"])}</button>
  <button type="button" id="nabilWholeRestart" data-nb-l="replay">{h(ui["replay"])}</button>
  <button type="button" id="nabilWholeVoice" class="voice" data-nb-l="voice_on" aria-pressed="true">{h(ui["voice_on"])}</button>
  <button type="button" id="nbRepeatStep" class="nb-solve-only" data-nb-l="repeat_step">{h(ui["repeat_step"])}</button>
  <button type="button" id="nbBackToLesson" class="nb-solve-only" data-nb-l="back_to_lesson">{h(ui["back_to_lesson"])}</button>
  <button type="button" id="nbToolsToggle" aria-expanded="false" aria-controls="nbTools" data-nb-l="tools">{h(ui["tools"])}</button>
  <span class="nb-status" id="nbStatus"></span>
 </nav>
 <div class="nb-ctl nb-tools" id="nbTools" hidden>
  <select id="nbSpeed" aria-label="speed"><option value="0.5">0.5×</option><option value="0.7" selected>0.7×</option><option value="1">1×</option><option value="1.25">1.25×</option></select>
  <button type="button" id="nbArVoice" data-nb-l="ar_voice" aria-pressed="false">{h(ui["ar_voice"])}</button>
  {('<label class="nb-exlab"><span data-nb-l="exercise">' + h(ui["exercise"]) + '</span> <select id="nbExercise" aria-label="' + h(ui["pick_exercise"]) + '"><option value="" disabled selected>' + h(ui["pick_exercise"]) + '</option>' + ''.join('<option value="' + str(e["scene"]) + '">' + h(str(e["n"])) + ('' if e["solved"] else ' …') + '</option>' for e in data["exercises"]) + '</select></label>') if data["exercises"] else ''}
  <button type="button" class="nb-lost-btn" id="nbLost" data-nb-l="lost">{h(ui["lost"])}</button>
  <button type="button" class="nb-planbtn" data-nb-plan="open">📄 تحضير الدرس | Lesson Plan | Fiche de préparation</button>
 </div>
</div>
<div class="nb-modal" id="nbPlanModal" hidden role="dialog" aria-modal="true" aria-label="Lesson plan">
 <div class="nb-modal-box">
  <div class="nb-modal-bar">
   <label>🌐 <select id="nbPlanLang"><option value="ar">العربية</option><option value="en">English</option><option value="fr">Français</option></select></label>
   <label><span id="nbPlanMinLab">⏱</span> <input id="nbPlanMin" type="number" min="20" max="180" step="5" value="45" style="width:70px"> min</label>
   <label><span id="nbPlanSesLab">#</span> <input id="nbPlanSes" type="number" min="1" max="10" step="1" value="1" style="width:56px"></label>
   <button type="button" id="nbPlanGen">⟳</button>
   <button type="button" id="nbPlanPrint">🖨</button>
   <button type="button" id="nbPlanDocx">⬇ Word (.docx)</button>
   <button type="button" id="nbPlanClose">✕</button>
  </div>
  <div class="nb-plan-note" id="nbPlanNote"></div>
  <div id="nbPlanDoc" class="nb-plan-doc" contenteditable="true" spellcheck="false"></div>
 </div>
</div>
<img id="teacherHand" alt="" aria-hidden="true">
<script type="application/json" id="nabilV6Data">{data_json}</script>
<script type="text/plain" id="nabilV6HandPayload">{hand_payload()}</script>
<script type="text/plain" id="nabilV18CardEnginePayload">{engine_b64}</script>
<script data-nabil-no-translate="1">
(() => {{
 const payload=document.getElementById('nabilV18CardEnginePayload');
 const bytes=Uint8Array.from(atob(payload.textContent.trim()),c=>c.charCodeAt(0));
 const script=document.createElement('script');
 script.textContent=new TextDecoder().decode(bytes);
 payload.after(script);
 if(typeof window.NABILScientificCards?.fromLesson!=='function'){{
   throw new Error('V18_GOLDEN_CARD_ENGINE_BOOTSTRAP_FAILED');
 }}
 window.__NABIL_V18_CARDS=window.NABILScientificCards;
}})();
</script>
<script data-nabil-no-translate="1">{_read("golden_v6_engine.js")}</script>
<script data-nabil-no-translate="1">{_read("golden_v6_plan.js")}</script>
<script data-nabil-no-translate="1">{_read("golden_v6_solver.js")}</script>
</section>'''
