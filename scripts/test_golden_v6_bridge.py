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

# --- master lab (original drawings + steps + book exercises) and the honest status badge
import json
cat = {x["lesson_id"]: x for x in json.loads(pathlib.Path("data/NABIL_GOLDEN_CATALOGUE.json").read_text(encoding="utf-8"))["lessons"]}
e12 = cat["G12-MATH-GS-001"]
t12 = pathlib.Path("data/golden_artifacts/G12-MATH-GS-001.txt").read_text(encoding="utf-8")
p12 = build_v6_page(e12, t12, {"language": "English"})
assert p12 and "svgScene" in p12 and "Drive master lab" in p12, "G12 must be built from the master lab with its drawings"
assert '"completeness": "partial:' in p12 and "status_text" in p12, "missing parts must be declared, never hidden"
assert "EX12 (p.17)" in p12 and '"solved": true' in p12, "verified book exercises must be offered with their solutions"
assert "nbSolveBtn" in p12 and "nbToolsToggle" in p12 and "data-nb-plan" in p12
assert p12.index('id="nbSolveBtn"') < p12.index('id="nbToolsToggle"'), "Solve button is in the header, tools are collapsed below"
p1 = build_v6_page(cat["G01-MATH-EN-002"], T, {"language": "English"})
assert "drawings" in p1 and "verified exercise solutions" in p1 and "partial:drawings,solutions,labs" in p1
print("golden v6 bridge (master lab + status): PASS")
