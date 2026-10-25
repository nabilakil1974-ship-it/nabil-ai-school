"""Grade 1 Mathematics — The numbers up to 13."""
from scripts.direct_lessons.templates import teens_lesson
LESSON_ID = "G01-MATH-EN-024"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers up to 13", "ar": "الأعداد حتى 13", "fr": "Les nombres jusqu'à 13"}
THEORY, EXERCISES = teens_lesson(11, 13, 64)
