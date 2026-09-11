from __future__ import annotations

import json
import os
import secrets
from datetime import datetime, timedelta
from html import escape

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.student_learning import StudentLearningProfile
from app.db.ai_usage import AIUsageLog


router = APIRouter(tags=["admin"])


def _admin_token() -> str:
    return os.getenv("NABIL_ADMIN_TOKEN", "").strip()


def require_admin(token: str = Query(default="")):
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
    for name in ("subscription_status", "plan_status", "account_status"):
        value = getattr(profile, name, None)
        if value:
            return str(value)
    return "trial"


def _last_activity(profile) -> str:
    for name in ("updated_at", "last_activity_at", "last_active_at", "created_at"):
        value = getattr(profile, name, None)
        if value:
            if isinstance(value, datetime):
                return value.strftime("%Y-%m-%d %H:%M")
            return str(value)
    return "—"


def _student_id(profile) -> str:
    for name in ("student_id", "user_id", "student_name"):
        value = getattr(profile, name, None)
        if value:
            return str(value)
    return f"student-{getattr(profile, 'id', '—')}"


def _row(profile) -> dict:
    mastery = _loads(getattr(profile, "lesson_mastery_json", "[]"), [])
    assessments = _loads(getattr(profile, "test_results_json", "[]"), [])
    strengths = _loads(getattr(profile, "strengths_json", "[]"), [])

    mastered = sum(
        1 for item in mastery
        if isinstance(item, dict) and item.get("status") == "mastered"
    )
    needs_review = sum(
        1 for item in mastery
        if isinstance(item, dict) and item.get("status") == "needs_review"
    )

    return {
        "student_id": _student_id(profile),
        "progress": float(getattr(profile, "overall_progress_percent", 0) or 0),
        "mastered": mastered,
        "needs_review": needs_review,
        "tests": len(assessments),
        "strengths": len(strengths),
        "subscription": _subscription(profile),
        "last_activity": _last_activity(profile),
    }


def _ai_stats(db: Session) -> dict:
    now = datetime.utcnow()
    since = now - timedelta(hours=24)

    q = db.query(AIUsageLog).filter(AIUsageLog.created_at >= since)

    total = q.count()
    successful = q.filter(AIUsageLog.success.is_(True)).count()
    failed = q.filter(AIUsageLog.success.is_(False)).count()
    cache_hits = q.filter(AIUsageLog.cache_hit.is_(True)).count()
    errors_429 = q.filter(AIUsageLog.error_type == "provider_429").count()
    errors_503 = q.filter(AIUsageLog.status_code == 503).count()

    avg_ms = (
        db.query(func.avg(AIUsageLog.response_time_ms))
        .filter(
            AIUsageLog.created_at >= since,
            AIUsageLog.response_time_ms.isnot(None),
        )
        .scalar()
    )

    success_rate = round((successful / total * 100), 1) if total else 0.0

    if total == 0:
        health = "لا توجد طلبات خلال آخر 24 ساعة"
        health_code = "idle"
    elif success_rate >= 95:
        health = "ممتاز"
        health_code = "good"
    elif success_rate >= 70:
        health = "مستقر"
        health_code = "warn"
    else:
        health = "يحتاج متابعة"
        health_code = "bad"

    recent = (
        db.query(AIUsageLog)
        .order_by(AIUsageLog.created_at.desc())
        .limit(25)
        .all()
    )

    recent_rows = []
    for item in recent:
        recent_rows.append({
            "time": (
                item.created_at.strftime("%Y-%m-%d %H:%M:%S")
                if item.created_at else "—"
            ),
            "student_id": item.student_id or "—",
            "grade": item.grade or "—",
            "subject": item.subject or "—",
            "lesson": item.lesson or "—",
            "success": bool(item.success),
            "status_code": int(item.status_code or 0),
            "error_type": item.error_type or "",
            "response_time_ms": (
                round(float(item.response_time_ms), 0)
                if item.response_time_ms is not None else None
            ),
            "cache_hit": bool(item.cache_hit),
        })

    return {
        "window": "24h",
        "total": total,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate,
        "cache_hits": cache_hits,
        "errors_429": errors_429,
        "errors_503": errors_503,
        "avg_response_ms": round(float(avg_ms), 0) if avg_ms is not None else 0,
        "health": health,
        "health_code": health_code,
        "recent": recent_rows,
    }


@router.get(
    "/api/admin/summary",
    dependencies=[Depends(require_admin)],
)
def admin_summary(db: Session = Depends(get_db)):
    profiles = (
        db.query(StudentLearningProfile)
        .order_by(StudentLearningProfile.id.desc())
        .all()
    )

    rows = [_row(p) for p in profiles]

    return {
        "students": len(rows),
        "trial": sum(1 for r in rows if r["subscription"].lower() == "trial"),
        "paid": sum(
            1 for r in rows
            if r["subscription"].lower() in {"paid", "active", "subscribed"}
        ),
        "mastered_lessons": sum(r["mastered"] for r in rows),
        "needs_review": sum(r["needs_review"] for r in rows),
        "tests": sum(r["tests"] for r in rows),
        "students_data": rows,
        "ai": _ai_stats(db),
    }


@router.get(
    "/admin",
    response_class=HTMLResponse,
    dependencies=[Depends(require_admin)],
)
def admin_dashboard(token: str = Query(default="")):
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
body{{margin:0;background:#101416;color:#eef6ff;font-family:Arial,Tahoma,sans-serif}}
header{{padding:24px;background:linear-gradient(135deg,#2469a8,#173c69);text-align:center}}
header h1{{margin:0 0 7px;font-size:27px}}
header p{{margin:0;opacity:.8}}
main{{max-width:1350px;margin:auto;padding:22px}}
h2{{font-size:19px;margin:25px 0 12px}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:14px;margin-bottom:20px}}
.card{{background:#171d20;border:1px solid #29475d;border-radius:14px;padding:18px}}
.card small{{color:#a9bac7}}
.card strong{{display:block;font-size:28px;color:#70b9ff;margin-top:8px}}
.card .unit{{font-size:13px;color:#8fa6b6;margin-top:4px}}
.health-good{{color:#6ee7a8!important}}
.health-warn{{color:#ffd166!important}}
.health-bad{{color:#ff8d8d!important}}
.health-idle{{color:#a9bac7!important}}
.toolbar{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}}
input{{flex:1;min-width:220px;background:#111719;color:white;border:1px solid #36546a;border-radius:10px;padding:12px}}
button{{background:#155dcc;color:white;border:0;border-radius:10px;padding:11px 17px;cursor:pointer;font-weight:700}}
.table-wrap{{overflow:auto;border:1px solid #29475d;border-radius:14px;margin-bottom:24px}}
table{{width:100%;border-collapse:collapse;min-width:900px}}
th,td{{padding:13px;border-bottom:1px solid #25343e;text-align:center}}
th{{background:#18232a;position:sticky;top:0}}
tr:hover{{background:#172127}}
.badge{{display:inline-block;padding:4px 9px;border-radius:999px;background:#243845}}
.ok{{color:#6ee7a8}}
.fail{{color:#ff8d8d}}
.cache{{color:#ffd166}}
.progress{{width:110px;height:8px;background:#29343a;border-radius:10px;overflow:hidden;margin:5px auto}}
.progress span{{display:block;height:100%;background:#58aef8}}
#error{{color:#ff9c9c;padding:10px 0}}
.note{{color:#8fa6b6;font-size:13px;margin-top:-5px;margin-bottom:12px}}
</style>
</head>
<body>
<header>
<h1>🛡️ لوحة إدارة NABIL AI</h1>
<p>الطلاب • التقدم • الاختبارات • الاشتراكات • مراقبة الذكاء الاصطناعي</p>
</header>

<main>
<h2>📚 الطلاب والتعلم</h2>
<div class="cards">
 <div class="card"><small>إجمالي الطلاب</small><strong id="students">—</strong></div>
 <div class="card"><small>تجريبي</small><strong id="trial">—</strong></div>
 <div class="card"><small>مدفوع/نشط</small><strong id="paid">—</strong></div>
 <div class="card"><small>دروس متقنة</small><strong id="mastered">—</strong></div>
 <div class="card"><small>تحتاج مراجعة</small><strong id="review">—</strong></div>
 <div class="card"><small>الاختبارات</small><strong id="tests">—</strong></div>
</div>

<h2>🤖 حالة NABIL AI - آخر 24 ساعة</h2>
<div class="cards">
 <div class="card"><small>طلبات AI</small><strong id="aiTotal">—</strong></div>
 <div class="card"><small>ناجحة</small><strong id="aiSuccess">—</strong></div>
 <div class="card"><small>فاشلة</small><strong id="aiFailed">—</strong></div>
 <div class="card"><small>نسبة النجاح</small><strong id="aiRate">—</strong></div>
 <div class="card"><small>Cache Hits</small><strong id="aiCache">—</strong></div>
 <div class="card"><small>أخطاء 429</small><strong id="ai429">—</strong></div>
 <div class="card"><small>أخطاء 503</small><strong id="ai503">—</strong></div>
 <div class="card"><small>متوسط الاستجابة</small><strong id="aiSpeed">—</strong><div class="unit">ms</div></div>
 <div class="card"><small>الحالة</small><strong id="aiHealth">—</strong></div>
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
<th>الطالب</th><th>التقدم</th><th>متقن</th><th>مراجعة</th>
<th>اختبارات</th><th>نقاط قوة</th><th>الاشتراك</th><th>آخر نشاط</th>
</tr>
</thead>
<tbody id="rows"></tbody>
</table>
</div>

<h2>🧾 آخر طلبات الذكاء الاصطناعي</h2>
<div class="note">يعرض آخر 25 طلبًا مسجلًا في المنصة.</div>
<div class="table-wrap">
<table>
<thead>
<tr>
<th>الوقت</th><th>الطالب</th><th>الصف</th><th>المادة</th><th>الدرس</th>
<th>النتيجة</th><th>HTTP</th><th>الخطأ</th><th>الزمن</th><th>Cache</th>
</tr>
</thead>
<tbody id="aiRows"></tbody>
</table>
</div>
</main>

<script>
const ADMIN_TOKEN = {json.dumps(safe_token)};
let allRows = [];

function esc(v) {{
 return String(v ?? "")
  .replaceAll("&","&amp;").replaceAll("<","&lt;")
  .replaceAll(">","&gt;").replaceAll('"',"&quot;");
}}

function renderRows(rows) {{
 const body = document.getElementById("rows");
 body.innerHTML = rows.map(r => `
 <tr>
  <td><b>${{esc(r.student_id)}}</b></td>
  <td>${{Number(r.progress).toFixed(0)}}%
   <div class="progress"><span style="width:${{Math.max(0,Math.min(100,r.progress))}}%"></span></div>
  </td>
  <td>${{r.mastered}}</td><td>${{r.needs_review}}</td>
  <td>${{r.tests}}</td><td>${{r.strengths}}</td>
  <td><span class="badge">${{esc(r.subscription)}}</span></td>
  <td>${{esc(r.last_activity)}}</td>
 </tr>`).join("");
}}

function renderAIRows(rows) {{
 document.getElementById("aiRows").innerHTML = (rows || []).map(r => `
 <tr>
  <td>${{esc(r.time)}}</td>
  <td>${{esc(r.student_id)}}</td>
  <td>${{esc(r.grade)}}</td>
  <td>${{esc(r.subject)}}</td>
  <td>${{esc(r.lesson)}}</td>
  <td class="${{r.success ? "ok" : "fail"}}">${{r.success ? "✓ ناجح" : "✕ فشل"}}</td>
  <td>${{esc(r.status_code)}}</td>
  <td>${{esc(r.error_type || "—")}}</td>
  <td>${{r.response_time_ms == null ? "—" : esc(r.response_time_ms) + " ms"}}</td>
  <td class="${{r.cache_hit ? "cache" : ""}}">${{r.cache_hit ? "✓" : "—"}}</td>
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

  const ai = data.ai || {{}};
  document.getElementById("aiTotal").textContent = ai.total ?? 0;
  document.getElementById("aiSuccess").textContent = ai.successful ?? 0;
  document.getElementById("aiFailed").textContent = ai.failed ?? 0;
  document.getElementById("aiRate").textContent = (ai.success_rate ?? 0) + "%";
  document.getElementById("aiCache").textContent = ai.cache_hits ?? 0;
  document.getElementById("ai429").textContent = ai.errors_429 ?? 0;
  document.getElementById("ai503").textContent = ai.errors_503 ?? 0;
  document.getElementById("aiSpeed").textContent = ai.avg_response_ms ?? 0;

  const health = document.getElementById("aiHealth");
  health.textContent = ai.health || "—";
  health.className = "health-" + (ai.health_code || "idle");

  allRows = data.students_data || [];
  renderRows(allRows);
  renderAIRows(ai.recent || []);

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
setInterval(loadData, 60000);
</script>
</body>
</html>"""
    )
