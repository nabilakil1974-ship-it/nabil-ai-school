"""Unit tests of the exercise solver service. A fake gateway is used HERE ONLY (unit tests);
it proves parsing/validation/safety logic, not the quality of a real model."""
import os, sys, pathlib, json, subprocess, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
from app.services import exercise_solver as sv

FAILS = []
def ok(name, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + name + ("" if cond else "  -> " + str(detail)))
    if not cond: FAILS.append(name)

class FakeGW:
    def __init__(self, reply): self.reply, self.calls = reply, []
    def generate(self, instructions, messages, image_bytes=None, image_mime_type="image/jpeg", max_output_tokens=1400, fast_lesson=False):
        self.calls.append({"img": image_bytes is not None, "instr": instructions, "msg": messages[0]["content"]}); return self.reply

def with_gw(reply):
    gw = FakeGW(reply)
    sv._gateway = lambda: gw
    return gw

# --- no provider configured: honest error, never a fake answer
for k in sum((list(v) for v in sv.PROVIDER_ENV.values()), []): os.environ.pop(k, None)
try:
    sv._gateway = sv.__dict__["_gateway"].__wrapped__ if hasattr(sv._gateway, "__wrapped__") else sv._gateway
except Exception: pass
import importlib; importlib.reload(sv)
try:
    sv.solve(statement="x+1=2"); ok("no provider -> PROVIDER_NOT_CONFIGURED", False)
except sv.SolverError as e:
    ok("no provider -> PROVIDER_NOT_CONFIGURED (503, honest message)", e.code == "PROVIDER_NOT_CONFIGURED" and e.http == 503)
ok("status never exposes key values", json.dumps(sv.providers_status()).count("sk-") == 0 and all(isinstance(v, bool) for v in sv.providers_status()["providers"].values()))

# --- typed question needs no model
r = sv.read_statement(text="  2x + 3 = 7  ", lang="ar")
ok("typed question is returned as typed (no provider call)", r["status"] == "ok" and r["statement"] == "2x + 3 = 7" and r["source"] == "typed")

# --- JSON extraction
ok("extract_json handles code fences", sv.extract_json('```json\n{"a":1}\n```') == {"a": 1})
ok("extract_json handles chatter around JSON", sv.extract_json('Sure! {"a": 2} done') == {"a": 2})
try: sv.extract_json("no json"); ok("extract_json rejects non-JSON", False)
except sv.SolverError as e: ok("extract_json rejects non-JSON", e.code == "BAD_MODEL_OUTPUT")

# --- normalise: clarification, incomplete, sanitising
ok("needs_clarification is passed through with questions", sv.normalise_solution({"needs_clarification": True, "questions": ["what is AB?"]})["status"] == "needs_clarification")
try: sv.normalise_solution({"steps": [{"text": "x"}], "answer": "1"}); ok("one-step 'solution' rejected", False)
except sv.SolverError as e: ok("one-step 'solution' rejected as incomplete", e.code == "INCOMPLETE_SOLUTION")
good = {"title": "Linear", "given": ["2x+3=7"], "required": ["x"],
        "figure": {"points": {"A": [0, 0], "B": [4, 0], "C": [0, 3], "Z": ["bad", 1]}, "segments": [["A", "B", "4 cm"], ["A", "Q"], ["B", "C"]],
                   "marks": [{"type": "right_angle", "at": "A", "between": ["B", "C"]}, {"type": "right_angle", "at": "Q", "between": ["B", "C"]}]},
        "steps": [{"say": "We subtract 3", "text": "Subtract 3 from both sides.", "formula": "2x = 4", "justification": "Equality is kept"},
                  {"say": "We divide", "text": "Divide both sides by 2.", "formula": "x = 2"}],
        "answer": "x = 2", "machine_check": {"equation": "2*x+3=7", "variable": "x", "solutions": ["2"]}}
n = sv.normalise_solution(json.loads(json.dumps(good)))
ok("figure keeps valid points/segments only", set(n["figure"]["points"]) == {"A", "B", "C"} and len(n["figure"]["segments"]) == 2 and len(n["figure"]["marks"]) == 1, n["figure"])
ok("machine check verifies a correct equation answer", n["verification"]["status"] == "verified", n["verification"])
bad = json.loads(json.dumps(good)); bad["machine_check"]["solutions"] = ["3"]
ok("machine check flags a wrong answer as mismatch", sv.normalise_solution(bad)["verification"]["status"] == "mismatch")
inj = json.loads(json.dumps(good)); inj["machine_check"]["equation"] = "__import__('os').system('id')=0"
ok("machine check refuses code-like input (not_checked)", sv.normalise_solution(inj)["verification"]["status"] == "not_checked")
quad = json.loads(json.dumps(good)); quad["machine_check"] = {"equation": "x^2-5*x+6=0", "variable": "x", "solutions": ["2", "3"]}
ok("quadratic roots verified", sv.normalise_solution(quad)["verification"]["status"] == "verified")

# --- solve via fake gateway: statement is passed, language is requested, confirmed only
gw = with_gw(json.dumps(good))
out = sv.solve(statement="Solve 2x+3=7", lang="fr", grade="7", subject="Mathematics")
ok("solve returns normalised solution and keeps the statement", out["status"] == "ok" and out["statement"] == "Solve 2x+3=7" and out["lang"] == "fr")
ok("solve prompt asks for the student's terminology language", "in French" in gw.calls[0]["instr"])
ok("solve sends the student's confirmed text to the model", "Solve 2x+3=7" in gw.calls[0]["msg"])

# --- image reading: the model is told never to guess; unclear parts force clarification
gw = with_gw(json.dumps({"statement": "Find x if 3x + ? = 9", "unclear": ["digit after + is cut off"], "has_figure": False, "figure_description": ""}))
r = sv.read_statement(file_bytes=b"\xff\xd8\xff\xe0fake-jpeg", mime="image/jpeg")
ok("image with unclear part -> needs_clarification (never silently guessed)", r["status"] == "needs_clarification" and r["unclear"] and gw.calls[0]["img"])
gw = with_gw(json.dumps({"statement": "", "unclear": ["blurry"], "has_figure": False}))
ok("unreadable image -> unreadable", sv.read_statement(file_bytes=b"\xff\xd8\xff\xe0x", mime="image/jpeg")["status"] == "unreadable")
try: sv.read_statement(file_bytes=b"GIF89a", mime="image/gif"); ok("unsupported type rejected", False)
except sv.SolverError as e: ok("unsupported type rejected (415)", e.http == 415)
try: sv.read_statement(file_bytes=b"x" * (sv.MAX_UPLOAD_BYTES + 1), mime="image/png"); ok("oversize rejected", False)
except sv.SolverError as e: ok("oversize upload rejected (413)", e.http == 413)

# --- PDF with a text layer is read WITHOUT a model
def make_pdf(text):
    body = f"BT /F1 14 Tf 72 720 Td ({text}) Tj ET"
    objs = ["<</Type/Catalog/Pages 2 0 R>>", "<</Type/Pages/Kids[3 0 R]/Count 1>>",
            "<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>",
            f"<</Length {len(body)}>>\nstream\n{body}\nendstream", "<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>"]
    out, offs = b"%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out)); out += f"{i} 0 obj\n{o}\nendobj\n".encode()
    x = len(out); out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
    for o in offs: out += f"{o:010d} 00000 n \n".encode()
    return out + f"trailer<</Size {len(objs)+1}/Root 1 0 R>>\nstartxref\n{x}\n%%EOF".encode()
gw = with_gw("{}")
r = sv.read_statement(file_bytes=make_pdf("Exercise 4: Solve the equation 3x - 5 = 10 and check your answer."), mime="application/pdf")
ok("text PDF read through pdftotext, no model call", r["status"] == "ok" and "3x - 5 = 10" in r["statement"] and not gw.calls, r)
try: sv.read_statement(file_bytes=b"not a pdf", mime="application/pdf"); ok("fake PDF rejected", False)
except sv.SolverError as e: ok("fake PDF rejected", e.code == "NOT_A_PDF")

print(f"\n{'ALL PASSED' if not FAILS else str(len(FAILS)) + ' FAILED'}")
sys.exit(1 if FAILS else 0)
