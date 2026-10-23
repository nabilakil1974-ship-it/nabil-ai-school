"""Test fixtures for the Golden V6 board (lesson DATA only, never board code).

CUBE_SCENES are the approved Cube V6 scenes, converted one-to-one from the
reference template (English voice text + Arabic display text); the only change is
the approved terminology: Sides instead of Edges (F = 6, S = 12, V = 8).
POWERS_ACTIVITIES is a clearly-labelled FIXTURE (not a published lesson).
"""
from scripts.nabil_factory.cards.golden_v6 import build_scenes

CUBE_REF = [
 ("Cube — Faces, Sides and Vertices", [
  ("t", "We draw a cube with six square faces.", "نرسم مكعبًا، ونميّز الوجوه والأضلاع والرؤوس."), ("draw", "cubeOutline"),
  ("t", "A cube has six faces, twelve sides and eight vertices.", "للمكعب ستة وجوه مربعة، واثنا عشر ضلعًا، وثمانية رؤوس."),
  ("formula", "F = 6     S = 12     V = 8"),
  ("t", "All twelve sides have the same length a.", "جميع أضلاع المكعب متساوية في الطول، ونرمز لطول الضلع بالحرف a.")]),
 ("Color the Cube", [
  ("t", "Now the pen colors the visible faces, one by one.", "نلوّن الوجوه الظاهرة واحدًا بعد الآخر، مع الحفاظ على حدود المكعب."),
  ("draw", "cubeOutline"), ("draw", "cubeColor"),
  ("t", "Opposite faces are parallel and equal.", "كل وجهين متقابلين متوازيان ومتساويان في المساحة.")]),
 ("Rotate the Cube", [
  ("t", "We rotate the cube to observe its different faces.", "ندير المكعب تدريجيًا لنشاهد وجوهه المختلفة."),
  ("draw", "cubeOutline"), ("draw", "cubeColor"), ("draw", "cubeRotate"),
  ("t", "Rotation does not change the side length or volume.", "الدوران لا يغيّر طول الضلع ولا حجم المكعب.")]),
 ("Unfold — Net of a Cube", [
  ("t", "The six square faces can open into a flat net.", "نفتح وجوه المكعب الستة تدريجيًا لتصبح شبكة مستوية."),
  ("draw", "cubeOutline"), ("draw", "cubeColor"), ("draw", "cubeUnfold"),
  ("t", "Every square in the net has the same side length.", "كل مربع في الشبكة له طول الضلع نفسه a."),
  ("formula", "Total surface area = 6a^{2}")]),
 ("Worked Example — Volume and Area", [
  ("t", "Suppose the side length of the cube is four centimeters.", "مثال: مكعب طول ضلعه أربعة سنتيمترات، أوجد حجمه ومساحته الكلية."),
  ("draw", "cubeOutline"), ("draw", "cubeColor"), ("formula", "a = 4 cm"),
  ("t", "The volume is the cube of the side length.", "حجم المكعب يساوي مكعب طول ضلعه."),
  ("formula", "V = a^{3}"), ("formula", "V = 4^{3} = 4 × 4 × 4"), ("formula", "V = 64 cm^{3}"),
  ("t", "The total area is the area of one face multiplied by six.", "المساحة الكلية تساوي مساحة الوجه الواحد مضروبة بستة."),
  ("formula", "A = 6a^{2}"), ("formula", "A = 6 × 4^{2} = 6 × 16"), ("formula", "A = 96 cm^{2}")]),
]


def cube_scenes(display="ar"):
    scenes = []
    for title, steps in CUBE_REF:
        out = []
        for s in steps:
            if s[0] == "t":
                out.append({"t": "text", "text": s[2] if display == "ar" else s[1], "label": "", "speech": s[1]})
            elif s[0] == "formula":
                out.append({"t": "formula", "text": s[1]})
            else:
                out.append({"t": "draw", "draw": s[1], "args": {"label": "a"}})
        scenes.append({"id": title, "title": title, "start_mode": "dual", "steps": out})
    return scenes


POWERS_ACTIVITIES = [
 {"concept_id": "P1", "title": "Power: base and exponent",
  "lab_spec": {"kind": "POWER_EXPLORER", "law": "definition"},
  "teaching_steps": [
   {"label": "Definition", "kind": "step", "sentence": "A power a^{n} means the base a multiplied by itself n times.", "formula": ""},
   {"label": "Example", "kind": "step", "sentence": "In 2^{5} the base is 2 and the exponent is 5, so there are five factors equal to 2.", "formula": "2^{5} = 2 × 2 × 2 × 2 × 2"},
   {"label": "Calculation", "kind": "step", "sentence": "Multiply the five factors one after another.", "formula": "2^{5} = 32"}]},
 {"concept_id": "P2", "title": "Product of powers with the same base",
  "lab_spec": {"kind": "POWER_EXPLORER", "law": "product_same_base"},
  "teaching_steps": [
   {"label": "Rule", "kind": "step", "sentence": "To multiply powers with the same base, keep the base and add the exponents.", "formula": "a^{m} × a^{n} = a^{m+n}"},
   {"label": "Substitution", "kind": "step", "sentence": "Take a = 2, m = 3 and n = 2.", "formula": "2^{3} × 2^{2} = 2^{3+2}"},
   {"label": "Calculation", "kind": "step", "sentence": "Add the exponents, then compute the power.", "formula": "2^{5} = 32"}]},
 {"concept_id": "P3", "title": "Exercise: write as a single power",
  "teaching_steps": [
   {"label": "Given", "kind": "step", "sentence": "Write 3^{4} × 3^{2} as one power.", "formula": ""},
   {"label": "Rule", "kind": "step", "sentence": "The bases are equal, so add the exponents.", "formula": "3^{4} × 3^{2} = 3^{4+2}"},
   {"label": "Final", "kind": "final", "sentence": "The answer is 3^{6}.", "formula": "3^{6} = 729"}]},
]


def powers_scenes(lang="en"):
    return build_scenes(POWERS_ACTIVITIES, lang, "Powers")


def powers_single_scenes(lang="en"):
    """Text-only Powers stages (no drawing needed): one full-width board."""
    sc = build_scenes([a for a in POWERS_ACTIVITIES if not a.get("lab_spec")], lang, "Powers")
    return sc


def mixed_scenes():
    """single -> dual -> single INSIDE one scene, plus a following text-only scene."""
    t = lambda s, ar="": {"t": "text", "text": ar or s, "label": "", "speech": s}
    return [
        {"id": "M1", "title": "Mixed lesson", "start_mode": "single", "steps": [
            t("First we state the idea in words.", "نذكر الفكرة أولًا بالكلمات."),
            {"t": "draw", "draw": "powerFactors", "args": {"base": 2, "exp": 4, "value": "16", "title": "2⁴"}},
            t("The drawing stays visible while we explain.", "يبقى الرسم ظاهرًا أثناء الشرح."),
            {"t": "formula", "text": "2^{4} = 2 × 2 × 2 × 2 = 16"},
            {"t": "mode", "mode": "single"},
            t("Now we only need writing again.", "الآن نحتاج الكتابة فقط.")]},
        {"id": "M2", "title": "Text only", "start_mode": "single", "steps": [t("This stage has no drawing.", "هذه المرحلة بلا رسم.")]},
    ]


GOLDEN = {"sections": [{"label": "Results:", "items": ["fixture"]}], "key_results": ["fixture"], "title": "fixture",
          "kind": "mathematics", "subject": "mathematics", "language": "en", "verification": ["ok"],
          "panels": [{"title": "Verified lesson results", "icon": "✅", "steps": ["fixture"]}],
          "rule_summary": "fixture", "concept_ids": ["x"], "avatar_src": ""}
