import math
from scripts.direct_lessons.common import T, F, EX, st
from scripts.direct_lessons.graphs import section, add_ex, add_sec
from scripts.direct_lessons.draw import unit_circle


def upgrade(m):
    s = section(m, "The identity sin² + cos² = 1")
    s.append(unit_circle((30, 45, 60), tag="C1"))
    s.append(T("On the unit circle (radius 1) each point is (cos θ, sin θ). The dashed legs of the right triangle are cos θ and sin θ and the radius is the hypotenuse 1, so Pythagoras gives cos²θ + sin²θ = 1. Check at 30°: 0.866² + 0.5² = 0.75 + 0.25 = 1.",
               "على دائرة الوحدة (نصف القطر 1) كل نقطة هي (cos θ, sin θ). ضلعا المثلث القائم المتقطعان هما cos θ وsin θ ونصف القطر هو الوتر 1 فتعطي فيثاغورس cos²θ + sin²θ = 1. تحقق عند 30°: 0.866² + 0.5² = 0.75 + 0.25 = 1.",
               "Sur le cercle unité, le point est (cos θ ; sin θ) ; Pythagore : cos²θ + sin²θ = 1. À 30° : 0,75 + 0,25 = 1."))
    add_sec(m, ("Special angles", "الزوايا الخاصة", "Angles remarquables"), [
        T("Three angles come up all the time. At 30°: sin = 1/2, cos = √3/2, tan = 1/√3. At 45°: sin = cos = √2/2, tan = 1. At 60°: sin = √3/2, cos = 1/2, tan = √3. Notice sin 30° = cos 60°: the sine of an angle equals the cosine of its complement.",
          "ثلاث زوايا تتكرر دائمًا. عند 30°: sin = 1/2 وcos = √3/2 وtan = 1/√3. عند 45°: sin = cos = √2/2 وtan = 1. عند 60°: sin = √3/2 وcos = 1/2 وtan = √3. لاحظ أن sin 30° = cos 60°: جيب زاوية يساوي جيب تمام متممتها.",
          "30° : 1/2, √3/2, 1/√3. 45° : √2/2, √2/2, 1. 60° : √3/2, 1/2, √3."),
        F("sin 30° = 1/2    cos 30° = √3/2    sin 45° = cos 45° = √2/2    tan 45° = 1"),
    ])
    add_ex(m, [
        EX("", "", st("A right triangle has legs 3 and 4. Find the hypotenuse, sin, cos and tan of the angle opposite the side 3.", "مثلث قائم ضلعاه 3 و4. جد الوتر وsin وcos وtan للزاوية المقابلة للضلع 3.", "Triangle rectangle de côtés 3 et 4 : hypoténuse, sin, cos, tan de l'angle opposé à 3."), [
            T("Hypotenuse = √(9 + 16) = 5.", "الوتر = √(9 + 16) = 5.", "Hypoténuse 5."), T("sin = 3/5, cos = 4/5, tan = 3/4. Check: (3/5)² + (4/5)² = 9/25 + 16/25 = 1 ✓.", "sin = 3/5 وcos = 4/5 وtan = 3/4. تحقق: (3/5)² + (4/5)² = 9/25 + 16/25 = 1 ✓.", "sin = 3/5 ; cos = 4/5 ; tan = 3/4."), F("hyp 5   sin 3/5   cos 4/5   tan 3/4")]),
        EX("", "", st("A 5 m ladder leans on a wall making 60° with the ground. How high does it reach and how far is its foot from the wall?", "سلّم طوله 5 م يستند إلى جدار ويصنع زاوية 60° مع الأرض. إلى أي ارتفاع يصل وكم يبعد طرفه عن الجدار؟", "Échelle de 5 m, 60° avec le sol : hauteur et distance au mur."), [
            T("Height = 5 sin 60° = 5 × 0.866 ≈ 4.33 m. Distance from the wall = 5 cos 60° = 5 × 0.5 = 2.5 m.", "الارتفاع = 5 sin 60° = 5 × 0.866 ≈ 4.33 م. البعد عن الجدار = 5 cos 60° = 5 × 0.5 = 2.5 م.", "h ≈ 4,33 m ; d = 2,5 m."), F("height ≈ 4.33 m      distance = 2.5 m"), F("Check: 4.33² + 2.5² ≈ 18.75 + 6.25 = 25 ✓")]),
        EX("", "", st("A shadow is 12 m long when the Sun is 45° above the horizon. How tall is the tree?", "ظلّ شجرة طوله 12 م حين تكون الشمس بارتفاع 45° فوق الأفق. ما ارتفاع الشجرة؟", "Ombre de 12 m, Soleil à 45° : hauteur de l'arbre ?"), [
            T("tan 45° = height / shadow = 1, so height = 12 m.", "tan 45° = الارتفاع / الظل = 1 إذن الارتفاع = 12 م.", "tan 45° = 1 → 12 m."), F("12 m")]),
        EX("", "", st("If sin θ = 3/5 and θ is acute, find cos θ and tan θ.", "إذا كان sin θ = 3/5 وθ حادة فجد cos θ وtan θ.", "sin θ = 3/5, θ aigu : cos θ et tan θ."), [
            T("cos²θ = 1 − 9/25 = 16/25, and cos θ > 0 for an acute angle: cos θ = 4/5.", "cos²θ = 1 − 9/25 = 16/25 وcos θ > 0 لزاوية حادة: cos θ = 4/5.", "cos θ = 4/5."), F("cos θ = 4/5      tan θ = (3/5)/(4/5) = 3/4")]),
    ])
