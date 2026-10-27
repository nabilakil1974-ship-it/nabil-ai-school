"""Grade 10 Mathematics — Self evaluation: answers and hints."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-027"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Self evaluation — answers and hints", "ar": "التقييم الذاتي — إجابات وتلميحات", "fr": "Auto-évaluation — réponses et indices"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "You solve 2x + 7 = 15 and get x = 11. Which error type is most likely?", "opts": ["Algebra (sign/operation)", "Geometry", "Reading", "None"], "a": 0,
     "why": {"Geometry": _w("There is no figure.", "لا شكل هنا.", "Pas de figure."),
             "Reading": _w("The statement is clear.", "النص واضح.", "Énoncé clair."),
             "None": _w("2×11 + 7 = 29 ≠ 15.", "2×11 + 7 = 29 ≠ 15.", "29 ≠ 15.")}, "ok": "added 7 instead of subtracting"},
    {"q": "You were sure of an answer, but it is wrong. This is …", "opts": ["a misconception worth reviewing", "bad luck", "a calculation slip only", "mastery"], "a": 0,
     "why": {"bad luck": _w("Certainty plus error means a hidden idea.", "ثقة مع خطأ تعني فكرة خاطئة.", "Idée fausse."),
             "a calculation slip only": _w("Maybe, but check the reasoning.", "ربما، لكن راجع الاستدلال.", "Vérifie."),
             "mastery": _w("Not yet.", "ليس بعد.", "Pas encore.")}, "ok": "review it"},
    {"q": "Mastery means …", "opts": ["right reasoning + right result + explaining why", "a right result", "a fast answer", "a guess that works"], "a": 0,
     "why": {"a right result": _w("A guess can give it.", "التخمين قد يعطيه.", "Une devinette."),
             "a fast answer": _w("Speed is not understanding.", "السرعة ليست فهمًا.", "Non."),
             "a guess that works": _w("Explain how you got it.", "اشرح كيف وصلت.", "Explique.")}, "ok": "all three"},
]

THEORY = [
    ("Not an answer page", "ليست صفحة أجوبة", "Pas une page de réponses", "269", [
        T("Hello! Self-evaluation is not a page of answers. The goal is to know what you can do alone and exactly where you stumble. So every problem starts with your own attempt, before any hint.",
          "مرحبًا! التقييم الذاتي ليس صفحة أجوبة. الهدف أن نعرف ماذا تستطيع أن تفعل وحدك وأين تحديدًا تتعثر. لذلك تبدأ كل مسألة بمحاولة منك قبل أي تلميح.",
          "D'abord ta tentative."),
    ]),
    ("The help ladder", "سلّم المساعدة", "L'échelle d'aide", "269", [
        T("Attempt: explain your idea even if you did not finish. Hint 1: only the concept or the starting point. Hint 2: a more specific step, without revealing the whole solution. Then the full reasoning, a check of result and method, and a reflection: what type of error was it?",
          "المحاولة: اشرح فكرتك ولو لم تكمل. التلميح الأول: المفهوم أو نقطة البداية فقط. التلميح الثاني: خطوة أكثر تحديدًا دون كشف الحل كاملًا. ثم الشرح الكامل، ثم التحقق من النتيجة والطريقة، ثم التأمل: ما نوع الخطأ؟",
          "Tentative, indice 1, indice 2, solution."),
        F("Attempt → Hint 1 → Hint 2 → Solution → Check → Reflect"),
    ]),
    ("Fair marking", "تقدير عادل", "Évaluation juste", "270", [
        T("If your final answer is wrong but your reasoning is right until the last arithmetic step, you are not someone who did not understand: we point at the arithmetic slip itself. And if you reach the right answer by guessing, I ask how you got there before calling it mastery.",
          "إذا كان جوابك النهائي خاطئًا لكن استدلالك صحيح حتى آخر خطوة حسابية فلست ممن لم يفهم الدرس: نحدد الخطأ الحسابي نفسه. وإذا أصبت الجواب بتخمين فأسألك كيف وصلت إليه قبل اعتباره إتقانًا.",
          "Raisonnement juste ≠ incompris."),
    ]),
    ("A practice example (our own)", "مثال تدريبي (من إعدادنا)", "Exemple d'entraînement", "270", [
        T("This is original practice, not a question from the book. You start moving terms randomly in 2x + 7 = 15. Hint 1: what do you want to isolate? Hint 2: undo the +7 on both sides. Then 2x = 8 and x = 4. Check: 2×4 + 7 = 15.",
          "هذا تدريب أصلي من إعدادنا وليس سؤالًا من الكتاب. بدأت تنقل الحدود عشوائيًا في 2x + 7 = 15. التلميح الأول: ما الذي تريد عزله؟ التلميح الثاني: تخلّص من +7 في الطرفين. فنجد 2x = 8 وx = 4. نتحقق: 2×4 + 7 = 15.",
          "Exemple original."),
        F("2x + 7 = 15  →  2x = 8  →  x = 4"),
    ]),
    ("Confidence check", "فحص الثقة", "Niveau de confiance", "271", [
        T("After solving, choose: sure, hesitant, or guessed. If you were sure and wrong, that is an important misconception to review. If you were hesitant and right, we fix the reason so success stops being luck and becomes understanding.",
          "بعد الحل اختر: متأكد، متردد، أو خمّنت. إذا كنت متأكدًا وجوابك خاطئ فهذا تصوّر خاطئ مهم نراجعه. وإذا كنت مترددًا وجوابك صحيح نثبّت السبب حتى يتحول النجاح من صدفة إلى فهم.",
          "Sûr / hésitant / deviné."),
    ]),
    ("Error journal", "سجل الأخطاء", "Journal d'erreurs", "271", [
        T("I collect the type of error, not just the number of errors: concept, algebra, geometry, reading or calculation. After several problems I can say: most of your errors are not in the concept but in signs during algebra, so we do a mini-practice on that point.",
          "أجمع نوع الخطأ لا عدد الأخطاء فقط: مفهوم، جبر، هندسة، قراءة أو حساب. وبعد عدة مسائل أقول: معظم أخطائك ليست في المفهوم بل في الإشارات أثناء الجبر، فنعمل تدريبًا مصغّرًا على هذه النقطة.",
          "Type d'erreur."),
        F("concept · algebra · geometry · reading · calculation"),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Try before a hint. Explain reasoning, not only the answer. Hints grow gradually stronger. Classify the error. Mastery = correct reasoning + correct result + the ability to explain why.",
          "نحاول قبل التلميح. نشرح الاستدلال لا الجواب فقط. التلميحات تقوى تدريجيًا. نصنّف الخطأ. الإتقان = استدلال صحيح + نتيجة صحيحة + القدرة على شرح السبب.",
          "Maîtrise = raisonnement + résultat + explication."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Solve 2x + 7 = 15 with the help ladder.", "حلّ 2x + 7 = 15 بسلّم المساعدة.", "Résous 2x + 7 = 15."), [F("2x = 8      x = 4")]),
    EX("2", "", st("Classify the error 2x + 7 = 15 → x = 11.", "صنّف الخطأ 2x + 7 = 15 → x = 11.", "Type d'erreur."), [T("Algebra: 7 was added instead of subtracted.", "جبر: جُمع 7 بدل طرحه.", "Algèbre.")]),
    EX("3", "", st("What do you do after a correct guess?", "ماذا نفعل بعد جواب صحيح بالتخمين؟", "Après une devinette ?"), [T("Explain how you got it.", "نشرح كيف وصلنا إليه.", "Explique.")]),
    EX("4", "", st("Define mastery.", "عرّف الإتقان.", "Définis la maîtrise."), [T("Correct reasoning, correct result, explanation.", "استدلال صحيح ونتيجة صحيحة وشرح.", "Les trois.")]),
]
