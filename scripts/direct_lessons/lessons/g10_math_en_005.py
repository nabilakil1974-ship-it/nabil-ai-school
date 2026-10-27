"""Grade 10 Mathematics — Order of real numbers."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-005"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Order of real numbers", "ar": "ترتيب الأعداد الحقيقية", "fr": "Ordre des réels"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "−5x ≥ 20 → x ? −4", "opts": ["≤", "≥", "<", ">"], "a": 0,
     "why": {"≥": _w("We divided by −5, a negative: the sign reverses.", "قسمنا على −5 وهو سالب: ينعكس الرمز.", "Division par un négatif : on inverse."),
             "<": _w("Reverse ≥ gives ≤, and −4 is included.", "عكس ≥ هو ≤ و−4 مشمولة.", "−4 est inclus."),
             ">": _w("Reverse ≥ gives ≤.", "عكس ≥ هو ≤.", "Inverse de ≥ : ≤.")}, "ok": "x ≤ −4"},
    {"q": "−2x < 6 → x ? −3", "opts": [">", "<", "≤", "="], "a": 0,
     "why": {"<": _w("Dividing by −2 reverses the order.", "القسمة على −2 تعكس الترتيب.", "On inverse."),
             "≤": _w("Strict inequality stays strict.", "المتباينة الصارمة تبقى صارمة.", "Reste strict."),
             "=": _w("It is an inequality.", "هي متباينة.", "Inégalité.")}, "ok": "x > −3"},
    {"q": "From 3 < 8 add −5 to both sides: −2 ? 3", "opts": ["<", ">", "="], "a": 0,
     "why": {">": _w("Adding the same number keeps the order.", "إضافة العدد نفسه تحفظ الترتيب.", "L'addition conserve l'ordre."),
             "=": _w("They are not equal.", "ليسا متساويين.", "Pas égaux.")}, "ok": "−2 < 3"},
]

THEORY = [
    ("Order on the real line", "الترتيب على المستقيم الحقيقي", "L'ordre sur la droite", "55", [
        T("Farther right means greater. a < b means a is to the left of b. So −3 < 2, and −7 < −4. The minus sign must not fool you: look at the position on the line.",
          "الأبعد إلى اليمين هو الأكبر. a < b تعني أن a يقع يسار b. إذن −3 < 2 و−7 < −4. لا تدع إشارة الناقص تخدعك: انظر إلى الموضع على المستقيم.",
          "Plus à droite = plus grand : −7 < −4."),
        F("−7 < −4 < −3 < 2"),
    ]),
    ("Compare by the difference", "المقارنة بالفرق", "Comparer par la différence", "55", [
        T("To compare A and B study A − B: positive means A > B, negative means A < B, zero means equal. Example: 7/4 and 5/3. Denominators are positive, so cross-multiply: 7×3 = 21 and 5×4 = 20. Since 21 > 20, 7/4 > 5/3, with no decimals.",
          "لمقارنة A وB ندرس A − B: موجب يعني A > B وسالب يعني A < B وصفر يعني متساويان. مثال: 7/4 و5/3. المقامات موجبة فنضرب بالتبادل: 7×3 = 21 و5×4 = 20. وبما أن 21 > 20 فإن 7/4 > 5/3 دون كسور عشرية.",
          "7×3 = 21 > 20 = 5×4, donc 7/4 > 5/3."),
        F("7 × 3 = 21      5 × 4 = 20      7/4 > 5/3"),
    ]),
    ("Adding the same number", "إضافة العدد نفسه", "Ajouter le même nombre", "56", [
        T("If a < b then a + c < b + c for any real c: both points move the same distance. −2 < 5, add 4: 2 < 9. 3 < 8, add −5: −2 < 3. Addition or subtraction never reverses the inequality.",
          "إذا كان a < b فإن a + c < b + c لأي عدد حقيقي c: النقطتان تتحركان المسافة نفسها. −2 < 5 وبإضافة 4: 2 < 9. و3 < 8 وبإضافة −5: −2 < 3. الجمع والطرح لا يقلبان المتباينة.",
          "a < b ⇒ a + c < b + c."),
        F("−2 + 4 = 2      5 + 4 = 9      2 < 9"),
    ]),
    ("Multiplying: the sign of the multiplier", "الضرب: إشارة العامل", "Multiplier : le signe", "56", [
        T("Multiplying by a positive number keeps the order: 2 < 5, ×3 gives 6 < 15. Multiplying by a negative number reflects the line about 0 and reverses the order: 2 < 5, ×(−1) gives −2 > −5. 4 < 9, ×(−2) gives −8 > −18. Never decide before knowing the sign of the multiplier.",
          "الضرب في عدد موجب يحفظ الترتيب: 2 < 5 وبالضرب في 3 يصبح 6 < 15. أما الضرب في عدد سالب فينعكس المستقيم حول الصفر فينعكس الترتيب: 2 < 5 وبالضرب في (−1) يصبح −2 > −5. و4 < 9 وبالضرب في (−2) يصبح −8 > −18. لا نقرر قبل معرفة إشارة العامل.",
          "Facteur positif : ordre conservé ; négatif : inversé."),
        F("2 × 3 = 6      5 × 3 = 15      6 < 15"),
        F("−3x < 12  ⇒  x > −4"),
    ]),
    ("Exact before decimal", "الدقة قبل التقريب", "Exact avant décimal", "57", [
        T("Compare √5 and 11/5. Both are positive, so squaring keeps the order: (√5)² = 5 and (11/5)² = 121/25 = 4.84. Since 5 > 4.84, √5 > 11/5. Rounding must not decide the answer.",
          "قارن √5 و11/5. كلاهما موجب فالتربيع يحفظ الترتيب: (√5)² = 5 و(11/5)² = 121/25 = 4.84. وبما أن 5 > 4.84 فإن √5 > 11/5. لا ندع التقريب يقرر الجواب.",
          "√5 > 11/5 car 5 > 121/25."),
        F("(√5)² = 5      (11/5)² = 121/25 = 4.84"),
    ]),
    ("Inequalities and intervals", "المتباينات والمجالات", "Inégalités et intervalles", "57", [
        T("x < 3: all points left of 3, and 3 is not included. x ≤ 3: 3 is included. x ≥ −2 starts at −2, included, and goes right toward +∞; infinity is never included.",
          "x < 3: كل النقاط يسار 3 و3 غير داخلة. x ≤ 3: 3 داخلة. x ≥ −2 تبدأ من −2 المشمولة وتمتد يمينًا نحو +∞، والمالانهاية لا تُشمَل أبدًا.",
          "x ≥ −2 : [−2 ; +∞[."),
        F("x ≥ −2   →   [−2 , +∞["),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Identify the operation and the sign BEFORE touching the inequality symbol. Adding or subtracting never reverses it; multiplying or dividing by a negative does. Moving a term across is not the reason.",
          "نحدّد العملية والإشارة قبل أن نلمس رمز المتباينة. الجمع والطرح لا يقلبانها والضرب أو القسمة على سالب يقلبانها. والانتقال إلى الطرف الآخر ليس هو السبب.",
          "Opération et signe d'abord."),
        F("× or ÷ by a negative  ⇒  reverse the sign"),
    ]),
]

EXERCISES = [
    EX("1", "", st("Compare −7 and −4.", "قارن −7 و−4.", "Compare −7 et −4."), [F("−7 < −4")]),
    EX("2", "", st("From 3 < 8, add −5 to both sides.", "من 3 < 8 أضف −5 إلى الطرفين.", "De 3 < 8, ajoute −5."), [F("3 − 5 = −2      8 − 5 = 3      −2 < 3")]),
    EX("3", "", st("From 4 < 9, multiply by −2.", "من 4 < 9 اضرب في −2.", "De 4 < 9, multiplie par −2."), [F("4 × (−2) = −8      9 × (−2) = −18      −8 > −18")]),
    EX("4", "", st("Solve −5x ≥ 20 and check.", "حلّ −5x ≥ 20 وتحقق.", "Résous −5x ≥ 20."), [T("Divide by −5, a negative, so reverse: x ≤ −4. Test x = −5: −5·(−5) = 25 ≥ 20 true. Test x = 0: 0 ≥ 20 false.", "نقسم على −5 وهو سالب فنعكس: x ≤ −4. نختبر x = −5: −5·(−5) = 25 ≥ 20 صحيح. ونختبر x = 0: 0 ≥ 20 خطأ.", "x ≤ −4."), F("x ≤ −4")]),
    EX("5", "", st("Error detective: −2x < 6 solved as x < −3.", "المحقق: حُلّت −2x < 6 هكذا x < −3.", "Détective : −2x < 6 donne x < −3."), [T("Dividing by −2 reverses the order: x > −3. Test x = 0: 0 < 6 true, and 0 > −3 true.", "القسمة على −2 تعكس الترتيب: x > −3. اختبر x = 0: 0 < 6 صحيح و0 > −3 صحيح.", "x > −3."), F("x > −3")]),
    EX("6", "", st("Solve 7 − 3x ≤ 16.", "حلّ 7 − 3x ≤ 16.", "Résous 7 − 3x ≤ 16."), [F("−3x ≤ 9      x ≥ −3"), T("Check the boundary x = −3: 7 + 9 = 16 ≤ 16, so −3 is included.", "نتحقق من الحد x = −3: 7 + 9 = 16 ≤ 16 فالقيمة −3 مشمولة.", "Borne incluse.")]),
]
