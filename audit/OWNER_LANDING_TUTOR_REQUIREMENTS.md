# Open landing tutor — owner acceptance criteria (2026-09-19)

Status: REQUESTED, NOT IMPLEMENTED OR VERIFIED.

The existing blue NABIL robot screen is to be the main home page. Remove the separate welcome and grade-only entry screens. Keep grade/subject/language/lesson selection inside the lesson area, but never require these selections for an open spoken or typed question.

The home screen shall greet the student briefly and let students submit typed questions, record a voice question, and see an answer card with the same lesson/solution layout as the main platform. Voice and text share the same backend question understanding, pedagogical rules, transcription, response context, scientific terminology and synthetic voice configuration. No separate simplified voice engine.

Understand colloquial Lebanese Arabic and mixed French/English subject terms and spelling, but answer in the question's language for open questions: an English request to study or draw a function gets the full correct English function study and graph, without switching to Arabic. French requests likewise. When a learner speaks Arabic about a selected English/French lesson, use accessible conversational Arabic while preserving the textbook scientific terms, unless the learner asks for an entirely English/French answer.

The answer board near the robot must render verified subject-appropriate graphs and diagrams using the SAME renderer as in full and interactive lessons; preserve image-uploaded source diagrams and add valid step-by-step annotations only if the renderer supports them. Cards should be readable on mobile. Do not invent figure coordinates.

Improve first-response latency and provide bounded errors, input and processing indicators. Unify the blue visual style across robot, explanation and figure backgrounds. Retain all textbook grounding and source-integrity rules.

Implementation is not done merely by recording this request. Inspect the actual landing HTML/scripts, implement and commit, then verify the current Railway deployment. Beware the existing large legacy app/static/chat.html and raw JavaScript leaking into DOM.

## Owner screenshot follow-up — unified blue visuals and real learning actions

Status: OPEN — requirements recorded; frontend implementation and Railway regression NOT yet verified.

1. **One consistent dark/royal blue backdrop.** The avatar home/lesson panel AND each diagram/figure/graph display area must use the same blue visual family as the top header reading «منصة النبيل التعليمية الذكية», not a white page behind a giant robot or a mismatched canvas. Ensure diagrams, labels, shapes, contrast and scroll remain readable on phones and desktops. Do not recolor a scientific figure in a way that obscures meaning.
2. **Move the “مسار التعلم الذكي” dock lower.** Place it below the answer's «نسخ الإجابة» control and below the response/lesson content, not overlapping the avatar, lesson board or composer. Mobile layout should wrap and scroll naturally; controls must remain clickable and readable.
3. **No empty/demo buttons.** Every learning-path control must perform its named real action *for the actual selected grade, subject, lesson and latest explanation or exercise*. Clicking shows meaningful content immediately in the same answer/learning area, rather than an inert button, a canned response, or a disconnected toast:
   - سؤال تحقق / quick check: one lesson-relevant age-appropriate question and accepts student's answer;
   - تصحيح من فهمي / self-check: asks learner to explain and gives evidence-grounded feedback;
   - جرب بطريقة أخرى / explain differently: changes pedagogical representation, not rephrases;
   - خطوة تالية / next step: a genuine progression within the same lesson;
   - تدريب علاجي / remedial practice: targets an evidenced misunderstanding, not an invented weakness;
   - بطاقات مراجعة / flashcards: real concepts drawn from current lesson;
   - تقدمي / progress: persisted evidence-based learning, never fabricated mastery/XP;
   - any other existing button must have equivalent substantive behavior.
4. **Age adaptation:** early primary uses short sentences, concrete visuals and one task at a time; upper primary uses guided small steps; middle grades add reasoning and graduated practice; secondary uses authentic subject terminology, justification, calculations and diagrams as appropriate. Open-question mode must not require choosing a grade.
5. **Acceptance tests:** for a real textbook-grounded lesson, click EVERY visible learning-path button and verify it submits its intended action, renders its actual result, allows an answer/follow-up, and does not leak code. Verify separately on desktop and phone, and confirm the dock is BELOW «نسخ الإجابة». Screenshot evidence and actual Railway deployed commit required before marking PASS.

## Owner final visual/voice acceptance (2026-09-19)

- Final colour reference is the uploaded rational-function NABIL AI platform screenshot (navy page, blue/cyan borders, blue/cyan titles, green Start Lesson, red microphone, blue Send), NOT the earlier chemistry diagram as the overall palette. Keep graphs' mathematical data-colours untouched.
- Speech must be understandable at the pace of the spoken words: offer a student-visible speed control and make home and lesson use the SAME TTS voice and speed configuration. Never let a welcome message overlap microphone recording; spoken and visual explanations should be consistent. Do not pretend estimated per-word timing is exact synchronisation.
- English and French explanations, controls and copied foreign-language words must use real left-to-right text direction, including when embedded in an Arabic page; Arabic stays right-to-left. Respect displayed mathematics.
- Figures must remain large, uncropped, legible and colour-consistent in full view and preview on desktop and mobile. When the mathematical/scientific request calls for an actual 3D model, render a genuine supported 3D representation with responsive controls; do NOT call a flat drawing 3D or fabricate a model if unsupported.
- In addition to answer-card tabs, understand voice/text commands in Arabic, Lebanese, French and English to show the existing explanation or existing drawing; offer real «عرض الشرح / عرض الرسمة» controls, show the relevant content rather than submitting an unrelated new answer. If a drawing does not exist, clearly say so and let the student request the correct drawing from the shared tutor.
- Record what was implemented and syntax/build checks, plus what cannot be verified without live Railway/browser testing. Running GitHub commits or passing syntax alone does NOT constitute full production acceptance.

## Owner correction: beside-the-student terminology and figure-only (2026-09-19)

- Narration is a companion teacher who says what is being substituted into which formula NOW and shows the exact substitution on screen, e.g. «هلق منحط 4 محل x، فبتصير 2×4+3، ومنحسبها سوا». Do this for every subject at age-appropriate depth; not an essay of static Domain / Given / Formula headings or a theoretical lecture. Spoken and on-screen steps must remain semantically and numerically identical.
- For Lebanese Arabic discussing an English textbook use familiar ENGLISH scientific terms naturally: function (not دالة), numerator (البسط), denominator (المقام), derivative, limit, increasing/decreasing, max/min, graph. For a French textbook use fonction, numérateur, dénominateur, dérivée, limite, croissante/décroissante etc. Crucial: numerator=بسط, denominator=مقام, never invert them even if a speech transcription does. English-only and French-only questions receive fully English/French teaching, respectively. Apply to Math, Physics, Chemistry, Biology and every subject, from kindergarten to Secondary 3.
- On open questions like «Draw a sphere with radius 5 cm, only the figure», return a TRUE VISUAL ONLY in the large blue previewable board; no estimated time, learning objectives, lessons, quick checks, audio lecture, arbitrary dimensions or cylinder comparison. Use the measured radius given in the request, with deterministic fallback when the object is mathematically unambiguous.
- Move the robot artwork to the far-left and give the right answer/diagram board the majority of desktop width, keeping responsive mobile layout and full-size uncropped diagrams. Show the full rich answer plus a separate approximate spoken-word typewriter; do not claim sample-time estimates equal real TTS word timestamps.

Implementation commits: a9cf244, 3409d2a, e6de4ac, f733957, fdadf84, d180edc, e84b9fa, cac76e8; QA tests scripts/test_tutor_contract.py and .github/workflows/nabil-ui-build.yml. GitHub Build phases 14–16 PASS; Railway desktop/mobile + actual TTS + drawing rendering remain REQUIRED for production PASS. A green static build alone is insufficient.
