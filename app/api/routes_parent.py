from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.student_learning import StudentLearningProfile


router = APIRouter(tags=["parent"])


# ==========================================================
# Helpers
# ==========================================================

def _loads_list(value):
    if not value:
        return []

    if isinstance(value, list):
        return value

    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return []


def _format_datetime(value):
    if not value:
        return None

    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")

    return str(value)


def _get_student_or_404(
    db: Session,
    student_id: str,
):
    profile = (
        db.query(StudentLearningProfile)
        .filter(
            StudentLearningProfile.student_id == student_id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="لم يتم العثور على ملف هذا الطالب.",
        )

    return profile


# ==========================================================
# Parent dashboard
# ==========================================================

@router.get("/parent/student")
def parent_student_dashboard(
    student_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    """
    Return a parent-friendly educational report
    for one student.
    """

    profile = _get_student_or_404(
        db,
        student_id,
    )

    lessons_studied = _loads_list(
        profile.lessons_studied_json
    )

    lesson_mastery = _loads_list(
        profile.lesson_mastery_json
    )

    strengths = _loads_list(
        profile.strengths_json
    )

    weaknesses = _loads_list(
        profile.weaknesses_json
    )

    frequent_mistakes = _loads_list(
        profile.frequent_mistakes_json
    )

    concepts_to_review = _loads_list(
        profile.concepts_to_review_json
    )

    test_results = _loads_list(
        profile.test_results_json
    )

    # ------------------------------------------------------
    # Mastery statistics
    # ------------------------------------------------------

    mastered_lessons = []

    needs_review_lessons = []

    learning_lessons = []

    for item in lesson_mastery:

        if not isinstance(item, dict):
            continue

        status = str(
            item.get("status", "")
        ).lower()

        if status == "mastered":
            mastered_lessons.append(item)

        elif status == "needs_review":
            needs_review_lessons.append(item)

        else:
            learning_lessons.append(item)

    # ------------------------------------------------------
    # Test statistics
    # ------------------------------------------------------

    scores = []

    for test in test_results:

        if not isinstance(test, dict):
            continue

        score = test.get("score")

        try:
            if score is not None:
                scores.append(float(score))
        except Exception:
            pass

    average_test_score = (
        round(
            sum(scores) / len(scores),
            1,
        )
        if scores
        else None
    )

    # ------------------------------------------------------
    # Parent status
    # ------------------------------------------------------

    progress = float(
        profile.overall_progress_percent or 0
    )

    if progress >= 85:
        progress_status = "ممتاز"

    elif progress >= 70:
        progress_status = "جيد جدًا"

    elif progress >= 50:
        progress_status = "جيد"

    elif progress > 0:
        progress_status = "يحتاج إلى متابعة"

    else:
        progress_status = "لم يبدأ التقييم بعد"

    # ------------------------------------------------------
    # Smart parent alerts
    # ------------------------------------------------------

    alerts = []

    if concepts_to_review:
        alerts.append(
            {
                "type": "review",
                "title": "مراجعة مطلوبة",
                "message": (
                    f"لدى الطالب "
                    f"{len(concepts_to_review)} "
                    "مفهومًا يحتاج إلى مراجعة."
                ),
            }
        )

    if weaknesses:
        alerts.append(
            {
                "type": "weakness",
                "title": "نقاط تحتاج دعمًا",
                "message": (
                    f"تم رصد "
                    f"{len(weaknesses)} "
                    "نقطة تحتاج إلى مزيد من التدريب."
                ),
            }
        )

    if frequent_mistakes:
        alerts.append(
            {
                "type": "mistakes",
                "title": "أخطاء متكررة",
                "message": (
                    f"تم رصد "
                    f"{len(frequent_mistakes)} "
                    "نوع من الأخطاء المتكررة."
                ),
            }
        )

    if progress >= 80:
        alerts.append(
            {
                "type": "success",
                "title": "تقدم مميز",
                "message": (
                    "يحقق الطالب تقدمًا جيدًا جدًا "
                    "في مساره التعليمي."
                ),
            }
        )

    if not alerts:
        alerts.append(
            {
                "type": "info",
                "title": "المتابعة التعليمية",
                "message": (
                    "سيبدأ NABIL AI بإظهار "
                    "التوصيات فور توفر نشاط تعليمي كافٍ."
                ),
            }
        )

    # ------------------------------------------------------
    # Suggested next action
    # ------------------------------------------------------

    if concepts_to_review:
        next_action = (
            "مراجعة المفاهيم التي حددها NABIL AI "
            "قبل الانتقال إلى درس جديد."
        )

    elif weaknesses:
        next_action = (
            "حل تمارين إضافية على نقاط الضعف "
            "لرفع مستوى الإتقان."
        )

    elif progress >= 80:
        next_action = (
            "الاستمرار في الدرس التالي "
            "ضمن المسار التعليمي المقترح."
        )

    else:
        next_action = (
            "متابعة التعلم وإجراء تمارين إضافية "
            "حتى يتمكن NABIL AI من بناء تقييم أدق."
        )

    # ------------------------------------------------------
    # Response
    # ------------------------------------------------------

    return {
        "student": {
            "student_id": profile.student_id,

            "grade": profile.current_grade,

            "branch": profile.current_branch,

            "subject": profile.current_subject,

            "current_lesson": profile.current_lesson,

            "progress_percent": progress,

            "progress_status": progress_status,

            "mastered_lessons_count": (
                profile.mastered_lessons_count or 0
            ),

            "learning_minutes": (
                profile.total_learning_minutes or 0
            ),

            "interaction_count": (
                profile.interaction_count or 0
            ),

            "last_activity": (
                profile.last_active_activity
            ),

            "last_updated": _format_datetime(
                profile.updated_at
            ),
        },

        "learning": {
            "lessons_studied": lessons_studied,

            "mastered_lessons": mastered_lessons,

            "needs_review_lessons": (
                needs_review_lessons
            ),

            "learning_lessons": learning_lessons,

            "strengths": strengths,

            "weaknesses": weaknesses,

            "frequent_mistakes": (
                frequent_mistakes
            ),

            "concepts_to_review": (
                concepts_to_review
            ),
        },

        "tests": {
            "count": len(test_results),

            "average_score": average_test_score,

            "results": test_results,
        },

        "parent_insights": {
            "alerts": alerts,

            "recommended_next_action": (
                next_action
            ),
        },

        "subscription": {
            "status": (
                profile.subscription_status
            ),

            "trial_ends_at": _format_datetime(
                profile.trial_ends_at
            ),

            "subscription_ends_at": (
                _format_datetime(
                    profile.subscription_ends_at
                )
            ),
        },
    }


# ==========================================================
# Lightweight progress endpoint
# ==========================================================

@router.get("/parent/progress")
def parent_student_progress(
    student_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    profile = _get_student_or_404(
        db,
        student_id,
    )

    return {
        "student_id": profile.student_id,

        "progress_percent": float(
            profile.overall_progress_percent or 0
        ),

        "mastered_lessons": (
            profile.mastered_lessons_count or 0
        ),

        "learning_minutes": (
            profile.total_learning_minutes or 0
        ),

        "current_subject": (
            profile.current_subject
        ),

        "current_lesson": (
            profile.current_lesson
        ),

        "last_activity": (
            profile.last_active_activity
        ),
    }
