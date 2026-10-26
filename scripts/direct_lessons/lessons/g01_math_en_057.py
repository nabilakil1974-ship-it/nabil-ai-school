"""Grade 1 Mathematics — The numbers up to 99."""
from scripts.direct_lessons.templates import decade_lesson

LESSON_ID = "G01-MATH-EN-057"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers up to 99", "ar": "الأعداد حتى 99", "fr": "Les nombres jusqu'à 99"}
THEORY, EXERCISES = decade_lesson(9, "ninety", "تسعون", "quatre-vingt-dix", 146)
