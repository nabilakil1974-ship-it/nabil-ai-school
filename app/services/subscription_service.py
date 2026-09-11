import os
from datetime import datetime, timedelta

from app.db.student_learning import StudentLearningProfile


TRIAL_DAYS = int(os.getenv("NABIL_TRIAL_DAYS", "30"))
MONTHLY_PRICE_USD = float(os.getenv("NABIL_MONTHLY_PRICE_USD", "5"))
WHISH_RECEIVER_NUMBER = os.getenv("WHISH_RECEIVER_NUMBER", "")


def subscription_state(profile: StudentLearningProfile) -> dict:
    now = datetime.utcnow()

    active_paid = (
        profile.subscription_status == "active"
        and profile.subscription_ends_at is not None
        and profile.subscription_ends_at > now
    )

    trial_active = (
        profile.trial_ends_at is not None
        and profile.trial_ends_at > now
    )

    if active_paid:
        state = "active"
        expires_at = profile.subscription_ends_at

    elif trial_active:
        state = "trial"
        expires_at = profile.trial_ends_at

    else:
        state = "expired"
        expires_at = profile.subscription_ends_at or profile.trial_ends_at

    return {
        "state": state,
        "is_allowed": state in {"active", "trial"},
        "expires_at": (
            expires_at.isoformat()
            if expires_at
            else None
        ),
        "monthly_price_usd": MONTHLY_PRICE_USD,
        "whish_receiver_configured": bool(WHISH_RECEIVER_NUMBER),
        "receiver_number": WHISH_RECEIVER_NUMBER,
    }


def activate_one_month(profile: StudentLearningProfile):
    now = datetime.utcnow()

    if (
        profile.subscription_ends_at is not None
        and profile.subscription_ends_at > now
    ):
        start = profile.subscription_ends_at
    else:
        start = now

    profile.subscription_status = "active"
    profile.subscription_started_at = (
        profile.subscription_started_at
        or now
    )
    profile.subscription_ends_at = (
        start + timedelta(days=30)
    )
