"""Grade 10 Mathematics — Plane sections of common solids."""
from scripts.direct_lessons.common import T, F, EX, st

LESSON_ID = "G10-MATH-EN-024"
GRADE = 10
SUBJECT = "math"
TITLES = {"en": "Plane sections of common solids", "ar": "مقاطع المجسمات المألوفة بمستوٍ", "fr": "Sections planes de solides usuels"}

def _w(en, ar, fr):
    return {"en": en, "ar": ar, "fr": fr}

QUIZ = [
    {"q": "A plane section is …", "opts": ["the intersection of a plane and a solid", "the outside of the solid", "any two points joined", "a drawing"], "a": 0,
     "why": {"the outside of the solid": _w("It lies inside the cut.", "تقع في موضع القطع.", "Intersection."),
             "any two points joined": _w("Points must lie in a common face.", "النقطتان في وجه واحد.", "Même face."),
             "a drawing": _w("It is a geometric set.", "مجموعة هندسية.", "Ensemble géométrique.")}, "ok": "intersection"},
    {"q": "We may join two intersection points only if they lie …", "opts": ["in the same face", "close on paper", "anywhere", "on the same edge only"], "a": 0,
     "why": {"close on paper": _w("Closeness on paper is no proof.", "القرب على الورقة ليس دليلًا.", "Pas une preuve."),
             "anywhere": _w("Segments must lie in faces.", "القطع في الأوجه.", "Dans une face."),
             "on the same edge only": _w("Same face is enough.", "يكفي وجه واحد.", "Même face.")}, "ok": "same face"},
    {"q": "Moving the cutting plane …", "opts": ["can change the section", "never changes it", "changes the solid", "removes faces"], "a": 0,
     "why": {"never changes it": _w("The intersection points change.", "تتغير نقاط التقاطع.", "Points changent."),
             "changes the solid": _w("The solid is fixed.", "المجسم ثابت.", "Fixe."),
             "removes faces": _w("Faces stay.", "الأوجه تبقى.", "Restent.")}, "ok": "section changes"},
]

THEORY = [
    ("Cutting a solid", "قطع المجسم", "Couper un solide", "243", [
        T("Hello! Picture a loaf or a block and pass a very thin flat surface through it. The shape the cut draws inside the solid is the plane section. We do not guess it from the outside shape; we follow where the cutting plane meets the boundary of the solid.",
          "مرحبًا! تخيّل رغيفًا أو قالبًا ومرّر خلاله سطحًا مستويًا رقيقًا جدًا. الشكل الذي يرسمه القطع داخل المجسم هو المقطع المستوي. لا نخمّنه من الشكل الخارجي، بل نتتبع أين يلتقي مستوي القطع بحدود المجسم.",
          "Section = intersection."),
    ]),
    ("The method", "الطريقة", "La méthode", "243", [
        T("Identify the solid and the cutting plane. Look for intersection points with edges or faces. Inside each face we join only points that really lie in that same face, then move on to the neighbouring face until the section closes.",
          "نحدد المجسم ومستوي القطع، ثم نبحث عن نقاط التقاطع مع الحروف أو الأوجه. داخل كل وجه نصل فقط بين نقاط تقع فعلًا في الوجه نفسه، ثم ننتقل إلى الوجه المجاور حتى يُغلق المقطع.",
          "Relier seulement dans une même face."),
        F("intersection points → same face → connect → verify"),
    ]),
    ("Conceptual example", "مثال تصوري", "Exemple", "244", [
        T("If a plane cuts a prism-like solid through three edges at three different points, those points are candidates for the boundary of the section. But we never join two random points across space: every segment of the section must exist in a face the cut passes through.",
          "إذا قطع مستوٍ مجسمًا شبيهًا بالمنشور ومرّ بثلاثة حروف في ثلاث نقاط مختلفة فهذه النقاط مرشحة لتكوين حدود المقطع. لكن لا نصل أي نقطتين عشوائيًا عبر الفراغ: كل قطعة من المقطع يجب أن تقع في وجه يمر به القطع.",
          "Chaque segment est dans une face."),
    ]),
    ("Why the shape changes", "لماذا يتغير الشكل", "Pourquoi la forme change", "244", [
        T("Why can the section change when we move or tilt the plane while the solid stays the same? Because the set of intersection points changes.",
          "لماذا قد يتغير شكل المقطع عندما نحرك المستوي أو نغيّر ميله مع أن المجسم نفسه لم يتغير؟ لأن مجموعة نقاط التقاطع نفسها تتغير.",
          "Les points d'intersection changent."),
    ]),
    ("Error detective", "المحقق", "Détective", "245", [
        T("A student saw four intersection points and joined them by how close they looked on paper. That is not enough. He must say which face contains each segment; if a supposed segment does not lie on a suitable face, the construction is not justified.",
          "رأى طالب أربع نقاط تقاطع فوصلها حسب قربها على الورقة. هذا غير كافٍ. عليه أن يحدد الوجه الذي يحتوي كل قطعة؛ فإن لم تقع القطعة المفترضة على وجه مناسب فالبناء غير مبرَّر.",
          "Nomme la face de chaque segment."),
    ]),
    ("Challenge", "تحدٍّ", "Défi", "245", [
        T("Two different planes cut the same solid. Must the sections be identical? No. In every section each point belongs to both the solid and the cutting plane, and each drawn part respects the faces it crosses.",
          "مستويان مختلفان يقطعان المجسم نفسه. هل يجب أن ينتج مقطعان متطابقان؟ لا. في كل مقطع كل نقطة تنتمي إلى المجسم وإلى مستوي القطع معًا، وكل جزء مرسوم يحترم الأوجه التي يمر بها.",
          "Pas forcément identiques."),
    ]),
    ("Summary", "الخلاصة", "Résumé", "", [
        T("Section = intersection of plane and solid. Find intersection points first, connect only through valid faces, and never construct from a visual guess alone.",
          "المقطع = تقاطع مستوٍ مع مجسم. نجد نقاط التقاطع أولًا ونصل فقط عبر أوجه صحيحة ولا نبني من تخمين بصري وحده.",
          "Points, faces, relier, vérifier."),
    ]),
]

EXERCISES = [
    EX("1", "", st("Define a plane section.", "عرّف المقطع المستوي.", "Définis la section."), [T("The intersection of a plane and a solid.", "تقاطع مستوٍ مع مجسم.", "Intersection.")]),
    EX("2", "", st("Why must section segments lie in faces?", "لماذا يجب أن تقع قطع المقطع في أوجه؟", "Pourquoi dans les faces ?"), [T("Every point must belong to the solid and the plane.", "كل نقطة تنتمي للمجسم والمستوي.", "Solide et plan.")]),
    EX("3", "", st("Error detective: joining four points by closeness.", "المحقق: وصل أربع نقاط بالقرب.", "Détective."), [T("Name the face of each segment.", "نسمّي وجه كل قطعة.", "Nomme la face.")]),
    EX("4", "", st("How can moving the plane change the section?", "كيف يغيّر تحريك المستوي المقطع؟", "Changer le plan."), [T("The intersection points change.", "تتغير نقاط التقاطع.", "Points changent.")]),
]
