#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NABIL AI — Full-Coverage Quiz Engine
Add-on module imported by the lesson factory.
"""
import html
import json
import os
from typing import List, Dict, Any, Optional
from scripts.nabil_i18n import t as _t

DEFAULT_PASS_THRESHOLD_FRACTION = 0.70

def _pass_threshold(value: Optional[float] = None) -> float:
    raw = value if value is not None else os.getenv(
        "NABIL_QUIZ_PASS_THRESHOLD", str(DEFAULT_PASS_THRESHOLD_FRACTION))
    try:
        threshold = float(raw)
    except (TypeError, ValueError):
        raise RuntimeError(f"QUIZ_THRESHOLD_INVALID:{raw!r}")
    if not (0.0 < threshold <= 1.0):
        raise RuntimeError(f"QUIZ_THRESHOLD_OUT_OF_RANGE:{threshold}")
    return threshold

def build_full_quiz_items(activities_theory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build one item per gradable activity/concept. No arbitrary cap."""
    if not activities_theory:
        return []
    items = []
    for act in activities_theory:
        q = act.get("student_question")
        if not isinstance(q, dict):
            continue
        options = q.get("options")
        if not isinstance(options, list) or len(options) < 2 or "correct_index" not in q:
            continue
        try:
            correct_index = int(q["correct_index"])
        except (TypeError, ValueError):
            continue
        if not 0 <= correct_index < len(options):
            continue
        question = str(q.get("q") or "").strip()
        if not question:
            continue
        evidence = act.get("evidence") if isinstance(act.get("evidence"), dict) else {}
        items.append({
            "id": len(items) + 1,
            "concept_id": act.get("concept_id") or act.get("activity_num"),
            "source_page": act.get("source_page") or evidence.get("source_page"),
            "question": question,
            "options": [str(x) for x in options],
            "correct_index": correct_index,
            "explanation": str(q.get("explanation") or act.get("conclusion") or "").strip(),
            "evidence_quote": str(
                evidence.get("quote") or act.get("evidence_quote") or act.get("source_quote") or ""
            ).strip(),
        })
    return items

def render_quiz_html(
        quiz_items: List[Dict[str, Any]],
        lang_code: str,
        pass_threshold: Optional[float] = None) -> str:
    """Render full quiz, score, configurable threshold, and grounded explanation."""
    if not quiz_items:
        return ""
    threshold = _pass_threshold(pass_threshold)
    total = len(quiz_items)
    pass_score = max(1, int(total * threshold + 0.999999999))

    items_html = []
    explanations = {}
    for item in quiz_items:
        qid = int(item["id"])
        correct_index = int(item["correct_index"])
        opts = []
        for i, opt in enumerate(item["options"]):
            flag = "true" if i == correct_index else "false"
            opts.append(
                f'<button type="button" onclick="quizAnswer(this,{qid},{flag})" '
                f'class="q-opt" data-qid="{qid}">{html.escape(str(opt))}</button>'
            )
        page_note = ""
        if item.get("source_page"):
            page_note = (
                ' <span style="font-size:11px;color:#bed4e5;">(p. '
                + html.escape(str(item["source_page"])) + ')</span>'
            )
        concept_id = html.escape(str(item.get("concept_id") or ""))
        items_html.append(
            '<div class="quiz-item nabil-reference-concept" data-qid="' + str(qid) +
            '" data-concept-id="' + concept_id + '" style="margin-bottom:16px;padding:12px;">'
            '<div style="font-weight:700;margin-bottom:8px;">' +
            html.escape(_t(lang_code, "question_label")) + ' ' + str(qid) + ': ' +
            html.escape(str(item["question"])) + page_note + '</div>'
            '<div style="display:flex;gap:8px;flex-wrap:wrap;">' + ''.join(opts) + '</div>'
            '<div class="quiz-fb" data-qid="' + str(qid) +
            '" style="margin-top:8px;font-size:13px;font-weight:700;display:none;"></div>'
            '<div class="quiz-explanation" data-qid="' + str(qid) +
            '" style="margin-top:8px;display:none;line-height:1.55;"></div></div>'
        )
        explanations[str(qid)] = {
            "explanation": str(item.get("explanation") or ""),
            "evidence_quote": str(item.get("evidence_quote") or ""),
        }

    strings = {
        "correct": _t(lang_code, "ws_correct"),
        "incorrect": _t(lang_code, "ws_incorrect"),
        "result_prefix": _t(lang_code, "quiz_result_prefix"),
        "pass": _t(lang_code, "quiz_pass"),
        "retry": _t(lang_code, "quiz_retry"),
        "question": _t(lang_code, "question_label"),
        "remaining": {"ar": "متبقية", "fr": "restantes", "en": "remaining"}.get(lang_code, "remaining"),
    }
    exp_json = json.dumps(explanations, ensure_ascii=False).replace("<", "\u003c")
    strings_json = json.dumps(strings, ensure_ascii=False).replace("<", "\u003c")

    return """
<div class="card" id="fullQuizBlock" style="margin-top:24px;" data-pass-threshold="%s">
  <h3 style="margin:0 0 12px 0;color:#65dfff;">%s</h3>
  %s
  <button type="button" onclick="submitFullQuiz()" class="nav-btn" style="margin-top:8px;">%s</button>
  <div id="fullQuizResult" style="margin-top:12px;font-size:15px;font-weight:700;display:none;"></div>
</div>
<script>
const NABIL_QUIZ_TOTAL = %d;
const NABIL_QUIZ_PASS_SCORE = %d;
const NABIL_QUIZ_THRESHOLD = %s;
const NABIL_QUIZ_EXPLANATIONS = %s;
const NABIL_QUIZ_STRINGS = %s;
const nabilQuizAnswers = {};

function quizAnswer(btn,qid,isCorrect){
  const container=btn.closest('.quiz-item');
  if(!container || container.dataset.locked) return;
  container.dataset.locked='true';
  nabilQuizAnswers[qid]=!!isCorrect;
  container.querySelectorAll('.q-opt').forEach(function(opt){opt.disabled=true;});
  const fb=container.querySelector('.quiz-fb[data-qid="'+qid+'"]');
  if(fb){
    fb.style.display='block';
    fb.style.color=isCorrect?'#7ce6b8':'#ff8b98';
    fb.textContent=isCorrect?NABIL_QUIZ_STRINGS.correct:NABIL_QUIZ_STRINGS.incorrect;
  }
  const detail=NABIL_QUIZ_EXPLANATIONS[String(qid)]||{};
  const box=container.querySelector('.quiz-explanation[data-qid="'+qid+'"]');
  if(box && (detail.explanation||detail.evidence_quote)){
    box.style.display='block';
    box.textContent=detail.explanation||detail.evidence_quote;
  }
}

function submitFullQuiz(){
  const answered=Object.keys(nabilQuizAnswers).length;
  if(answered<NABIL_QUIZ_TOTAL){
    alert(NABIL_QUIZ_STRINGS.question+': '+(NABIL_QUIZ_TOTAL-answered)+' '+NABIL_QUIZ_STRINGS.remaining);
    return;
  }
  const score=Object.values(nabilQuizAnswers).filter(Boolean).length;
  const resultBox=document.getElementById('fullQuizResult');
  if(!resultBox) return;
  const passed=score>=NABIL_QUIZ_PASS_SCORE;
  resultBox.style.display='block';
  resultBox.style.color=passed?'#7ce6b8':'#ff8b98';
  resultBox.textContent=NABIL_QUIZ_STRINGS.result_prefix+' '+score+' / '+NABIL_QUIZ_TOTAL+
    ' — '+(passed?NABIL_QUIZ_STRINGS.pass:NABIL_QUIZ_STRINGS.retry);
}
</script>""" % (
        threshold,
        html.escape(_t(lang_code, "quiz_title")),
        "".join(items_html),
        html.escape(_t(lang_code, "quiz_submit")),
        total,
        pass_score,
        repr(threshold),
        exp_json,
        strings_json,
    )

__all__ = [
    "DEFAULT_PASS_THRESHOLD_FRACTION",
    "build_full_quiz_items",
    "render_quiz_html",
]
