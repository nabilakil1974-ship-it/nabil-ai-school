"""NABIL payment inbox worker. Local OCR only; uncertain receipts fail closed to manual review."""
from __future__ import annotations
import email, imaplib, os, re, smtplib
from email.message import EmailMessage
from app.db.session import SessionLocal
from app.db.subscription import PaymentRecord
from app.services.payment_verification import make_activation_code, ocr_receipt, parse_whish_receipt, receipt_sha256, validate_whish_receipt

PAYMENT_EMAIL=os.getenv("NABIL_PAYMENT_EMAIL","paymentnabilai@gmail.com")
IMAP_PASSWORD=os.getenv("NABIL_PAYMENT_GMAIL_APP_PASSWORD","")
SMTP_PASSWORD=IMAP_PASSWORD
PHONE_RE=re.compile(r"(?:\+?961)?\s*(\d{7,8})")

def _student_id(msg):
    hay=" ".join([str(msg.get("Subject") or ""),str(msg.get("From") or "")])
    for part in msg.walk():
        if part.get_content_type()=="text/plain":
            try: hay+=" "+part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8","replace")
            except Exception: pass
    m=PHONE_RE.search(hay); return m.group(1) if m else ""

def _attachments(msg):
    for part in msg.walk():
        ctype=part.get_content_type()
        if ctype.startswith("image/") or ctype=="application/pdf":
            data=part.get_payload(decode=True)
            if data:
                suffix=".pdf" if ctype=="application/pdf" else "."+ctype.split("/",1)[1].replace("jpeg","jpg")
                yield data,suffix

def _send_code(to_addr,code,student_id,tx):
    if not to_addr or "@" not in to_addr:return
    m=EmailMessage();m["From"]=PAYMENT_EMAIL;m["To"]=to_addr;m["Subject"]="NABIL AI activation code"
    m.set_content(f"Payment verified for NABIL account {student_id}.\nTransaction reference: {tx}\nActivation code: {code}\nThis transaction can activate one subscription only.")
    with smtplib.SMTP_SSL("smtp.gmail.com",465,timeout=30) as s:s.login(PAYMENT_EMAIL,SMTP_PASSWORD);s.send_message(m)

def _manual(db,student_id,tx,reason):
    p=PaymentRecord(student_id=student_id or "unknown",provider="whish",amount_usd=0.0,
                    receiver_reference=os.getenv("WHISH_RECEIVER_NUMBER",""),transaction_reference=tx or None,
                    status="manual_review",verification_mode=("manual:"+reason.replace(",","+"))[:60])
    db.add(p);db.commit()

def process_message(msg):
    student_id=_student_id(msg)
    if not student_id:return "manual_review:no_student_phone"
    db=SessionLocal()
    try:
        saw=False
        for data,suffix in _attachments(msg):
            saw=True;digest=receipt_sha256(data);digest_tag="ocr:"+digest[:56]
            if db.query(PaymentRecord).filter(PaymentRecord.verification_mode==digest_tag).first():return "duplicate_receipt"
            try:text=ocr_receipt(data,suffix=suffix)
            except Exception:_manual(db,student_id,None,"ocr_failed");return "manual_review:ocr_failed"
            parsed=parse_whish_receipt(text);tx=str(parsed.get("transaction_reference") or "").strip().upper()
            if tx and db.query(PaymentRecord).filter(PaymentRecord.transaction_reference==tx).first():return "duplicate_transaction"
            ok,errors=validate_whish_receipt(parsed)
            if not ok:_manual(db,student_id,tx or None,",".join(errors) or "invalid_receipt");return "manual_review:"+",".join(errors)
            p=PaymentRecord(student_id=student_id,provider="whish",amount_usd=float(parsed["amount_usd"]),
                            receiver_reference=os.getenv("WHISH_RECEIVER_NUMBER",""),transaction_reference=tx,
                            status="verified_pending_activation",verification_mode=digest_tag)
            db.add(p);db.commit();code=make_activation_code(student_id,tx)
            sender=email.utils.parseaddr(msg.get("Reply-To") or msg.get("From") or "")[1];_send_code(sender,code,student_id,tx)
            return "verified_pending_activation"
        return "manual_review:no_attachment" if not saw else "manual_review:no_valid_receipt"
    finally:db.close()

def main():
    if not IMAP_PASSWORD:raise RuntimeError("NABIL_PAYMENT_GMAIL_APP_PASSWORD_NOT_CONFIGURED")
    with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
        imap.login(PAYMENT_EMAIL,IMAP_PASSWORD);imap.select("INBOX");_,data=imap.search(None,"UNSEEN")
        for uid in data[0].split():
            _,raw=imap.fetch(uid,"(RFC822)");msg=email.message_from_bytes(raw[0][1])
            try:result=process_message(msg)
            except Exception as exc:result="worker_error:"+type(exc).__name__
            print(uid.decode(),result)
            if not result.startswith("worker_error"):
                imap.store(uid,"+FLAGS","\\Seen")
if __name__=="__main__":main()
