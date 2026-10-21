"""Student-facing cleanliness gate (LL-25): nothing internal may reach the student's screen or voice."""
import re
from typing import Any, Dict, List

BANNED = re.compile(r"\b(Golden|QA|UNVERIFIED|Claude|Anthropic|factory|debug|TODO|PLACEHOLDER)\b|Student\s*p\.?\s*\d|Teacher\s*(guide|p\.)|Guide\s*p\.?\s*\d|source_(page|figure)|"
                    r"مصنع|دليل المعلم|ص\.?\s*الدليل", re.I)
TEXT_KEYS = ("text", "en", "fr", "ar", "label", "hint", "speech", "speech_en", "speech_fr", "speech_ar", "title", "title_en", "title_fr", "title_ar", "caption")


def audit_student_text(scenes: List[Dict[str, Any]]) -> Dict[str, Any]:
    hits = []
    for si, sc in enumerate(scenes or []):
        for k in ("title", "title_en", "title_fr", "title_ar"):
            if isinstance(sc.get(k), str) and BANNED.search(sc[k]):
                hits.append((si, None, k, sc[k][:60]))
        for ti, st in enumerate(sc.get("steps") or []):
            for k in TEXT_KEYS:
                v = st.get(k)
                if isinstance(v, str) and BANNED.search(v):
                    hits.append((si, ti, k, v[:60]))
            args = st.get("args") if isinstance(st.get("args"), dict) else {}
            for k in ("caption", "label"):
                if isinstance(args.get(k), str) and BANNED.search(args[k]):
                    hits.append((si, ti, "args." + k, args[k][:60]))
    return {"verdict": "FAIL" if hits else "PASS", "hits": hits}
