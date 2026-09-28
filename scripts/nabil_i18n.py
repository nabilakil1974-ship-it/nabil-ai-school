#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NABIL AI — Localization Layer
Add-on module: does NOT replace nabil_book_factory.py, imported by it.
Provides Arabic/French/English UI strings for everything student-facing,
and a language-aware prompt wrapper so the LLM narrates/solves in the
lesson's own declared language instead of always English.

Fail-closed: an unknown language code raises rather than silently
falling back to English (silently serving the wrong language to an
Arabic-speaking student is itself a correctness bug).
"""

SUPPORTED_LANGUAGES = ("ar", "fr", "en")

UI_STRINGS = {
    "ar": {
        "view_exercises": "عرض التمارين ➔",
        "back_to_lesson": "⬅ العودة إلى الدرس",
        "phenomenon": "الظاهرة",
        "investigation": "الاستقصاء",
        "observation": "الملاحظة",
        "interpretation": "التفسير",
        "conclusion": "الاستنتاج العلمي",
        "check_understanding": "تحقق من فهمك",
        "worksheet_title": "📝 ورقة عمل تفاعلية للطالب",
        "score_label": "النتيجة",
        "question_label": "السؤال",
        "correct_feedback": "✓ صحيح! ",
        "incorrect_feedback": "✗ غير صحيح. ",
        "ws_correct": "إجابة صحيحة! ",
        "ws_incorrect": "إجابة غير صحيحة. ",
        "exercise_label": "تمرين",
        "problem_label": "مسألة",
        "additional_practice": "تدريب إضافي",
        "additional_practice_note": "تدريب إضافي — تمت الموافقة عليه عبر بوابة التدقيق العلمي للدرس",
        "source_page": "المصدر: صفحة",
        "solve_on_demand": "حل {sec} {num} فورًا ⚡",
        "connecting_solver": "جارٍ الاتصال بمحرك الحل...",
        "verified_solution": "<b>الحل المؤكد:</b><br>",
        "step_label": "الخطوة",
        "final_answer_label": "الإجابة النهائية",
        "solution_error": "<b>خطأ:</b> ",
        "network_error": "<b>خطأ في الشبكة:</b> تعذّر الوصول إلى محرك الحل.",
        "golden_reference_card": "بطاقة المرجع الذهبية",
        "study_reminder": "تذكير للمذاكرة",
        "study_reminder_text": "تمت الصياغة حصرًا من صفحات الكتاب الرسمي {start}–{end}.",
        "official_figure_caption": "شكل من المنهج الرسمي: صفحة {page} (اضغط للتكبير)",
        "exercise_figure_caption": "شكل مرجعي لـ {sec} {num} (اضغط للتكبير)",
        "lab_title": "🔬 المختبر التفاعلي",
        "lab_instructions": "التعليمات",
        "lab_hypothesis": "الفرضية",
        "lab_run": "شغّل التجربة",
        "lab_reset": "إعادة ضبط",
        "lab_result": "النتيجة",
        "lab_conclusion_prompt": "ماذا تستنتج من هذه التجربة؟",
        "quiz_title": "📋 اختبار الدرس",
        "quiz_submit": "تسليم الإجابات",
        "quiz_result_prefix": "نتيجتك:",
        "quiz_pass": "ممتاز، أتقنت هذا الدرس!",
        "quiz_retry": "راجع الدرس وحاول مرة أخرى.",
        "based_on_verified_findings": "استنادًا إلى النتائج الموثقة في «{title}»، ما الاستنتاج المؤكد؟",
        "confirmed_deduction_question": "ما الاستنتاج العلمي المؤكد بشأن «{title}»؟",
        "grounded_feedback": "صحيح، وهذا الاستنتاج مستند مباشرة إلى دليل المنهج الموثق.",
        "grounded_explanation": "مستند مباشرة إلى دليل المنهج في الصفحة {page} (المرجع: {ref}).",
        "formula_law": "القانون / الصيغة",
        "units_label": "الوحدات",
        "extracted_principle": "المبدأ المستخلص",
        "verified_evidence_grounding": "✓ التوثيق بالدليل متحقق",
        "exercises_page_title": "{title} - التمارين والمسائل",
        "solution_steps": "خطوات الحل",
        "quiz_remaining": "متبقية",
        "quiz_explanation": "التفسير",
        "quiz_evidence": "الدليل",
    },
    "fr": {
        "view_exercises": "Voir les exercices ➔",
        "back_to_lesson": "⬅ Retour à la leçon",
        "phenomenon": "Phénomène",
        "investigation": "Investigation",
        "observation": "Observation",
        "interpretation": "Interprétation",
        "conclusion": "Déduction scientifique",
        "check_understanding": "Vérifiez votre compréhension",
        "worksheet_title": "📝 Fiche de travail interactive",
        "score_label": "Score",
        "question_label": "Question",
        "correct_feedback": "✓ Correct ! ",
        "incorrect_feedback": "✗ Incorrect. ",
        "ws_correct": "Correct ! ",
        "ws_incorrect": "Incorrect. ",
        "exercise_label": "Exercice",
        "problem_label": "Problème",
        "additional_practice": "Exercice supplémentaire",
        "additional_practice_note": "Exercice supplémentaire — approuvé par la vérification scientifique de la leçon",
        "source_page": "Source : page",
        "solve_on_demand": "Résoudre {sec} {num} ⚡",
        "connecting_solver": "Connexion au moteur de résolution...",
        "verified_solution": "<b>Solution vérifiée :</b><br>",
        "step_label": "Étape",
        "final_answer_label": "Réponse finale",
        "solution_error": "<b>Erreur :</b> ",
        "network_error": "<b>Erreur réseau :</b> impossible de joindre le moteur de résolution.",
        "golden_reference_card": "Fiche de référence",
        "study_reminder": "Rappel d'étude",
        "study_reminder_text": "Rédigé exclusivement à partir des pages officielles {start}–{end}.",
        "official_figure_caption": "Figure du programme officiel : page {page} (cliquez pour zoomer)",
        "exercise_figure_caption": "Figure de référence pour {sec} {num} (cliquez pour zoomer)",
        "lab_title": "🔬 Laboratoire interactif",
        "lab_instructions": "Instructions",
        "lab_hypothesis": "Hypothèse",
        "lab_run": "Lancer l'expérience",
        "lab_reset": "Réinitialiser",
        "lab_result": "Résultat",
        "lab_conclusion_prompt": "Que concluez-vous de cette expérience ?",
        "quiz_title": "📋 Évaluation de la leçon",
        "quiz_submit": "Soumettre les réponses",
        "quiz_result_prefix": "Votre score :",
        "quiz_pass": "Excellent, leçon maîtrisée !",
        "quiz_retry": "Revoyez la leçon et réessayez.",
        "based_on_verified_findings": "D’après les résultats vérifiés de « {title} », quelle conclusion est confirmée ?",
        "confirmed_deduction_question": "Quelle déduction scientifique est confirmée à propos de « {title} » ?",
        "grounded_feedback": "Correct : cette conclusion est directement fondée sur les preuves vérifiées du programme.",
        "grounded_explanation": "Fondé directement sur les preuves du programme à la page {page} (réf. : {ref}).",
        "formula_law": "Formule / Loi",
        "units_label": "Unités",
        "extracted_principle": "Principe établi",
        "verified_evidence_grounding": "✓ Ancrage dans les preuves vérifié",
        "exercises_page_title": "{title} - Exercices et problèmes",
        "solution_steps": "Étapes de résolution",
        "quiz_remaining": "restantes",
        "quiz_explanation": "Explication",
        "quiz_evidence": "Preuve",
    },
    "en": {
        "view_exercises": "View Exercises ➔",
        "back_to_lesson": "⬅ Back to Lesson",
        "phenomenon": "Phenomenon",
        "investigation": "Investigation",
        "observation": "Observation",
        "interpretation": "Interpretation",
        "conclusion": "Scientific Deduction",
        "check_understanding": "Check Understanding",
        "worksheet_title": "📝 Interactive Student Worksheet",
        "score_label": "Score",
        "question_label": "Question",
        "correct_feedback": "✓ Correct! ",
        "incorrect_feedback": "✗ Incorrect. ",
        "ws_correct": "Correct! ",
        "ws_incorrect": "Incorrect. ",
        "exercise_label": "Exercise",
        "problem_label": "Problem",
        "additional_practice": "Additional Practice",
        "additional_practice_note": "Additional Practice — passed lesson scientific gate",
        "source_page": "Source Page",
        "solve_on_demand": "Solve {sec} {num} On-Demand ⚡",
        "connecting_solver": "Connecting to NABIL Solver Backend...",
        "verified_solution": "<b>Verified Resolution:</b><br>",
        "step_label": "Step",
        "final_answer_label": "Final Answer",
        "solution_error": "<b>Error:</b> ",
        "network_error": "<b>Network Error:</b> Failed to reach solver endpoint.",
        "golden_reference_card": "Golden Reference Card",
        "study_reminder": "Study Reminder",
        "study_reminder_text": "Formulated strictly from official textbook page ranges {start}–{end}.",
        "official_figure_caption": "Official Curriculum Figure: Page {page} (Click to Zoom)",
        "exercise_figure_caption": "Source Figure for {sec} {num} (Click to Zoom)",
        "lab_title": "🔬 Interactive Lab",
        "lab_instructions": "Instructions",
        "lab_hypothesis": "Hypothesis",
        "lab_run": "Run Experiment",
        "lab_reset": "Reset",
        "lab_result": "Result",
        "lab_conclusion_prompt": "What do you conclude from this experiment?",
        "quiz_title": "📋 Lesson Quiz",
        "quiz_submit": "Submit Answers",
        "quiz_result_prefix": "Your score:",
        "quiz_pass": "Excellent, lesson mastered!",
        "quiz_retry": "Review the lesson and try again.",
        "based_on_verified_findings": "Based on the verified findings in “{title}”, what conclusion is confirmed?",
        "confirmed_deduction_question": "Which scientific deduction is confirmed regarding “{title}”?",
        "grounded_feedback": "Correct. This conclusion is grounded directly in verified curriculum evidence.",
        "grounded_explanation": "Grounded directly in curriculum evidence on page {page} (Ref: {ref}).",
        "formula_law": "Formula / Law",
        "units_label": "Units",
        "extracted_principle": "Extracted Principle",
        "verified_evidence_grounding": "✓ Verified Evidence Grounding",
        "exercises_page_title": "{title} - Exercises & Problems",
        "solution_steps": "Solution Steps",
        "quiz_remaining": "remaining",
        "quiz_explanation": "Explanation",
        "quiz_evidence": "Evidence",
    },
}


def resolve_lang_code(entry_language: str) -> str:
    """Map a canonical catalog 'language' field to a supported UI code.

    Fail-closed: never guess. An unrecognized language must be fixed in
    the catalog, not silently defaulted to English.
    """
    raw = str(entry_language or "").strip().lower()
    mapping = {
        "ar": "ar", "arabic": "ar", "العربية": "ar",
        "fr": "fr", "french": "fr", "français": "fr", "francais": "fr",
        "en": "en", "english": "en",
    }
    code = mapping.get(raw)
    if code is None:
        raise RuntimeError(
            f"LANGUAGE_NOT_SUPPORTED: '{entry_language}' has no UI "
            f"localization. Supported: {SUPPORTED_LANGUAGES}"
        )
    return code


def t(lang_code: str, key: str, **kwargs) -> str:
    """Fetch a localized UI string. Raises on missing key (fail-closed) —
    a missing translation must be caught at build time, not shown blank
    to a real student.
    """
    if lang_code not in UI_STRINGS:
        raise RuntimeError(f"LANGUAGE_NOT_SUPPORTED: {lang_code}")
    table = UI_STRINGS[lang_code]
    if key not in table:
        raise RuntimeError(
            f"MISSING_TRANSLATION_KEY: '{key}' not localized for '{lang_code}'"
        )
    text = table[key]
    return text.format(**kwargs) if kwargs else text


def html_dir_attr(lang_code: str) -> str:
    """Return HTML direction and fail closed for an unsupported language."""
    if lang_code not in SUPPORTED_LANGUAGES:
        raise RuntimeError(f"LANGUAGE_NOT_SUPPORTED: {lang_code}")
    return "rtl" if lang_code == "ar" else "ltr"


def narrative_language_instruction(lang_code: str) -> str:
    """Instruction fragment injected into LLM prompts so narration text,
    exercise solutions, and generated practice are produced in the
    lesson's own language rather than defaulting to English.
    """
    names = {
        "ar": "Modern Standard Arabic (الفصحى)",
        "fr": "French",
        "en": "English",
    }
    if lang_code not in names:
        raise RuntimeError(f"LANGUAGE_NOT_SUPPORTED: {lang_code}")
    return (
        f"Write ALL student-facing text (phenomenon, investigation, "
        f"observation, interpretation, conclusion, distractors, exercise "
        f"solution steps, final answers) strictly in {names[lang_code]}. "
        f"Keep any mathematical notation, chemical formulas, and units in "
        f"their standard international symbolic form (unaffected by "
        f"language). Keep prose in the declared lesson language; standard "
        f"mathematical/scientific symbols, formulas, units, and source-authentic "
        f"technical terms may remain unchanged when translation would reduce precision."
    )
