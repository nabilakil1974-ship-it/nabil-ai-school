"""Prevent a partial textbook exercise set from becoming a complete lesson."""
from collections import Counter
import json


def require_textbook_coverage(expected, actual, stage):
    def identities(rows):
        ids = []
        for row in rows:
            if row.get("source_origin", "TEXTBOOK") != "TEXTBOOK":
                continue
            identity = row.get("exercise_id")
            if not isinstance(identity, str) or not identity.strip():
                raise RuntimeError("TEXTBOOK_EXERCISE_ID_MISSING:" + stage)
            ids.append(identity)
        if len(ids) != len(set(ids)):
            raise RuntimeError("TEXTBOOK_EXERCISE_ID_DUPLICATED:" + stage)
        return Counter(ids)

    required, received = identities(expected), identities(actual)
    if required != received:
        raise RuntimeError("TEXTBOOK_EXERCISE_COVERAGE_INCOMPLETE:" + json.dumps({
            "stage": stage, "missing": list((required - received).elements()),
            "unexpected": list((received - required).elements()),
        }, sort_keys=True))
