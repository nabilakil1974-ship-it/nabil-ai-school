import json, re, sys
from pathlib import Path
src = (Path(__file__).resolve().parents[1] / "scripts/nabil_factory/p1/source_pipeline.py").read_text(encoding="utf-8")
a = src.index("_LATEX_CMD_RE = re.compile(")
b = src.index("def _execute_llm_json_strict(")
ns = {"json": json, "re": re}
exec(src[a:b], ns)
salvage = ns["salvage_llm_json"]


def test_valid_unchanged():
    assert salvage('{"items":[{"id":"1","text":"x"}]}') == ({"items": [{"id": "1", "text": "x"}]}, "none")


def test_latex_backslashes_and_fence_repaired_without_changing_content():
    raw = '```json\n{"items":[{"id":"1","text":"احسب \\(67 \\times 10^2\\) = 6700"}]}\n```'
    v, m = salvage(raw)
    assert m == "syntax_repair"
    assert v["items"][0]["text"] == "احسب \\(67 \\times 10^2\\) = 6700"


def test_raw_newline_and_trailing_comma():
    v, _ = salvage('{"a":"line1\nline2","b":[1,2,],}')
    assert v == {"a": "line1\nline2", "b": [1, 2]}


def test_truncated_is_not_completed():
    import pytest
    with pytest.raises(json.JSONDecodeError):
        salvage('{"items":[{"id":"1","text":"abc')
