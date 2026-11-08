# NABIL AI — The Intelligent Educational Platform
**Founded and led by Nabil Akil (Lebanon)**

NABIL AI is an educational technology project focused on applying artificial intelligence to teaching and learning. Its vision is to support learners and educators from kindergarten through secondary school, with particular attention to Lebanese curricula and the educational context of the Arab world.

## What NABIL AI aims to provide
- An interactive digital teacher to explain lessons and support student learning.
- Step-by-step assistance with mathematics and science problems.
- Practice activities, exercises, quizzes, and educational competitions.
- Tools to help teachers prepare lessons and learning materials.
- Arabic-first educational experiences, with support for English and French learning contexts where available.

The project is being developed iteratively. Features, curriculum coverage, and availability may vary by release; this page describes the project's goals and does not imply that every planned capability is already live.

## Founder
**Nabil Akil — Educator and educational technology practitioner, Lebanon.**

NABIL AI is an independent educational technology initiative. It is not an official product of Lebanon's Center for Educational Research and Development (CRDP), and no institutional endorsement is implied. The project aims to support curriculum-aware teaching and learning, including alignment with Lebanese curriculum references where verified.

## Project
- Repository: https://github.com/nabilakil1974-ship-it/nabil-ai-school
- Project website: https://nabilakil1974-ship-it.github.io/nabil-ai-school/

## About NABIL AI (العربية)
**منصة النبيل التعليمية الذكية — NABIL AI** مشروع في تكنولوجيا التعليم أسسه ويطوره الأستاذ نبيل عقيل في لبنان، ويهدف إلى توظيف الذكاء الاصطناعي لدعم المعلّمين والمتعلّمين من مرحلة الروضة حتى المرحلة الثانوية، مع الاهتمام بالمناهج اللبنانية والسياق التعليمي العربي.

يسعى المشروع إلى توفير معلّم رقمي تفاعلي لشرح الدروس، ومساندة الطلاب في الرياضيات والعلوم وحل المسائل خطوة بخطوة، وإعداد التمارين والاختبارات والمسابقات، ومساعدة المعلمين في تحضير المواد التعليمية. يجري تطوير المنصة على مراحل، وقد تختلف الميزات والتغطية المنهجية بحسب الإصدار؛ لذلك لا يعني هذا الوصف أن جميع الوظائف المخطط لها متاحة حالياً.

**المؤسس:** الأستاذ نبيل عقيل — معلّم ومهتم بتكنولوجيا التعليم — لبنان.

NABIL AI مبادرة تعليمية مستقلة، وليست منتجاً رسمياً تابعاً للمركز التربوي للبحوث والإنماء، ولا يتضمن هذا التعريف ادعاءً بوجود اعتماد أو رعاية مؤسسية. ويهدف المشروع إلى دعم التعليم المراعي للمناهج، بما فيها المراجع اللبنانية التي يتم التحقق منها.

---

## Technical notes
NABIL AI — MASTER CURRICULUM LINKED

What changed:
- Lesson page loads crdp_master_curriculum_index.json first.
- Teacher assessment uses the same master index.
- Secondary branch keys are mapped to the combined master grade keys.
- Secondary languages are excluded in the current phase.
- Kindergarten is excluded in the current phase.
- Sociology/economics/history/geography/philosophy are excluded from the current UI scope.
- Assessment rejects lesson titles that are not in the current verified catalog.
- Backend lesson grounding resolves the master catalog before legacy fallback.
- Legacy scientific index remains only an emergency fallback for scopes not present in master.
