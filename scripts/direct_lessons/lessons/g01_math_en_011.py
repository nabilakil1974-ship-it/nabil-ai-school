"""Grade 1 Mathematics — The numbers from 1 to 9."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.templates import counting_lesson

LESSON_ID = "G01-MATH-EN-011"
GRADE = 1
SUBJECT = "math"
TITLES = {"en": "The numbers from 1 to 9", "ar": "الأعداد من 1 إلى 9", "fr": "Les nombres de 1 à 9"}

THEORY, EXERCISES = counting_lesson(8, 9, 36)
EXERCISES.append(EX("6", "37", st("Order the boxes from the fewest to the most: A has 8, B has 6, C has 9, D has 7.", "رتّب الصناديق من الأقل إلى الأكثر: A فيه 8، B فيه 6، C فيه 9، D فيه 7.", "Range les boîtes du moins au plus : A en a 8, B en a 6, C en a 9, D en a 7."), [
    F("A = 8      B = 6      C = 9      D = 7"),
    T("We start with the smallest quantity: 6, then 7, then 8, then 9.",
      "نبدأ بأصغر كمية: 6 ثم 7 ثم 8 ثم 9.",
      "On commence par la plus petite quantité : 6, 7, 8, puis 9."),
    F("B → D → A → C"),
    F("6 → 7 → 8 → 9"),
]))
EXERCISES.append(EX("7", "37", st("Read the numerals in mixed order: 9, 4, 8, 2, 7, 1, 6, 3, 5.", "اقرأ الأرقام بترتيب مختلط: 9، 4، 8، 2، 7، 1، 6، 3، 5.", "Lis les chiffres dans le désordre : 9, 4, 8, 2, 7, 1, 6, 3, 5."), [
    F("nine, four, eight, two, seven, one, six, three, five"),
    T("If we confuse 8 and 9, we connect each numeral with its quantity: 8 goes with eight dots and 9 goes with nine dots.",
      "إذا خلطنا بين 8 و9 نربط كل رقم بكميته: 8 مع ثماني نقاط و9 مع تسع نقاط.",
      "Si on confond 8 et 9, on relie chaque chiffre à sa quantité : 8 avec huit points, 9 avec neuf points."),
]))
