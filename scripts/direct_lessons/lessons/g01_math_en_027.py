"""Grade 1 Mathematics — The numbers up to 19."""
from scripts.direct_lessons.templates import teens_lesson
LESSON_ID = "G01-MATH-EN-027"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers up to 19", "ar": "الأعداد حتى 19", "fr": "Les nombres jusqu'à 19"}
THEORY, EXERCISES = teens_lesson(17, 19, 70)
