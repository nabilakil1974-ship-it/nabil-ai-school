"""Serve a Golden lesson on the approved NABIL Golden V6 board.

Pure adapter: the Golden artifact text (already verified, zero-AI) is parsed into scenes
and handed to the static V6 engine. Nothing is invented: every board line is a line of
the artifact. Any failure returns None so the caller can fall back to the older page.
"""
from __future__ import annotations

import html
import re
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


def build_v6_page(entry: Dict[str, Any], text: str, meta: Dict[str, Any]) -> Optional[str]:
    try:
        from scripts.nabil_factory.cards.golden_v6 import render_golden_v6_board
        lang = _lang_code(entry, meta, text)
        parsed = parse_golden_text(text, lang)
        scenes: List[Dict[str, Any]] = []
        for sc in parsed["scenes"]:
            steps = []
            for i, ln in enumerate(sc["lines"]):
                st = {"t": "text", "text": ln, "label": sc["title"] if i == 0 else "",
                      "speech": ln if lang == "en" else ""}
                if lang == "ar":
                    st["ar"] = ln
                steps.append(st)
            if not steps and sc["title"]:
                steps.append({"t": "text", "text": sc["title"], "label": "", "speech": sc["title"] if lang == "en" else ""})
            if steps:
                scenes.append({"id": sc["id"], "page": "", "title": sc["title"], "start_mode": "single", "steps": steps})
        if not scenes:
            return None
        label = {"ar": "الخلاصة:", "fr": "Résumé :", "en": "Summary:"}[lang]
        spec = {"sections": [{"label": label, "items": parsed["summary"] or [entry.get("title", "")]}],
                "key_results": parsed["summary"][:3], "title": entry.get("title", "")}
        title = str(entry.get("title") or "")
        page = render_golden_v6_board(title, scenes, lang, golden_spec=spec,
                                      contract="golden-artifact-v6", mode="lesson", titles={lang: title},
                                      meta={"lesson_id": entry.get("lesson_id", ""), "source": "golden-artifact"})
        lang_attr = "ar" if lang == "ar" else lang
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
