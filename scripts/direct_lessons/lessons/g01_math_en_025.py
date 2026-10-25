"""Grade 1 Mathematics — The numbers up to 16."""
from scripts.direct_lessons.templates import teens_lesson
LESSON_ID = "G01-MATH-EN-025"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers up to 16", "ar": "الأعداد حتى 16", "fr": "Les nombres jusqu'à 16"}
THEORY, EXERCISES = teens_lesson(14, 16, 66)
