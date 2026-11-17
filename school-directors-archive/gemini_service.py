"""Gemini Vision extraction for the NABIL School Directors Archive.

Original pages are saved to Google Drive by app.py before this module is called.
This module only reads the ordered image bytes and returns validated JSON data.
"""
import json
import os
import re
import time

from google import genai
from google.genai import types


class GeminiError(Exception):
    pass


class GeminiNotConfigured(GeminiError):
    pass


PROMPT = """أنت موظف أرشفة خبير بالمستندات الإدارية والتربوية اللبنانية.
اقرأ كل الصور المرفقة باعتبارها صفحات متتابعة لمستند واحد، وبالترتيب الذي أرسلت به.
انقل النص كاملاً قدر الإمكان، مع الحفاظ على ترتيب الصفحات والفقرات والأرقام.
افحص أعلى الصفحة وأسفلها والترويسة والتذييل والتوقيع والختم وأي تاريخ مكتوب بخط اليد.
استخرج رقم هذا المستند وتاريخ إصداره هو، ولا تخلطهما بأرقام وتواريخ القوانين أو القرارات التي يذكرها النص.
استخرج الجهة المصدرة والموضوع، وسجّل كل قرار أو تعميم مشار إليه في قائمة المراجع بصورة منفصلة.
لا تخمّن ولا تستنتج رقماً أو تاريخاً غير ظاهر. عند عدم وضوح أي معلومة اتركها فارغة واكتب سبب الالتباس في review_notes.
لا ترفض المستند بسبب ضعف صورة أو نقص البيانات. أعد النص المتاح حتى لو تعذر تحديد البيانات الوصفية.
استخدم العربية كما تظهر في المستند، ولا تترجم النص ولا تلخصه.
"""


RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "document_type": {"type": "STRING"},
        "document_number": {"type": "STRING"},
        "document_date": {"type": "STRING"},
        "issuer": {"type": "STRING"},
        "subject": {"type": "STRING"},
        "full_text": {"type": "STRING"},
        "referenced_decisions": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "reference_type": {"type": "STRING"},
                    "reference_number": {"type": "STRING"},
                    "reference_date": {"type": "STRING"},
                },
                "required": ["reference_type", "reference_number", "reference_date"],
            },
        },
        "field_confidence": {
            "type": "OBJECT",
            "properties": {
                "document_type": {"type": "STRING", "enum": ["high", "medium", "low"]},
                "document_number": {"type": "STRING", "enum": ["high", "medium", "low"]},
                "document_date": {"type": "STRING", "enum": ["high", "medium", "low"]},
                "issuer": {"type": "STRING", "enum": ["high", "medium", "low"]},
                "subject": {"type": "STRING", "enum": ["high", "medium", "low"]},
            },
            "required": ["document_type", "document_number", "document_date", "issuer", "subject"],
        },
        "data_verified": {"type": "BOOLEAN"},
        "review_notes": {"type": "STRING"},
    },
    "required": [
        "document_type", "document_number", "document_date", "issuer", "subject",
        "full_text", "referenced_decisions", "field_confidence", "data_verified",
        "review_notes",
    ],
}


def _client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiNotConfigured("GEMINI_API_KEY غير مضبوط في إعدادات Render")
    return genai.Client(api_key=api_key)


def _is_transient(exc):
    code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
    if code in (408, 409, 429, 500, 502, 503, 504):
        return True
    message = str(exc).lower()
    return any(token in message for token in (
        "429", "resource_exhausted", "503", "502", "500",
        "deadline", "timed out", "temporarily unavailable",
        "connection reset", "connection error",
    ))


def analyze_document_images(images):
    """Analyze ordered image dicts: {bytes: ..., mime_type: ...}."""
    if not images:
        raise GeminiError("لا توجد صور لإرسالها إلى Gemini")

    model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()
    contents = [types.Part.from_text(text=PROMPT)]

    for index, image in enumerate(images, start=1):
        data = image.get("bytes")
        mime_type = image.get("mime_type")
        if not data or not mime_type or not mime_type.startswith("image/"):
            raise GeminiError(f"بيانات الصورة رقم {index} أو نوعها غير صالح")
        contents.append(types.Part.from_bytes(data=data, mime_type=mime_type))

    client = _client()
    last_error = None
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    response_mime_type="application/json",
                    response_schema=RESPONSE_SCHEMA,
                    max_output_tokens=16000,
                ),
            )
            response_text = (response.text or "").strip()
            if not response_text:
                raise GeminiError("Gemini أعاد نتيجة فارغة")
            result = json.loads(response_text)
            if not isinstance(result, dict):
                raise GeminiError("تنسيق نتيجة Gemini غير صالح")

            # Normalize the contract consumed by app.py; never promote missing data.
            for key in ("document_type", "document_number", "document_date",
                        "issuer", "subject", "full_text", "review_notes"):
                value = result.get(key, "")
                result[key] = value.strip() if isinstance(value, str) else ""

            result["referenced_decisions"] = (
                result.get("referenced_decisions")
                if isinstance(result.get("referenced_decisions"), list) else []
            )
            confidence = result.get("field_confidence")
            result["field_confidence"] = confidence if isinstance(confidence, dict) else {}
            result["data_verified"] = bool(
                result.get("data_verified")
                and result["document_number"]
                and result["document_date"]
                and result["subject"]
            )
            return result
        except Exception as exc:
            last_error = exc
            if attempt == 2 or not _is_transient(exc):
                break
            time.sleep(2 ** attempt)

    raise GeminiError(f"تعذرت معالجة المستند بواسطة Gemini: {str(last_error)[:700]}")
