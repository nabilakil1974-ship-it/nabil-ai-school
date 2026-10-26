"""Grade 3 Mathematics — Division (from the teacher plan; book figures are not reproduced)."""
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.lessons.g03_math_en_053 import share

LESSON_ID = "G03-MATH-EN-056"
GRADE = 3
SUBJECT = "math"
TITLES = {"en": "Division", "ar": "القسمة", "fr": "La division"}

THEORY = [
    ("Sharing and grouping", "التوزيع والتجميع", "Partage et groupement", "118", [
        T("Hello, champion! Division finds equal shares or the number of equal groups. 12 ÷ 3: share 12 into 3 equal groups, 4 each. Or make groups of 3 from 12: 4 groups. Both give 4.",
          "مرحبًا يا بطل! القسمة تجد الأنصبة المتساوية أو عدد المجموعات المتساوية. 12 ÷ 3: نوزّع 12 على 3 مجموعات متساوية فيكون في كل مجموعة 4. أو نكوّن مجموعات من 3 من 12 فتكون 4 مجموعات. الجوابان 4.",
          "12 ÷ 3 : partager en 3 parts de 4, ou faire des groupes de 3 : 4 groupes."),
        share(1, 2, 3),
        F("12 ÷ 3 = 4"),
    ]),
    ("Division and multiplication", "القسمة والضرب", "Division et multiplication", "118", [
        T("Multiplication checks division. 12 ÷ 3 = 4 because 4 × 3 = 12. The quotient times the divisor gives the dividend.",
          "الضرب يتحقق من القسمة. 12 ÷ 3 = 4 لأن 4 × 3 = 12. الناتج × المقسوم عليه = المقسوم.",
          "12 ÷ 3 = 4 car 4 × 3 = 12."),
        F("4 × 3 = 12  ⇒  12 ÷ 3 = 4"),
    ]),
    ("Read the quotient in context", "نفسّر الناتج في المسألة", "Interpréter le quotient", "119", [
        T("20 pencils are shared equally among 4 children: 20 ÷ 4 = 5 pencils each. The question tells us what the quotient means. The groups must be equal.",
          "تُوزَّع 20 قلمًا بالتساوي على 4 أطفال: 20 ÷ 4 = 5 أقلام لكل طفل. السؤال يحدد معنى الناتج، ويجب أن تكون المجموعات متساوية.",
          "20 crayons pour 4 enfants : 5 chacun."),
        share(2, 0, 4),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Interpret, form equal groups, divide, read the quotient, check by multiplication.", "نفسّر ونكوّن مجموعات متساوية ونقسم ونقرأ الناتج ونتحقق بالضرب.", "Interpréter, grouper, diviser, vérifier."),
        F("INTERPRET → EQUAL GROUPS → DIVIDE → CHECK × "),
    ]),
]

EXERCISES = [
    EX("1", "118", st("Share 15 sweets among 3 children.", "وزّع 15 حلوى على 3 أطفال.", "Partage 15 bonbons entre 3 enfants."), [F("15 ÷ 3 = 5      5 × 3 = 15")]),
    EX("2", "118", st("Make groups of 4 from 20 balls. How many groups?", "كوّن مجموعات من 4 من 20 كرة. كم مجموعة؟", "Groupes de 4 avec 20 balles."), [F("20 ÷ 4 = 5      5 × 4 = 20")]),
    EX("3", "119", st("Write the multiplication fact for 18 ÷ 3.", "اكتب حقيقة الضرب المرتبطة بـ 18 ÷ 3.", "Multiplication liée à 18 ÷ 3."), [F("6 × 3 = 18  ⇒  18 ÷ 3 = 6")]),
    EX("4", "119", st("Error detective: 20 sweets, groups of 6, 3 groups and 2 left over: is it equal sharing?", "المحقق: 20 حلوى في مجموعات من 6 فصارت 3 مجموعات وبقي 2؛ هل هذا توزيع متساوٍ؟", "Détective : 20 bonbons, groupes de 6 : 3 groupes et 2 restent."), [
        T("The groups are equal, but the remainder is not part of the equal sharing; we use only exact divisions here.", "المجموعات متساوية لكن الباقي ليس جزءًا من التوزيع المتساوي؛ نستعمل هنا القسمات التامة فقط.", "Ici on utilise des divisions exactes."),
    ]),
]
