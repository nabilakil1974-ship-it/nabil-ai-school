"""Grade 1 Mathematics — The numbers up to 89."""
from scripts.direct_lessons.templates import decade_lesson

LESSON_ID = "G01-MATH-EN-056"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers up to 89", "ar": "الأعداد حتى 89", "fr": "Les nombres jusqu'à 89"}
THEORY, EXERCISES = decade_lesson(8, "eighty", "ثمانون", "quatre-vingts", 144)
