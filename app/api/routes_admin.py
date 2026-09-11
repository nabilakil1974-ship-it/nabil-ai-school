from __future__ import annotations

import json
import os
import secrets
from datetime import datetime
from html import escape

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.student_learning import StudentLearningProfile


router = APIRouter(tags=["admin"])


def _admin_token() -> str:
    return os.getenv("NABIL_ADMIN_TOKEN", "").strip()


def require_admin(
    token: str = Query(default=""),
):
    expected = _admin_token()

    if not expected:
        raise HTTPException(
            status_code=503,
            detail="NABIL_ADMIN_TOKEN is not configured.",
        )

    if not secrets.compare_digest(token, expected):
        raise HTTPException(
            status_code=403,
            detail="غير مصرح بالدخول إلى لوحة الإدارة.",
        )

    return True


def _loads(value, default):
    if value is None:
        return default

    if isinstance(value, (list, dict)):
        return value

    try:
        return json.loads(value)
    except Exception:
        return default


def _subscription(profile) -> str:
    for name in (
        "subscription_status",
        "plan_status",
        "account_status",
    ):
        value = getattr(profile, name, None)
        if value:
            return str(value)

    return "trial"


def _last_activity(profile) -> str:
    for name in (
        "updated_at",
        "last_activity_at",
        "last_active_at",
        "created_at",
    ):
        value = getattr(profile, name, None)
        if value:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M")
            return str(value)

    return "—"


def _student_id(profile) -> str:
    for name in (
        "student_id",
        "user_id",
        "student_name",
    ):
        value = getattr(profile, name, None)
        if value:
            return str(value)

    return f"student-{getattr(profile, 'id', '—')}"


def _row(profile) -> dict:
    mastery = _loads(
        getattr(profile, "lesson_mastery_json", "[]"),
        [],
    )
    assessments = _loads(
        getattr(profile, "test_results_json", "[]"),
        [],
    )
    strengths = _loads(
        getattr(profile, "strengths_json", "[]"),
        [],
    )
    review = _loads(
        getattr(profile, "concepts_to_review_json", "[]"),
        [],
    )

    mastered = sum(
        1
        for item in mastery
        if isinstance(item, dict)
        and item.get("status") == "mastered"
    )

    needs_review = sum(
        1
        for item in mastery
        if isinstance(item, dict)
        and item.get("status") == "needs_review"
    )

    return {
        "student_id": _student_id(profile),
        "progress": float(
            getattr(profile, "overall_progress_percent", 0) or 0
        ),
        "mastered": mastered,
        "needs_review": needs_review,
        "tests": len(assessments),
        "strengths": len(strengths),
        "subscription": _subscription(profile),
        "last_activity": _last_activity(profile),
    }


@router.get(
    "/api/admin/summary",
    dependencies=[Depends(require_admin)],
)
def admin_summary(
    db: Session = Depends(get_db),
):
    profiles = (
        db.query(StudentLearningProfile)
        .order_by(StudentLearningProfile.id.desc())
        .all()
    )

    rows = [_row(p) for p in profiles]

    return {
        "students": len(rows),
        "trial": sum(
            1 for r in rows
            if r["subscription"].lower() == "trial"
        ),
        "paid": sum(
            1 for r in rows
            if r["subscription"].lower()
            in {"paid", "active", "subscribed"}
        ),
        "mastered_lessons": sum(
            r["mastered"] for r in rows
        ),
        "needs_review": sum(
            r["needs_review"] for r in rows
        ),
        "tests": sum(
            r["tests"] for r in rows
        ),
        "students_data": rows,
    }


@router.get(
    "/admin",
    response_class=HTMLResponse,
    dependencies=[Depends(require_admin)],
)
def admin_dashboard(
    token: str = Query(default=""),
):
    safe_token = escape(token, quote=True)

    return HTMLResponse(
        f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NABIL AI - لوحة الإدارة</title>
<style>
*{{box-sizing:border-box}}
body{{
 margin:0;background:#101416;color:#eef6ff;
 font-family:Arial,Tahoma,sans-serif
}}
header{{
 padding:24px;background:linear-gradient(135deg,#2469a8,#173c69);
 text-align:center
}}
header h1{{margin:0 0 7px;font-size:27px}}
header p{{margin:0;opacity:.8}}
main{{max-width:1250px;margin:auto;padding:22px}}
.cards{{
 display:grid;grid-template-columns:repeat(auto-fit,minmax(165px,1fr));
 gap:14px;margin-bottom:20px
}}
.card{{
 background:#171d20;border:1px solid #29475d;border-radius:14px;
 padding:18px
}}
.card small{{color:#a9bac7}}
.card strong{{display:block;font-size:29px;color:#70b9ff;margin-top:8px}}
.toolbar{{
 display:flex;gap:10px;flex-wrap:wrap;margin:16px 0
}}
input{{
 flex:1;min-width:220px;background:#111719;color:white;
 border:1px solid #36546a;border-radius:10px;padding:12px
}}
button{{
 background:#155dcc;color:white;border:0;border-radius:10px;
 padding:11px 17px;cursor:pointer;font-weight:700
}}
.table-wrap{{overflow:auto;border:1px solid #29475d;border-radius:14px}}
table{{width:100%;border-collapse:collapse;min-width:900px}}
th,td{{padding:13px;border-bottom:1px solid #25343e;text-align:center}}
th{{background:#18232a;position:sticky;top:0}}
tr:hover{{background:#172127}}
.badge{{
 display:inline-block;padding:4px 9px;border-radius:999px;
 background:#243845
}}
.progress{{
 width:110px;height:8px;background:#29343a;border-radius:10px;
 overflow:hidden;margin:5px auto
}}
.progress span{{
 display:block;height:100%;background:#58aef8
}}
#error{{color:#ff9c9c;padding:10px 0}}
</style>
</head>
<body>
<header>
<h1>🛡️ لوحة إدارة NABIL AI</h1>
<p>الطلاب • التقدم • الاختبارات • الاشتراكات</p>
</header>

<main>
<div class="cards">
 <div class="card"><small>إجمالي الطلاب</small><strong id="students">—</strong></div>
 <div class="card"><small>تجريبي</small><strong id="trial">—</strong></div>
 <div class="card"><small>مدفوع/نشط</small><strong id="paid">—</strong></div>
 <div class="card"><small>دروس متقنة</small><strong id="mastered">—</strong></div>
 <div class="card"><small>تحتاج مراجعة</small><strong id="review">—</strong></div>
 <div class="card"><small>الاختبارات</small><strong id="tests">—</strong></div>
</div>

<div class="toolbar">
 <input id="search" placeholder="ابحث عن طالب...">
 <button onclick="loadData()">↻ تحديث</button>
</div>

<div id="error"></div>

<div class="table-wrap">
<table>
<thead>
<tr>
<th>الطالب</th>
<th>التقدم</th>
<th>متقن</th>
<th>مراجعة</th>
<th>اختبارات</th>
<th>نقاط قوة</th>
<th>الاشتراك</th>
<th>آخر نشاط</th>
</tr>
</thead>
<tbody id="rows"></tbody>
</table>
</div>
</main>

<script>
const ADMIN_TOKEN = {json.dumps(safe_token)};
let allRows = [];

function esc(v) {{
 return String(v ?? "")
  .replaceAll("&","&amp;")
  .replaceAll("<","&lt;")
  .replaceAll(">","&gt;")
  .replaceAll('"',"&quot;");
}}

function renderRows(rows) {{
 const body = document.getElementById("rows");
 body.innerHTML = rows.map(r => `
 <tr>
  <td><b>${{esc(r.student_id)}}</b></td>
  <td>
   ${{Number(r.progress).toFixed(0)}}%
   <div class="progress"><span style="width:${{Math.max(0,Math.min(100,r.progress))}}%"></span></div>
  </td>
  <td>${{r.mastered}}</td>
  <td>${{r.needs_review}}</td>
  <td>${{r.tests}}</td>
  <td>${{r.strengths}}</td>
  <td><span class="badge">${{esc(r.subscription)}}</span></td>
  <td>${{esc(r.last_activity)}}</td>
 </tr>`).join("");
}}

async function loadData() {{
 const error = document.getElementById("error");
 error.textContent = "";

 try {{
  const response = await fetch(
   "/api/admin/summary?token=" + encodeURIComponent(ADMIN_TOKEN)
  );

  if (!response.ok) {{
   throw new Error("تعذر تحميل بيانات الإدارة: " + response.status);
  }}

  const data = await response.json();
  document.getElementById("students").textContent = data.students;
  document.getElementById("trial").textContent = data.trial;
  document.getElementById("paid").textContent = data.paid;
  document.getElementById("mastered").textContent = data.mastered_lessons;
  document.getElementById("review").textContent = data.needs_review;
  document.getElementById("tests").textContent = data.tests;

  allRows = data.students_data || [];
  renderRows(allRows);
 }} catch (e) {{
  error.textContent = e.message;
 }}
}}

document.getElementById("search").addEventListener("input", e => {{
 const q = e.target.value.trim().toLowerCase();
 renderRows(
  allRows.filter(r =>
   String(r.student_id).toLowerCase().includes(q)
  )
 );
}});

loadData();
</script>
</body>
</html>"""
    )
