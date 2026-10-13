import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.api.lesson_naming import parse_factory_filename  # noqa: E402


def test_factory_names_become_clean_student_titles():
    a = parse_factory_filename("G07-MATHEMATICS--69B7C840--001--POWERS.html")
    b = parse_factory_filename("G07-MATHEMATICS--69B7C840--001--POWERS--EXERCISES.html")
    assert a == {"grade": "7", "subject": "MATHEMATICS", "lesson": "Powers", "exercises": False}
    assert b["lesson"] == "Powers" and b["exercises"] is True
    assert parse_factory_filename("G09-PHYSICS--AB12CD34--012--OHMIC-CONDUCTORS.html")["lesson"] == "Ohmic Conductors"


def test_other_names_are_left_to_legacy_parser():
    assert parse_factory_filename("EB07-Mathematics--Lines and Circles.html") is None
    assert parse_factory_filename("NABIL SOLIDE AND LIQUID.html") is None
