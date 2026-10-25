"""Grade 1 Mathematics — The numbers from 1 to 7."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.templates import counting_lesson

LESSON_ID = "G01-MATH-EN-010"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers from 1 to 7", "ar": "الأعداد من 1 إلى 7", "fr": "Les nombres de 1 à 7"}

THEORY, EXERCISES = counting_lesson(6, 7, 34)
EXERCISES.append(EX("6", "35", st("Order the boxes from the fewest to the most: A has 7, B has 5, C has 6, D has 3.", "رتّب الصناديق من الأقل إلى الأكثر: A فيه 7، B فيه 5، C فيه 6، D فيه 3.", "Range les boîtes du moins au plus : A en a 7, B en a 5, C en a 6, D en a 3."), [
    F("A = 7      B = 5      C = 6      D = 3"),
    T("We start with the smallest quantity: 3, then 5, then 6, then 7.",
      "نبدأ بأصغر كمية: 3 ثم 5 ثم 6 ثم 7.",
      "On commence par la plus petite quantité : 3, puis 5, puis 6, puis 7."),
    F("D → B → C → A"),
    F("3 → 5 → 6 → 7"),
]))
EXERCISES.append(EX("7", "35", st("Read the numerals in mixed order: 7, 2, 6, 1, 4, 3, 5.", "اقرأ الأرقام بترتيب مختلط: 7، 2، 6، 1، 4، 3، 5.", "Lis les chiffres dans le désordre : 7, 2, 6, 1, 4, 3, 5."), [
    F("seven, two, six, one, four, three, five"),
    T("If we confuse 6 and 7 we do not rely on the shape alone: 6 goes with six dots, and 7 goes with seven dots.",
      "إذا خلطنا بين 6 و7 فلا نعتمد على الشكل وحده: 6 مع ست نقاط، و7 مع سبع نقاط.",
      "Si on confond 6 et 7, on ne se fie pas à la forme seule : 6 va avec six points, 7 avec sept points."),
]))
