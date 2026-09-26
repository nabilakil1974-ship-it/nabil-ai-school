#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NABIL AI — محرك Quiz كامل التغطية.
يبني سؤالاً من بيانات كل مفهوم الموثقة مسبقاً؛ لا يستدعي LLM جديداً ولا يخترع محتوى.
لا يفرض نسبة نجاح اعتباطية؛ يعرض الدرجة الحقيقية فقط.
"""
import html
from typing import List,Dict,Any
try:
    from scripts.nabil_i18n import t as _t
except Exception:
    from nabil_i18n import t as _t

def build_full_quiz_items(activities_theory:List[Dict[str,Any]])->List[Dict[str,Any]]:
    if not activities_theory:
        raise RuntimeError("QUIZ_GENERATION_FAILED: no activities")
    items=[]
    for idx,act in enumerate(activities_theory,1):
        q=act.get("student_question") or {}
        options=list(q.get("options") or [])
        if not q.get("q") or not options or "correct_index" not in q:
            raise RuntimeError(f"QUIZ_GENERATION_FAILED: activity {idx} missing gradable data")
        ci=int(q["correct_index"])
        if ci<0 or ci>=len(options):
            raise RuntimeError(f"QUIZ_GENERATION_FAILED: activity {idx} invalid correct_index")
        items.append({
            "id":idx,
            "concept_id":act.get("concept_id") or act.get("activity_num"),
            "source_page":act.get("source_page"),
            "question":str(q["q"]),
            "options":options,
            "correct_index":ci,
            "explanation":str(act.get("conclusion") or "")
        })
    return items

def render_quiz_html(quiz_items:List[Dict[str,Any]],lang_code:str)->str:
    if not quiz_items:
        raise RuntimeError("QUIZ_RENDER_FAILED: empty quiz")
    total=len(quiz_items)
    rows=[]
    for item in quiz_items:
        opts="".join(
            f'<button type="button" class="q-opt" onclick="nabilQuizAnswer(this,{item["id"]},{str(i==item["correct_index"]).lower()})">{html.escape(str(opt))}</button>'
            for i,opt in enumerate(item["options"])
        )
        rows.append(f"""
        <div class="quiz-item" data-qid="{item['id']}" style="margin:12px 0;padding:12px;background:#fff;border:1px solid #e2e8f0;border-radius:8px;">
          <div style="font-weight:700;margin-bottom:8px;">{html.escape(_t(lang_code,'question_label'))} {item['id']}: {html.escape(item['question'])}</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;">{opts}</div>
          <div class="quiz-fb" style="display:none;margin-top:8px;font-size:13px;"></div>
        </div>""")
    return f"""
    <section class="card" id="fullQuizBlock" style="margin-top:24px;">
      <h3 style="margin-top:0;color:#0284c7;">{html.escape(_t(lang_code,'quiz_title'))}</h3>
      {''.join(rows)}
      <button type="button" class="nav-btn" onclick="nabilQuizSubmit()">{html.escape(_t(lang_code,'quiz_submit'))}</button>
      <div id="fullQuizResult" style="display:none;margin-top:12px;font-weight:700;"></div>
    </section>
    <script>
    const NABIL_QUIZ_TOTAL={total};
    const NABIL_QUIZ_ANSWERS={{}};
    function nabilQuizAnswer(btn,qid,isCorrect){{
      const item=btn.closest('.quiz-item');
      if(item.dataset.locked==='1')return;
      item.dataset.locked='1';
      NABIL_QUIZ_ANSWERS[qid]=!!isCorrect;
      const fb=item.querySelector('.quiz-fb');
      fb.style.display='block';
      fb.style.color=isCorrect?'#059669':'#dc2626';
      fb.textContent=isCorrect?'{html.escape(_t(lang_code,'ws_correct'))}':'{html.escape(_t(lang_code,'ws_incorrect'))}';
    }}
    function nabilQuizSubmit(){{
      const result=document.getElementById('fullQuizResult');
      const answered=Object.keys(NABIL_QUIZ_ANSWERS).length;
      result.style.display='block';
      if(answered<NABIL_QUIZ_TOTAL){{
        result.style.color='#b45309';
        result.textContent='{html.escape(_t(lang_code,'question_label'))}: '+(NABIL_QUIZ_TOTAL-answered);
        return;
      }}
      const score=Object.values(NABIL_QUIZ_ANSWERS).filter(Boolean).length;
      result.style.color='#0369a1';
      result.textContent='{html.escape(_t(lang_code,'quiz_result_prefix'))} '+score+' / '+NABIL_QUIZ_TOTAL;
    }}
    </script>"""
