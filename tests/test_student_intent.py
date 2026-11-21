import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.services.student_intent import (  # noqa: E402
    Context, classify, detect_language, extract_lesson_query, rank_lessons)

CASES = [
    # (message, kind, number, language)
    ("اشرحلي الدرس", "explain_lesson", None, "ar"),
    ("اشرح لي درس المثلثات المتطابقة", "explain_lesson", None, "ar"),
    ("شو يعني هالكلمة", "simplify", None, "ar"),
    ("ما فهمت شو يعني", "simplify", None, "ar"),
    ("مافهمت", "simplify", None, "ar"),
    ("عيد الشرح بطريقة أبسط", "simplify", None, "ar"),
    ("أعطني مثالاً", "example", None, "ar"),
    ("عطيني مثال", "example", None, "ar"),
    ("أعطني السؤال رقم 5", "get_question", 5, "ar"),
    ("عطيني سؤال رقم خمسة", "get_question", 5, "ar"),
    ("حل السؤال الثالث", "solve_question", 3, "ar"),
    ("حلّي تمرين ٤", "solve_question", 4, "ar"),
    ("افتح التمرين 2", "open_exercise", 2, "ar"),
    ("ارسم الشكل", "draw", None, "ar"),
    ("ارسملي مثلث", "draw", None, "ar"),
    ("اختبرني", "quiz_me", None, "ar"),
    ("صحح إجابتي", "check_answer", None, "ar"),
    ("Explain lesson Congruent Triangles", "explain_lesson", None, "en"),
    ("Give me question 4", "get_question", 4, "en"),
    ("Solve exercise 2", "solve_question", 2, "en"),
    ("I didn't understand", "simplify", None, "en"),
    ("explain it in a simpler way", "simplify", None, "en"),
    ("give me an example", "example", None, "en"),
    ("draw the triangle", "draw", None, "en"),
    ("quiz me", "quiz_me", None, "en"),
    ("check my answer", "check_answer", None, "en"),
    ("Explique-moi cette leçon", "explain_lesson", None, "fr"),
    ("Donne-moi la question 3", "get_question", 3, "fr"),
    ("Résous l'exercice 5", "solve_question", 5, "fr"),
    ("je n'ai pas compris", "simplify", None, "fr"),
    ("donne un exemple", "example", None, "fr"),
    ("dessine le triangle", "draw", None, "fr"),
    ("question numéro trois", "get_question", 3, "fr"),
    # typos
    ("اشرحلي الدرس بسرعه", "explain_lesson", None, "ar"),
    ("explian lesson powers", "explain_lesson", None, "en"),
    ("qestion 5", "get_question", 5, "en"),
    ("exercise 3 solv", "solve_question", 3, "en"),
    # mixed language
    ("اشرح لي lesson Powers please", "explain_lesson", None, "ar"),
    ("بدي question 5", "get_question", 5, "ar"),
    # playback
    ("وقف", "pause", None, "ar"),
    ("stop", "pause", None, "en"),
    ("اعد", "repeat", None, "ar"),
    ("repeat", "repeat", None, "en"),
    ("التالي", "next", None, "ar"),
    ("next", "next", None, "en"),
    ("ابطأ", "slower", None, "ar"),
]


@pytest.mark.parametrize("msg,kind,number,lang", CASES)
def test_intent(msg, kind, number, lang):
    r = classify(msg)
    assert r.kind == kind, (msg, r)
    assert r.number == number, (msg, r)
    assert r.language == lang, (msg, r)


def test_lebanese_flag():
    assert classify("شو يعني هيك، ما فهمت").lebanese
    assert not classify("Explain lesson Powers").lebanese


def test_lesson_name_is_extracted_as_typed():
    assert extract_lesson_query("اشرح لي درس Congruent Triangles") == "Congruent Triangles"
    assert extract_lesson_query("Explain lesson Congruent Triangles") == "Congruent Triangles"
    assert extract_lesson_query("Explique-moi la leçon sur les nombres premiers") == "nombres premiers"
    assert "المثلثات" in extract_lesson_query("اشرح لي درس المثلثات المتطابقة")
    assert extract_lesson_query("اشرحلي الدرس") == ""
    # a numbered question request is not a lesson name
    assert extract_lesson_query("Give me question 4") == ""


def test_followups_use_context():
    ctx = Context(current_lesson="Congruent Triangles", last_intent="get_question", last_question_number=3)
    assert classify("حله", ctx).kind == "solve_question"
    r = classify("solve it", ctx)
    assert r.kind == "solve_question" and r.number == 3 and "number" in r.from_context
    r = classify("وبعدين الرابع", ctx)
    assert r.kind == "get_question" and r.number == 4
    r = classify("and the fifth one", ctx)
    assert r.kind == "get_question" and r.number == 5
    r = classify("اشرحلي", ctx)
    assert r.kind == "explain_lesson" and "lesson" in r.from_context


def test_hint_and_full_solution():
    ctx = Context(last_question_number=3, last_intent="get_question")
    assert classify("ساعدني بتلميح", ctx).kind == "hint"
    r = classify("بدي الحل كاملا", ctx)
    assert r.kind == "full_solution" and r.wants_full_solution and r.number == 3
    assert classify("give me a hint", ctx).kind == "hint"
    assert classify("solution complète", ctx).kind == "full_solution"


def test_pause_resume_after_pause():
    assert classify("كمل", Context(last_intent="pause")).kind == "resume"
    assert classify("continue", Context(last_intent="pause")).kind == "resume"


def test_unrelated_text_is_general_and_low_confidence():
    r = classify("what is the weather like in beirut")
    assert r.kind == "general" and r.confidence <= 0.4
    assert classify("").kind == "general"


def test_language_detection():
    assert detect_language("Explique-moi la leçon") == "fr"
    assert detect_language("Give me question 4") == "en"
    assert detect_language("شو يعني") == "ar"


LESSONS = [
    {"lesson": "Congruent Triangles", "grade": "9", "subject": "Mathematics", "aliases": ["المثلثات المتطابقة", "Triangles isométriques"]},
    {"lesson": "Powers", "grade": "7", "subject": "Mathematics", "aliases": ["القوى"]},
    {"lesson": "Prime Numbers", "grade": "7", "subject": "Mathematics", "aliases": ["الأعداد الأولية", "Nombres premiers"]},
    {"lesson": "Ohmic Conductors", "grade": "9", "subject": "Physics"},
]


def test_rank_lessons_finds_real_lessons_in_all_languages():
    for q, want in [("Congruent Triangles", "Congruent Triangles"), ("congruent triangle", "Congruent Triangles"),
                    ("المثلثات المتطابقة", "Congruent Triangles"), ("القوى", "Powers"),
                    ("nombres premiers", "Prime Numbers"), ("الاعداد الاولية", "Prime Numbers"),
                    ("prime numbrs", "Prime Numbers")]:
        r = rank_lessons(q, LESSONS)
        assert r and r[0]["lesson"] == want, (q, r)


def test_rank_lessons_returns_nothing_for_unknown_lesson():
    assert rank_lessons("Quantum Chromodynamics", LESSONS) == []
    assert rank_lessons("", LESSONS) == []


def test_grade_hint_prefers_matching_grade():
    two = [{"lesson": "Powers", "grade": "7"}, {"lesson": "Powers", "grade": "8"}]
    assert rank_lessons("Powers", two, grade="8")[0]["grade"] == "8"


def test_exercise_parser_keeps_old_behaviour_and_understands_words():
    from app.services.textbook_page_request import parse_textbook_exercise_request as p
    assert p("exercise 5") == 5 and p("تمرين 7") == 7 and p("question 12") == 12   # unchanged
    assert p("حل السؤال الثالث") == 3
    assert p("عطيني سؤال رقم خمسة") == 5
    assert p("Donne-moi la question trois") == 3
    assert p("give me the fifth exercise") == 5
    assert p("اشرح لي الدرس") is None
    assert p("what is 5 plus 3") is None           # a bare number is not an exercise request
