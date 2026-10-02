import os
from datetime import datetime, timedelta
from app.db.student_learning import StudentLearningProfile
TRIAL_DAYS=int(os.getenv("NABIL_TRIAL_DAYS","30")); MONTHLY_PRICE_USD=float(os.getenv("NABIL_MONTHLY_PRICE_USD","5")); WHISH_RECEIVER_NUMBER=os.getenv("WHISH_RECEIVER_NUMBER","")
def subscription_state(profile: StudentLearningProfile)->dict:
    now=datetime.utcnow(); paid=profile.subscription_status=="active" and profile.subscription_ends_at and profile.subscription_ends_at>now; trial=profile.trial_ends_at and profile.trial_ends_at>now
    if paid: state,expires="active",profile.subscription_ends_at
    elif trial: state,expires="trial",profile.trial_ends_at
    else: state,expires="expired",profile.subscription_ends_at or profile.trial_ends_at
    remaining=max(0,int((expires-now).total_seconds())) if expires else 0
    return {"state":state,"is_allowed":state in {"active","trial"},"expires_at":expires.isoformat() if expires else None,"remaining_seconds":remaining,"remaining_days":remaining//86400,"monthly_price_usd":MONTHLY_PRICE_USD,"whish_receiver_configured":bool(WHISH_RECEIVER_NUMBER),"receiver_number":WHISH_RECEIVER_NUMBER}
def activate_one_month(profile: StudentLearningProfile):
    now=datetime.utcnow(); start=profile.subscription_ends_at if profile.subscription_ends_at and profile.subscription_ends_at>now else now
    profile.subscription_status="active"; profile.subscription_started_at=profile.subscription_started_at or now; profile.subscription_ends_at=start+timedelta(days=30)
