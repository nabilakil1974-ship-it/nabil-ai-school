"""NABIL Student Intent Engine.

Understands a student's natural request in Lebanese Arabic, Modern Standard
Arabic, English and French (including typos and mixed-language sentences) and
returns a structured intent. It never answers and never invents content: it
only decides WHAT the student wants so the existing lesson / textbook / chat
pipeline can fetch the real material.

Pure Python, no I/O, no model call: deterministic and unit-testable.
Context (current lesson, last question, grade...) disambiguates short follow-ups
such as "وبعدين الرابع" or "solve it".
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field, asdict
from difflib import SequenceMatcher

# ---------------------------------------------------------------- normalising
_AR_DIGITS = {ord(a): str(i) for i, a in enumerate("٠١٢٣٤٥٦٧٨٩")}
_AR_DIGITS.update({ord(a): str(i) for i, a in enumerate("۰۱۲۳۴۵۶۷۸۹")})


def strip_marks(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text or ""))
    return "".join(c for c in text if not unicodedata.combining(c))


def normalize(text: str) -> str:
    t = strip_marks(text).translate(_AR_DIGITS).lower()
    t = re.sub("[ـً-ْ]", "", t)
    t = (t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ٱ", "ا")
         .replace("ى", "ي").replace("ة", "ه").replace("ؤ", "و").replace("ئ", "ي"))
    t = t.replace("n°", " n ").replace("№", " n ").replace("#", " n ")
    t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
    return re.sub(r"\s+", " ", t).strip()


def detect_language(text: str, hint: str = "") -> str:
    """ar / fr / en (by dominant script and function words)."""
    s = str(text or "")
    ar = len(re.findall(r"[؀-ۿ]", s))
    lat = len(re.findall(r"[A-Za-zÀ-ſ]", s))
    if ar >= 3 or (ar and ar >= lat):
        return "ar"
    n = " " + normalize(s) + " "
    fr_words = (" le la les un une des est que quoi explique expliquer moi lecon cours exercice "
                "question donne donnemoi resous resoudre dessine je ne pas compris comprends "
                "comment pourquoi avec sur dans pour numero trois quatre cinq ")
    fr = sum(1 for w in fr_words.split() if f" {w} " in n)
    en_words = (" the explain lesson give me question exercise solve draw what why how is are "
                "please number show did not understand don t about ")
    en = sum(1 for w in en_words.split() if f" {w} " in n)
    if re.search(r"[éèêàçùôîâû]", str(text or "").lower()) and fr >= en:
        return "fr"
    if fr > en:
        return "fr"
    if en or lat:
        return "en"
    return hint if hint in ("ar", "fr", "en") else "ar"


LEBANESE_CUES = ("شو", "هلق", "بدي", "عطيني", "هيك", "منيح", "ليش", "كيف", "يعني شو", "مش", "ما فهمت",
                 "اشرحلي", "فهمني", "عيد", "لسا", "هاد", "هاي", "ايمتى")


def is_lebanese(text: str) -> bool:
    n = normalize(text)
    return any(normalize(c) in n.split() or (" " in c and normalize(c) in n) for c in LEBANESE_CUES)


# --------------------------------------------------------------- number words
_NUM_WORDS: dict[str, int] = {}


def _reg(n: int, *forms: str) -> None:
    for f in forms:
        _NUM_WORDS[normalize(f)] = n


_reg(1, "واحد", "واحده", "الاول", "اول", "الاولي", "الاولى", "one", "first", "un", "une", "premier", "premiere", "1er", "1st")
_reg(2, "اثنين", "اثنان", "اثنتين", "ثنتين", "الثاني", "الثانيه", "ثاني", "two", "second", "deux", "deuxieme")
_reg(3, "ثلاثه", "ثلاث", "تلاته", "تلات", "الثالث", "الثالثه", "ثالث", "three", "third", "trois", "troisieme")
_reg(4, "اربعه", "اربع", "الرابع", "الرابعه", "رابع", "four", "fourth", "quatre", "quatrieme")
_reg(5, "خمسه", "خمس", "الخامس", "الخامسه", "خامس", "five", "fifth", "cinq", "cinquieme")
_reg(6, "سته", "ست", "السادس", "السادسه", "سادس", "six", "sixth", "sixieme")
_reg(7, "سبعه", "سبع", "السابع", "السابعه", "سابع", "seven", "seventh", "sept", "septieme")
_reg(8, "ثمانيه", "ثماني", "تمانيه", "الثامن", "الثامنه", "ثامن", "eight", "eighth", "huit", "huitieme")
_reg(9, "تسعه", "تسع", "التاسع", "التاسعه", "تاسع", "nine", "ninth", "neuf", "neuvieme")
_reg(10, "عشره", "عشر", "العاشر", "العاشره", "عاشر", "ten", "tenth", "dix", "dixieme")
_reg(11, "احدعش", "حداش", "الحادي عشر", "eleven", "onze")
_reg(12, "اثنعش", "طناعش", "twelve", "douze")
_reg(13, "ثلاثه عشر", "تلتعش", "thirteen", "treize")
_reg(14, "اربعتعش", "fourteen", "quatorze")
_reg(15, "خمستعش", "fifteen", "quinze")
_reg(16, "سطعش", "sixteen", "seize")
_reg(17, "سبعتعش", "seventeen")
_reg(18, "تمنتعش", "eighteen")
_reg(19, "تسعتعش", "nineteen")
_reg(20, "عشرين", "twenty", "vingt")

# --------------------------------------------------------------------- cues
# A cue ending in '*' matches any token that starts with it (اشرح* → اشرحلي).
# Multi-word cues must match consecutive tokens. Cues are written pre-normalised.
CUES: dict[str, list[tuple[str, float]]] = {
    "simplify": [
        ("ما فهمت*", 3), ("مافهمت*", 3), ("ماني فاهم*", 3), ("مش فاهم*", 3), ("لم افهم", 3), ("ما فهمنا", 3),
        ("مو فاهم*", 3), ("شو يعني", 2.5), ("يعني شو", 2.5), ("ما معني", 2), ("ماذا يعني", 2.5), ("ما المقصود", 2.5),
        ("عيد الشرح", 3), ("اعد الشرح", 3), ("بسط*", 3), ("ابسط", 3), ("اسهل", 2.5), ("بطريقه اخري", 2.5),
        ("بطريقه ثانيه", 2.5), ("بشكل ابسط", 3), ("بطريقه ابسط", 3), ("صعب", 1.5),
        ("i did not understand", 3), ("i didn t understand", 3), ("didn t understand", 3), ("don t understand", 3),
        ("do not understand", 3), ("don t get", 3), ("not understand", 3), ("simpler", 3), ("simplify", 3),
        ("explain again", 3), ("another way", 2.5), ("what does it mean", 2.5), ("what do you mean", 2),
        ("je n ai pas compris", 3), ("pas compris", 3), ("je ne comprends pas", 3), ("comprends pas", 3),
        ("plus simple", 3), ("simplifie*", 3), ("autrement", 2.5), ("reexplique*", 3), ("ca veut dire", 2.5),
        ("qu est ce que ca veut dire", 3), ("veut dire", 1.5)],
    "example": [
        ("مثال*", 3), ("امثله", 3), ("مثلا", 1.5), ("عطيني مثال", 3), ("example", 3), ("examples", 3), ("for instance", 2),
        ("exemple", 3), ("exemples", 3)],
    "explain_lesson": [
        ("اشرح*", 3), ("شرح", 2.5), ("فهمني", 3), ("علمني", 3), ("فسر*", 2.5), ("وضح*", 2.5), ("درس", 1.5),
        ("الدرس", 1.5), ("بدي افهم", 3), ("بدي اتعلم", 3), ("explain", 3), ("teach", 3), ("lesson", 1.5), ("learn", 2),
        ("tell me about", 2), ("explique*", 3), ("expliquer", 3), ("lecon", 2), ("cours", 1.5), ("apprendre", 2),
        ("apprends moi", 3), ("chapitre", 1.5), ("chapter", 1.5), ("unit", 1)],
    "get_question": [
        ("سوال", 2), ("السوال", 2), ("اسئله", 1.5), ("تمرين", 2.5), ("التمرين", 2.5), ("تمارين", 1.5), ("مساله", 2),
        ("المساله", 2), ("question", 2.5), ("questions", 1.5), ("exercise", 2.5), ("exercises", 1.5), ("exercice", 2.5),
        ("exercices", 1.5), ("problem", 2), ("probleme", 2), ("ex", 1), ("q", 1)],
    "ask_for_text": [
        ("عطيني", 1.5), ("اعطني", 1.5), ("اعطيني", 1.5), ("جيب", 1.5), ("هات", 1.5), ("اعرض", 1.5), ("ورجيني", 1.5),
        ("اقرا", 1.5), ("اقرأ", 1.5), ("ما هو", 1), ("شو", 0.5), ("give", 1.5), ("show", 1.5), ("read", 1.5),
        ("what is", 1), ("donne*", 1.5), ("montre*", 1.5), ("lis", 1.5), ("affiche*", 1)],
    "solve": [
        ("حل", 3), ("حلي", 3), ("حله", 3), ("حلها", 3), ("احسب", 2.5), ("جاوب*", 2.5), ("اجب", 2.5), ("جواب", 1.5), ("solve", 3),
        ("solution", 1.5), ("answer", 1.5), ("work out", 2.5), ("resous", 3), ("resoudre", 3), ("resolution", 2),
        ("corrige", 1.5), ("calcule", 2.5)],
    "open_exercise": [
        ("افتح", 3), ("افتحلي", 3), ("open", 3), ("ouvre", 3), ("ouvrir", 3)],
    "draw": [
        ("ارسم*", 3), ("رسم", 2.5), ("الرسم", 2.5), ("الشكل", 2), ("شكل", 1.5), ("مخطط", 2), ("draw", 3), ("sketch", 2.5),
        ("figure", 2), ("diagram", 2.5), ("graph", 2), ("plot", 2), ("dessine*", 3), ("dessiner", 3),
        ("schema", 2.5), ("trace", 2.5), ("show the figure", 3), ("on the board", 2), ("sur le tableau", 2),
        ("على السبوره", 2.5), ("بالسبوره", 2.5)],
    "quiz_me": [
        ("اختبرني", 3), ("اسالني", 3), ("اختبار", 2), ("quiz", 3), ("test me", 3), ("quiz me", 3), ("teste moi", 3),
        ("interroge moi", 3), ("evalue moi", 3), ("قيمني", 3), ("امتحني", 3)],
    "check_answer": [
        ("صحح*", 3), ("تحقق", 2.5), ("جوابي", 2.5), ("اجابتي", 2.5), ("صح ولا غلط", 3), ("check my", 3), ("is my answer", 3),
        ("am i right", 3), ("correct my", 3), ("corrige", 2.5), ("verifie*", 2.5), ("ma reponse", 3), ("c est juste", 3)],
    "hint": [
        ("تلميح", 3), ("لمحه", 3), ("ساعدني", 2), ("hint", 3), ("clue", 2.5), ("indice", 3), ("un coup de pouce", 3)],
    "full_solution": [
        ("الحل كاملا", 3.5), ("الحل الكامل", 3.5), ("حل كامل", 3.5), ("كامل", 1), ("full solution", 3.5), ("complete solution", 3.5),
        ("solution complete", 3.5), ("solution complète", 3.5), ("show me the solution", 3), ("whole solution", 3.5)],
    "repeat": [
        ("اعد", 3), ("عيد", 3), ("كرر*", 2.5), ("مره ثانيه", 2.5), ("repeat", 3), ("again", 1.5), ("repete*", 3),
        ("encore", 2), ("say that again", 3)],
    "next": [
        ("التالي", 3), ("بعده", 2), ("وبعدين", 2.5), ("كمل", 3), ("اكمل", 3), ("تابع", 3), ("next", 3), ("continue", 3),
        ("go on", 3), ("keep going", 3), ("suivant", 3), ("continue", 3), ("la suite", 3), ("apres", 1.5)],
    "previous": [
        ("السابق", 3), ("ارجع", 3), ("رجوع", 2.5), ("previous", 3), ("go back", 3), ("back", 1.5), ("precedent*", 3),
        ("retour", 2.5)],
    "pause": [
        ("وقف*", 3), ("توقف", 3), ("اسكت", 3), ("كفايه", 2), ("pause", 3), ("stop", 3), ("wait", 2), ("silence", 3),
        ("attends", 3), ("tais toi", 3), ("arrete*", 3)],
    "resume": [
        ("استانف", 3), ("كمل", 1), ("resume", 3), ("reprends", 3), ("reprendre", 3), ("play", 2)],
    "slower": [
        ("ابطا", 3), ("بطيء", 3), ("بطئ", 3), ("بالراحه", 3), ("slower", 3), ("slow down", 3), ("plus lentement", 3),
        ("moins vite", 3), ("doucement", 3)],
    "faster": [
        ("اسرع", 3), ("faster", 3), ("speed up", 3), ("plus vite", 3)],
    "greet": [
        ("مرحبا", 2), ("اهلا", 2), ("السلام", 2), ("هلا", 2), ("hello", 2), ("hi", 2), ("hey", 2), ("bonjour", 2),
        ("salut", 2), ("bonsoir", 2)],
}

STOPWORDS = set(normalize(w) for w in """
لي لنا الي على عن من في الى هذا هذه هاد هاي بدي اريد ممكن لو سمحت يا استاذ استاذه نبيل رقم الان هلق بعد
اعطني عطيني اعطيني جيب هات اعرض شو ما هو هي كيف ليش لماذا بطريقه بشكل
the a an of on in to me please can you could would for about is are be my our this that it and or
explain give show tell teach lesson class grade number no n
le la les un une des de du pour sur dans moi s il vous te toi ce cet cette et ou donne montre explique lecon cours
""".split())

_EXERCISE_WORDS = {normalize(w) for w in (
    "سؤال السؤال اسئلة تمرين التمرين تمارين مسألة المسألة question questions exercise exercises exercice exercices "
    "problem probleme ex q").split()}


# ------------------------------------------------------------------ matching
def _tok_match(cue_tok: str, tok: str) -> bool:
    if cue_tok.endswith("*"):
        stem = cue_tok[:-1]
        return tok.startswith(stem)
    if tok == cue_tok:
        return True
    # fuzzy only for longer words (typo tolerance), never for short ones
    if len(cue_tok) >= 5 and len(tok) >= 4 and abs(len(cue_tok) - len(tok)) <= 2:
        return SequenceMatcher(None, cue_tok, tok).ratio() >= 0.84
    # Arabic proclitics: و ف ب ل ك + word
    if len(tok) > len(cue_tok) + 0 and tok[1:] == cue_tok and tok[0] in "وفبلكس" and len(cue_tok) >= 3:
        return True
    return False


def _cue_hits(tokens: list[str], cue: str) -> list[int]:
    ct = normalize(cue.replace("*", "")).split()
    star = cue.endswith("*")
    ct = [c for c in ct]
    if star and ct:
        ct[-1] += "*"
    hits = []
    for i in range(len(tokens) - len(ct) + 1):
        if all(_tok_match(c, tokens[i + j]) for j, c in enumerate(ct)):
            hits.append(i)
    return hits


_QUESTION_INTENTS = ("get_question", "solve_question", "open_exercise", "full_solution", "hint")


def _is_exercise_word(t: str) -> bool:
    if t in _EXERCISE_WORDS or re.fullmatch(r"(?:ex|q)\d+", t):
        return True
    if len(t) >= 6:
        return any(len(w) >= 5 and SequenceMatcher(None, w, t).ratio() >= 0.84 for w in _EXERCISE_WORDS)
    return False


@dataclass
class Context:
    """What the tutor already knows about this conversation."""
    current_lesson: str = ""
    grade: str = ""
    subject: str = ""
    last_intent: str = ""
    last_question_number: int | None = None
    last_topic: str = ""
    language: str = ""


@dataclass
class Intent:
    kind: str = "general"                 # see KINDS
    language: str = "ar"
    lebanese: bool = False
    number: int | None = None             # question / exercise / page number
    lesson_query: str = ""                # the lesson the student named, as typed
    wants_drawing: bool = False
    wants_hint: bool = False
    wants_full_solution: bool = False
    simpler: bool = False
    from_context: list[str] = field(default_factory=list)
    confidence: float = 0.0
    matched: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


KINDS = ("explain_lesson", "simplify", "example", "get_question", "solve_question", "open_exercise", "draw",
         "quiz_me", "check_answer", "hint", "full_solution", "repeat", "next", "previous", "pause", "resume",
         "slower", "faster", "greet", "general")


def extract_number(tokens: list[str], near: int | None = None) -> int | None:
    """Digits or number words. If `near` is given prefer the number closest after it."""
    found: list[tuple[int, int]] = []
    for i, t in enumerate(tokens):
        if re.fullmatch(r"\d{1,3}", t):
            found.append((i, int(t)))
        elif re.fullmatch(r"(\d{1,3})(?:st|nd|rd|th|er|e|eme)", t):
            found.append((i, int(re.match(r"\d+", t).group())))
        elif t in _NUM_WORDS:
            found.append((i, _NUM_WORDS[t]))
        elif len(tokens) > i + 1 and f"{t} {tokens[i + 1]}" in _NUM_WORDS:
            found.append((i, _NUM_WORDS[f"{t} {tokens[i + 1]}"]))
        elif len(t) > 3 and t[0] in "وفبل" and t[1:] in _NUM_WORDS:
            found.append((i, _NUM_WORDS[t[1:]]))
    if not found:
        return None
    if near is None:
        return found[0][1]
    after = [f for f in found if f[0] >= near]
    pool = after or found
    return min(pool, key=lambda f: abs(f[0] - near))[1]


# --------------------------------------------------------------- classification
def classify(message: str, ctx: Context | None = None) -> Intent:
    ctx = ctx or Context()
    raw = str(message or "").strip()
    lang = detect_language(raw, ctx.language)
    out = Intent(language=lang, lebanese=is_lebanese(raw))
    norm = normalize(raw)
    tokens = norm.split()
    if not tokens:
        return out

    scores: dict[str, float] = {}
    hits_pos: dict[str, list[int]] = {}
    for kind, cues in CUES.items():
        for cue, w in cues:
            h = _cue_hits(tokens, cue)
            if h:
                scores[kind] = scores.get(kind, 0.0) + w
                hits_pos.setdefault(kind, []).extend(h)
                out.matched.append(f"{kind}:{cue}")

    # number nearest an exercise word
    ex_idx = [i for i, t in enumerate(tokens) if _is_exercise_word(t)]
    num: int | None = None
    if ex_idx:
        for i in ex_idx:
            m = re.fullmatch(r"(?:ex|q)(\d+)", tokens[i])
            if m:
                num = int(m.group(1))
                break
        if num is None:
            # number may follow ("question 4", "السؤال رقم 4") or precede ("4th question", "الرابع سؤال")
            after = extract_number(tokens[ex_idx[0] + 1:ex_idx[0] + 4])
            before = extract_number(tokens[max(0, ex_idx[0] - 2):ex_idx[0]])
            num = after if after is not None else before
    if num is None and not ex_idx:
        # "n 5" / "رقم 5" / bare ordinal follow-up like "الرابع" / "and the fourth one"
        for i, t in enumerate(tokens):
            if t in ("n", "no", "numero", "number", "رقم") and i + 1 < len(tokens):
                num = extract_number(tokens[i + 1:i + 3])
                if num is not None:
                    break
    if num is None and len(tokens) <= 5 and ctx.last_intent in _QUESTION_INTENTS:
        num = extract_number(tokens)      # bare follow-up: "وبعدين الرابع", "and the fifth one"
    out.number = num

    has_q_ref = bool(ex_idx) or ("get_question" in scores)
    solve = scores.get("solve", 0.0)
    ask = scores.get("ask_for_text", 0.0)

    # ---- decide the kind -------------------------------------------------
    kind = "general"
    simple_score = scores.get("simplify", 0.0)
    if simple_score >= 2.5:
        kind = "simplify"
        out.simpler = True
    elif scores.get("full_solution", 0) >= 3 and (has_q_ref or ctx.last_question_number):
        kind = "full_solution"
        out.wants_full_solution = True
    elif scores.get("hint", 0) >= 2.5:
        kind = "hint"
        out.wants_hint = True
    elif scores.get("check_answer", 0) >= 2.5:
        kind = "check_answer"
    elif scores.get("quiz_me", 0) >= 3:
        kind = "quiz_me"
    elif scores.get("open_exercise", 0) >= 3 and (has_q_ref or num):
        kind = "open_exercise"
    elif solve >= 2.5 and (has_q_ref or num is not None):
        kind = "solve_question"
    elif has_q_ref and num is not None:
        kind = "get_question"
    elif scores.get("draw", 0) >= 2.5:
        kind = "draw"
    elif scores.get("example", 0) >= 3:
        kind = "example"
    elif scores.get("explain_lesson", 0) >= 2.5:
        kind = "explain_lesson"
    elif scores.get("slower", 0) >= 3:
        kind = "slower"
    elif scores.get("faster", 0) >= 3:
        kind = "faster"
    elif scores.get("pause", 0) >= 3:
        kind = "pause"
    elif scores.get("previous", 0) >= 3:
        kind = "previous"
    elif scores.get("resume", 0) >= 3 or (scores.get("next", 0) >= 3 and len(tokens) <= 3 and ctx.last_intent == "pause"):
        kind = "resume"
    elif scores.get("next", 0) >= 3 and len(tokens) <= 4:
        kind = "next"
    elif scores.get("repeat", 0) >= 2.5 and len(tokens) <= 5:
        kind = "repeat"
    elif solve >= 2.5 and ctx.last_question_number:
        kind = "solve_question"
        out.number = ctx.last_question_number
        out.from_context.append("number")
    elif has_q_ref and num is None and ask >= 1:
        kind = "get_question"          # asked for "the question" without a number: ask which one
    elif scores.get("greet", 0) >= 2 and len(tokens) <= 4:
        kind = "greet"
    elif num is not None and len(tokens) <= 5 and ctx.last_intent in ("get_question", "solve_question", "open_exercise", "full_solution", "hint"):
        # "وبعدين الرابع" / "and the fourth one" right after a question request
        kind = "solve_question" if solve >= 2 else "get_question"
        out.from_context.append("intent")
    elif solve >= 2.5:
        kind = "solve_question"        # "solve it": the tutor falls back to the last visible exercise

    out.kind = kind
    out.wants_drawing = scores.get("draw", 0) >= 2.5
    out.wants_hint = out.wants_hint or scores.get("hint", 0) >= 2.5
    out.wants_full_solution = out.wants_full_solution or scores.get("full_solution", 0) >= 3

    # follow-up numbers: "give me question 4" then "solve it"
    if kind in ("solve_question", "full_solution", "hint", "check_answer") and out.number is None and ctx.last_question_number:
        out.number = ctx.last_question_number
        out.from_context.append("number")

    # ---- lesson name the student typed ----------------------------------
    if kind in ("explain_lesson", "example", "simplify", "draw", "quiz_me", "general", "get_question",
                "solve_question", "open_exercise"):
        out.lesson_query = extract_lesson_query(raw)
        if not out.lesson_query and ctx.current_lesson and kind in (
                "explain_lesson", "example", "simplify", "draw", "quiz_me", "get_question", "solve_question", "open_exercise"):
            out.from_context.append("lesson")
    top = max(scores.values()) if scores else 0.0
    out.confidence = round(min(1.0, (top / 4.0) + (0.15 if out.number is not None else 0) + (0.1 if out.lesson_query else 0)), 2)
    if kind == "general":
        out.confidence = 0.2 if not scores else min(out.confidence, 0.4)
    return out


# ----------------------------------------------------------- lesson name text
_STRIP_PHRASES = [
    r"اشرح(?:لي|لنا|ي)?", r"شرح", r"فهمني", r"علمني", r"فسر(?:لي)?", r"وضح(?:لي)?", r"بدي افهم", r"بدي اتعلم",
    r"عيد الشرح", r"ما فهمت", r"درس", r"الدرس", r"عن", r"حول", r"موضوع", r"المفهوم", r"مفهوم", r"وحده", r"الوحده",
    r"الفصل", r"فصل", r"اريد", r"بدي", r"ممكن", r"لو سمحت", r"يا استاذ", r"استاذ", r"نبيل",
    r"explain(?: to me| me)?", r"teach(?: me)?", r"tell me about", r"i want to learn(?: about)?", r"lesson on", r"lesson",
    r"about", r"please", r"can you", r"could you", r"the", r"chapter", r"unit", r"topic", r"concept of",
    r"explique(?:-moi| moi)?", r"expliquer", r"apprends(?:-moi| moi)?", r"la lecon (?:sur|de|des)?", r"lecon", r"le cours (?:sur|de)?",
    r"sur", r"concernant", r"s il te plait", r"s il vous plait", r"le", r"la", r"les", r"chapitre", r"cours",
]
_STRIP_RE = None


def extract_lesson_query(message: str) -> str:
    """The lesson/topic phrase left once request words are removed. Keeps the
    student's own spelling (and Latin case) so it can be fuzzy-matched later."""
    global _STRIP_RE
    s = strip_marks(str(message or "")).translate(_AR_DIGITS)
    s = re.sub(r"[ً-ْـ]", "", s)
    # drop sentences about numbered questions: those are not lesson names
    if re.search(r"(?i)\b(?:question|exercise|exercice|problem)\b|سؤال|السؤال|تمرين|التمرين|مسألة", s):
        s = re.sub(r"(?i)(?:\bquestion\b|\bexercise\b|\bexercice\b|\bproblem\b|سؤال|السؤال|تمرين|التمرين|مسألة)\s*(?:رقم|n°|number|numéro|no\.?)?\s*\S+", " ", s)
    if _STRIP_RE is None:
        parts = sorted(_STRIP_PHRASES, key=len, reverse=True)
        _STRIP_RE = re.compile(r"(?i)(?:(?<=\s)|^)(?:" + "|".join(parts) + r")(?=\s|$)")
    prev = None
    s = re.sub(r"[?؟!.,،:;]", " ", s)
    s = " " + re.sub(r"\s+", " ", s) + " "
    while prev != s:
        prev = s
        s = _STRIP_RE.sub(" ", s)
        s = re.sub(r"\s+", " ", s)
    s = s.strip()
    toks = [t for t in s.split() if normalize(t) not in STOPWORDS and not re.fullmatch(r"\d+", t)]
    return " ".join(toks).strip()


# ------------------------------------------------------------- lesson matching
def _lesson_tokens(text: str) -> list[str]:
    return [t for t in normalize(text).split() if t not in STOPWORDS and len(t) > 1]


def rank_lessons(query: str, lessons: list[dict], *, grade: str = "", subject: str = "", limit: int = 5) -> list[dict]:
    """Fuzzy-rank real catalogue entries (dicts with title/lesson/aliases/grade/subject).
    Returns [] when nothing is genuinely close: callers must say 'not found'."""
    q = _lesson_tokens(query)
    if not q:
        return []
    ranked = []
    for item in lessons:
        names = [item.get("lesson") or item.get("title") or item.get("canonical_title") or ""]
        names += list(item.get("aliases") or [])
        best = 0.0
        for name in names:
            nt = _lesson_tokens(name)
            if not nt:
                continue
            joined_q, joined_n = " ".join(q), " ".join(nt)
            if joined_q == joined_n:
                score = 1.0
            else:
                matched = 0.0
                for qt in q:
                    m = max((1.0 if qt == t else SequenceMatcher(None, qt, t).ratio() for t in nt), default=0.0)
                    matched += m if m >= 0.8 else 0.0
                cover_q = matched / len(q)
                cover_n = matched / len(nt)
                score = 0.65 * cover_q + 0.35 * cover_n
            best = max(best, score)
        g = str(item.get("grade") or "")
        if grade and g and re.sub(r"\D", "", g) != re.sub(r"\D", "", str(grade)):
            best *= 0.6
        if subject and item.get("subject") and normalize(str(item["subject"])) != normalize(subject):
            best *= 0.85
        if best >= 0.62:
            ranked.append((best, item))
    ranked.sort(key=lambda x: -x[0])
    return [dict(item, match_score=round(s, 2)) for s, item in ranked[:limit]]
