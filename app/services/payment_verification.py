from __future__ import annotations
import hashlib, hmac, os, re, secrets, subprocess, tempfile
from datetime import datetime, timezone
from pathlib import Path

RECEIVER_PHONE = re.sub(r"\D", "", os.getenv("WHISH_RECEIVER_NUMBER", ""))
MONTHLY_PRICE_USD = float(os.getenv("NABIL_MONTHLY_PRICE_USD", "5"))
PAYMENT_SECRET = os.getenv("NABIL_PAYMENT_SECRET", "")
MAX_RECEIPT_AGE_HOURS = int(os.getenv("NABIL_PAYMENT_MAX_RECEIPT_AGE_HOURS", "72"))
_TX = re.compile(r"(?:transaction\s*(?:id|reference)|reference\s*(?:id|no\.?))\s*[:#-]?\s*([A-Z0-9-]{5,64})", re.I)
_AMOUNT = re.compile(r"(?:amount\s*[:#-]?\s*)?([0-9]+(?:\.[0-9]{1,2})?)\s*(USD|US\$|\$)", re.I)
_PHONE = re.compile(r"(?:receiver\s*(?:phone\s*)?(?:number)?\s*[:#-]?\s*)?(\+?961\s*\d{7,8})", re.I)
_DATE = re.compile(r"(20\d{2})[\-/](\d{1,2})[\-/](\d{1,2})(?:\s+(\d{1,2}):(\d{2})(?::(\d{2}))?)?")
SUCCESS_WORDS = ("whish to whish", "successful", "success", "completed", "paid", "تمت", "ناجحة")

def receipt_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def ocr_receipt(data: bytes, suffix: str = ".png") -> str:
    """Local OCR only. PDF receipts are rendered to PNG first; no AI/network call."""
    with tempfile.TemporaryDirectory(prefix="nabil-whish-") as td:
        root = Path(td); src = root / ("receipt" + (suffix or ".png").lower()); src.write_bytes(data); target = src
        if src.suffix.lower() == ".pdf":
            out = root / "receipt_page"
            proc = subprocess.run(["pdftoppm", "-f", "1", "-singlefile", "-png", "-r", "220", str(src), str(out)],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=45)
            target = root / "receipt_page.png"
            if proc.returncode != 0 or not target.exists(): raise RuntimeError("PAYMENT_PDF_RENDER_FAILED")
        proc = subprocess.run(["tesseract", str(target), "stdout", "-l", "eng+ara", "--psm", "6"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=45)
        if proc.returncode != 0: raise RuntimeError("PAYMENT_OCR_FAILED")
        text = proc.stdout.strip()
        if not text: raise RuntimeError("PAYMENT_OCR_EMPTY")
        return text

def parse_whish_receipt(text: str) -> dict:
    compact = " ".join(str(text or "").split()); tx = _TX.search(compact)
    amounts = [(float(a), c.upper()) for a, c in _AMOUNT.findall(compact)]
    phones = [re.sub(r"\D", "", p) for p in _PHONE.findall(compact)]
    date_match = _DATE.search(compact); occurred_at = None
    if date_match:
        y,m,d,hh,mm,ss = date_match.groups()
        try: occurred_at = datetime(int(y),int(m),int(d),int(hh or 0),int(mm or 0),int(ss or 0),tzinfo=timezone.utc)
        except ValueError: occurred_at = None
    return {"transaction_reference": tx.group(1).strip().upper() if tx else "",
            "amount_usd": amounts[0][0] if amounts else None, "receiver_phones": phones,
            "occurred_at": occurred_at, "success_marker": any(w in compact.casefold() for w in SUCCESS_WORDS), "raw_text": compact}

def validate_whish_receipt(parsed: dict, *, now: datetime | None = None) -> tuple[bool,list[str]]:
    errors=[]; tx=str(parsed.get("transaction_reference") or "").strip()
    if not tx: errors.append("missing_transaction_id")
    amount=parsed.get("amount_usd")
    if amount is None or abs(float(amount)-MONTHLY_PRICE_USD)>0.001: errors.append("wrong_amount")
    if RECEIVER_PHONE:
        phones={re.sub(r"\D","",str(x)) for x in parsed.get("receiver_phones") or []}
        if RECEIVER_PHONE not in phones: errors.append("wrong_receiver")
    else: errors.append("receiver_not_configured")
    if not parsed.get("success_marker"): errors.append("missing_success_marker")
    occurred=parsed.get("occurred_at")
    if occurred is None: errors.append("missing_or_invalid_date")
    else:
        now=now or datetime.now(timezone.utc); age_h=(now-occurred).total_seconds()/3600
        if age_h < -2 or age_h > MAX_RECEIPT_AGE_HOURS: errors.append("receipt_date_out_of_range")
    return (not errors,errors)

def _secret() -> bytes:
    if not PAYMENT_SECRET or len(PAYMENT_SECRET)<24: raise RuntimeError("NABIL_PAYMENT_SECRET_NOT_CONFIGURED")
    return PAYMENT_SECRET.encode()

def make_activation_code(student_id: str, transaction_reference: str) -> str:
    nonce=secrets.token_hex(4).upper(); payload=f"{student_id}|{transaction_reference.upper()}|{nonce}"
    sig=hmac.new(_secret(),payload.encode(),hashlib.sha256).hexdigest()[:12].upper(); return f"NABIL-{nonce}-{sig}"

def verify_activation_code(student_id: str, transaction_reference: str, code: str) -> bool:
    m=re.fullmatch(r"NABIL-([A-F0-9]{8})-([A-F0-9]{12})",str(code or "").strip().upper())
    if not m:return False
    nonce,got=m.groups(); payload=f"{student_id}|{transaction_reference.upper()}|{nonce}"
    expected=hmac.new(_secret(),payload.encode(),hashlib.sha256).hexdigest()[:12].upper(); return hmac.compare_digest(got,expected)
