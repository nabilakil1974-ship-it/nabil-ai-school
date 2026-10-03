from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.student_learning import StudentLearningProfile
from app.db.subscription import PaymentRecord
from app.services.payment_verification import verify_activation_code
from app.services.subscription_service import MONTHLY_PRICE_USD, WHISH_RECEIVER_NUMBER, activate_one_month, subscription_state

router = APIRouter()


def get_profile(db: Session, student_id: str) -> StudentLearningProfile:
    sid = str(student_id or "").strip()
    if not sid:
        raise HTTPException(status_code=422, detail="student_id is required")
    profile = db.query(StudentLearningProfile).filter_by(student_id=sid).first()
    if profile is None:
        profile = StudentLearningProfile(student_id=sid)
        db.add(profile); db.commit(); db.refresh(profile)
    return profile


@router.get("/student/{student_id}/dashboard")
def student_dashboard(student_id: str, db: Session = Depends(get_db)):
    profile = get_profile(db, student_id)
    return {
        "student_id": profile.student_id, "current_grade": profile.current_grade,
        "current_branch": profile.current_branch, "current_subject": profile.current_subject,
        "current_lesson": profile.current_lesson, "overall_progress_percent": profile.overall_progress_percent,
        "mastered_lessons_count": profile.mastered_lessons_count, "total_learning_minutes": profile.total_learning_minutes,
        "interaction_count": profile.interaction_count, "last_active_activity": profile.last_active_activity,
        "lessons_studied": profile.loads_list(profile.lessons_studied_json),
        "strengths": profile.loads_list(profile.strengths_json), "weaknesses": profile.loads_list(profile.weaknesses_json),
        "frequent_mistakes": profile.loads_list(profile.frequent_mistakes_json),
        "concepts_to_review": profile.loads_list(profile.concepts_to_review_json),
        "test_results": profile.loads_list(profile.test_results_json), "subscription": subscription_state(profile),
    }


@router.get("/student/{student_id}/subscription")
def get_subscription(student_id: str, db: Session = Depends(get_db)):
    return subscription_state(get_profile(db, student_id))


class PaymentRequest(BaseModel):
    transaction_reference: str | None = Field(default=None, max_length=255)


@router.post("/student/{student_id}/payment/whish")
def submit_whish_payment(student_id: str, payload: PaymentRequest, db: Session = Depends(get_db)):
    if not WHISH_RECEIVER_NUMBER:
        raise HTTPException(status_code=503, detail="رقم Whish غير مضبوط بعد.")
    tx = str(payload.transaction_reference or "").strip().upper() or None
    if tx:
        existing = db.query(PaymentRecord).filter(PaymentRecord.transaction_reference == tx).first()
        if existing:
            return {"payment_id": existing.id, "status": existing.status, "amount_usd": existing.amount_usd,
                    "receiver_number": WHISH_RECEIVER_NUMBER, "message": "هذه العملية مسجلة مسبقًا."}
    payment = PaymentRecord(student_id=str(student_id).strip(), provider="whish", amount_usd=MONTHLY_PRICE_USD,
                            receiver_reference=WHISH_RECEIVER_NUMBER, transaction_reference=tx,
                            status="pending_receipt_email", verification_mode="gmail_receipt_ocr")
    db.add(payment); db.commit(); db.refresh(payment)
    return {"payment_id": payment.id, "status": payment.status, "amount_usd": payment.amount_usd,
            "receiver_number": WHISH_RECEIVER_NUMBER, "payment_email": "paymentnabilai@gmail.com",
            "message": "أرسل صورة إيصال Whish إلى بريد الدفع مع رقم هاتف حساب NABIL. يتم الفحص آليًا كل 30 دقيقة."}


class ActivationRequest(BaseModel):
    transaction_reference: str = Field(min_length=5, max_length=255)
    activation_code: str = Field(min_length=10, max_length=80)


@router.post("/student/{student_id}/payment/activate")
def activate_verified_payment(student_id: str, payload: ActivationRequest, db: Session = Depends(get_db)):
    sid = str(student_id or "").strip(); tx = str(payload.transaction_reference or "").strip().upper()
    payment = (db.query(PaymentRecord).filter(PaymentRecord.student_id == sid,
               PaymentRecord.transaction_reference == tx).order_by(PaymentRecord.id.desc()).first())
    if payment is None:
        raise HTTPException(status_code=404, detail="عملية الدفع غير موجودة لهذا الحساب.")
    if payment.status == "verified":
        raise HTTPException(status_code=409, detail="تم استخدام هذه العملية وتفعيل الاشتراك مسبقًا.")
    if payment.status != "verified_pending_activation":
        raise HTTPException(status_code=409, detail="الإيصال لم يُعتمد آليًا بعد.")
    if not verify_activation_code(sid, tx, payload.activation_code):
        raise HTTPException(status_code=403, detail="رمز التفعيل غير صحيح.")
    profile = get_profile(db, sid); activate_one_month(profile)
    payment.status = "verified"; payment.verified_at = datetime.utcnow()
    db.add(profile); db.add(payment); db.commit(); db.refresh(profile)
    return {"ok": True, "subscription": subscription_state(profile)}
