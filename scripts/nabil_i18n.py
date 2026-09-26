#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NABIL AI — طبقة التعريب واللغة.
هذا الملف لا يغيّر الحقيقة العلمية؛ يترجم واجهة الطالب فقط ويجبر السرد على لغة الدرس.
Fail-Closed: أي لغة أو مفتاح غير معروف يوقف البناء بدل أن يعرض لغة خاطئة.
"""

SUPPORTED_LANGUAGES=("ar","fr","en")

UI_STRINGS={
"ar":{
"view_exercises":"عرض التمارين ➔","back_to_lesson":"⬅ العودة إلى الدرس",
"phenomenon":"الظاهرة","investigation":"الاستقصاء","observation":"الملاحظة",
"interpretation":"التفسير","conclusion":"الاستنتاج العلمي","check_understanding":"تحقق من فهمك",
"worksheet_title":"📝 ورقة عمل تفاعلية للطالب","score_label":"النتيجة","question_label":"السؤال",
"ws_correct":"✓ إجابة صحيحة! ","ws_incorrect":"✗ إجابة غير صحيحة. ",
"golden_reference_card":"بطاقة المرجع الذهبية","study_reminder":"تذكير للمذاكرة",
"lab_title":"🔬 المختبر التفاعلي","lab_run":"شغّل التجربة","lab_result":"النتيجة",
"quiz_title":"📋 اختبار الدرس","quiz_submit":"تسليم الإجابات","quiz_result_prefix":"نتيجتك:"
},
"fr":{
"view_exercises":"Voir les exercices ➔","back_to_lesson":"⬅ Retour à la leçon",
"phenomenon":"Phénomène","investigation":"Investigation","observation":"Observation",
"interpretation":"Interprétation","conclusion":"Déduction scientifique","check_understanding":"Vérifiez votre compréhension",
"worksheet_title":"📝 Fiche de travail interactive","score_label":"Score","question_label":"Question",
"ws_correct":"✓ Correct ! ","ws_incorrect":"✗ Incorrect. ",
"golden_reference_card":"Fiche de référence","study_reminder":"Rappel d'étude",
"lab_title":"🔬 Laboratoire interactif","lab_run":"Lancer l'expérience","lab_result":"Résultat",
"quiz_title":"📋 Évaluation de la leçon","quiz_submit":"Soumettre les réponses","quiz_result_prefix":"Votre score :"
},
"en":{
"view_exercises":"View Exercises ➔","back_to_lesson":"⬅ Back to Lesson",
"phenomenon":"Phenomenon","investigation":"Investigation","observation":"Observation",
"interpretation":"Interpretation","conclusion":"Scientific Deduction","check_understanding":"Check Understanding",
"worksheet_title":"📝 Interactive Student Worksheet","score_label":"Score","question_label":"Question",
"ws_correct":"✓ Correct! ","ws_incorrect":"✗ Incorrect. ",
"golden_reference_card":"Golden Reference Card","study_reminder":"Study Reminder",
"lab_title":"🔬 Interactive Lab","lab_run":"Run Experiment","lab_result":"Result",
"quiz_title":"📋 Lesson Quiz","quiz_submit":"Submit Answers","quiz_result_prefix":"Your score:"
}}

def resolve_lang_code(entry_language:str)->str:
    raw=str(entry_language or "").strip().lower()
    mapping={"ar":"ar","arabic":"ar","العربية":"ar","fr":"fr","french":"fr","français":"fr","francais":"fr","en":"en","english":"en"}
    code=mapping.get(raw)
    if code is None:
        raise RuntimeError(f"LANGUAGE_NOT_SUPPORTED: {entry_language!r}; supported={SUPPORTED_LANGUAGES}")
    return code

def t(lang_code:str,key:str,**kwargs)->str:
    if lang_code not in UI_STRINGS:
        raise RuntimeError(f"LANGUAGE_NOT_SUPPORTED: {lang_code}")
    if key not in UI_STRINGS[lang_code]:
        raise RuntimeError(f"MISSING_TRANSLATION_KEY: {key!r} for {lang_code!r}")
    value=UI_STRINGS[lang_code][key]
    return value.format(**kwargs) if kwargs else value

def html_dir_attr(lang_code:str)->str:
    return "rtl" if lang_code=="ar" else "ltr"

def narrative_language_instruction(lang_code:str)->str:
    names={"ar":"Modern Standard Arabic (الفصحى)","fr":"French","en":"English"}
    if lang_code not in names:
        raise RuntimeError(f"LANGUAGE_NOT_SUPPORTED: {lang_code}")
    foreign_rule=(
        "When a scientific/technical term is conventionally written in English or French, "
        "preserve that original term when pedagogically useful. Arabic explanatory prose must be Modern Standard Arabic. "
        "Mathematical notation, fractions, powers, roots, derivatives, functions, chemical formulas, ions, units and symbols "
        "must keep their standard international notation."
    )
    return (
        f"Write all student-facing explanatory prose in {names[lang_code]}. "
        "Use a clear concept-by-concept teaching progression: introduction, explanation, observation/visual or experiment when useful, "
        "scientific conclusion, application, then understanding check. "
        + foreign_rule
    )
