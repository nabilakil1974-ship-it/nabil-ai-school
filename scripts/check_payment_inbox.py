"""NABIL payment inbox worker. Reads unseen payment emails, validates Whish receipts locally, never calls AI."""
from __future__ import annotations
import email, imaplib, os, re, smtplib
from email.message import EmailMessage
from app.db.session import SessionLocal
from app.db.subscription import PaymentRecord
from app.db.student_learning import StudentLearningProfile
from app.services.payment_verification import ocr_receipt, parse_whish_receipt, validate_whish_receipt, make_activation_code

PAYMENT_EMAIL = os.getenv("NABIL_PAYMENT_EMAIL", "paymentnabilai@gmail.com")
IMAP_PASSWORD = os.getenv("NABIL_PAYMENT_GMAIL_APP_PASSWORD", "")
SMTP_PASSWORD = os.getenv("NABIL_PAYMENT_GMAIL_APP_PASSWORD", "")
PHONE_RE = re.compile(r"(?:\+?961)?\s*(\d{7,8})")

def _student_id(msg) -> str:
    hay = " ".join([str(msg.get("Subject") or ""), str(msg.get("From") or "")])
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            try: hay += " " + part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
            except Exception: pass
    m = PHONE_RE.search(hay)
    return m.group(1) if m else ""

def _attachments(msg):
    for part in msg.walk():
        ctype = part.get_content_type()
        if ctype.startswith("image/") or ctype == "application/pdf":
            data = part.get_payload(decode=True)
            if data:
                suffix = ".pdf" if ctype == "application/pdf" else "." + ctype.split("/",1)[1].replace("jpeg","jpg")
                yield data, suffix

def _send_code(to_addr: str, code: str, student_id: str):
    if not to_addr or "@" not in to_addr: return
    m = EmailMessage(); m["From"] = PAYMENT_EMAIL; m["To"] = to_addr; m["Subject"] = "NABIL AI activation code"
    m.set_content(f"Payment verified for NABIL account {student_id}. Activation code: {code}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
        s.login(PAYMENT_EMAIL, SMTP_PASSWORD); s.send_message(m)

def process_message(msg) -> str:
    student_id = _student_id(msg)
    if not student_id: return "manual_review:no_student_phone"
    db = SessionLocal()
    try:
        for data, suffix in _attachments(msg):
            try: text = ocr_receipt(data, suffix=suffix)
            except Exception: continue
            parsed = parse_whish_receipt(text); ok, errors = validate_whish_receipt(parsed)
            if not ok: continue
            tx = parsed["transaction_reference"]
            existing = db.query(PaymentRecord).filter(PaymentRecord.transaction_reference == tx).first()
            if existing: return "duplicate_transaction"
            payment = PaymentRecord(student_id=student_id, provider="whish", amount_usd=float(parsed["amount_usd"]),
                                    receiver_reference=os.getenv("WHISH_RECEIVER_NUMBER", ""), transaction_reference=tx,
                                    status="verified_pending_activation", verification_mode="receipt_ocr_strict")
            db.add(payment); db.commit()
            code = make_activation_code(student_id, tx)
            sender = email.utils.parseaddr(msg.get("Reply-To") or msg.get("From") or "")[1]
            _send_code(sender, code, student_id)
            return "verified_pending_activation"
        return "manual_review:no_valid_receipt"
    finally: db.close()

def main():
    if not IMAP_PASSWORD: raise RuntimeError("NABIL_PAYMENT_GMAIL_APP_PASSWORD_NOT_CONFIGURED")
    with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(PAYMENT_EMAIL, IMAP_PASSWORD); imap.select("INBOX")
        _, data = imap.search(None, 'UNSEEN')
        for uid in data[0].split():
            _, raw = imap.fetch(uid, "(RFC822)")
            msg = email.message_from_bytes(raw[0][1])
            result = process_message(msg)
            print(uid.decode(), result)
            if result.startswith("verified") or result.startswith("duplicate"):
                imap.store(uid, "+FLAGS", "\\Seen")
if __name__ == "__main__": main()
