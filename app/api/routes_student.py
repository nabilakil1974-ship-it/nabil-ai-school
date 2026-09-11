from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.student_learning import StudentLearningProfile
from app.db.subscription import PaymentRecord
from app.services.subscription_service import (
    MONTHLY_PRICE_USD,
    WHISH_RECEIVER_NUMBER,
    activate_one_month,
    subscription_state,
)

router = APIRouter()


def get_profile(
    db: Session,
    student_id: str,
) -> StudentLearningProfile:
    profile = (
        db.query(StudentLearningProfile)
        .filter_by(student_id=student_id)
        .first()
    )

    if profile is None:
        profile = StudentLearningProfile(
            student_id=student_id,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    return profile


@router.get("/student/{student_id}/dashboard")
def student_dashboard(
    student_id: str,
    db: Session = Depends(get_db),
):
    profile = get_profile(
        db,
        student_id,
    )

    return {
        "student_id": profile.student_id,
        "current_grade": profile.current_grade,
        "current_branch": profile.current_branch,
        "current_subject": profile.current_subject,
        "current_lesson": profile.current_lesson,
        "overall_progress_percent": profile.overall_progress_percent,
        "mastered_lessons_count": profile.mastered_lessons_count,
        "total_learning_minutes": profile.total_learning_minutes,
        "interaction_count": profile.interaction_count,
        "last_active_activity": profile.last_active_activity,
        "lessons_studied": profile.loads_list(
            profile.lessons_studied_json
        ),
        "strengths": profile.loads_list(
            profile.strengths_json
        ),
        "weaknesses": profile.loads_list(
            profile.weaknesses_json
        ),
        "frequent_mistakes": profile.loads_list(
            profile.frequent_mistakes_json
        ),
        "concepts_to_review": profile.loads_list(
            profile.concepts_to_review_json
        ),
        "test_results": profile.loads_list(
            profile.test_results_json
        ),
        "subscription": subscription_state(
            profile
        ),
    }


@router.get("/student/{student_id}/subscription")
def get_subscription(
    student_id: str,
    db: Session = Depends(get_db),
):
    profile = get_profile(
        db,
        student_id,
    )

    return subscription_state(
        profile
    )


class PaymentRequest(BaseModel):
    transaction_reference: str | None = None


@router.post("/student/{student_id}/payment/whish")
def submit_whish_payment(
    student_id: str,
    payload: PaymentRequest,
    db: Session = Depends(get_db),
):
    if not WHISH_RECEIVER_NUMBER:
        raise HTTPException(
            status_code=503,
            detail=(
                "رقم Whish غير مضبوط بعد. "
                "أضف WHISH_RECEIVER_NUMBER في Railway."
            ),
        )

    payment = PaymentRecord(
        student_id=student_id,
        provider="whish",
        amount_usd=MONTHLY_PRICE_USD,
        receiver_reference=WHISH_RECEIVER_NUMBER,
        transaction_reference=payload.transaction_reference,
        status="pending",
        verification_mode="external_api_required",
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "payment_id": payment.id,
        "status": payment.status,
        "amount_usd": payment.amount_usd,
        "receiver_number": WHISH_RECEIVER_NUMBER,
        "message": (
            "تم تسجيل طلب الدفع. "
            "التفعيل الآلي الكامل يحتاج ربط API رسمي من Whish."
        ),
    }


class AdminActivatePayment(BaseModel):
    payment_id: int


@router.post("/student/{student_id}/payment/activate")
def activate_payment_for_testing(
    student_id: str,
    payload: AdminActivatePayment,
    db: Session = Depends(get_db),
):
    # DEVELOPMENT endpoint only. Protect/remove before public launch.
    payment = (
        db.query(PaymentRecord)
        .filter_by(
            id=payload.payment_id,
            student_id=student_id,
        )
        .first()
    )

    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="عملية الدفع غير موجودة.",
        )

    profile = get_profile(
        db,
        student_id,
    )

    activate_one_month(
        profile
    )

    payment.status = "verified"
    payment.verified_at = datetime.utcnow()

    db.add(profile)
    db.add(payment)
    db.commit()

    return {
        "ok": True,
        "subscription": subscription_state(
            profile
        ),
    }
