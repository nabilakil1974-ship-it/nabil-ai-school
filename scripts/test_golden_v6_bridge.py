"""Golden artifact -> V6 board adapter: nothing invented, Arabic opening only on Arabic boards."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from app.services.golden_v6_bridge import parse_golden_text, build_v6_page

T = pathlib.Path("data/golden_artifacts/G01-MATH-EN-002.txt").read_text(encoding="utf-8")
en = parse_golden_text(T, "en")
ar = parse_golden_text(T, "ar")
assert en["scenes"][0]["id"].endswith("C01"), "English board must not start with the Arabic opening"
assert ar["scenes"][0]["id"] == "opening"
body = " ".join(l for s in en["scenes"] for l in s["lines"])
assert "⭐ = one = 1" in body and en["summary"][0] == "⭐ = one = 1"
page = build_v6_page({"lesson_id": "G01-MATH-EN-002", "title": "The Numbers from 1 to 3"}, T, {"language": "en"})
assert page and page.startswith("<!doctype html>") and "nabilWholeLessonSmartLab" in page and "viewport" in page
assert build_v6_page({"lesson_id": "x", "title": "x"}, "nothing here", {"language": "en"}) is None
print("golden v6 bridge: PASS")
