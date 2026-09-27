#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NABIL AI — Full-Coverage Quiz Engine
Add-on module: does NOT replace nabil_book_factory.py, imported by it.

Fixes the current hardcoded cap in synthesize_universal_pedagogy():
    if idx <= 5:
        worksheet.append(...)

This silently drops quiz coverage for any lesson with more than 5 concepts —
a lesson with 8 activities gets a quiz testing only the first 5, with no
warning to the teacher. This module:
  1. Builds one question per concept (ALL of them, not capped at 5).
  2. Adds a real pass/fail threshold and final score summary.
  3. Reuses the exact same grounded narrative fields (conclusion +
     distractor_1/2) already produced by synthesize_concept_narrative —
     no new LLM calls, no new invented content, same evidence guarantee.
"""

import html
from typing import List, Dict, Any

from scripts.nabil_i18n import t as _t

PASS_THRESHOLD_FRACTION = 0.70  # configurable; matches typical Lebanese 70% pass mark


def build_full_quiz_items(activities_theory: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build one quiz item per activity/concept. No cap.

    Each item reuses the SAME grounded conclusion/distractor fields already
    verified by synthesize_concept_narrative — this function only assembles
    presentation, it introduces no new claims.
    """
    if not activities_theory:
        return []

    items = []
    for act in activities_theory:
        q = act.get("student_question")
        if not q or not q.get("options") or "correct_index" not in q:
            continue
        items.append({
            "id": len(items) + 1,
            "concept_id": act.get("concept_id") or act.get("activity_num"),
            "source_page": act.get("source_page"),
            "question": q["q"],
            "options": q["options"],
            "correct_index": q["correct_index"],
            "explanation": act.get("conclusion", ""),
        })
    return items


def render_quiz_html(quiz_items: List[Dict[str, Any]], lang_code: str) -> str:
    """Render the full quiz as a gradable HTML block with a real final
    score summary and pass/fail message — not just per-item feedback.
    """
    if not quiz_items:
        return ""

    total = len(quiz_items)
    pass_score = max(1, round(total * PASS_THRESHOLD_FRACTION))

    items_html = ""
    for item in quiz_items:
        opts_html = "".join(
            f'<button onclick="quizAnswer(this, {item["id"]}, {i == item["correct_index"]})" '
            f'class="q-opt" data-qid="{item["id"]}">{html.escape(opt)}</button>'
            for i, opt in enumerate(item["options"])
        )
        page_note = (
            f' <span style="font-size:11px; color:#64748b;">(p. {item["source_page"]})</span>'
            if item.get("source_page") else ""
        )
        items_html += f'''
        <div class="quiz-item" data-qid="{item["id"]}" style="margin-bottom:16px; padding:12px; background:#fff; border:1px solid #e2e8f0; border-radius:6px;">
          <div style="font-weight:600; margin-bottom:8px;">{_t(lang_code, "question_label")} {item["id"]}: {html.escape(item["question"])}{page_note}</div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">{opts_html}</div>
          <div class="quiz-fb" data-qid="{item["id"]}" style="margin-top:6px; font-size:12px; font-weight:600; display:none;"></div>
        </div>'''

    submit_label = _t(lang_code, "quiz_submit")
    result_prefix = _t(lang_code, "quiz_result_prefix")
    pass_msg = _t(lang_code, "quiz_pass")
    retry_msg = _t(lang_code, "quiz_retry")
    title = _t(lang_code, "quiz_title")

    return f'''
    <div class="card" id="fullQuizBlock" style="margin-top:24px;">
      <h3 style="margin:0 0 12px 0; color:#0284c7;">{html.escape(title)}</h3>
      {items_html}
      <button onclick="submitFullQuiz()" class="nav-btn" style="margin-top:8px;">{html.escape(submit_label)}</button>
      <div id="fullQuizResult" style="margin-top:12px; font-size:15px; font-weight:700; display:none;"></div>
    </div>
    <script>
    const NABIL_QUIZ_TOTAL = {total};
    const NABIL_QUIZ_PASS_SCORE = {pass_score};
    const nabilQuizAnswers = {{}};

    function quizAnswer(btn, qid, isCorrect) {{
      const container = btn.closest('.quiz-item');
      if (container.dataset.locked) return;
      container.dataset.locked = 'true';
      nabilQuizAnswers[qid] = isCorrect;
      const fb = container.querySelector('.quiz-fb[data-qid="' + qid + '"]');
      fb.style.display = 'block';
      fb.style.color = isCorrect ? '#059669' : '#dc2626';
      fb.innerText = isCorrect ? '{_t(lang_code, "ws_correct")}' : '{_t(lang_code, "ws_incorrect")}';
    }}

    function submitFullQuiz() {{
      const answered = Object.keys(nabilQuizAnswers).length;
      if (answered < NABIL_QUIZ_TOTAL) {{
        alert('{_t(lang_code, "question_label")}: ' + (NABIL_QUIZ_TOTAL - answered) + ' remaining');
        return;
      }}
      const score = Object.values(nabilQuizAnswers).filter(Boolean).length;
      const resultBox = document.getElementById('fullQuizResult');
      resultBox.style.display = 'block';
      const passed = score >= NABIL_QUIZ_PASS_SCORE;
      resultBox.style.color = passed ? '#059669' : '#dc2626';
      resultBox.innerHTML = '{html.escape(result_prefix)} ' + score + ' / ' + NABIL_QUIZ_TOTAL + '<br>' +
        (passed ? '{html.escape(pass_msg)}' : '{html.escape(retry_msg)}');
    }}
    </script>'''
