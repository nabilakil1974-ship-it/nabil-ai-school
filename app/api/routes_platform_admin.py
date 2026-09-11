from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.student_learning import StudentLearningProfile
from app.db.subscription import PaymentRecord

router = APIRouter()


@router.get("/platform-summary")
def platform_summary(
    db: Session = Depends(get_db),
):
    total_students = (
        db.query(StudentLearningProfile)
        .count()
    )

    active_students = (
        db.query(StudentLearningProfile)
        .filter(
            StudentLearningProfile.interaction_count > 0
        )
        .count()
    )

    pending_payments = (
        db.query(PaymentRecord)
        .filter_by(status="pending")
        .count()
    )

    verified_payments = (
        db.query(PaymentRecord)
        .filter_by(status="verified")
        .count()
    )

    return {
        "total_students": total_students,
        "active_students": active_students,
        "pending_payments": pending_payments,
        "verified_payments": verified_payments,
    }
