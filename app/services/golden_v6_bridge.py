"""Serve a Golden lesson on the approved NABIL Golden V6 board.

Pure adapter: the Golden artifact text (already verified, zero-AI) is parsed into scenes
and handed to the static V6 engine. Nothing is invented: every board line is a line of
the artifact. Any failure returns None so the caller can fall back to the older page.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

_ARABIC = re.compile(r"[؀-ۿ]")
_HEAD = re.compile(r"^(CONCEPT_ID|EXERCISE_ID|LAB_KEY):")
_SKIP = ("GOLDEN SOURCE ARTIFACT", "This repository artifact", "Drive file ID", "START OF STUDENT",
         "END OF STUDENT", "NABIL_INTERNAL")


_EMBED_HEAD_JS = """<script>
/* inside the student shell the parent page owns full screen; the board must not make the
   iframe itself the fullscreen element (that would hide the parent's back/fullscreen bar). */
(function(){if(new URLSearchParams(location.search).get("embedded")!=="1")return;
  var ok=function(){return Promise.resolve()};
  Element.prototype.requestFullscreen=ok;Element.prototype.webkitRequestFullscreen=ok;})();
</script>"""

_EMBED_JS = """<script>
/* embedded in the student shell: start the lesson at once when allowed, else the single
   start button of the board stays visible. No other UI is added. */
(function(){
  var q=new URLSearchParams(location.search);
  if(q.get("embedded")!=="1")return;
  var st=document.createElement("style");
  st.textContent="#nbFullscreen{display:none!important}"+(q.get("teacher")==="1"?"":"[data-nb-plan]{display:none!important}");
  document.head.appendChild(st);
  document.addEventListener("click",function(e){var x=e.target.closest&&e.target.closest("#nbExit");
    if(x){e.preventDefault();e.stopImmediatePropagation();parent.postMessage({type:"nabil:back"},"*")}},true);
  var go=function(){var b=document.getElementById("nbStart");if(b&&b.offsetParent!==null){b.click();return true}return false};
  var n=0,t=setInterval(function(){n++;if(q.get("autostart")==="1"&&go()||n>40)clearInterval(t)},150);
  window.addEventListener("message",function(e){if(e.data&&e.data.type==="nabil:autostart")go()});
})();
</script>"""


def _lang_code(entry: Dict[str, Any], meta: Dict[str, Any], text: str) -> str:
    raw = str(meta.get("language") or entry.get("language") or "")
    m = re.search(r"^LANGUAGE:\s*(.+)$", text, re.M)
    raw = (m.group(1) if m else raw).strip().lower()
    if raw.startswith(("en", "eng")):
        return "en"
    if raw.startswith(("fr", "fra", "fran")):
        return "fr"
    return "ar"


def parse_golden_text(text: str, lang: str) -> Dict[str, Any]:
    body = text.split("START OF STUDENT EXPERIENCE", 1)[-1].split("END OF STUDENT EXPERIENCE", 1)[0]
    summary: List[str] = []
    scenes: List[Dict[str, Any]] = []
    cur: Optional[Dict[str, Any]] = None
    in_summary = False
    pending_id = ""
    seen_block = False
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(("CONCEPT_ID:", "EXERCISE_ID:")):
            seen_block = True
        if not seen_block and lang != "ar":
            continue  # opening narration is Arabic dialect: Arabic boards only
        if line.startswith("GOLDEN SUMMARY"):
            in_summary, cur = True, None
            continue
        if in_summary:
            summary.append(line)
            continue
        if line.startswith("CONCEPT_ID:") or line.startswith("EXERCISE_ID:"):
            pending_id = line.split(":", 1)[1].strip()
            cur = None
            continue
        if line.startswith("LAB_KEY:"):
            continue
        if line.startswith("MISCONCEPTION CLINIC"):
            cur = {"id": "clinic", "title": "Misconception clinic" if lang != "ar" else "عيادة الأخطاء", "lines": []}
            scenes.append(cur)
            continue
        if line.startswith("NABIL:") or line.startswith("“") or line.startswith("[") and "]" in line:
            # opening narration is in Arabic dialect: shown only on Arabic boards
            if lang != "ar":
                continue
            if cur is None or cur.get("id") != "opening":
                cur = {"id": "opening", "title": "", "lines": []}
                scenes.append(cur)
            t = line.replace("NABIL:", "").strip(" “”")
            if t:
                cur["lines"].append(t)
            continue
        if cur is None or pending_id:
            cur = {"id": pending_id or f"s{len(scenes) + 1}", "title": line, "lines": []}
            pending_id = ""
            scenes.append(cur)
            continue
        if lang != "ar" and _ARABIC.search(line) and cur.get("id") == "opening":
            continue
        cur["lines"].append(line)
    return {"scenes": scenes, "summary": summary}


MASTER_DIR = Path(__file__).resolve().parents[2] / "data" / "golden_masters"

_KIND = {
    "ask": {"ar": "فكّر", "en": "Think", "fr": "Réfléchis"},
    "notice": {"ar": "لاحظ", "en": "Notice", "fr": "Observe"},
    "explain": {"ar": "اشرح", "en": "Explain", "fr": "Explique"},
    "why": {"ar": "لماذا؟", "en": "Why?", "fr": "Pourquoi ?"},
    "worked": {"ar": "مثال محلول", "en": "Worked example", "fr": "Exemple résolu"},
    "live": {"ar": "قراءة حية", "en": "Live reading", "fr": "Lecture en direct"},
    "your_turn": {"ar": "دورك", "en": "Your turn", "fr": "À toi"},
    "check": {"ar": "تحقّق", "en": "Check", "fr": "Vérifie"},
    "micro_check": {"ar": "تحقّق سريع", "en": "Quick check", "fr": "Vérification rapide"},
}
_TXT = {
    "status": {"ar": "حالة المحتوى", "en": "Content status", "fr": "État du contenu"},
    "problem": {"ar": "المسألة", "en": "Problem", "fr": "Énoncé"},
    "given": {"ar": "المعطيات", "en": "Given", "fr": "Données"},
    "answer": {"ar": "الجواب", "en": "Answer", "fr": "Réponse"},
    "verification": {"ar": "التحقق", "en": "Check", "fr": "Vérification"},
    "fact": {"ar": "تذكّر", "en": "Remember", "fr": "Retiens"},
    "ex": {"ar": "تمرين", "en": "Exercise", "fr": "Exercice"},
}
_MISSING = {
    "drawings": {"ar": "رسوم الدرس", "en": "lesson drawings", "fr": "les dessins de la leçon"},
    "solutions": {"ar": "حلول التمارين المصدّقة", "en": "verified exercise solutions", "fr": "les solutions d'exercices vérifiées"},
    "labs": {"ar": "المختبرات التفاعلية", "en": "interactive labs", "fr": "les laboratoires interactifs"},
    "sliders": {"ar": "المنزلقات التفاعلية للمختبر", "en": "the lab's interactive sliders", "fr": "les curseurs interactifs du laboratoire"},
    "ar_only": {"ar": "حلول التمارين متوفرة بالعربية فقط", "en": "exercise solutions exist in Arabic only", "fr": "les solutions d'exercices n'existent qu'en arabe"},
}


def _status_text(lang: str, missing: List[str], source: str) -> str:
    items = "، ".join(_MISSING[m][lang] for m in missing) if lang == "ar" else "; ".join(_MISSING[m][lang] for m in missing)
    head = {"ar": "نسخة جزئية من الدرس الذهبي (المصدر: %s). غير متوفر بعد: %s.",
            "en": "Partial version of the Golden lesson (source: %s). Not yet available: %s.",
            "fr": "Version partielle de la leçon Golden (source : %s). Pas encore disponible : %s."}[lang]
    return head % (source, items)


def load_master(lesson_id: str) -> Optional[Dict[str, Any]]:
    path = MASTER_DIR / f"{lesson_id}.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logging_exc = __import__("logging").getLogger(__name__)
        logging_exc.exception("GOLDEN_MASTER_READ_FAILED %s", lesson_id)
        return None


def _step(text: str, label: str, lang: str, speech: Optional[str] = None, speech_lang: Optional[str] = None) -> Dict[str, Any]:
    st: Dict[str, Any] = {"t": "text", "text": text, "label": label, "speech": speech if speech is not None else text}
    sl = speech_lang or (lang if lang != "en" else None)
    if sl:
        st["speech_lang"] = sl
    if lang == "ar" or speech_lang == "ar":
        st["ar"] = text
    return st


def scenes_from_master(m: Dict[str, Any], lang: str) -> Dict[str, Any]:
    vb = m.get("vb") or [640, 450]
    scenes: List[Dict[str, Any]] = []
    shown_any_svg = False
    for sc in m.get("scenes", []):
        n = sc["no"]
        steps: List[Dict[str, Any]] = []
        if sc.get("svg"):
            steps.append({"t": "draw", "draw": "svgScene", "args": {"svg": sc["svg"], "vb": vb, "show": []}})
            shown_any_svg = True
        for st in [x for x in m.get("steps", []) if x["scene_index"] == n]:
            kind = _KIND.get(st.get("kind"), {}).get(lang, "")
            txt = (st.get("text") or {}).get(lang) or ""
            spk = (st.get("speech") or {}).get(lang) or txt
            if sc.get("svg") and st.get("show_ids"):
                steps.append({"t": "draw", "draw": "svgScene", "clear": False,
                              "args": {"show": [i for i in st["show_ids"] if i]}})
            if txt:
                steps.append(_step(txt, kind, lang, speech=(txt + (". " + spk if spk and spk != txt else ""))))
            if st.get("formula"):
                steps.append({"t": "formula", "text": st["formula"]})
            fact = (st.get("fact") or {}).get(lang) if isinstance(st.get("fact"), dict) else ""
            if fact:
                steps.append(_step(fact, _TXT["fact"][lang], lang))
        if steps:
            title = (sc.get("title") or {}).get(lang) or ""
            scenes.append({"id": f"master-{n}", "page": "", "title": title, "start_mode": "single", "steps": steps})
    cc = m.get("cross_check") or {}
    if cc.get("prompt"):
        steps = [_step(cc["prompt"][lang], _KIND["check"][lang], lang)]
        for i, o in enumerate(cc.get("options") or []):
            steps.append(_step("%s) %s" % ("ABC"[i] if i < 3 else i + 1, o[lang]), "", lang))
        ci = int(cc.get("correct") or 0)
        steps.append(_step("%s) — %s" % ("ABC"[ci] if ci < 3 else ci + 1, (cc.get("why") or {}).get(lang, "")), _TXT["answer"][lang], lang))
        scenes.append({"id": "cross", "page": "", "title": _KIND["check"][lang], "start_mode": "single", "steps": steps})
    nex = 0
    for ve in (m.get("golden_summary") or {}).get("verified_examples") or []:
        num = str(ve.get("exercise_id", "")).split("-")[-1]
        steps = [_step(ve.get("question", ""), _TXT["problem"][lang] + " (p.%s)" % ve.get("source_page", "?"), "ar", speech_lang="ar")]
        for g in ve.get("given") or []:
            steps.append(_step(g, _TXT["given"][lang] if g is ve["given"][0] else "", "ar", speech_lang="ar"))
        if ve.get("visual_svg"):
            steps.append({"t": "draw", "draw": "svgScene", "args": {"svg": ve["visual_svg"], "vb": [760, 500], "show": [
                i for i in re.findall(r'id="([^"]+)"', ve["visual_svg"])]}})
        for i, sp in enumerate(ve.get("steps") or []):
            e = _step(sp.get("work", ""), "%d" % (i + 1), "ar", speech_lang="ar")
            if sp.get("why"):
                e["hint"] = sp["why"]
            steps.append(e)
        if ve.get("final_answer"):
            steps.append(_step(ve["final_answer"], _TXT["answer"][lang], "ar", speech_lang="ar"))
        if ve.get("verification"):
            steps.append(_step(ve["verification"], _TXT["verification"][lang], "ar", speech_lang="ar"))
        scenes.append({"id": ve.get("exercise_id", ""), "page": str(ve.get("source_page", "")), "exercise": "%s (p.%s)" % (num, ve.get("source_page", "?")),
                       "solved": True, "title": "%s %s" % (_TXT["ex"][lang], num), "start_mode": "single", "steps": steps})
        nex += 1
    gs = m.get("golden_summary") or {}
    items = [x for x in ((gs.get("flow") or {}).get(lang), (gs.get("takeaway") or {}).get(lang)) if x]
    spec = {"sections": [{"label": {"ar": "الخلاصة:", "fr": "Résumé :", "en": "Summary:"}[lang], "items": items or [""]}],
            "key_results": items[-1:], "title": (m.get("title") or {}).get(lang, "")}
    missing = ["sliders"] + (["ar_only"] if nex and lang != "ar" else [])
    return {"scenes": scenes, "spec": spec, "missing": missing, "has_drawings": shown_any_svg, "exercise_solutions": nex}


def build_v6_page(entry: Dict[str, Any], text: str, meta: Dict[str, Any]) -> Optional[str]:
    try:
        from scripts.nabil_factory.cards.golden_v6 import render_golden_v6_board
        lang = _lang_code(entry, meta, text)
        master = load_master(str(entry.get("lesson_id") or ""))
        title = str(entry.get("title") or "")
        if master:
            built = scenes_from_master(master, lang)
            scenes, spec, missing, source = built["scenes"], built["spec"], built["missing"], "Drive master lab"
            title = (master.get("title") or {}).get(lang) or title
        else:
            parsed = parse_golden_text(text, lang)
            scenes = []
            for sc in parsed["scenes"]:
                steps = []
                for i, ln in enumerate(sc["lines"]):
                    st = {"t": "text", "text": ln, "label": sc["title"] if i == 0 else "",
                          "speech": ln if lang == "en" else ""}
                    if lang == "ar":
                        st["ar"] = ln
                    steps.append(st)
                if not steps and sc["title"]:
                    steps.append({"t": "text", "text": sc["title"], "label": "",
                                  "speech": sc["title"] if lang == "en" else ""})
                if steps:
                    scenes.append({"id": sc["id"], "page": "", "title": sc["title"], "start_mode": "single", "steps": steps})
            label = {"ar": "الخلاصة:", "fr": "Résumé :", "en": "Summary:"}[lang]
            spec = {"sections": [{"label": label, "items": parsed["summary"] or [title]}],
                    "key_results": parsed["summary"][:3], "title": title}
            missing, source = ["drawings", "solutions", "labs"], "Golden text artifact"
        if not scenes:
            return None
        # honest status: the lesson is never presented as complete when parts are missing (persistent badge)
        board_meta = {"lesson_id": entry.get("lesson_id", ""), "grade": entry.get("grade", ""),
                      "subject": entry.get("subject", ""), "language": entry.get("language", ""),
                      "completeness": "partial:" + ",".join(missing),
                      "status_text": _status_text(lang, missing, source)}
        page = render_golden_v6_board(title, scenes, lang, golden_spec=spec, contract="golden-artifact-v6",
                                      mode="lesson", titles={lang: title}, meta=board_meta)
        lang_attr = lang
        return (
            '<!doctype html><html lang="' + lang_attr + '" dir="' + ("rtl" if lang == "ar" else "ltr") + '"><head>'
            '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            '<title>' + html.escape(title) + '</title>' + _EMBED_HEAD_JS +
            '<style>html,body{margin:0;padding:0;height:100%;overflow-x:hidden;background:#eaf0f6}</style></head><body>'
            + page + _EMBED_JS + '</body></html>'
        )
    except Exception:  # never break the route: caller falls back to the older classroom
        import logging
        logging.getLogger(__name__).exception("GOLDEN_V6_RENDER_FAILED")
        return None
