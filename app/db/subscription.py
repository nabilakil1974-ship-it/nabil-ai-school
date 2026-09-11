from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from app.db.session import Base


class PaymentRecord(Base):
    __tablename__ = "payment_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(255), nullable=False, index=True)
    provider = Column(String(50), nullable=False, default="whish")
    amount_usd = Column(Float, nullable=False, default=5.0)
    receiver_reference = Column(String(255), nullable=True)
    transaction_reference = Column(String(255), nullable=True, index=True)

    status = Column(String(40), nullable=False, default="pending")
    verification_mode = Column(
        String(60),
        nullable=False,
        default="manual_or_external_api",
    )

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
