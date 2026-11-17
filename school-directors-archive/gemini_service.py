"""Gemini vision extraction for NABIL School Directors Archive.

Uses the Gemini REST API so the service does not need a heavyweight OCR process.
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request


class GeminiError(Exception):
    pass


class GeminiNotConfigured(GeminiError):
    pass


PROMPT = """أنت نظام أرشفة رسمي للمستندات الإدارية والتربوية اللبنانية.
اقرأ جميع الصور المرفقة بالترتيب الذي أرسلت به. قد تكون صفحات متتابعة لوثيقة واحدة.
افحص الصفحة كاملة بما فيها الترويسة والتذييل والتوقيع والختم، وابحث عن تاريخ إصدار المستند حتى لو كان أسفل الصفحة أو بخط اليد.
لا تخلط بين تاريخ هذا المستند وبين تواريخ وأرقام القرارات أو التعاميم التي يشير إليها داخله.
لا تخمّن أي معلومة غير مقروءة. احتفظ بالنص كما يظهر قدر الإمكان، ولا تلخّصه.
أعد JSON فقط بالمفاتيح التالية:
{
 "document_type": "نوع المستند أو نص فارغ",
 "document_number": "رقم المستند نفسه أو نص فارغ",
 "document_date": "تاريخ إصدار المستند نفسه بصيغة YYYY-MM-DD إذا كان واضحاً، وإلا النص الظاهر أو نص فارغ",
 "issuer": "الجهة المصدرة أو نص فارغ",
 "subject": "الموضوع أو عنوان واضح أو نص فارغ",
 "full_text": "النص الكامل لجميع الصفحات بالترتيب، مع فواصل واضحة بين الصفحات",
 "referenced_decisions": [
   {"reference_type":"نوع المرجع","reference_number":"الرقم","reference_date":"التاريخ"}
 ],
 "field_confidence": {
   "document_type":"high|medium|low",
   "document_number":"high|medium|low",
   "document_date":"high|medium|low",
   "issuer":"high|medium|low",
   "subject":"high|medium|low"
 },
 "data_verified": true,
 "review_notes": "أي التباس أو حقل غير مقروء"
}
اجعل data_verified true فقط إذا كان رقم المستند وتاريخه وموضوعه واضحين من المستند نفسه.
إذا تعذر استخراج أي حقل، اتركه فارغاً ولا تضع عبارة تخمينية. لا ترفض المستند بسبب ضعف الصورة.
"""


def analyze_document_images(images):
    """images: list of dicts with keys bytes and mime_type; preserves list order."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiNotConfigured("GEMINI_API_KEY غير مضبوط في إعدادات Render")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    parts = [{"text": PROMPT}]
    for image in images:
        parts.append({
            "inline_data": {
                "mime_type": image["mime_type"],
                "data": __import__("base64").b64encode(image["bytes"]).decode("ascii"),
            }
        })
    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json",
        },
    }
    url = "https://generativelanguage.googleapis.com/v1beta/models/" + urllib.parse.quote(model, safe="") + ":generateContent?key=" + urllib.parse.quote(api_key, safe="")
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    last_error = None
    for attempt in range(3):
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=110) as response:
                raw = json.loads(response.read().decode("utf-8"))
            candidates = raw.get("candidates") or []
            if not candidates:
                raise GeminiError("Gemini لم يُرجع نتيجة قابلة للقراءة")
            text_parts = candidates[0].get("content", {}).get("parts", [])
            response_text = "".join(p.get("text", "") for p in text_parts).strip()
            if not response_text:
                raise GeminiError("Gemini أعاد نصاً فارغاً")
            result = json.loads(response_text)
            if not isinstance(result, dict):
                raise GeminiError("تنسيق نتيجة Gemini غير صالح")
            return result
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")[:1200]
            last_error = f"Gemini HTTP {exc.code}: {body}"
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, GeminiError) as exc:
            last_error = str(exc)
            if attempt == 2:
                break
        time.sleep(2 ** attempt)
    raise GeminiError(last_error or "تعذرت معالجة المستند بواسطة Gemini")
