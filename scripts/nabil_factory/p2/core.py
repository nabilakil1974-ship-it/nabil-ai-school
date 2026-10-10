from __future__ import annotations

# ==============================================================================
# 2. UNIVERSAL PEDAGOGY & CURRICULUM PROFILES
# ==============================================================================
PEDAGOGY_PROFILES = {
    "L1": {"strategy": ["observe", "explore", "describe", "practice", "check"], "max_concepts": 1},
    "L2": {"strategy": ["phenomenon", "investigation", "observation", "interpretation", "rule", "application", "check"], "max_concepts": 1},
    "L3": {"strategy": ["problem", "analysis", "model", "reasoning", "derivation", "application", "verification"], "max_concepts": 2},
}

SUBJECT_PROFILES = {
    "physics": {
        "sequence": ["phenomenon", "experiment", "observation", "interpretation", "law", "application"],
        "visual_types": ["source_figure", "scientific_diagram", "graph", "simulation"],
    },
    "chemistry": {
        "sequence": ["phenomenon", "experiment", "observation", "particle_model", "equation", "application"],
        "visual_types": ["apparatus", "molecular_model", "equation", "table"],
    },
    "biology": {
        "sequence": ["observation", "structure", "function", "relationship", "interpretation", "application"],
        "visual_types": ["source_figure", "labelled_diagram", "process_diagram"],
    },
    "mathematics": {
        "sequence": ["prerequisite", "concept", "worked_example", "reasoning", "guided_practice", "independent_practice"],
        "visual_types": ["geometric_figure", "graph", "number_line", "table"],
    },
    "general_science": {
        "sequence": ["phenomenon", "investigation", "observation", "concept", "application"],
        "visual_types": ["source_figure", "scientific_diagram", "table"],
    }
}

# Non-science subjects use the same evidence-first architecture. These
# profiles define teaching order/visual form only; lesson facts still come
# exclusively from Evidence Map.
SUBJECT_PROFILES.update({
    "arabic_language": {
        "sequence": ["context", "reading", "meaning", "language_pattern", "rule", "guided_practice", "application"],
        "visual_types": ["text_highlight", "sentence_structure", "sequence", "table"],
    },
    "english_language": {
        "sequence": ["context", "reading", "meaning", "language_pattern", "rule", "guided_practice", "application"],
        "visual_types": ["text_highlight", "sentence_structure", "sequence", "table"],
    },
    "french_language": {
        "sequence": ["context", "reading", "meaning", "language_pattern", "rule", "guided_practice", "application"],
        "visual_types": ["text_highlight", "sentence_structure", "sequence", "table"],
    },
    "history": {
        "sequence": ["context", "source", "chronology", "evidence", "cause_effect", "interpretation", "synthesis"],
        "visual_types": ["timeline", "map", "source_excerpt", "comparison_table"],
    },
    "geography": {
        "sequence": ["map_or_data", "observation", "comparison", "pattern", "interpretation", "application"],
        "visual_types": ["map", "chart", "table", "process_diagram"],
    },
    "civics": {
        "sequence": ["situation", "concept", "rule", "rights_responsibilities", "case_application", "check"],
        "visual_types": ["scenario", "flowchart", "comparison_table"],
    },
    "philosophy": {
        "sequence": ["problematic", "concepts", "argument", "reasoning", "comparison", "synthesis", "critical_check"],
        "visual_types": ["argument_map", "concept_map", "comparison_table"],
    },
    "economics": {
        "sequence": ["situation", "data", "concept", "relationship", "interpretation", "application", "check"],
        "visual_types": ["chart", "table", "flowchart", "graph"],
    },
    "sociology": {
        "sequence": ["situation", "data", "concept", "relationship", "interpretation", "application", "check"],
        "visual_types": ["chart", "table", "relationship_map"],
    },
    "computer_science": {
        "sequence": ["problem", "inputs_outputs", "algorithm", "trace", "test", "debug", "application"],
        "visual_types": ["flowchart", "trace_table", "state_diagram", "code_highlight"],
    },
})

SUBJECT_ALIASES = {
    "math": "mathematics", "maths": "mathematics",
    "mathématiques": "mathematics", "رياضيات": "mathematics",
    "physique": "physics", "فيزياء": "physics",
    "chimie": "chemistry", "كيمياء": "chemistry",
    "biologie": "biology", "أحياء": "biology",
    "science": "general_science", "sciences": "general_science", "علوم": "general_science",
    "arabic": "arabic_language", "arabic_language": "arabic_language",
    "العربية": "arabic_language", "لغة_عربية": "arabic_language",
    "english": "english_language", "english_language": "english_language",
    "الإنجليزية": "english_language", "الانجليزية": "english_language",
    "french": "french_language", "français": "french_language",
    "french_language": "french_language", "الفرنسية": "french_language",
    "histoire": "history", "تاريخ": "history",
    "géographie": "geography", "جغرافيا": "geography",
    "civic_education": "civics", "تربية_مدنية": "civics", "مدنيات": "civics",
    "philosophie": "philosophy", "فلسفة": "philosophy",
    "économie": "economics", "اقتصاد": "economics",
    "sociologie": "sociology", "علم_الاجتماع": "sociology", "اجتماع": "sociology",
    "informatics": "computer_science", "informatique": "computer_science",
    "معلوماتية": "computer_science",
}


TEACHING_ENGINE_PROFILES = {
    "L1": {
        "learner": "early primary",
        "pace": "one concrete idea at a time; very short sentences; frequent visible checks",
        "teacher_moves": [
            "show one concrete object/action",
            "ask the learner to predict or point",
            "name what was observed",
            "state one simple rule",
            "let the learner imitate or try",
            "check with one short question",
        ],
    },
    "L2": {
        "learner": "upper primary/intermediate",
        "pace": "short connected steps; ask why before stating the rule; guided practice before independence",
        "teacher_moves": [
            "start from a visible phenomenon, diagram or problem",
            "ask a focused prediction",
            "run or inspect the evidence",
            "compare what changed and what stayed invariant",
            "explain why in student language",
            "formulate the rule/property",
            "apply it to one guided case",
            "check understanding before moving on",
        ],
    },
    "L3": {
        "learner": "secondary",
        "pace": "compact but rigorous; connect representations; derive or justify before exam-style application",
        "teacher_moves": [
            "state the problem or mathematical/scientific target",
            "separate givens from what must be proved/found",
            "choose and justify the property/model",
            "derive or prove step by step",
            "connect formula, graph, diagram or microscopic model",
            "verify signs, units, domain, assumptions or logical conditions",
            "apply to a representative problem",
            "end with a concise synthesis and independent check",
        ],
    },
}

SUBJECT_TEACHING_ENGINES = {
    "mathematics": {
        "default": [
            "activate the exact prerequisite",
            "show the object/problem",
            "let the learner notice a pattern",
            "name/define the idea",
            "derive or prove the property",
            "work one example while explaining WHY each step is legal",
            "let the learner try a nearby case",
            "verify and summarize",
        ],
        "geometry": [
            "read givens directly on the figure",
            "mark only verified equalities/parallelism/perpendicularity/midpoints",
            "state exactly what is required",
            "choose the theorem/property and explain why its conditions hold",
            "build the proof one relation at a time while the matching visual mark appears",
            "distinguish what is given from what is proved",
            "finish with a compact proof chain and a check question",
        ],
        "functions": [
            "identify the expression and domain first",
            "study limits/intercepts/asymptotes only when applicable",
            "compute and interpret the derivative",
            "build sign/variation reasoning",
            "connect the variation table to the graph",
            "highlight maxima/minima and verified intersections",
            "check the graph against the algebra",
        ],
        "algebra": [
            "identify the target and known form",
            "choose the transformation/property",
            "perform one algebraic move at a time",
            "explain why equivalence is preserved",
            "check by substitution or reverse operation when appropriate",
        ],
        "statistics_probability": [
            "identify population/data/events",
            "organize the given information visually",
            "choose the exact statistic/probability rule",
            "calculate with units/denominators visible",
            "interpret the result in the problem context",
        ],
    },
    "physics": {
        "default": [
            "show the physical situation",
            "identify system, variables and directions",
            "predict what should happen",
            "run/inspect the experiment or diagram",
            "state the observation",
            "explain the physical reason/model",
            "derive/state the law with units and sign convention",
            "apply and verify",
        ],
    },
    "chemistry": {
        "default": [
            "start from the observable change or chemical question",
            "separate macroscopic observation from particle interpretation",
            "identify species/symbols/charges from evidence",
            "show particle/electron/bond changes visually",
            "write and balance the equation only when supported",
            "check atom/charge conservation",
            "apply to a nearby case",
        ],
    },
    "biology": {
        "default": [
            "observe the structure/process",
            "identify parts using verified labels",
            "connect each structure to its function",
            "follow the process in causal order",
            "compare normal/changed states only when evidence supports it",
            "formulate the biological relationship",
            "apply and check understanding",
        ],
    },
    "general_science": {
        "default": [
            "observe the phenomenon",
            "ask a testable question",
            "inspect evidence or run the activity",
            "record what changes and what remains",
            "interpret without exceeding the evidence",
            "formulate the concept",
            "apply and check",
        ],
    },
}




# Teaching engines for languages/humanities remain evidence-driven.
SUBJECT_TEACHING_ENGINES.update({
    "arabic_language": {"default": [
        "read the source in context",
        "highlight the exact word/sentence feature",
        "ask the learner to infer meaning or pattern",
        "explain the language rule from the evidence",
        "apply it to one guided item",
        "let the learner produce or analyze a nearby item",
        "check and summarize",
    ]},
    "english_language": {"default": [
        "read/listen to the source in context",
        "highlight the target expression or structure",
        "infer meaning/pattern from examples",
        "state the language rule or usage clearly",
        "practice one guided item",
        "let the learner respond independently",
        "check and reformulate",
    ]},
    "french_language": {"default": [
        "read/listen to the source in context",
        "highlight the target expression or structure",
        "infer meaning/pattern from examples",
        "state the language rule or usage clearly",
        "practice one guided item",
        "let the learner respond independently",
        "check and reformulate",
    ]},
    "history": {"default": [
        "place the event/source in its verified context",
        "identify actors, dates and places only from evidence",
        "arrange the verified chronology",
        "distinguish evidence from interpretation",
        "explain supported causes/consequences",
        "connect the pieces into a concise historical synthesis",
        "check with a source-based question",
    ]},
    "geography": {"default": [
        "read the map/data/source first",
        "locate and identify verified features",
        "compare values/regions/patterns",
        "describe what the evidence shows",
        "interpret the supported relationship",
        "apply the same reading method to a nearby case",
        "check the conclusion against the data",
    ]},
    "civics": {"default": [
        "start from the verified situation or text",
        "identify the civic concept/rule",
        "separate rights, duties and institutions when present",
        "explain how the rule applies to the case",
        "compare alternatives without adding an outside claim",
        "check with a practical scenario",
    ]},
    "philosophy": {"default": [
        "state the source's problem/question",
        "define concepts from the source context",
        "reconstruct the argument and premises",
        "show the reasoning relation step by step",
        "compare positions only when the source provides them",
        "build a concise synthesis",
        "check whether the conclusion follows from the presented argument",
    ]},
    "economics": {"default": [
        "identify the economic situation and variables",
        "read the verified table/graph/data",
        "define the relevant concept from the lesson",
        "trace the supported relationship",
        "interpret the result in context",
        "apply to a guided case",
        "check against the original data",
    ]},
    "sociology": {"default": [
        "identify the social situation/source",
        "read the verified data or statements",
        "define the relevant concept",
        "map the supported relationships",
        "interpret without exceeding the evidence",
        "apply to a guided case",
        "check against the source",
    ]},
    "computer_science": {"default": [
        "state the exact problem, inputs and expected outputs",
        "trace the given algorithm/code/state",
        "show one execution step at a time",
        "explain why each step changes the state",
        "test with source-supported examples",
        "identify an error only when the trace proves it",
        "summarize the reusable method",
    ]},
})

# Topic modes change HOW NABIL teaches, never WHAT is scientifically true.
# Content still comes only from Evidence Map / verified solution.
SUBJECT_TEACHING_ENGINES["mathematics"].update({
    "trigonometry": [
        "identify the angle/triangle/circle data and the exact target",
        "place the known relations on the visual before calculating",
        "choose the relevant verified trigonometric relation",
        "transform one step at a time with exact symbolic notation",
        "connect algebraic result to the geometry",
        "check sign, interval/quadrant and reasonableness when applicable",
    ],
    "vectors_analytic_geometry": [
        "place points/vectors in the coordinate system",
        "separate geometric information from coordinate data",
        "build the required vector/line relation step by step",
        "show each coordinate operation beside the visual",
        "interpret the algebraic result geometrically",
        "verify the final relation on the diagram",
    ],
    "sequences": [
        "identify how the terms are defined and what is known",
        "generate only source-supported terms or relations",
        "look for the relevant recurrence/direct-form structure",
        "derive the requested relation one step at a time",
        "connect symbolic result to term behavior",
        "check with a permitted term/example",
    ],
    "complex_numbers": [
        "separate algebraic and geometric representations",
        "identify the requested form or geometric meaning",
        "perform one legal complex-number transformation at a time",
        "connect modulus/argument/affix to the diagram when applicable",
        "verify the result in the alternate representation",
    ],
})
SUBJECT_TEACHING_ENGINES["physics"].update({
    "mechanics": [
        "define the system and reference frame",
        "mark directions, known quantities and target on the diagram",
        "predict the motion/effect qualitatively",
        "select the source-supported law/model",
        "derive with signs and units visible",
        "connect equation to motion/force/energy representation",
        "verify dimensions, sign and physical meaning",
    ],
    "electricity": [
        "identify components and actual circuit connections",
        "mark current/voltage directions only when supported",
        "predict the circuit state before calculation",
        "apply the verified circuit law one relation at a time",
        "animate current only when the circuit state permits it",
        "check units, conservation and component values",
    ],
    "optics": [
        "identify the optical elements and reference lines",
        "mark normals/axes/points only when established",
        "trace the verified ray construction step by step",
        "state the applicable optical relation",
        "connect the construction to the conclusion",
        "check orientation/angles against the evidence",
    ],
    "waves": [
        "identify what is oscillating/propagating and the measured variables",
        "show the time/space representation",
        "connect period, frequency, wavelength or speed only when present",
        "derive the requested relation with units",
        "relate the graph/animation to the physical meaning",
        "verify the result against the observed behavior",
    ],
})
SUBJECT_TEACHING_ENGINES["chemistry"].update({
    "acid_base": [
        "identify the given species/solution information",
        "separate observation from acid-base interpretation",
        "write only evidence-supported species/reactions",
        "track the relevant transfer/equilibrium visually",
        "calculate with units and definitions visible",
        "check chemical and charge consistency",
    ],
    "redox": [
        "identify the species before and after change",
        "track oxidation states/electron transfer only when supported",
        "separate oxidation from reduction",
        "balance the verified transformation systematically",
        "check atoms and charge",
        "connect the symbolic equation to the observed process",
    ],
    "organic": [
        "identify the verified functional group/structure",
        "show the structural change visually",
        "name the reaction/property only when supported",
        "track atoms/groups through the transformation",
        "write the verified equation or product",
        "check structure and conservation",
    ],
    "quantitative": [
        "list the measured/given quantities with units",
        "identify the exact amount-of-substance relation",
        "convert units before substitution",
        "calculate symbolically then numerically",
        "connect the number to the chemical meaning",
        "check units and conservation",
    ],
})
SUBJECT_TEACHING_ENGINES["biology"].update({
    "cell": [
        "zoom from whole structure to the verified cell component",
        "identify each labelled part before naming a function",
        "connect structure to function one relation at a time",
        "animate transport/process only when evidence supports it",
        "summarize the cell-level relationship",
        "check by asking the learner to locate or explain one part",
    ],
    "genetics": [
        "identify the given genetic entities and generations/data",
        "separate observation/data from inheritance interpretation",
        "track chromosomes/alleles/process stages visually when supported",
        "build the reasoning chain without skipping a generation or condition",
        "verify ratios/conclusions against the supplied data",
        "finish with one transfer question",
    ],
    "physiology": [
        "locate the organ/structure in the system",
        "follow the verified path of matter/signal/process",
        "connect each structure to its role",
        "explain causal links in order",
        "compare states only when evidence supports the comparison",
        "check the whole pathway from start to finish",
    ],
    "ecology": [
        "identify organisms/populations/environmental factors",
        "map verified relationships visually",
        "follow matter/energy/interaction in the supported direction",
        "interpret changes without inventing causes",
        "connect local relation to the system-level conclusion",
        "check using the same evidence map",
    ],
})


SECONDARY_YEAR_TEACHING = {
    10: {
        "stage": "first_secondary",
        "depth": "build the secondary-school model from prerequisite ideas; keep one new abstraction visible at a time",
        "assessment": "guided transfer before independent multi-step work",
    },
    11: {
        "stage": "second_secondary",
        "depth": "connect several representations and require explicit justification of each chosen law/property",
        "assessment": "multi-step application with an intermediate self-check",
    },
    12: {
        "stage": "third_secondary",
        "depth": "exam-ready synthesis: select the method independently, justify assumptions, and verify the final result rigorously",
        "assessment": "representative exam-style transfer after the concept is understood, never before",
    },
}


def _concept_teaching_text(concept: dict) -> str:
    return (
        str(concept.get("title") or "") + " " +
        str(concept.get("raw_text") or "")
    ).casefold()


def _subject_teaching_mode(concept: dict, subject: str) -> str:
    """Choose a PEDAGOGICAL mode only; this never creates subject facts."""
    text = _concept_teaching_text(concept)
    if subject == "mathematics":
        return _mathematics_teaching_mode(concept)
    if subject == "physics":
        if re.search(r"motion|velocity|speed|acceleration|force|energy|momentum|mouvement|vitesse|accélération|force|énergie|حركة|سرعة|تسارع|قوة|طاقة", text):
            return "mechanics"
        if re.search(r"circuit|current|voltage|resistance|electric|circuit|courant|tension|résistance|دارة|تيار|توتر|جهد|مقاومة|كهرب", text):
            return "electricity"
        if re.search(r"light|mirror|lens|reflection|refraction|optics|lumière|miroir|lentille|réflexion|réfraction|ضوء|مرآة|عدسة|انعكاس|انكسار|بصري", text):
            return "optics"
        if re.search(r"wave|frequency|period|sound|onde|fréquence|période|son|موجة|تواتر|تردد|دور|صوت", text):
            return "waves"
    if subject == "chemistry":
        if re.search(r"acid|base|ph|acide|base|حمض|قاعدة", text):
            return "acid_base"
        if re.search(r"oxid|reduc|redox|electro|أكسد|اختزال|كهروكيمي", text):
            return "redox"
        if re.search(r"organic|hydrocarbon|alcohol|ester|organique|hydrocarbure|alcool|عضوي|هيدروكربون|كحول|إستر", text):
            return "organic"
        if re.search(r"mole|stoich|molar|amount of substance|quantité de matière|مول|ستوكيومتر|كمية المادة", text):
            return "quantitative"
    if subject == "biology":
        if re.search(r"cell|membrane|organelle|cellule|membrane|خلية|غشاء|عضية", text):
            return "cell"
        if re.search(r"gene|dna|chromosome|inherit|gène|adn|chromosome|hérédit|جين|وراث|صبغي|كروموسوم", text):
            return "genetics"
        if re.search(r"organ|system|blood|respir|digest|nerve|organe|système|sang|تنفس|هضم|عصب|عضو|جهاز|دم", text):
            return "physiology"
        if re.search(r"ecosystem|ecology|population|food chain|écosystème|écologie|سلسلة غذائية|نظام بيئي|بيئة", text):
            return "ecology"
    return "default"


def _mathematics_teaching_mode(concept: dict) -> str:
    text = _concept_teaching_text(concept)
    if re.search(
        r"triangle|circle|angle|tangent|parallel|perpendicular|"
        r"midpoint|bisector|congruen|similar|polygon|geometry|"
        r"مثلث|دائرة|زاوية|مماس|متواز|عمود|منتصف|منصف|هندس",
        text,
    ):
        return "geometry"
    if re.search(
        r"function|fonction|domain|domaine|limit|limite|derivative|"
        r"dérivée|asymptote|variation|graph|دال|نهاية|مشتق|مقارب",
        text,
    ):
        return "functions"
    if re.search(
        r"trigon|sine|cosine|tangent ratio|sinus|cosinus|trigonom|"
        r"جيب|جيب تمام|مثلثات",
        text,
    ):
        return "trigonometry"
    if re.search(
        r"vector|coordinate|analytic geometry|droite|repère|vecteur|"
        r"متجه|إحداثي|معلم|مستقيم",
        text,
    ):
        return "vectors_analytic_geometry"
    if re.search(
        r"sequence|suite|recurrence|récurrence|متتالية|تراجعية",
        text,
    ):
        return "sequences"
    if re.search(
        r"complex number|nombre complexe|affix|module|argument|"
        r"عدد مركب|لاحقة|مطال",
        text,
    ):
        return "complex_numbers"
    if re.search(
        r"probability|probabilité|statistics|statistique|mean|median|"
        r"احتمال|إحصاء|متوسط|وسيط",
        text,
    ):
        return "statistics_probability"
    if re.search(
        r"equation|inequality|factor|expand|polynomial|identity|"
        r"معادلة|متراجحة|تحليل|نشر|كثير حدود",
        text,
    ):
        return "algebra"
    return "default"


def resolve_teaching_signature(concept: dict, profile: dict) -> dict:
    subject = profile["subject"]
    level = profile["level"]
    level_spec = TEACHING_ENGINE_PROFILES[level]
    subject_spec = SUBJECT_TEACHING_ENGINES[subject]
    mode = _subject_teaching_mode(concept, subject)
    sequence = subject_spec.get(mode) or subject_spec["default"]
    grade = int(profile.get("grade") or 0)
    secondary_year = SECONDARY_YEAR_TEACHING.get(grade) if level == "L3" else None
    return {
        "level": level,
        "learner": level_spec["learner"],
        "pace": level_spec["pace"],
        "teacher_moves": list(level_spec["teacher_moves"]),
        "subject": subject,
        "mode": mode,
        "subject_sequence": list(sequence),
        "secondary_year_contract": dict(secondary_year) if secondary_year else None,
        "autonomous_teacher": True,
        "human_teacher_required": False,
    }



def _attach_source_verified_student_check(steps, question, concept):
    """Wire source-audited question into SEE→TRY→NOTICE teacher flow.

    Do not fabricate answers: only the already approved question/answer
    accompanying this very concept may become an interactive checkpoint.
    No checkpoint when the source question is missing or unverified.
    """
    if not isinstance(question, dict) or not isinstance(steps, list):
        return steps
    options = question.get("options")
    index = question.get("correct_index")
    prompt = str(question.get("q") or "").strip()
    if (not prompt or not isinstance(options, list) or
            not isinstance(index, int) or not 0 <= index < len(options)):
        return steps
    expected = str(options[index] or "").strip()
    if not expected or not str(concept.get("raw_text") or "").strip():
        return steps
    # The source-scope audit is mandatory. A generated distractor alone never
    # authorizes publishing an answer or blocking a student's progress.
    if not question.get("source_scope_verified", False):
        return steps
    for step in steps:
        if step.get("kind") in ("student_try", "observation", "reasoning"):
            # Do not reveal the answer in the prompt; comparison stays local.
            step["student_check"] = {
                "question": prompt,
                "expected": expected,
                "hint": str(step.get("label") or ""),
                "wrong_feedback": str(question.get("wrong_feedback") or ""),
                "correct_feedback": str(question.get("correct_feedback") or question.get("feedback") or ""),
                "source_page": concept.get("source_page"),
                "concept_id": concept.get("concept_id"),
                "verified_against_source": True,
            }
            break
    return steps


def build_teaching_steps(
        concept: dict, narrative: dict, profile: dict,
        lab_spec: Optional[dict] = None) -> list:
    """Build the student-facing teaching sequence without adding new science.

    The scientific sentences are reused from the already source-audited
    narrative or from the evidence-locked GEOMETRY_PROOF steps.  This function
    decides only pedagogical order/labels for the learner's age and subject.
    """
    sig = resolve_teaching_signature(concept, profile)
    lang = resolve_lang_code(profile["language"])
    subject = sig["subject"]
    mode = sig["mode"]
    concept_id = str(concept.get("concept_id") or "")
    source_page = concept.get("source_page")
    lab_key = f"concept:{concept_id}"

    if isinstance(lab_spec, dict) and str(lab_spec.get("kind") or "").upper() == "GEOMETRY_PROOF":
        out = []
        for idx, proof in enumerate(lab_spec.get("proof_steps") or [], 1):
            sentence = str(proof.get("text") or "").strip()
            if not sentence:
                continue
            out.append({
                "step_id": f"{concept_id}-S{idx:02d}",
                "concept_id": concept_id,
                "kind": "reasoning",
                "order": idx,
                "label": str(proof.get("title") or "").strip(),
                "sentence": sentence,
                "formula": str(proof.get("formula") or "").strip(),
                "evidence": {
                    "concept_id": concept_id,
                    "source_page": source_page,
                    "quote": str(proof.get("evidence_quote") or "").strip(),
                },
                "visual_cues": [{
                    "cue_type": "proof_visual_marks",
                    "target_ids": [str(v) for v in proof.get("target_ids") or []],
                    "reveal_marks": [str(v) for v in proof.get("reveal_marks") or []],
                }],
                "lab_key": lab_key,
            })
        if out:
            return out

    labels = {
        "ar": {
            "math_geometry": ["المعطيات", "ابنِ الفكرة", "لاحظ", "فكّر في السبب", "استنتج"],
            "math_functions": ["ابدأ من الدالة", "ادرس", "لاحظ العلاقة", "فسّر", "استنتج"],
            "math_algebra": ["حدّد المطلوب", "نفّذ خطوة", "لاحظ", "لماذا هذه الخطوة صحيحة؟", "النتيجة"],
            "math_default": ["ابدأ من المعطى", "جرّب", "لاحظ", "فكّر", "استنتج"],
            "physics": ["شاهد الظاهرة", "جرّب", "لاحظ", "فسّر", "استنتج القانون أو القاعدة"],
            "chemistry": ["ابدأ من التغيّر", "جرّب أو تتبّع", "لاحظ", "فسّر على المستوى الجسيمي", "استنتج"],
            "biology": ["لاحظ", "تتبّع البنية أو العملية", "ما الوظيفة؟", "فسّر العلاقة", "استنتج"],
            "general_science": ["لاحظ الظاهرة", "اختبر", "سجّل الملاحظة", "فسّر", "استنتج"],
        },
        "fr": {
            "math_geometry": ["Données", "Construis l’idée", "Observe", "Justifie", "Conclus"],
            "math_functions": ["Pars de la fonction", "Étudie", "Observe la relation", "Interprète", "Conclus"],
            "math_algebra": ["Identifie l’objectif", "Transforme", "Observe", "Justifie", "Résultat"],
            "math_default": ["Pars des données", "Essaie", "Observe", "Réfléchis", "Conclus"],
            "physics": ["Observe le phénomène", "Expérimente", "Observe", "Interprète", "Énonce la loi ou la règle"],
            "chemistry": ["Pars du changement", "Expérimente", "Observe", "Interprète au niveau particulaire", "Conclus"],
            "biology": ["Observe", "Repère la structure ou le processus", "Quelle fonction ?", "Interprète la relation", "Conclus"],
            "general_science": ["Observe le phénomène", "Teste", "Note l’observation", "Interprète", "Conclus"],
        },
        "en": {
            "math_geometry": ["Givens", "Build the idea", "Notice", "Why is this valid?", "Conclude"],
            "math_functions": ["Start from the function", "Study", "Notice the relation", "Interpret", "Conclude"],
            "math_algebra": ["Identify the target", "Transform", "Notice", "Why is this valid?", "Result"],
            "math_default": ["Start from the givens", "Try", "Notice", "Think", "Conclude"],
            "physics": ["See the phenomenon", "Try the experiment", "Observe", "Explain", "State the law or rule"],
            "chemistry": ["Start from the change", "Try or trace", "Observe", "Interpret at particle level", "Conclude"],
            "biology": ["Observe", "Trace the structure or process", "What is its function?", "Explain the relation", "Conclude"],
            "general_science": ["Observe the phenomenon", "Test", "Record the observation", "Explain", "Conclude"],
        },
    }
    labels["ar"].update({
        "language": ["اقرأ في السياق", "جرّب", "لاحظ النمط", "فسّر", "استنتج القاعدة"],
        "history": ["حدّد السياق", "رتّب الأدلة", "لاحظ", "فسّر العلاقة", "ركّب الخلاصة"],
        "geography": ["اقرأ الخريطة أو البيانات", "قارن", "لاحظ النمط", "فسّر", "استنتج"],
        "civics": ["ابدأ من الحالة", "حدّد المفهوم", "طبّق القاعدة", "فسّر", "استنتج"],
        "philosophy": ["اطرح الإشكالية", "حدّد المفاهيم", "حلّل الحجة", "اختبر الترابط", "ركّب الخلاصة"],
        "social_science": ["اقرأ المعطيات", "نظّمها", "لاحظ العلاقة", "فسّر", "استنتج"],
        "computer_science": ["حدّد المطلوب", "تتبّع الخطوات", "لاحظ تغيّر الحالة", "فسّر", "استنتج الطريقة"],
    })
    labels["fr"].update({
        "language": ["Lis en contexte", "Essaie", "Observe le modèle", "Explique", "Formule la règle"],
        "history": ["Situe le contexte", "Ordonne les preuves", "Observe", "Interprète", "Synthétise"],
        "geography": ["Lis la carte ou les données", "Compare", "Observe", "Interprète", "Conclus"],
        "civics": ["Pars de la situation", "Identifie le concept", "Applique la règle", "Explique", "Conclus"],
        "philosophy": ["Pose la problématique", "Définis les concepts", "Analyse l’argument", "Vérifie le raisonnement", "Synthétise"],
        "social_science": ["Lis les données", "Organise", "Observe la relation", "Interprète", "Conclus"],
        "computer_science": ["Identifie l’objectif", "Trace les étapes", "Observe l’état", "Explique", "Dégage la méthode"],
    })
    labels["en"].update({
        "language": ["Read in context", "Try", "Notice the pattern", "Explain", "State the rule"],
        "history": ["Set the context", "Order the evidence", "Notice", "Interpret", "Synthesize"],
        "geography": ["Read the map or data", "Compare", "Notice the pattern", "Interpret", "Conclude"],
        "civics": ["Start from the case", "Identify the concept", "Apply the rule", "Explain", "Conclude"],
        "philosophy": ["State the problem", "Define the concepts", "Analyze the argument", "Test the reasoning", "Synthesize"],
        "social_science": ["Read the data", "Organize it", "Notice the relation", "Interpret", "Conclude"],
        "computer_science": ["Identify the target", "Trace the steps", "Notice the state", "Explain", "Extract the method"],
    })

    if subject == "mathematics":
        label_key = {
            "geometry": "math_geometry",
            "functions": "math_functions",
            "algebra": "math_algebra",
        }.get(mode, "math_default")
    else:
        label_key = {
            "arabic_language": "language",
            "english_language": "language",
            "french_language": "language",
            "history": "history",
            "geography": "geography",
            "civics": "civics",
            "philosophy": "philosophy",
            "economics": "social_science",
            "sociology": "social_science",
            "computer_science": "computer_science",
        }.get(subject, subject if subject in {
            "physics", "chemistry", "biology", "general_science"
        } else "general_science")
    display = labels.get(lang, labels["en"])[label_key]
    fields = [
        ("hook", "phenomenon"),
        ("student_try", "investigation"),
        ("observation", "observation"),
        ("reasoning", "interpretation"),
        ("law_or_rule", "conclusion"),
    ]
    out = []
    order = 0
    for pos, (kind, field) in enumerate(fields):
        sentence = str(narrative.get(field) or "").strip()
        if not sentence:
            continue
        order += 1
        out.append({
            "step_id": f"{concept_id}-S{order:02d}",
            "concept_id": concept_id,
            "kind": kind,
            "order": order,
            "label": display[pos],
            "sentence": sentence,
            "formula": "",
            "evidence": {
                "concept_id": concept_id,
                "source_page": source_page,
                "quote": str(concept.get("raw_text") or "")[:700],
            },
            "visual_cues": [{"cue_type": "point", "target_ids": []}],
            "lab_key": lab_key,
        })

    # Self-heal pedagogical structure locally. The source-scope auditor may
    # legitimately delete generated narrative fields; that must not collapse
    # the teacher sequence below the required three steps. Fill only from
    # already-verified source evidence, never from new scientific generation.
    if len(out) < 3:
        raw_source = re.sub(
            r"\s+", " ", str(concept.get("raw_text") or "")).strip()
        source_chunks = [
            part.strip()
            for part in re.split(r"(?<=[.!?;:])\s+|\n+", raw_source)
            if part.strip()
        ]
        if raw_source and raw_source not in source_chunks:
            source_chunks.append(raw_source)

        existing = {
            re.sub(r"\s+", " ", str(step.get("sentence") or "")).strip()
            for step in out
            if str(step.get("sentence") or "").strip()
        }
        fallback_labels = (
            list(sig.get("subject_sequence") or [])
            or list(sig.get("teacher_moves") or [])
            or ["Observe", "Reason", "Apply"]
        )

        for chunk in source_chunks:
            if len(out) >= 3:
                break
            normalized = re.sub(r"\s+", " ", chunk).strip()
            if not normalized or normalized in existing:
                continue
            order += 1
            out.append({
                "step_id": f"{concept_id}-S{order:02d}",
                "concept_id": concept_id,
                "kind": "evidence_read",
                "order": order,
                "label": str(
                    fallback_labels[(order - 1) % len(fallback_labels)]
                ).strip() or f"Step {order}",
                "sentence": normalized,
                "formula": "",
                "evidence": {
                    "concept_id": concept_id,
                    "source_page": source_page,
                    "quote": raw_source[:700],
                },
                "visual_cues": [{"cue_type": "point", "target_ids": []}],
                "lab_key": lab_key,
            })
            existing.add(normalized)

        # If the verified source is one compact sentence, create pedagogical
        # moves around that SAME evidence. These prompts add no scientific fact.
        safe_prompts = {
            "ar": [
                "اقرأ الدليل الموثق بعناية.",
                "حدّد الفكرة التي يثبتها الدليل الموثق.",
                "طبّق الفكرة بالاعتماد على الدليل الموثق فقط.",
            ],
            "fr": [
                "Lis attentivement la preuve vérifiée.",
                "Repère l'idée établie par la preuve vérifiée.",
                "Applique l'idée en utilisant uniquement la preuve vérifiée.",
            ],
            "en": [
                "Read the verified evidence carefully.",
                "Identify the idea established by the verified evidence.",
                "Apply the idea using only the verified evidence.",
            ],
        }.get(lang, [
            "Read the verified evidence carefully.",
            "Identify the idea established by the verified evidence.",
            "Apply the idea using only the verified evidence.",
        ])

        for prompt_text in safe_prompts:
            if len(out) >= 3:
                break
            order += 1
            out.append({
                "step_id": f"{concept_id}-S{order:02d}",
                "concept_id": concept_id,
                "kind": "evidence_guided",
                "order": order,
                "label": str(
                    fallback_labels[(order - 1) % len(fallback_labels)]
                ).strip() or f"Step {order}",
                "sentence": prompt_text,
                "formula": "",
                "evidence": {
                    "concept_id": concept_id,
                    "source_page": source_page,
                    "quote": raw_source[:700],
                },
                "visual_cues": [{"cue_type": "point", "target_ids": []}],
                "lab_key": lab_key,
            })

        if len(out) >= 3:
            progress(
                "TEACHING_SEQUENCE_SELF_HEALED_FROM_VERIFIED_EVIDENCE",
                concept_id=concept_id,
                source_page=source_page,
                step_count=len(out),
            )
    return out


def resolve_pedagogy_profile(entry: dict) -> dict:
    if "grade" not in entry or entry["grade"] is None:
        raise RuntimeError("CANONICAL_CATALOG_CORRUPT: Missing grade")
    if "language" not in entry or not str(entry["language"]).strip():
        raise RuntimeError("CANONICAL_CATALOG_CORRUPT: Missing mandatory field 'language'")

    grade = int(entry["grade"])
    subject_raw = entry.get("subject", "").strip()
    subject_key = subject_raw.lower().replace(" ", "_")
    subject = SUBJECT_ALIASES.get(subject_key, subject_key)

    if subject not in SUBJECT_PROFILES:
        raise RuntimeError(f"PEDAGOGY_PROFILE_MISMATCH: Unknown curriculum subject '{subject}'")

    level = "L1" if grade <= 6 else ("L2" if grade <= 9 else "L3")
    return {
        "level": level,
        "level_profile": PEDAGOGY_PROFILES[level],
        "subject": subject,
        "subject_raw": subject_raw,
        "subject_profile": SUBJECT_PROFILES[subject],
        "branch": entry.get("branch") or entry.get("track") or "",
        "language": entry["language"],
        "grade": grade,
    }



# ==============================================================================
# 7. MULTI-MODAL GROUNDED SOLVER & STRICT FAIL-CLOSED VERIFIER
# ==============================================================================
def grounded_subject_solver(exercise: dict, evidence_map: dict, profile: dict) -> Dict[str, Any]:
    prompt = exercise["exact_source_prompt"]
    page = exercise.get("source_page")
    subj = profile["subject"]
    grade = profile.get("grade", 7)
    source_origin = exercise.get("source_origin", "TEXTBOOK")

    fig_base64 = None
    if exercise.get("figure_refs"):
        for p in evidence_map["pages_evidence"]:
            if p["page_num"] == page:
                for f in p["figures"]:
                    if f["figure_id"] in exercise["figure_refs"]:
                        try:
                            fig_base64 = base64.b64encode(
                                Path(f["image_path"]).read_bytes()
                            ).decode("ascii")
                        except Exception as exc:
                            raise RuntimeError(
                                "FIGURE_EVIDENCE_MISSING: Cannot read "
                                f"referenced source image: {exc}")
                        break

    all_scope = [
        {
            "concept_id": c.get("concept_id"),
            "title": c.get("title"),
            "source_page": c.get("source_page"),
            "text": c.get("normalized_text") or c.get("raw_text"),
        }
        for c in evidence_map.get("concepts", [])
        if str(c.get("normalized_text") or c.get("raw_text") or "").strip()
    ]

    if source_origin == "TEXTBOOK":
        provenance = f"official textbook exercise verbatim from Page {page}"
        source_exercise_examples = [
            {
                "source_kind": "TEXTBOOK_EXERCISE_EVIDENCE",
                "exercise_id": e.get("exercise_id"),
                "number": e.get("number"),
                "source_page": e.get("source_page"),
                "text": e.get("exact_source_prompt"),
            }
            for e in evidence_map.get("exercise_evidence", [])
            if e.get("verified_against_source") is True
            and str(e.get("exact_source_prompt") or "").strip()
        ]
        supported_scope = all_scope + source_exercise_examples
    else:
        provenance = (
            "additional practice exercise already approved by the strict "
            "lesson-scope scientific gate"
        )
        supported = set(exercise.get("scope_concept_ids") or [])
        supported_scope = [
            item for item in all_scope
            if item.get("concept_id") in supported
        ]

    if not supported_scope:
        raise RuntimeError(
            "PRE_SOLVE_FAILED: no verified lesson scope for exercise")

    scope_note = (
        "\nVERIFIED LESSON EVIDENCE — use this and the exercise itself only:\n"
        + json.dumps(supported_scope, ensure_ascii=False)
    )

    reconstructed_note = ""
    if exercise.get("reconstructed_diagram_verified"):
        reconstructed_note = (
            "\nUse ONLY this independently verified NABIL schematic plan as "
            "the student-facing visual. The original textbook/source image, if "
            "available, is hidden evidence only and must never be reproduced "
            "or exposed to the student: "
            + json.dumps(
                exercise.get("reconstructed_diagram_plan") or {},
                ensure_ascii=False)
        )

    solver_lang_code = resolve_lang_code(profile["language"])
    figure_rule = (
        "A verified source figure is attached. Treat only relationships actually "
        "visible in that figure as visual evidence. Never claim that objects are "
        "connected, aligned, equal, parallel, at the same level, measured, or "
        "made of a particular material unless the prompt, verified lesson text, "
        "or attached figure establishes that relationship."
        if fig_base64 else
        "No source figure is attached. Do not infer any missing geometry or "
        "visual relationship."
    )
    query = (
        f"You are Teacher NABIL, master professor of Lebanese "
        f"{subj.capitalize()} Grade {grade}.\n"
        f"{narrative_language_instruction(solver_lang_code)}\n"
        f"Solve this {provenance}.\n"
        f"Prompt: {prompt}\n"
        f"Subquestions: {json.dumps(exercise.get('subquestions', []))}"
        f"{scope_note}{reconstructed_note}\n\n"
        "STRICT SOURCE RULES:\n"
        "1. Answer the textbook task directly and minimally. The final_answer "
        "must itself answer EVERY explicit requested action/subquestion; do not "
        "leave a required part only in the reasoning steps.\n"
        "2. Every explanatory fact, law, property, example, material, unit, "
        "quantity, or scientific relationship must come from the exercise "
        "prompt, VERIFIED LESSON EVIDENCE, or a verified attached figure.\n"
        "3. Do not add general textbook knowledge merely because it is true. "
        "For example/list/classification questions, give the requested answer "
        "without adding unrelated background facts. Preserve exact source labels "
        "and example names when available; do not generalize them. Do not add "
        "unrequested drawing actions such as shading, coloring, measuring, "
        "marking, or construction steps unless the prompt/source requires them.\n"
        f"4. {figure_rule}\n"
        "5. If the prompt asks for a drawing, describe only what must be drawn "
        "from the verified rule and visible source geometry.\n"
        "Return strictly JSON: {'steps': [str], 'final_answer': str}"
    )
    _feedback = str(exercise.get("_solver_feedback") or "").strip()
    if _feedback:
        query = query.replace(
            "Return strictly JSON: {'steps'",
            "YOUR PREVIOUS ANSWER WAS REJECTED BY A DETERMINISTIC ARITHMETIC "
            "VERIFIER: " + _feedback[:600] + "\nRewrite the solution so EVERY "
            "calculation is a pure numeric equality on its own step (e.g. "
            "'5^2 × 5^4 = 25 × 625 = 15625'; for several parts start each step "
            "with its label 'a)', 'b)'...). Check each equality is true. "
            "final_answer must state ONLY values your steps computed.\n"
            "Return strictly JSON: {'steps'", 1)

    vision_context = ({
        "lesson_id": exercise.get("lesson_id"),
        "book_id": evidence_map.get("book_id"),
        "pdf_page": page,
    } if fig_base64 else None)

    def _generate_solution(extra_instruction: str = "") -> Tuple[dict, dict]:
        parsed = _execute_llm_json_strict(
            query + extra_instruction,
            image_base64=fig_base64,
            vision_context=vision_context,
            purpose=f"exercise_solution_{exercise.get('exercise_id')}",
            max_attempts=3,
        )
        provenance_data = get_last_llm_provenance()
        if not isinstance(parsed, dict):
            raise ValueError("Incomplete solver response schema")
        if not isinstance(parsed.get("steps"), list) or not parsed.get("steps"):
            raise ValueError("Incomplete solver steps")
        if not str(parsed.get("final_answer") or "").strip():
            raise ValueError("Incomplete solver final answer")
        return parsed, dict(provenance_data)

    def _audit_solution(candidate: dict) -> Tuple[dict, dict]:
        audit_prompt = (
            "Act as a DELETE-FIRST source-grounding auditor for a school "
            "exercise solution. Compare every step and the final answer against "
            "the exercise prompt, VERIFIED LESSON EVIDENCE, and the attached "
            "verified source figure when present.\n"
            "Reject unsupported embellishment even if scientifically true. "
            "A direct answer required by the exercise may be kept, but its "
            "explanation may not introduce outside facts. Any statement about "
            "connections, relative levels, orientation, shape, measurements, "
            "materials, or geometry must be stated in the prompt/evidence or be "
            "visibly established by the attached figure.\n"
            "Return strict JSON: {"
            "'keep_step_indexes':[int],"
            "'final_answer_valid':bool,"
            "'final_answer_complete':bool,"
            "'figure_faithful':bool,"
            "'no_unrequested_actions':bool,"
            "'pruned_solution_valid':bool,"
            "'reasons':[str]"
            "}. keep_step_indexes are ZERO-BASED indexes of steps that can remain "
            "unchanged. final_answer_complete=true only when the final answer "
            "itself answers every explicit requested action/subquestion. "
            "no_unrequested_actions=false for extra procedures such as shading, "
            "coloring, measuring, marking or construction not requested/supported "
            "by source evidence. pruned_solution_valid=true only when keeping exactly "
            "those steps plus the unchanged final answer produces a correct, "
            "complete, source-grounded solution. If no figure is attached, "
            "figure_faithful must be true.\n"
            f"Exercise: {prompt}\n"
            f"VERIFIED LESSON EVIDENCE: "
            f"{json.dumps(supported_scope, ensure_ascii=False)}\n"
            f"Candidate solution: {json.dumps(candidate, ensure_ascii=False)}"
        )
        parsed_audit = _execute_llm_json_strict(
            audit_prompt,
            image_base64=fig_base64,
            vision_context=vision_context,
            purpose=f"exercise_solution_audit_{exercise.get('exercise_id')}",
            max_attempts=3,
        )
        if not isinstance(parsed_audit, dict):
            raise ValueError("Incomplete solution audit schema")
        return parsed_audit, dict(get_last_llm_provenance())

    try:
        parsed, solution_provenance = _generate_solution()
        audit, verification_provenance = _audit_solution(parsed)

        def _apply_delete_first(candidate: dict, verdict: dict) -> Optional[dict]:
            try:
                keep = sorted({
                    int(x) for x in (verdict.get("keep_step_indexes") or [])
                    if 0 <= int(x) < len(candidate.get("steps") or [])
                })
            except (TypeError, ValueError):
                keep = []
            if not (
                verdict.get("final_answer_valid") is True
                and verdict.get("final_answer_complete") is True
                and verdict.get("figure_faithful") is True
                and verdict.get("no_unrequested_actions") is True
                and verdict.get("pruned_solution_valid") is True
                and keep
            ):
                return None
            removed = [
                idx for idx in range(len(candidate["steps"])) if idx not in keep
            ]
            for idx in removed:
                progress(
                    "REMOVED_OUT_OF_SCOPE_SOLUTION_STEP",
                    exercise_id=exercise.get("exercise_id"),
                    number=exercise.get("number"),
                    step_index=idx,
                )
            cleaned = dict(candidate)
            cleaned["steps"] = [candidate["steps"][idx] for idx in keep]
            cleaned["scope_audit_reasons"] = list(verdict.get("reasons") or [])
            return cleaned

        cleaned = _apply_delete_first(parsed, audit)
        if cleaned is None:
            progress(
                "SOLUTION_STRICT_REGENERATION_REQUIRED",
                exercise_id=exercise.get("exercise_id"),
                number=exercise.get("number"),
                reasons=[str(x) for x in (audit.get("reasons") or [])][:6],
            )
            correction = (
                "\n\nYour previous candidate failed source/figure grounding. "
                "Generate a NEW, shorter solution from scratch. Do not repeat "
                "the rejected claims. Use only the prompt, verified lesson "
                "evidence, and attached verified figure. Auditor reasons: "
                + json.dumps(audit.get("reasons") or [], ensure_ascii=False)
            )
            parsed, solution_provenance = _generate_solution(correction)
            audit, verification_provenance = _audit_solution(parsed)
            cleaned = _apply_delete_first(parsed, audit)

        if cleaned is None:
            raise RuntimeError(
                "SOLVER_SOLUTION_VALIDATION_FAILED:"
                f"{audit.get('reasons', [])}")

        exercise["solution_status"] = "SOLVED"
        cleaned["ai_provenance"] = {
            "solution": dict(solution_provenance),
            "verification": dict(verification_provenance),
        }
        cleaned["source_scope_audited"] = True
        return cleaned
    except (ProviderDailyQuotaError, ProviderTransientError,
            ProviderUnavailableError, NeedsAttentionError):
        raise
    except Exception as e:
        raise RuntimeError(
            "PRE_SOLVE_FAILED: grounded solver unavailable or failed for "
            f"Ex #{exercise['number']}: {e}")



def _apply_math_contract_or_omit(entry: dict, ex: dict, sol, regen=None):
    """V18 deterministic math gate with targeted regeneration.

    Returns (solution, regenerated) or (None, False) after marking ONLY this
    exercise unapproved (kept in the source backlog with its reason). A rejected
    solution is never reused: it is regenerated alone, up to
    NABIL_MATH_REGEN_MAX times (default 1), each time with the verifier's reason.
    """
    max_regen = max(0, min(3, int(os.getenv("NABIL_MATH_REGEN_MAX", "1"))))
    regenerated = False
    attempt = 0
    while True:
        try:
            return enforce_math_solution_contract(
                ex, sol, str(entry.get("subject") or "")), regenerated
        except RuntimeError as exc:
            reason = str(exc)
            if not (reason.startswith("MATH_SOLUTION_CONTRADICTION")
                    or reason.startswith("MATH_EXPRESSION_UNVERIFIED")):
                raise
            kind = ("CONTRADICTED" if reason.startswith("MATH_SOLUTION_CONTRADICTION")
                    else "VERIFIER_COULD_NOT_PARSE")
            if regen is not None and attempt < max_regen:
                attempt += 1
                progress("MATH_CONTRACT_REGENERATING_EXERCISE",
                         exercise_id=ex.get("exercise_id"), number=ex.get("number"),
                         attempt=attempt, kind=kind, reason=reason[:240])
                try:
                    ex["_solver_feedback"] = reason
                    sol = regen()
                    regenerated = True
                    continue
                except RuntimeError as regen_exc:
                    if not str(regen_exc).startswith("PRE_SOLVE_FAILED"):
                        raise
                    reason = reason + " | REGEN_FAILED:" + str(regen_exc)[:200]
                finally:
                    ex.pop("_solver_feedback", None)
            ex["solution_status"] = "OMITTED_UNVERIFIED"
            ex["_pre_solved_solution"] = None
            ex["solution_omission_reason"] = reason[:500]
            ex["solution_rejection_kind"] = kind
            progress("MATH_CONTRACT_EXERCISE_UNAPPROVED",
                     exercise_id=ex.get("exercise_id"), number=ex.get("number"),
                     kind=kind, reason=reason[:300])
            return None, False


def prepare_verified_solutions(entry: dict, exercises: list,
                               profile: dict, ev_map: dict,
                               drive_service=None,
                               persist: bool = False) -> None:
    """Solve once, checkpoint each verified exercise, and resume independently.

    Provider/transient failures pause the lesson; they are never converted into
    OMITTED_UNVERIFIED.  Scientific/source validation failures keep the original
    item-level fail-closed omission policy.
    """
    page_checkpoints = None
    checkpoint_root = None
    if persist:
        if drive_service is None:
            raise RuntimeError("SOLUTION_CHECKPOINT_REQUIRES_DRIVE_SERVICE")
        from scripts import nabil_page_checkpoint as page_checkpoints
        checkpoint_root = resolve_drive_root_id()

    for ex in exercises:
        if ex.get("solution_mode") != "PRE_SOLVED":
            continue
        unit_id = str(ex.get("exercise_id") or ex.get("number") or "exercise")
        cached = None
        if page_checkpoints:
            cached = page_checkpoints.load_solution(
                drive_service, checkpoint_root, entry, ex)
        if cached is not None:
            cached, repaired_powers = repair_numeric_power_payload(cached)
            if repaired_powers:
                page_checkpoints.save_solution(
                    drive_service, checkpoint_root, entry, ex, cached)
                progress(
                    "SOLUTION_NUMERIC_POWER_CACHE_SELF_HEALED",
                    exercise_id=ex.get("exercise_id"),
                    number=ex.get("number"),
                    repaired_claims=repaired_powers,
                )
            remaining_bad = check_power_claims(
                json.dumps(cached, ensure_ascii=False))
            if remaining_bad:
                raise RuntimeError(
                    "SOLUTION_NUMERIC_POWER_REPAIR_INCOMPLETE:"
                    + json.dumps(remaining_bad[:8], ensure_ascii=False))
            def _regen_cached():
                fresh = grounded_subject_solver(ex, ev_map, profile)
                fresh, _r = repair_numeric_power_payload(fresh)
                return fresh
            cached, _regen = _apply_math_contract_or_omit(
                entry, ex, cached, regen=_regen_cached)
            if cached is None:
                continue
            if _regen and page_checkpoints:
                page_checkpoints.save_solution(
                    drive_service, checkpoint_root, entry, ex, cached)
            ex["solution_status"] = "SOLVED"
            ex["_pre_solved_solution"] = cached
            progress("SOLUTION_RESTORED_FROM_DRIVE",
                     exercise_id=ex.get("exercise_id"),
                     number=ex.get("number"))
            continue

        try:
            sol = grounded_subject_solver(ex, ev_map, profile)
        except RuntimeError as exc:
            if not str(exc).startswith("PRE_SOLVE_FAILED"):
                raise
            _raise_if_provider_pause_required(
                entry, drive_service,
                unit_id=unit_id,
                operation="exercise_solution",
                exc=exc,
            )
            # Reaching here means the failure was not a provider availability,
            # quota, request-shape, or content-refusal class. Preserve the
            # scientific/source fail-closed item policy.
            ex["solution_status"] = "OMITTED_UNVERIFIED"
            ex["_pre_solved_solution"] = None
            ex["solution_omission_reason"] = str(exc)[:500]
            progress(
                "SKIPPED_UNVERIFIED_EXERCISE_SOLUTION",
                exercise_id=ex.get("exercise_id"),
                number=ex.get("number"),
                reason=str(exc)[:240],
            )
            continue

        sol, repaired_powers = repair_numeric_power_payload(sol)
        if repaired_powers:
            progress(
                "SOLUTION_NUMERIC_POWER_FRESH_SELF_HEALED",
                exercise_id=ex.get("exercise_id"),
                number=ex.get("number"),
                repaired_claims=repaired_powers,
            )
        remaining_bad = check_power_claims(
            json.dumps(sol, ensure_ascii=False))
        if remaining_bad:
            raise RuntimeError(
                "SOLUTION_NUMERIC_POWER_REPAIR_INCOMPLETE:"
                + json.dumps(remaining_bad[:8], ensure_ascii=False))
        def _regen_fresh():
            fresh = grounded_subject_solver(ex, ev_map, profile)
            fresh, _r = repair_numeric_power_payload(fresh)
            return fresh
        sol, _regen = _apply_math_contract_or_omit(
            entry, ex, sol, regen=_regen_fresh)
        if sol is None:
            continue
        ex["solution_status"] = "SOLVED"
        ex["_pre_solved_solution"] = sol
        if page_checkpoints:
            page_checkpoints.save_solution(
                drive_service, checkpoint_root, entry, ex, sol)
            # save_solution performs remote read-back verification; failure is
            # fail-closed and propagates as CheckpointWriteError.
            progress("SOLUTION_SAVED_TO_DRIVE",
                     exercise_id=ex.get("exercise_id"),
                     number=ex.get("number"))


def retain_only_verified_solved_exercises(
        exercises: list, *, origin: Optional[str] = None) -> List[dict]:
    """Drop only the exercise that cannot be solved/verified; never drop the lesson."""
    kept = []
    for ex in exercises:
        if origin and ex.get("source_origin", "TEXTBOOK") != origin:
            continue
        solved = (
            ex.get("solution_status") == "SOLVED"
            and isinstance(ex.get("_pre_solved_solution"), dict)
            and bool(ex["_pre_solved_solution"].get("steps"))
            and bool(str(ex["_pre_solved_solution"].get("final_answer") or "").strip())
        )
        if solved:
            kept.append(ex)
        else:
            progress(
                "EXERCISE_DROPPED_NOT_LESSON",
                exercise_id=ex.get("exercise_id"),
                number=ex.get("number"),
                origin=ex.get("source_origin", "TEXTBOOK"),
                reason=str(ex.get("solution_omission_reason") or
                           "NOT_SCIENTIFICALLY_VERIFIED")[:240],
            )
    return kept


def strip_source_rasters_from_student_html(
        html_text: str, ev_map: dict, page_name: str) -> str:
    """Absolute student-facing ban on textbook/page/figure raster pixels.

    Source figures remain available internally to OCR/vision/scientific audit.
    Only NABIL-generated SVG/redraw/lab visuals may reach the lesson pages.
    """
    source_paths = set()
    source_basenames = set()
    for page in ev_map.get("pages_evidence", []):
        for fig in page.get("figures") or []:
            raw = str(fig.get("image_path") or "").strip()
            if raw:
                source_paths.add(raw)
                source_basenames.add(Path(raw).name)

    img_re = re.compile(r"<img\b[^>]*>", re.I | re.S)
    src_re = re.compile(r"\bsrc\s*=\s*([\"'])(.*?)\1", re.I | re.S)
    removed = 0

    def scrub(match):
        nonlocal removed
        tag = match.group(0)
        sm = src_re.search(tag)
        src_value = sm.group(2).strip() if sm else ""
        low = src_value.lower()
        is_source = (
            low.startswith("data:image/")
            or low.startswith("file:")
            or any(path and path in src_value for path in source_paths)
            or any(name and name in src_value for name in source_basenames)
            or ("page" in low and ("cache" in low or "source" in low))
            or ("figure" in low and ("cache" in low or "source" in low))
        )
        if is_source:
            removed += 1
            return "<!-- NABIL: source textbook raster removed; evidence remains internal -->"
        return tag

    cleaned = img_re.sub(scrub, html_text)
    if removed:
        progress("STUDENT_SOURCE_RASTERS_REMOVED",
                 page=page_name, count=removed)

    # Belt-and-suspenders: source raster data URLs must never survive.
    if re.search(r"<img\b[^>]*\bsrc\s*=\s*['\"]data:image/", cleaned, re.I | re.S):
        raise RuntimeError(
            f"STUDENT_SOURCE_RASTER_LEAK_BLOCKED:{page_name}")
    for raw in source_paths:
        if raw and raw in cleaned:
            raise RuntimeError(
                f"STUDENT_SOURCE_RASTER_PATH_LEAK_BLOCKED:{page_name}")
    return cleaned

def build_factory_solution_card_spec(
        entry: dict, exercise: dict, solution: dict) -> Dict[str, Any]:
    """Build the approved Scientific Solution Card payload from verified data only.

    This layer never solves or changes a scientific value. It only maps the
    already-verified solver output into the shared frontend card contract.
    """
    lang_code = resolve_lang_code(entry.get("language", "en"))
    subject = str(entry.get("subject", "")).strip()
    kind_map = {
        "mathematics": "mathematics",
        "math": "mathematics",
        "physics": "physics",
        "chemistry": "chemistry",
        "biology": "biology",
        "science": "general_science",
        "general science": "general_science",
    }
    kind = kind_map.get(subject.lower(), subject.lower() or "general_science")
    steps = [
        str(step).strip() for step in solution.get("steps", [])
        if str(step).strip()
    ]
    final_answer = str(solution.get("final_answer") or "").strip()
    if not steps or not final_answer:
        raise RuntimeError("SCIENTIFIC_SOLUTION_CARD_REQUIRES_VERIFIED_SOLUTION")

    sections = [{
        "label": ui_t(lang_code, "solution_steps"),
        "items": steps,
    }]
    method = str(solution.get("method") or "").strip()
    if method:
        sections.insert(0, {
            "label": ui_t(lang_code, "formula_law"),
            "items": [method],
        })
    verification = solution.get("verification") or []
    if isinstance(verification, str):
        verification = [verification] if verification.strip() else []
    else:
        verification = [
            str(item).strip() for item in verification if str(item).strip()
        ]

    return {
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "lab_key": str(
            exercise.get("_solution_lab_key")
            or exercise.get("_prebuilt_lab_key")
            or ""
        ),
        "exercise_id": str(exercise.get("exercise_id") or ""),
        "kind": kind,
        "subject": subject,
        "language": lang_code,
        "title": str(exercise.get("exact_source_prompt") or entry["canonical_title"])[:220],
        "sections": sections,
        "key_results": [final_answer],
        "verification": verification,
        "source": {
            "lesson_id": entry["lesson_id"],
            "book_id": entry["book_id"],
            "source_page": exercise.get("source_page"),
            "exercise_id": exercise.get("exercise_id"),
            "source_origin": exercise.get("source_origin", "TEXTBOOK"),
        },
    }


def solve_exercise_on_demand_payload(lesson_id: str, sec_type: str, ex_num: int) -> Dict[str, Any]:
    """Universal On-Demand Backend Resolution — Zero Hardcode."""
    ev_path = PERM_EVIDENCE_DIR / f"{lesson_id}.json"
    if not ev_path.exists():
        raise RuntimeError(f"EVIDENCE_NOT_FOUND: {lesson_id}")

    ev_map = json.loads(ev_path.read_text(encoding="utf-8"))
    entry = resolve_canonical_entry(lesson_id)
    profile = resolve_pedagogy_profile(entry)

    matched = None
    for ex in ev_map.get("exercise_evidence", []):
        if ex["section_type"].upper() == sec_type.upper() and int(ex["number"]) == int(ex_num):
            matched = ex
            break

    if not matched:
        raise RuntimeError(f"EXERCISE_NOT_FOUND: {sec_type} #{ex_num} in lesson {lesson_id}")

    sol = grounded_subject_solver(matched, ev_map, profile)
    card = build_factory_solution_card_spec(entry, matched, sol)
    return {"status": "SUCCESS", "solution": sol, "solution_card": card}



# ==============================================================================
# 8. EVIDENCE-DRIVEN SYNTHESIS
# ==============================================================================
def sanitize_generated_narrative(
        concept: dict, narrative: dict, profile: dict,
        figure_image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None) -> dict:
    """Remove unsupported generated claims at field/item level.

    The official source concept is never edited here. Only AI-generated
    explanation fields, distractors, formulas and units can be removed.
    """
    scalar_fields = [
        "phenomenon", "investigation", "observation", "interpretation",
        "conclusion", "distractor_1", "distractor_2",
    ]
    source_text = str(concept.get("raw_text") or "")
    audit_prompt = (
        "You are a strict curriculum-grounding auditor. Compare the GENERATED "
        "content with the VERIFIED SOURCE text and the verified source figure "
        "when supplied. This audit is DELETE-ONLY: never rewrite, repair, add, "
        "or improve any generated statement.\n"
        "For phenomenon, investigation, observation, interpretation and "
        "conclusion: keep a field only when every scientific claim is supported "
        "by the source evidence.\n"
        "For distractor_1 and distractor_2: keep only when it is intentionally "
        "incorrect as a misconception, uses only concepts/vocabulary within the "
        "lesson scope, and introduces no outside fact, law, apparatus, unit, "
        "quantity or prerequisite.\n"
        "For formulas and units: keep only indexes whose entire item is explicitly "
        "supported by the verified evidence.\n"
        "If uncertain, remove it. Return strict JSON exactly as "
        "{\"keep_fields\":[str],\"keep_formula_indexes\":[int],"
        "\"keep_unit_indexes\":[int],\"removed_reasons\":{str:str}}.\n"
        "Allowed keep_fields: " + json.dumps(scalar_fields) + "\n"
        "VERIFIED SOURCE:\n" + source_text + "\nGENERATED:\n" +
        json.dumps(narrative, ensure_ascii=False)
    )
    try:
        audit = _execute_llm_json_strict(
            audit_prompt,
            image_base64=figure_image_base64,
            vision_context=vision_context,
            purpose=f"narrative_scope_audit_{concept.get('concept_id')}",
        )
    except (ProviderDailyQuotaError, ProviderTransientError,
            ProviderUnavailableError, NeedsAttentionError):
        raise
    except Exception as exc:
        progress(
            "GENERATED_NARRATIVE_AUDIT_FAILED_CONTENT_REMOVED",
            concept_id=concept.get("concept_id"),
            reason=str(exc)[:240],
        )
        audit = {
            "keep_fields": [],
            "keep_formula_indexes": [],
            "keep_unit_indexes": [],
            "removed_reasons": {
                "all": "AUDIT_UNAVAILABLE_FAIL_CLOSED"
            },
        }

    if not isinstance(audit, dict):
        audit = {}
    keep_fields = {
        str(x) for x in (audit.get("keep_fields") or [])
        if str(x) in scalar_fields
    }
    formula_indexes = {
        int(x) for x in (audit.get("keep_formula_indexes") or [])
        if isinstance(x, int) or (isinstance(x, str) and x.isdigit())
    }
    unit_indexes = {
        int(x) for x in (audit.get("keep_unit_indexes") or [])
        if isinstance(x, int) or (isinstance(x, str) and x.isdigit())
    }
    reasons = audit.get("removed_reasons")
    if not isinstance(reasons, dict):
        reasons = {}

    cleaned = dict(narrative)
    removed = []
    for field in scalar_fields:
        value = str(cleaned.get(field) or "").strip()
        if value and field not in keep_fields:
            removed.append(field)
            cleaned[field] = ""
            progress(
                "REMOVED_OUT_OF_SCOPE_GENERATED_CONTENT",
                concept_id=concept.get("concept_id"),
                component="narrative_field",
                field=field,
                reason=str(reasons.get(field) or "NOT_VERIFIED_AGAINST_SOURCE")[:240],
            )

    formulas = list(cleaned.get("formulas") or [])
    kept_formulas = []
    for idx, value in enumerate(formulas):
        if idx in formula_indexes:
            kept_formulas.append(value)
        else:
            progress(
                "REMOVED_OUT_OF_SCOPE_GENERATED_CONTENT",
                concept_id=concept.get("concept_id"),
                component="formula",
                field=str(idx),
                reason=str(reasons.get(f"formula_{idx}") or
                           "FORMULA_NOT_VERIFIED_AGAINST_SOURCE")[:240],
            )
    cleaned["formulas"] = kept_formulas

    units = list(cleaned.get("units") or [])
    kept_units = []
    for idx, value in enumerate(units):
        if idx in unit_indexes:
            kept_units.append(value)
        else:
            progress(
                "REMOVED_OUT_OF_SCOPE_GENERATED_CONTENT",
                concept_id=concept.get("concept_id"),
                component="unit",
                field=str(idx),
                reason=str(reasons.get(f"unit_{idx}") or
                           "UNIT_NOT_VERIFIED_AGAINST_SOURCE")[:240],
            )
    cleaned["units"] = kept_units
    cleaned["_removed_generated_fields"] = removed
    cleaned["_scope_audited"] = True
    return cleaned


def synthesize_concept_narrative(
        concept: dict, profile: dict,
        figure_image_base64: Optional[str] = None,
        vision_context: Optional[Dict[str, Any]] = None) -> dict:
    narrative_lang_code = resolve_lang_code(profile["language"])
    teaching_signature = resolve_teaching_signature(concept, profile)
    prompt = (
        f"You are Teacher NABIL, an autonomous digital teacher teaching this concept so a learner can understand it without a human teacher operating the lesson. "
        "Stay grounded STRICTLY in the extracted textbook text and verified source figure when provided. "
        "Teach like an excellent student-facing tutor: start directly, use small logical steps, explain WHY each move is made, ask the learner to notice/predict/try, and never dump textbook prose. "
        f"AGE/LEVEL TEACHING CONTRACT: {json.dumps(teaching_signature, ensure_ascii=False)}. "
        "Follow the subject_sequence as the pedagogical order, but NEVER add a scientific or mathematical fact that is not supported by evidence. "
        "Do NOT sound like a scanned textbook and do NOT reproduce textbook layout. Re-teach the idea in a natural classroom flow: "
        "phenomenon = what the learner should first LOOK AT or wonder about; "
        "investigation = what the learner should TRY or manipulate; "
        "observation = what the learner can NOTICE from the evidence; "
        "interpretation = the short WHY/WHAT-DOES-THIS-MEAN discussion; "
        "conclusion = the concise rule the learner should formulate. "
        "Keep each field short, concrete and age-appropriate. The lesson flow must feel like: SEE → TRY → NOTICE → THINK → CONCLUDE → APPLY. "
        f"Generate plausible wrong answers (distractors) derived only from common misconceptions of this same text.\n\n"
        f"{narrative_language_instruction(narrative_lang_code)}\n"
        + ("When the lesson language is Arabic, write clear Modern Standard Arabic (فصحى) only; understand dialect but do not imitate it. " if narrative_lang_code == "ar" else "")
        + "Preserve established mathematical/scientific terminology, symbols and units.\n\n"
        f"TEXT: {concept['raw_text']}\n\n"
        f"Subject: {profile['subject']}, Level: {profile['level']}\n"
        "Return strictly JSON: {"
        "'phenomenon': str, 'investigation': str, 'observation': str, 'interpretation': str, 'conclusion': str, "
        "'distractor_1': str, 'distractor_2': str, 'formulas': [str], 'units': [str]"
        "} — every field must be traceable to the TEXT above."
    )
    try:
        res = execute_llm_completion(
            prompt, json_mode=True, temperature=0.0,
            image_base64=figure_image_base64,
            vision_context=vision_context,
            operation=f"concept_narrative_{concept.get('concept_id')}",
            unit_id=str(concept.get("concept_id") or "concept"))
        parsed = json.loads(res)
        for k in ["phenomenon", "investigation", "observation", "interpretation", "conclusion", "distractor_1", "distractor_2"]:
            if not parsed.get(k):
                raise ValueError(f"Missing field {k}")
        cleaned = sanitize_generated_narrative(
            concept, parsed, profile,
            figure_image_base64=figure_image_base64,
            vision_context=vision_context)
        if narrative_lang_code == "ar":
            for key in (
                "phenomenon", "investigation", "observation",
                "interpretation", "conclusion", "distractor_1", "distractor_2",
            ):
                _assert_formal_arabic_text(
                    cleaned.get(key, ""),
                    purpose=f"narrative_{concept.get('concept_id')}_{key}",
                )
            cleaned["_formal_arabic_verified"] = True
        return cleaned
    except Exception as e:
        raise RuntimeError(f"NARRATIVE_SYNTHESIS_FAILED: Unable to ground concept narrative from evidence ({e})")


def _normalized_lab_evidence(value: str) -> str:
    # تطبيع بسيط للتحقق من أن الاقتباس الذي استند إليه المختبر موجود فعلاً في الدليل.
    return re.sub(r"\\s+", " ", str(value or "")).strip().lower()


def _deduction_question(lang_code: str, title: str) -> str:
    # صياغة السؤال بحسب لغة الدرس، من دون تغيير المصطلح العلمي الأصلي.
    if lang_code == "ar":
        return f"أي استنتاج علمي تؤكده الأدلة الخاصة بـ «{title}»؟"
    if lang_code == "fr":
        return f"Quelle déduction scientifique est confirmée par les preuves concernant « {title} » ?"
    return f"Which scientific deduction is confirmed by the evidence for '{title}'?"


def build_verified_lab_spec(entry: dict, concept: dict, narrative: dict, profile: dict,
                            figure_image_base64: Optional[str] = None,
                            vision_context: Optional[Dict[str, Any]] = None) -> dict:
    """
    يبني Lab Spec من الدليل نفسه.
    لا يُسمح للموديل بإدخال أرقام أو قوانين أو سلوك غير موجود في النص/الشكل الموثق.
    إذا المفهوم لا يناسب مختبراً من الأنواع المدعومة، يعيد supported=false.
    """
    lang_code = resolve_lang_code(entry["language"])
    math_records = concept.get("math_records") or []
    prompt = (
        "You are designing ONE evidence-grounded interactive educational lab strictly from verified curriculum evidence.\n"
        "If the SOURCE or verified FIGURE explicitly describes a manipulable change, observable invariant, quantitative relation, ordered process, or experiment that fits one of the allowed kinds, you MUST return supported=true and build it. "
        "Return supported=false only when no allowed interaction can be supported without adding scientific information. Never suppress an applicable lab just because the specification is difficult to produce.\n"
        "Allowed kinds only:\n"
        "1) FORMULA_CALCULATOR: only when an explicit two-input formula using +, -, *, or / exists in SOURCE or MATH_RECORDS. "
        "Never invent min/max/default/step values; the student will enter numbers.\n"
        "2) ORIENTATION_INVARIANT: only when SOURCE/FIGURE explicitly establishes that an observable element keeps a horizontal or vertical orientation while its surrounding object changes orientation.\n"
        "3) SHAPE_RESPONSE: only when SOURCE/FIGURE explicitly establishes that the observed object's shape is fixed or conforms to a changed container/boundary.\n"
        "4) DC_SERIES_CIRCUIT: only when SOURCE explicitly supports a two-resistor series circuit, Ohm's law, same-current-in-series, series equivalent resistance, AND the open/closed-switch current rule. "
        "Required fields: resistors=[two source labels], switch_control=true, rules={series_resistance_sum:true,series_same_current:true,ohms_law:true,open_switch_zero_current:true}.\n"
        "5) OPTICS_REFLECTION: only when SOURCE explicitly supports a normal perpendicular to the reflecting surface, angles measured from the normal, AND angle of incidence equals angle of reflection. "
        "Required fields: angles_measured_from_normal=true, normal_perpendicular_surface=true, law='angle_of_incidence_equals_angle_of_reflection'.\n"
        "6) IONIC_COMPOUND: only when SOURCE explicitly supports ionic electron transfer, the cation/anion charges, the whole-number ion ratio, and charge neutrality. "
        "Required fields: cation={symbol,charge}, anion={symbol,charge}, cation_ratio, anion_ratio, electron_transfer_count, bond_type='ionic'.\n"
        "7) GEOMETRY_PROOF: prefer this for geometry theorems/proofs/constructions when SOURCE or verified FIGURE supports named points/segments and proof relations. "
        "Required: points=[{label,x,y}] with x,y as 0..100 LAYOUT coordinates only; segments=[{id,a,b}]; marks=[...]; proof_steps=[...]. "
        "Allowed mark types: equal_segments, equal_angles, perpendicular, parallel, midpoint, symmetry_axis. "
        "Every mark MUST carry evidence_quote copied exactly from SOURCE. Equal segment marks use targets=[segment ids]; equal angle/perpendicular marks use angles=[{a,vertex,b}]; parallel/midpoint use targets; symmetry_axis uses axis_segment and optional point_pairs. "
        "Every proof step MUST contain title,text,formula,target_ids,reveal_marks,evidence_quote; evidence_quote must be an exact SOURCE quote. "
        "In target_ids use ONLY a mark id, point:<point label>, or segment:<segment id>; order target_ids to match the spoken sentences so the teacher arrow follows the sentence meaning. "
        "Never add an equality tick, equal-angle arc, right-angle square, parallel arrow, midpoint mark, congruence implication or symmetry effect merely because the sketch looks that way.\n"
        "8) PROCEDURE_OBSERVATION: prefer this when SOURCE explicitly describes a practical experiment, investigation, hands-on procedure, materials/apparatus, ordered actions, and/or observable outcomes. "
        "Required: procedure_steps=[{label,evidence_quote}] with 1..8 exact SOURCE-backed steps; observations=[{label,evidence_quote}] with 1..6 exact SOURCE-backed observations; materials=[{label,evidence_quote}] is optional and may contain ONLY materials/apparatus explicitly named by SOURCE. "
        "Never invent apparatus, quantities, safety instructions, control variables, measurements, outcomes, or procedural steps. If SOURCE does not state them, omit them.\n"
        "9) EVIDENCE_SEQUENCE: for ANY subject when SOURCE explicitly gives two or more ordered or structurally related evidence-backed ideas, parts, stages, transformations, constructions, grammatical steps, historical developments, geographic relations, or other explainable sequence that can be highlighted or animated without inventing a missing fact. "
        "Required field: steps=[{label:str,evidence_quote:str}] with 2..8 ordered steps; every evidence_quote must be an exact contiguous SOURCE quote.\n"
        "10) EVIDENCE_REVEAL: universal fallback for ANY subject/concept when no richer lab kind fits. "
        "Use 1..8 exact SOURCE-backed items and reveal/highlight them interactively. "
        "Required field: items=[{label:str,evidence_quote:str}], each evidence_quote an exact contiguous SOURCE quote. "
        "This means every concept can still have a real interactive lab without inventing science.\n"
        "For DC_SERIES_CIRCUIT, OPTICS_REFLECTION and IONIC_COMPOUND also return evidence_quotes: an object containing an EXACT SOURCE quote for EACH scientific invariant declared by the spec.\n"
        "Every supported lab must contain an exact evidence quote from SOURCE when evidence_basis=text. "
        "If evidence_basis=figure, a verified source figure must be supplied.\n"
        "Every supported lab MUST include teacher_script with 2..12 steps derived from THIS evidence, never a canned demo. "
        "Each step contains say,target_ids,action,state_before,state_after,scientific_constraints,evidence_quote. "
        "Allowed actions: point,highlight,set_state,animate,observe,explain,conclude. "
        "Apply state_after BEFORE NABIL speaks its consequence; target_ids follow the sentence meaning. "
        "For circuits, current/charge flow is forbidden while switch_closed=false; close the switch visibly first. "
        "For every domain, animate/reveal a result only after its evidence-backed conditions are established. "
        "All states/actions/constraints come from SOURCE or verified FIGURE; never invent science for animation.\n"
        "Student-facing title/instructions/observation must stay within the scientific meaning of the evidence.\n"
        "AGE APPROPRIATENESS: Grades 1-3 use one short concrete action/observation at a time and minimal text; Grades 4-9 use a guided prediction/procedure/observation flow; Grades 10-12 may use rigorous variables, relations, and interpretation ONLY when those details are explicitly supported by SOURCE. "
        "Age adaptation changes wording and interaction pacing only; it must never add scientific content.\n"
        + narrative_language_instruction(lang_code) + "\n\n"
        f"CONCEPT_ID: {concept['concept_id']}\n"
        f"SUBJECT: {profile['subject']}\n"
        f"GRADE: {profile.get('grade', entry.get('grade', ''))}\n"
        f"PEDAGOGY_LEVEL: {profile.get('level', '')}\n"
        f"SOURCE: {concept.get('raw_text','')}\n"
        f"MATH_RECORDS: {json.dumps(math_records, ensure_ascii=False)}\n"
        f"GROUNDED_NARRATIVE: {json.dumps(narrative, ensure_ascii=False)}\n\n"
        "Return strict JSON. For unsupported: "
        "{'supported': false, 'reason': str, 'evidence_ref': str}. "
        "For supported include: supported=true, kind, title, instructions, observation, evidence_ref, evidence_basis ('text'|'figure'), evidence_quote. "
        "FORMULA_CALCULATOR additionally: source_formula and formula={output,input_a,input_b,operator,output_unit}. "
        "ORIENTATION_INVARIANT additionally: invariant_orientation ('horizontal'|'vertical'). "
        "SHAPE_RESPONSE additionally: behavior ('fixed'|'conforms'). "
        "GEOMETRY_PROOF additionally uses the exact points/segments/marks/proof_steps schema above. "
        "PROCEDURE_OBSERVATION additionally: materials=[{label,evidence_quote}] optional, procedure_steps=[{label,evidence_quote}], observations=[{label,evidence_quote}]. "
        "EVIDENCE_SEQUENCE additionally: steps=[{label,evidence_quote}]. "
        "EVIDENCE_REVEAL additionally: items=[{label,evidence_quote}]. "
        "Advanced science kinds must include the exact fields listed above plus evidence_quotes."
    )
    try:
        spec = _execute_llm_json_strict(
            prompt,
            image_base64=figure_image_base64,
            vision_context=vision_context,
            purpose=f"lab_spec_{concept.get('concept_id')}",
            max_attempts=3,
        )
    except (ProviderDailyQuotaError, ProviderTransientError,
            ProviderUnavailableError, NeedsAttentionError):
        raise
    except Exception as exc:
        raise RuntimeError(f"LAB_SPEC_JSON_INVALID: {exc}") from exc

    if not isinstance(spec, dict):
        raise RuntimeError("LAB_SPEC_INVALID: expected object")
    if spec.get("supported") is not True:
        # Universal classroom contract: every concept must still have an
        # interactive lab. When no richer simulation is justified, fall back
        # deterministically to an evidence-reveal lab built only from the
        # verified source text. No new scientific claim is introduced.
        source_text = str(concept.get("raw_text") or "").strip()
        if not source_text:
            raise RuntimeError("LAB_FALLBACK_SOURCE_EMPTY")
        fallback_quote = source_text[:700]
        spec = {
            "supported": True,
            "kind": "EVIDENCE_REVEAL",
            "title": str(concept.get("title") or "NABIL Interactive Explanation"),
            "instructions": {
                "ar": "استكشف الفكرة مع نبيل خطوة خطوة.",
                "fr": "Explore l’idée avec NABIL étape par étape.",
                "en": "Explore the idea with NABIL step by step.",
            }.get(resolve_lang_code(entry.get("language", "en")), "Explore the idea with NABIL step by step."),
            "observation": {
                "ar": "كل ما يظهر هنا مأخوذ من الدليل الموثق لهذه الفكرة.",
                "fr": "Tout ce qui apparaît ici vient de la preuve vérifiée de cette idée.",
                "en": "Everything shown here comes from the verified evidence for this idea.",
            }.get(resolve_lang_code(entry.get("language", "en")), "Everything shown here comes from the verified evidence for this idea."),
            "evidence_ref": concept["concept_id"],
            "evidence_basis": "text",
            "evidence_quote": fallback_quote,
            "items": [{
                "label": str(concept.get("title") or "Verified idea"),
                "evidence_quote": fallback_quote,
            }],
            "fallback_reason": str(spec.get("reason") or "NO_RICHER_LAB_KIND"),
            "teacher_script": [
                {"say": str(concept.get("title") or "Observe the verified evidence."), "target_ids": ["evidence:0"], "action": "point",
                 "state_before": {"revealed_index": -1}, "state_after": {"revealed_index": 0},
                 "scientific_constraints": ["Reveal only verified source evidence."], "evidence_quote": fallback_quote},
                {"say": str(concept.get("title") or "Focus on the verified evidence."), "target_ids": ["evidence:0"], "action": "highlight",
                 "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
                 "scientific_constraints": ["Highlight only verified source evidence."], "evidence_quote": fallback_quote},
                {"say": str(narrative.get("observation") or concept.get("title") or "Observe the verified evidence."), "target_ids": ["evidence:0"], "action": "observe",
                 "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
                 "scientific_constraints": ["Do not exceed verified source evidence."], "evidence_quote": fallback_quote},
                {"say": str(narrative.get("conclusion") or narrative.get("observation") or concept.get("title") or "Conclude from the verified evidence."),
                 "target_ids": ["evidence:0"], "action": "conclude",
                 "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
                 "scientific_constraints": ["Do not exceed verified source evidence."], "evidence_quote": fallback_quote},
            ],
        }
        progress(
            "LAB_UNIVERSAL_EVIDENCE_REVEAL_FALLBACK",
            concept_id=concept.get("concept_id"),
            source_page=concept.get("source_page"),
        )
    # A provider can return a scientifically useful supported lab while omitting
    # the teacher_script object.  That is a recoverable output-shape failure,
    # not a reason to discard the verified lesson.  First ask for a bounded,
    # evidence-locked repair of the EXISTING spec.  If repair still fails,
    # downgrade only this lab to the deterministic EVIDENCE_REVEAL contract.
    # We never fabricate domain state transitions for a richer lab.
    def _teacher_script_shape_valid(value: Any) -> bool:
        if not isinstance(value, list) or not 2 <= len(value) <= 12:
            return False
        allowed_actions = {"point", "highlight", "set_state", "animate", "observe", "explain", "conclude"}
        for teacher_step in value:
            if not isinstance(teacher_step, dict):
                return False
            if not str(teacher_step.get("say") or "").strip():
                return False
            if str(teacher_step.get("action") or "") not in allowed_actions:
                return False
            if not isinstance(teacher_step.get("target_ids"), list):
                return False
            if not isinstance(teacher_step.get("state_before"), dict):
                return False
            if not isinstance(teacher_step.get("state_after"), dict):
                return False
            if not isinstance(teacher_step.get("scientific_constraints"), list):
                return False
            if not str(teacher_step.get("evidence_quote") or "").strip():
                return False
        return True

    teacher_script = spec.get("teacher_script")
    if spec.get("supported") is True and not _teacher_script_shape_valid(teacher_script):
        progress(
            "LAB_TEACHER_SCRIPT_REPAIR_START",
            concept_id=concept.get("concept_id"),
            source_page=concept.get("source_page"),
            kind=str(spec.get("kind") or ""),
        )
        repair_prompt = (
            "Repair ONLY the missing/invalid teacher_script of this already generated "
            "evidence-grounded lab. Do not add, remove, or alter any scientific claim, "
            "number, law, relation, geometry mark, circuit rule, or evidence quote. "
            "Return the COMPLETE lab spec as strict JSON. teacher_script must contain "
            "2..12 steps. Each step must contain say,target_ids,action,state_before,"
            "state_after,scientific_constraints,evidence_quote. Allowed actions: "
            "point,highlight,set_state,animate,observe,explain,conclude. Every "
            "evidence_quote must be an exact contiguous quote from SOURCE when the "
            "lab uses text evidence. target_ids must refer only to objects already "
            "present in the supplied lab spec. Apply state_after before speaking its "
            "consequence. Never animate/reveal a consequence before its verified "
            "condition is established. For a DC circuit, current/charge flow is "
            "forbidden while switch_closed=false; visibly close the switch first. "
            "If you cannot repair without inventing information, return "
            "{\"repairable\":false}.\n\n"
            f"SOURCE:\n{concept.get('raw_text','')}\n\n"
            f"EXISTING_LAB_SPEC:\n{json.dumps(spec, ensure_ascii=False)}"
        )
        repaired = None
        try:
            candidate = _execute_llm_json_strict(
                repair_prompt,
                image_base64=figure_image_base64,
                vision_context=vision_context,
                purpose=f"lab_teacher_script_repair_{concept.get('concept_id')}",
                max_attempts=2,
            )
            if isinstance(candidate, dict) and candidate.get("repairable") is not False:
                candidate_script = candidate.get("teacher_script")
                if _teacher_script_shape_valid(candidate_script):
                    # SECURITY/SCIENCE BOUNDARY: the repair model is allowed to
                    # supply ONLY teacher_script.  Never accept a rewritten kind,
                    # law, geometry, circuit state, evidence basis, quote, or any
                    # other scientific field from the repair response.
                    repaired = dict(spec)
                    repaired["teacher_script"] = candidate_script
        except (ProviderDailyQuotaError, ProviderTransientError,
                ProviderUnavailableError, NeedsAttentionError):
            raise
        except Exception as exc:
            progress(
                "LAB_TEACHER_SCRIPT_REPAIR_PROVIDER_FAILED",
                concept_id=concept.get("concept_id"),
                reason=str(exc)[:300],
            )

        if repaired is not None:
            spec = repaired
            progress(
                "LAB_TEACHER_SCRIPT_REPAIRED",
                concept_id=concept.get("concept_id"),
                steps=len(spec.get("teacher_script") or []),
            )
        else:
            source_text = str(concept.get("raw_text") or "").strip()
            if not source_text:
                raise RuntimeError("LAB_TEACHER_SCRIPT_REPAIR_FAILED_SOURCE_EMPTY")
            fallback_quote = source_text[:700]
            conclusion = str(
                narrative.get("conclusion")
                or narrative.get("observation")
                or concept.get("title")
                or "Conclude from the verified evidence."
            ).strip()
            spec = {
                "supported": True,
                "kind": "EVIDENCE_REVEAL",
                "title": str(concept.get("title") or "NABIL Interactive Explanation"),
                "instructions": {
                    "ar": "استكشف الفكرة مع نبيل خطوة خطوة.",
                    "fr": "Explore l’idée avec NABIL étape par étape.",
                    "en": "Explore the idea with NABIL step by step.",
                }.get(lang_code, "Explore the idea with NABIL step by step."),
                "observation": {
                    "ar": "كل ما يظهر هنا مأخوذ من الدليل الموثق لهذه الفكرة.",
                    "fr": "Tout ce qui apparaît ici vient de la preuve vérifiée de cette idée.",
                    "en": "Everything shown here comes from the verified evidence for this idea.",
                }.get(lang_code, "Everything shown here comes from the verified evidence for this idea."),
                "evidence_ref": concept["concept_id"],
                "evidence_basis": "text",
                "evidence_quote": fallback_quote,
                "items": [{
                    "label": str(concept.get("title") or "Verified idea"),
                    "evidence_quote": fallback_quote,
                }],
                "fallback_reason": "TEACHER_SCRIPT_OUTPUT_SHAPE_UNRECOVERABLE",
                "teacher_script": [
                    {
                        "say": str(concept.get("title") or "Observe the verified evidence."),
                        "target_ids": ["evidence:0"],
                        "action": "point",
                        "state_before": {"revealed_index": -1},
                        "state_after": {"revealed_index": 0},
                        "scientific_constraints": ["Reveal only verified source evidence."],
                        "evidence_quote": fallback_quote,
                    },
                    {
                        "say": conclusion,
                        "target_ids": ["evidence:0"],
                        "action": "conclude",
                        "state_before": {"revealed_index": 0},
                        "state_after": {"revealed_index": 0},
                        "scientific_constraints": ["Do not exceed verified source evidence."],
                        "evidence_quote": fallback_quote,
                    },
                ],
            }
            progress(
                "LAB_TEACHER_SCRIPT_SAFE_EVIDENCE_REVEAL_FALLBACK",
                concept_id=concept.get("concept_id"),
                source_page=concept.get("source_page"),
            )

    if spec.get("evidence_ref") != concept.get("concept_id"):
        # evidence_ref is provenance metadata, not a scientific claim. The lab
        # has just been generated from this concept's locked SOURCE/FIGURE, so
        # canonicalize a model formatting mistake instead of silently deleting
        # an otherwise verifiable interactive lab.
        progress(
            "LAB_SPEC_EVIDENCE_REF_CANONICALIZED",
            concept_id=concept.get("concept_id"),
            source_page=concept.get("source_page"),
            received_ref=str(spec.get("evidence_ref") or "")[:120],
        )
        spec["evidence_ref"] = concept["concept_id"]

    basis = str(spec.get("evidence_basis") or "").lower()
    quote = str(spec.get("evidence_quote") or "").strip()
    if basis == "text":
        if not quote:
            raise RuntimeError("LAB_SPEC_TEXT_EVIDENCE_MISSING")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        quote_norm = _normalized_lab_evidence(quote)
        if quote_norm not in source_norm:
            raise RuntimeError("LAB_SPEC_TEXT_EVIDENCE_NOT_FOUND")
    elif basis == "figure":
        if not figure_image_base64 or not concept.get("figure_refs"):
            raise RuntimeError("LAB_SPEC_FIGURE_EVIDENCE_MISSING")
    else:
        raise RuntimeError("LAB_SPEC_EVIDENCE_BASIS_INVALID")

    kind = str(spec.get("kind") or "").upper()
    if kind == "FORMULA_CALCULATOR":
        source_formula = _normalized_lab_evidence(spec.get("source_formula", ""))
        formula_haystack = _normalized_lab_evidence(
            str(concept.get("raw_text", "")) + " " +
            " ".join(str(r.get("raw") or "") for r in math_records if isinstance(r, dict))
        )
        if not source_formula or source_formula not in formula_haystack:
            raise RuntimeError("LAB_FORMULA_NOT_PRESENT_IN_SOURCE")

    # Advanced science labs must prove each declared invariant with an exact
    # textbook quote before deterministic rendering is allowed. This prevents
    # a visually impressive lab from silently introducing a scientific rule.
    advanced_required_quotes = {
        "DC_SERIES_CIRCUIT": {
            "series_resistance_sum",
            "series_same_current",
            "ohms_law",
            "open_switch_zero_current",
        },
        "OPTICS_REFLECTION": {
            "normal_perpendicular_surface",
            "angles_measured_from_normal",
            "reflection_law",
        },
        "IONIC_COMPOUND": {
            "ionic_bond",
            "cation_charge",
            "anion_charge",
            "ion_ratio",
            "electron_transfer",
            "charge_neutrality",
        },
    }
    if kind in advanced_required_quotes:
        evidence_quotes = spec.get("evidence_quotes")
        if not isinstance(evidence_quotes, dict):
            raise RuntimeError("LAB_ADVANCED_EVIDENCE_QUOTES_MISSING")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        missing = advanced_required_quotes[kind] - set(evidence_quotes)
        if missing:
            raise RuntimeError(
                "LAB_ADVANCED_EVIDENCE_QUOTES_INCOMPLETE:" +
                ",".join(sorted(missing)))
        for claim in sorted(advanced_required_quotes[kind]):
            exact_quote = _normalized_lab_evidence(evidence_quotes.get(claim, ""))
            if not exact_quote or exact_quote not in source_norm:
                raise RuntimeError(
                    f"LAB_ADVANCED_EVIDENCE_QUOTE_NOT_FOUND:{claim}")

    if kind == "GEOMETRY_PROOF":
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        marks = spec.get("marks")
        proof_steps = spec.get("proof_steps")
        if not isinstance(marks, list) or not isinstance(proof_steps, list):
            raise RuntimeError("LAB_GEOMETRY_EVIDENCE_STRUCTURE_MISSING")
        for index, mark in enumerate(marks):
            quote = _normalized_lab_evidence((mark or {}).get("evidence_quote", ""))
            if not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_GEOMETRY_MARK_EVIDENCE_NOT_FOUND:{index}")
        for index, step in enumerate(proof_steps):
            quote = _normalized_lab_evidence((step or {}).get("evidence_quote", ""))
            if not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_GEOMETRY_STEP_EVIDENCE_NOT_FOUND:{index}")

    if kind == "PROCEDURE_OBSERVATION":
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        groups = (
            ("materials", spec.get("materials") or [], 0, 8),
            ("procedure_steps", spec.get("procedure_steps"), 1, 8),
            ("observations", spec.get("observations"), 1, 6),
        )
        for group_name, group_items, minimum, maximum in groups:
            if not isinstance(group_items, list) or not minimum <= len(group_items) <= maximum:
                raise RuntimeError(f"LAB_PROCEDURE_{group_name.upper()}_INVALID")
            for index, item in enumerate(group_items):
                if not isinstance(item, dict):
                    raise RuntimeError(f"LAB_PROCEDURE_{group_name.upper()}_ITEM_INVALID:{index}")
                label = str(item.get("label") or "").strip()
                quote = _normalized_lab_evidence(item.get("evidence_quote", ""))
                if not label or not quote or quote not in source_norm:
                    raise RuntimeError(
                        f"LAB_PROCEDURE_{group_name.upper()}_EVIDENCE_NOT_FOUND:{index}")

    if kind == "EVIDENCE_SEQUENCE":
        steps = spec.get("steps")
        if not isinstance(steps, list) or not 2 <= len(steps) <= 8:
            raise RuntimeError("LAB_SEQUENCE_STEPS_INVALID")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        for index, step in enumerate(steps):
            if not isinstance(step, dict):
                raise RuntimeError(f"LAB_SEQUENCE_STEP_INVALID:{index}")
            label = str(step.get("label") or "").strip()
            quote = _normalized_lab_evidence(step.get("evidence_quote", ""))
            if not label or not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_SEQUENCE_EVIDENCE_QUOTE_NOT_FOUND:{index}")

    if kind == "EVIDENCE_REVEAL":
        items = spec.get("items")
        if not isinstance(items, list) or not 1 <= len(items) <= 8:
            raise RuntimeError("LAB_REVEAL_ITEMS_INVALID")
        source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise RuntimeError(f"LAB_REVEAL_ITEM_INVALID:{index}")
            label = str(item.get("label") or "").strip()
            quote = _normalized_lab_evidence(item.get("evidence_quote", ""))
            if not label or not quote or quote not in source_norm:
                raise RuntimeError(
                    f"LAB_REVEAL_EVIDENCE_QUOTE_NOT_FOUND:{index}")

    teacher_script = spec.get("teacher_script")
    if kind == "EVIDENCE_REVEAL":
        actions_now = {
            str(step.get("action") or "")
            for step in (teacher_script or [])
            if isinstance(step, dict)
        }
        required_reference_actions = {"point", "highlight", "explain", "conclude"}
        if not required_reference_actions.issubset(actions_now):
            verified_quote = str(spec.get("evidence_quote") or "").strip()
            verified_title = str(
                spec.get("title")
                or concept.get("title")
                or "Verified source evidence"
            ).strip()
            constraint = "Use only the verified source evidence."
            teacher_script = [
                {
                    "say": verified_title,
                    "target_ids": ["evidence:0"],
                    "action": "point",
                    "state_before": {"revealed_index": -1},
                    "state_after": {"revealed_index": 0},
                    "scientific_constraints": [constraint],
                    "evidence_quote": verified_quote,
                },
                {
                    "say": "Focus on the verified source evidence.",
                    "target_ids": ["evidence:0"],
                    "action": "highlight",
                    "state_before": {"revealed_index": 0},
                    "state_after": {"revealed_index": 0},
                    "scientific_constraints": [constraint],
                    "evidence_quote": verified_quote,
                },
                {
                    "say": "Read this verified evidence carefully.",
                    "target_ids": ["evidence:0"],
                    "action": "explain",
                    "state_before": {"revealed_index": 0},
                    "state_after": {"revealed_index": 0},
                    "scientific_constraints": [constraint],
                    "evidence_quote": verified_quote,
                },
                {
                    "say": "Keep the conclusion tied to this verified evidence.",
                    "target_ids": ["evidence:0"],
                    "action": "conclude",
                    "state_before": {"revealed_index": 0},
                    "state_after": {"revealed_index": 0},
                    "scientific_constraints": [constraint],
                    "evidence_quote": verified_quote,
                },
            ]
            spec["teacher_script"] = teacher_script
            progress(
                "R5_EVIDENCE_REVEAL_REFERENCE_CHOREOGRAPHY_COMPLETED",
                concept_id=concept.get("concept_id"),
                source_page=concept.get("source_page"),
            )
    if not isinstance(teacher_script, list) or not 2 <= len(teacher_script) <= 12:
        raise RuntimeError("LAB_TEACHER_SCRIPT_REQUIRED")
    allowed_teacher_actions = {"point","highlight","set_state","animate","observe","explain","conclude"}
    source_norm = _normalized_lab_evidence(concept.get("raw_text", ""))
    switch_closed = False
    for step_index, step in enumerate(teacher_script):
        if not isinstance(step, dict) or not str(step.get("say") or "").strip():
            raise RuntimeError(f"LAB_TEACHER_STEP_INVALID:{step_index}")
        if str(step.get("action") or "") not in allowed_teacher_actions:
            raise RuntimeError(f"LAB_TEACHER_ACTION_INVALID:{step_index}")
        if not isinstance(step.get("target_ids", []), list) or not isinstance(step.get("state_before"), dict) or not isinstance(step.get("state_after"), dict):
            raise RuntimeError(f"LAB_TEACHER_STATE_INVALID:{step_index}")
        if not isinstance(step.get("scientific_constraints"), list):
            raise RuntimeError(f"LAB_TEACHER_CONSTRAINTS_INVALID:{step_index}")
        q = _normalized_lab_evidence(step.get("evidence_quote", ""))
        if not q or (basis == "text" and q not in source_norm):
            raise RuntimeError(f"LAB_TEACHER_EVIDENCE_NOT_FOUND:{step_index}")
        if kind == "DC_SERIES_CIRCUIT":
            before=step.get("state_before") or {}; after=step.get("state_after") or {}
            if "switch_closed" in before and bool(before["switch_closed"]) != switch_closed:
                raise RuntimeError(f"LAB_CIRCUIT_STATE_DISCONTINUITY:{step_index}")
            next_closed=bool(after.get("switch_closed",switch_closed))
            words=(str(step.get("say") or "")+" "+str(step.get("action") or "")).lower()
            if any(x in words for x in ("current","charge flow","تيار","مرور الشحن")) and not next_closed:
                raise RuntimeError(f"LAB_CIRCUIT_FLOW_WITH_OPEN_SWITCH:{step_index}")
            switch_closed=next_closed
    validate_lab_spec(spec)
    # REQUIREMENT_5_FINAL_GATE
    # Final fail-closed source/science/visual acceptance. This runs AFTER the
    # existing domain validators and BEFORE the spec can leave the factory.
    spec = validate_requirement5_lab(
        spec,
        source_text=str(concept.get("raw_text") or ""),
        source_figure_verified=bool(
            figure_image_base64 and (concept.get("figure_refs") or vision_context)
        ),
    )
    assert_requirement5_publishable(
        spec,
        lesson_id=str(entry.get("lesson_id") or ""),
        lab_id=str(concept.get("concept_id") or ""),
    )
    # Grades 1-12 science/mathematics coverage contract. This adds no science:
    # it only certifies that the already R5-passed lab belongs to a covered
    # curriculum cell and remains source-locked.
    spec = validate_and_annotate_curriculum_lab(
        spec,
        entry=entry,
        profile=profile,
        concept=concept,
    )
    return spec



def render_whole_lesson_smart_lab(
        title: str, activities: list, lang_code: str,
        golden_spec: Optional[dict] = None) -> str:
    """V18 smart board: one idea at a time, its verified lab beneath it, and the
    Golden Card as the LAST stage inside the same section.

    Pure presentation of already-verified data; introduces no new science.
    The legacy iframe-orchestrator renderer was removed (V18 replacement).
    """
    if not activities:
        return ""
    from scripts.nabil_factory.cards.v18_board import render_v18_smart_board
    return render_v18_smart_board(
        title, activities, lang_code, golden_spec=golden_spec,
        contract=REFERENCE_RENDERER_CONTRACT)


def synthesize_universal_pedagogy(entry: dict, ev_map: dict, profile: dict,
                                  drive_service=None) -> dict:
    title = entry["canonical_title"]
    concepts = ev_map["concepts"]

    theory_checkpoints = None
    theory_checkpoint_root = None
    if drive_service is not None:
        theory_checkpoint_root = str(
            os.getenv("NABIL_CURRICULUM_ROOT_ID") or "").strip() or None
        if theory_checkpoint_root:
            from scripts import nabil_page_checkpoint as theory_checkpoints

    activities_theory = []
    worksheet = []
    panels = ""
    lesson_lang_code = resolve_lang_code(profile["language"])

    for idx, c in enumerate(concepts, 1):
        p_num = c["source_page"]
        # Textbook figures are EVIDENCE ONLY. Their pixels are never placed in
        # the student lesson. NABIL may inspect them to build an independently
        # audited redraw or interactive lab.
        fig_images = []
        for p in ev_map["pages_evidence"]:
            if p["page_num"] == p_num and p["figures"]:
                for f in p["figures"]:
                    if f["figure_id"] in c.get("figure_refs", []):
                        fig_images.append(f["image_path"])
        # Multiple source figures (e.g. 3a/3b) must be read together.
        figure_image_base64 = None
        if fig_images:
            from PIL import Image, ImageOps
            pictures = []
            for filename in fig_images:
                with Image.open(filename) as image:
                    pic = image.convert("RGB")
                    pic.thumbnail((1100, 850))
                    pictures.append(pic.copy())
            canvas = Image.new("RGB", (max(im.width for im in pictures),
                                       sum(im.height for im in pictures) + 8*(len(pictures)-1)), "white")
            top = 0
            for pic in pictures:
                canvas.paste(pic, (0, top))
                top += pic.height + 8
            buffered = io.BytesIO()
            canvas.save(buffered, format="PNG")
            figure_image_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")
        vision_context = ({
            "lesson_id": entry["lesson_id"],
            "book_id": entry["book_id"],
            "pdf_page": p_num,
        } if figure_image_base64 else None)
        concept_source_hash = hashlib.sha256(json.dumps({
            "raw_text": c.get("raw_text", ""),
            "figure_refs": list(c.get("figure_refs") or []),
            "figure_hashes": [
                f.get("image_sha256")
                for p in ev_map.get("pages_evidence", [])
                if p.get("page_num") == p_num
                for f in p.get("figures", [])
                if f.get("figure_id") in (c.get("figure_refs") or [])
            ],
        }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()

        narrative = None
        if theory_checkpoints:
            narrative = theory_checkpoints.load_paid_unit(
                drive_service, theory_checkpoint_root, entry,
                operation="concept_narrative",
                unit_id=c["concept_id"],
                source_hash=concept_source_hash,
                prompt_version=CONCEPT_NARRATIVE_PROMPT_VERSION,
            )
            if narrative is not None:
                progress("CONCEPT_NARRATIVE_RESTORED_FROM_DRIVE",
                         concept_id=c["concept_id"])
        if narrative is None:
            narrative = synthesize_concept_narrative(
                c, profile, figure_image_base64,
                vision_context=vision_context)
            if theory_checkpoints:
                theory_checkpoints.save_paid_unit(
                    drive_service, theory_checkpoint_root, entry,
                    operation="concept_narrative",
                    unit_id=c["concept_id"],
                    source_hash=concept_source_hash,
                    prompt_version=CONCEPT_NARRATIVE_PROMPT_VERSION,
                    payload=narrative,
                    provenance=get_last_llm_provenance(),
                )
                progress("CONCEPT_NARRATIVE_SAVED_TO_DRIVE",
                         concept_id=c["concept_id"])

        lab_source_hash = hashlib.sha256(json.dumps({
            "concept_source_hash": concept_source_hash,
            "narrative": narrative,
        }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
        lab_spec = None
        if theory_checkpoints:
            lab_spec = theory_checkpoints.load_paid_unit(
                drive_service, theory_checkpoint_root, entry,
                operation="lab_spec",
                unit_id=c["concept_id"],
                source_hash=lab_source_hash,
                prompt_version=LAB_SPEC_PROMPT_VERSION,
            )
            if lab_spec is not None:
                progress("LAB_SPEC_RESTORED_FROM_DRIVE",
                         concept_id=c["concept_id"])

        try:
            if lab_spec is None:
                lab_spec = build_verified_lab_spec(
                    entry, c, narrative, profile,
                    figure_image_base64=figure_image_base64,
                    vision_context=vision_context)
                if theory_checkpoints:
                    theory_checkpoints.save_paid_unit(
                        drive_service, theory_checkpoint_root, entry,
                        operation="lab_spec",
                        unit_id=c["concept_id"],
                        source_hash=lab_source_hash,
                        prompt_version=LAB_SPEC_PROMPT_VERSION,
                        payload=lab_spec,
                        provenance=get_last_llm_provenance(),
                    )
                    progress("LAB_SPEC_SAVED_TO_DRIVE",
                             concept_id=c["concept_id"])
        except RuntimeError as exc:
            reason = str(exc)
            if not reason.startswith("LAB_"):
                raise
            progress(
                "LAB_PIPELINE_BLOCKED",
                concept_id=c.get("concept_id"),
                source_page=p_num,
                reason=reason[:240],
            )
            # Technical/specification failures are not equivalent to "this
            # concept has no lab". Fail closed so an applicable animated lab
            # can never disappear silently and still be published.
            raise RuntimeError(
                f"LAB_PIPELINE_FAILED:{c.get('concept_id')}:{reason}") from exc
        concept_lab_html, concept_has_sim = render_verified_lab(
            lab_spec, lesson_lang_code, c["concept_id"])

        concept_visual = None
        if not concept_has_sim:
            visual_source_hash = concept_source_hash
            if theory_checkpoints:
                concept_visual = theory_checkpoints.load_paid_unit(
                    drive_service, theory_checkpoint_root, entry,
                    operation="concept_explanatory_redrawing",
                    unit_id=c["concept_id"],
                    source_hash=visual_source_hash,
                    prompt_version=REDRAW_PROMPT_VERSION,
                )
                if concept_visual is not None:
                    progress(
                        "CONCEPT_REDRAW_RESTORED_FROM_DRIVE",
                        concept_id=c["concept_id"])
            if concept_visual is None:
                concept_visual = build_nabil_explanatory_redrawing(
                    source_text=c.get("raw_text", ""),
                    page_num=p_num,
                    figure_paths=fig_images,
                    vision_context=vision_context,
                    purpose=f"concept_{c['concept_id']}",
                    visual_required=bool(c.get("figure_refs")),
                )
                if concept_visual is not None and theory_checkpoints:
                    prov = (
                        concept_visual.get("ai_provenance", {})
                        .get("audit", {})
                    )
                    theory_checkpoints.save_paid_unit(
                        drive_service, theory_checkpoint_root, entry,
                        operation="concept_explanatory_redrawing",
                        unit_id=c["concept_id"],
                        source_hash=visual_source_hash,
                        prompt_version=REDRAW_PROMPT_VERSION,
                        payload=concept_visual,
                        provenance=prov,
                    )
                    progress(
                        "CONCEPT_REDRAW_SAVED_TO_DRIVE",
                        concept_id=c["concept_id"])
        if c.get("figure_refs") and not concept_has_sim and not concept_visual:
            raise RuntimeError(
                f"NABIL_VISUAL_REQUIRED_BUT_NOT_VERIFIED:{c['concept_id']}:p{p_num}"
            )
        concept_visual_html = ""
        if concept_visual:
            caption = {
                "ar": "رسم NABIL التوضيحي المبني على الدليل",
                "fr": "Schéma explicatif NABIL fondé sur les preuves",
                "en": "NABIL explanatory visual built from verified evidence",
            }.get(lesson_lang_code, "NABIL explanatory visual built from verified evidence")
            concept_visual_html = (
                '<div class="nabil-explanatory-visual" style="margin:14px 0;">'
                + str(concept_visual["svg"])
                + '<div style="font-size:11px;color:#64748b;margin-top:5px;">'
                + html.escape(caption) + '</div></div>'
            )

        question_ready = all(
            str(narrative.get(k) or "").strip()
            for k in ("conclusion", "distractor_1", "distractor_2")
        )
        student_question = None
        if question_ready:
            student_question = {
                "q": ui_t(
                    lesson_lang_code, "based_on_verified_findings",
                    title=c["title"]),
                "options": [
                    narrative["conclusion"],
                    narrative["distractor_1"],
                    narrative["distractor_2"],
                ],
                "correct_index": 0,
                "source_scope_verified": bool(narrative.get("_scope_audited", False))
                    and bool(c.get("raw_text")),
                "feedback": ui_t(lesson_lang_code, "grounded_feedback"),
            }
        else:
            progress(
                "SKIPPED_UNVERIFIED_QUIZ_ITEM",
                concept_id=c.get("concept_id"),
                source_page=p_num,
                reason="GENERATED_QUIZ_CONTENT_REMOVED_BY_SCOPE_AUDIT",
            )

        activities_theory.append({
            "activity_num": c["concept_id"].replace("C", ""),
            "concept_id": c["concept_id"],
            "title": c["title"],
            "source_page": p_num,
            "source_excerpt": c.get("raw_text", ""),
            "phenomenon": narrative.get("phenomenon", ""),
            "investigation": narrative.get("investigation", ""),
            "observation": narrative.get("observation", ""),
            "interpretation": narrative.get("interpretation", ""),
            "conclusion": narrative.get("conclusion", ""),
            "visual_html": concept_visual_html,
            "visual_method": (
                concept_visual.get("method") if concept_visual else
                ("INTERACTIVE_LAB" if concept_has_sim else None)
            ),
            "source_figure_used_as_hidden_evidence": bool(fig_images),
            "lab_spec": lab_spec,
            "lab_html": concept_lab_html,
            "has_active_sim": concept_has_sim,
            "student_question": student_question,
            "generated_content_scope_audited": narrative.get("_scope_audited", False),
            "removed_generated_fields": narrative.get("_removed_generated_fields", []),
            "formal_arabic_verified": (
                narrative.get("_formal_arabic_verified", False)
                if lesson_lang_code == "ar" else True
            ),
            "teaching_signature": resolve_teaching_signature(c, profile),
            "teaching_steps": _attach_source_verified_student_check(
                build_teaching_steps(c, narrative, profile, lab_spec=lab_spec),
                student_question, c),
        })

        if question_ready:
            worksheet.append({
                "id": len(worksheet) + 1,
                "concept_id": c["concept_id"],
                "source_page": p_num,
                "source_hash": c["sha256"],
                "evidence_ref": c["concept_id"],
                "question": ui_t(
                    lesson_lang_code, "confirmed_deduction_question",
                    title=c["title"]),
                "options": [
                    narrative["conclusion"],
                    narrative["distractor_1"],
                    narrative["distractor_2"],
                ],
                "correct_index": 0,
                "explanation": ui_t(
                    lesson_lang_code, "grounded_explanation",
                    page=p_num, ref=c["concept_id"]),
            })

        formula_label = html.escape(ui_t(lesson_lang_code, "formula_law"))
        units_label = html.escape(ui_t(lesson_lang_code, "units_label"))
        formulas_html = "".join([f"<li><b>{formula_label}:</b> {html.escape(f)}</li>" for f in narrative.get("formulas", [])])
        units_html = "".join([f"<li><b>{units_label}:</b> {html.escape(u)}</li>" for u in narrative.get("units", [])])
        subject_metadata = f"<ul style='margin:4px 0 0 16px; padding:0; font-size:12px; color:#0369a1;'>{formulas_html}{units_html}</ul>" if (narrative.get("formulas") or narrative.get("units")) else ""

        principle_html = ""
        if str(narrative.get("conclusion") or "").strip():
            principle_html = (
                '<div style="margin-top:8px; font-size:13px; color:#334155; '
                'line-height:1.5;"><b>'
                + html.escape(ui_t(lesson_lang_code, "extracted_principle"))
                + ':</b> ' + html.escape(str(narrative["conclusion"])) + '</div>'
            )
        panels += f'''<div class="nabil-reference-concept" data-reference-concept="{html.escape(str(c["concept_id"]))}" style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:14px; box-shadow:0 2px 4px rgba(0,0,0,0.04);">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #e2e8f0; padding-bottom:6px;">
                <span style="font-weight:700; color:#0369a1; font-size:15px;">{html.escape(c["title"])}</span>
            </div>
            {principle_html}
            {subject_metadata}
            {concept_visual_html}
            <div style="margin-top:8px; font-size:12px; color:#059669; font-weight:600;">{html.escape(ui_t(lesson_lang_code, "verified_evidence_grounding"))}</div>
        </div>'''

    # V18: the Golden Card is data (rendered by the vendored V18 card engine as
    # the last stage of the whole-lesson lab), never hand-built legacy HTML.
    from scripts.nabil_factory.cards.v18_board import build_golden_spec
    golden_spec = build_golden_spec(
        title, activities_theory, lesson_lang_code,
        subject=str(entry.get("subject") or ""),
        verification_note=ui_t(lesson_lang_code, "verified_evidence_grounding"))
    ref_card_html = ""  # legacy field retained for return-shape compatibility

    # Aggregate labs across all concepts that actually produced one.
    all_labs_html = [
        act["lab_html"] for act in activities_theory if act.get("has_active_sim")
    ]
    any_active_sim = bool(all_labs_html)

    whole_lesson_lab_html = render_whole_lesson_smart_lab(
        title, activities_theory, lesson_lang_code, golden_spec)

    # Fail closed if any science/mathematics concept in Grades 1-12 has no
    # Requirement-5-locked interactive activity. Rich simulations are used
    # when evidence supports them; evidence sequence/reveal remains the safe
    # fallback when a physical/mathematical simulation would require invention.
    scientific_lab_coverage = validate_lesson_scientific_lab_coverage(
        profile, activities_theory)

    # Full-coverage quiz: reuses the exact grounded conclusion/distractor
    # fields already produced per concept above — no new LLM calls, no new
    # invented content, same evidence guarantee as the worksheet.
    full_quiz_items = build_full_quiz_items(activities_theory)
    full_quiz_html = render_quiz_html(full_quiz_items, lesson_lang_code)

    return {
        "title": title,
        "activities": activities_theory,
        "lab_html": "\n".join(all_labs_html),
        "has_active_sim": any_active_sim,
        "worksheet": worksheet,
        "quiz_items": full_quiz_items,
        "quiz_html": full_quiz_html,
        "quiz_eligible_count": sum(
            1 for act in activities_theory if act.get("student_question")),
        "reference_card_html": ref_card_html,
        "golden_card_spec": golden_spec,
        "whole_lesson_lab_html": whole_lesson_lab_html,
        "whole_lesson_lab_active": bool(whole_lesson_lab_html),
        "scientific_lab_coverage": scientific_lab_coverage,
    }




# ==============================================================================
# 11. QUALITY GATES & REAL PLAYWRIGHT CHROMIUM COMPREHENSIVE QA (390x844)
# ==============================================================================
def run_real_playwright_chromium_qa(
        html_path: str, label: str = "page") -> Dict[str, Any]:
    """Real mobile-browser QA with deterministic renderer fallback."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 390, "height": 844})
            page.goto(
                f"file://{Path(html_path).resolve()}",
                wait_until="domcontentloaded",
            )

            # Wait only on math delimiters that are actually visible in page
            # text nodes. Never infer "math present" from script/config source,
            # because the MathJax config itself contains \\( / \\[ tokens.
            visible_math_js = """() => {
              const walker = document.createTreeWalker(
                document.body, NodeFilter.SHOW_TEXT
              );
              while (walker.nextNode()) {
                const n = walker.currentNode;
                const p = n.parentElement;
                if (!p) continue;
                const tag = p.tagName;
                if (tag === 'SCRIPT' || tag === 'STYLE'
                    || tag === 'TEXTAREA' || tag === 'NOSCRIPT') continue;
                const v = n.nodeValue || '';
                if (v.includes('\\\\(') || v.includes('\\\\[')) {
                  return true;
                }
              }
              return false;
            }"""
            visible_math_present = bool(page.evaluate(visible_math_js))
            if visible_math_present:
                try:
                    page.wait_for_function(
                        """() => (
                          !!document.querySelector('mjx-container')
                          || document.documentElement.dataset.nabilMathFallback === 'true'
                        )""",
                        timeout=8000,
                    )
                except Exception:
                    # CDN unavailable/slow: use the deterministic local renderer
                    # immediately, then validate its visible result.
                    try:
                        page.evaluate(
                            """() => {
                              if (window.__NABIL_READABLE_MATH_FALLBACK) {
                                window.__NABIL_READABLE_MATH_FALLBACK();
                              }
                            }"""
                        )
                        page.wait_for_timeout(150)
                    except Exception:
                        pass

            check_result = page.evaluate("""() => {
                const doc = document.documentElement;
                const clip = (value, limit=100) =>
                  Array.from(String(value || '')).slice(0, limit).join('');
                const mathRoots = Array.from(
                  document.querySelectorAll('mjx-container')
                );
                let mathItems = [];
                try {
                  const collection = window.MathJax?.startup?.document?.math;
                  if (
                    collection
                    && typeof collection[Symbol.iterator] === 'function'
                  ) {
                    mathItems = Array.from(collection);
                  }
                } catch (_e) {}
                const sourceTexFor = el => {
                  const idx = mathRoots.indexOf(el);
                  if (idx < 0 || !mathItems[idx]) return "";
                  return clip(mathItems[idx].math || "", 220);
                };

                if (doc.scrollWidth > doc.clientWidth + 2) {
                    const offenders = Array.from(
                      document.querySelectorAll('body *')
                    ).map(el => {
                      const r = el.getBoundingClientRect();
                      return {
                        tag: el.tagName,
                        cls: String(el.className || '').slice(0, 120),
                        right: Math.round(r.right),
                        left: Math.round(r.left),
                        width: Math.round(r.width),
                        text: clip((el.innerText || '').trim(), 100),
                        sourceTex: sourceTexFor(el)
                      };
                    }).filter(x =>
                      x.right > doc.clientWidth + 2 || x.left < -2
                    ).sort((a,b) =>
                      Math.max(b.right - doc.clientWidth, -b.left)
                      - Math.max(a.right - doc.clientWidth, -a.left)
                    );
                    return {
                      passed: false,
                      reason: "HORIZONTAL_OVERFLOW",
                      scrollWidth: doc.scrollWidth,
                      clientWidth: doc.clientWidth,
                      offender: offenders[0] || null,
                      renderer: doc.dataset.nabilMathRenderer || "none"
                    };
                }

                const buttons = Array.from(
                  document.querySelectorAll('button, .q-opt')
                );
                for (let b of buttons) {
                    const style = getComputedStyle(b);
                    const rect = b.getBoundingClientRect();
                    const visible = (
                      style.display !== 'none'
                      && style.visibility !== 'hidden'
                      && Number(style.opacity || '1') !== 0
                      && rect.width > 0
                      && rect.height > 0
                    );
                    if (visible && rect.height < 43) {
                        return {
                          passed: false,
                          reason: "TOUCH_TARGET_TOO_SMALL",
                          height: rect.height,
                          text: clip(b.innerText || '', 80),
                          renderer: doc.dataset.nabilMathRenderer || "none"
                        };
                    }
                }

                const visibleTextNodes = [];
                const textWalker = document.createTreeWalker(
                  document.body, NodeFilter.SHOW_TEXT
                );
                while (textWalker.nextNode()) {
                    const n = textWalker.currentNode;
                    const p = n.parentElement;
                    if (!p) continue;
                    const tag = p.tagName;
                    if (tag === 'SCRIPT' || tag === 'STYLE'
                        || tag === 'TEXTAREA' || tag === 'NOSCRIPT') continue;
                    visibleTextNodes.push(n.nodeValue || '');
                }
                const visibleBodyText = visibleTextNodes.join(' ');
                const visibleRawMath = (
                  visibleBodyText.includes('\\\\(')
                  || visibleBodyText.includes('\\\\[')
                );
                if (visibleRawMath) {
                    return {
                      passed: false,
                      reason: "RAW_LATEX_DETECTED",
                      renderer: doc.dataset.nabilMathRenderer || "none"
                    };
                }

                const allElements = document.querySelectorAll(
                  'img, .card, mjx-container, p, h1, h2, h3'
                );
                for (let el of allElements) {
                    const rect = el.getBoundingClientRect();
                    if (rect.right > 392 || rect.left < -2) {
                        return {
                          passed: false,
                          reason: "ELEMENT_BOUNDING_BOX_OVERFLOW",
                          tag: el.tagName,
                          right: rect.right,
                          left: rect.left,
                          text: clip(el.innerText || '', 80),
                          sourceTex: sourceTexFor(el)
                        };
                    }
                }

                const mjxCount =
                  document.querySelectorAll('mjx-container').length;
                const fallbackReady =
                  doc.dataset.nabilMathFallback === 'true';
                // At this point visible raw delimiters must be gone. A page with
                // no visible raw delimiters and no MathJax nodes is valid when
                // it contains only Unicode/plain readable math. Do not count
                // delimiter strings inside scripts/configuration as lesson math.
                const originalMathPresent = visibleRawMath;

                if (originalMathPresent && mjxCount === 0 && !fallbackReady) {
                    return {
                      passed: false,
                      reason: "MATH_RENDERER_MISSING_DESPITE_MATH",
                      renderer: doc.dataset.nabilMathRenderer || "none"
                    };
                }

                const whole =
                  document.getElementById('nabilWholeLessonSmartLab');
                if (whole) {
                    const frame =
                      document.getElementById('nabilWholeLessonFrame');
                    if (!frame) {
                        return {
                          passed:false,
                          reason:"WHOLE_LESSON_FRAME_MISSING"
                        };
                    }
                    if (!window.NABILWholeLessonOrchestrator ||
                        typeof window.NABILWholeLessonOrchestrator.current !== 'function' ||
                        typeof window.NABILWholeLessonOrchestrator.stop !== 'function') {
                        return {
                          passed:false,
                          reason:"WHOLE_LESSON_ORCHESTRATOR_MISSING"
                        };
                    }
                    // V18: the Golden Card must be the LAST stage of the
                    // whole-lesson lab and must really render (never empty).
                    const orch = window.NABILWholeLessonOrchestrator;
                    if (typeof orch.goTo !== 'function' ||
                        !Number.isInteger(orch.finalIndex)) {
                        return {passed:false, reason:"V18_ORCHESTRATOR_API_MISSING"};
                    }
                    orch.goTo(orch.finalIndex);
                    const host = document.getElementById('goldenReferenceCard');
                    const card = host && host.querySelector('.nabil-sci-card');
                    const finalOk = !!card
                        && !!card.querySelector('.nabil-sci-final')
                        && !!card.querySelector('.nabil-sci-grid')
                        && (card.innerText || '').trim().length > 80
                        && whole.classList.contains('is-final')
                        && !host.dataset.failed
                        && card.getBoundingClientRect().height > 120;
                    const overflow = whole.scrollWidth > whole.clientWidth + 2;
                    orch.goTo(0);
                    if (!finalOk) {
                        // Keep the gate strict, but expose the actual browser
                        // failure instead of forcing a blind regeneration.
                        return {
                          passed:false,
                          reason:"V18_GOLDEN_CARD_NOT_RENDERED_AS_LAST_STAGE",
                          finalIndex:orch.finalIndex,
                          finalState:whole.classList.contains('is-final'),
                          hostPresent:!!host,
                          rendered:host?.dataset.rendered || null,
                          failed:host?.dataset.failed || null,
                          cardPresent:!!card,
                          cardHeight:card?.getBoundingClientRect().height || 0,
                          cardTextLength:(card?.innerText || '').trim().length,
                          hasFinalSection:!!card?.querySelector('.nabil-sci-final'),
                          hasGrid:!!card?.querySelector('.nabil-sci-grid'),
                          engineReady:typeof window.NABILScientificCards?.fromLesson==='function',
                          hostError:(host?.innerText || '').slice(0,350)
                        };
                    }
                    if (overflow) {
                        return {passed:false, reason:"V18_BOARD_HORIZONTAL_OVERFLOW"};
                    }
                }

                return {
                  passed: true,
                  renderer: doc.dataset.nabilMathRenderer || "none",
                  mjxCount,
                  mathPresent: originalMathPresent,
                  visibleRawMath,
                  fallbackUsed: fallbackReady
                };
            }""")
            browser.close()

            if (
                check_result.get("renderer") == "readable-fallback"
                or check_result.get("fallbackUsed") is True
            ):
                progress(
                    "MATHJAX_FALLBACK_USED",
                    page=label,
                    renderer=check_result.get("renderer"),
                    mjx_count=check_result.get("mjxCount"),
                )

            if not check_result.get("passed", False):
                progress(
                    "PLAYWRIGHT_QA_DIAGNOSTIC",
                    page=label,
                    reason=check_result.get("reason"),
                    details=json.dumps(
                        check_result, ensure_ascii=False
                    )[:1000],
                )
            else:
                progress(
                    "PLAYWRIGHT_QA_PASSED",
                    page=label,
                    renderer=check_result.get("renderer"),
                    mjx_count=check_result.get("mjxCount"),
                )
            return check_result
    except Exception as e:
        raise RuntimeError(
            f"PLAYWRIGHT_CHROMIUM_QA_EXECUTION_FAILED:{label}:{e}")



def ensure_verified_apply_steps(
        theory: dict, exercises: List[dict], evidence_map: dict,
        language_code: str) -> dict:
    """Ensure every concept has a real Apply step before rendering.

    Missing generated quiz/apply content is healed ONLY from verified textbook
    exercises already accepted into the student set. No new scientific claim is
    invented. The chosen exercise is the best deterministic lexical/page match.
    """
    activities = list(theory.get("activities") or [])
    verified = [
        ex for ex in (exercises or [])
        if ex.get("source_origin", "TEXTBOOK") == "TEXTBOOK"
        and ex.get("verified_against_source") is True
        and ex.get("solution_status") == "SOLVED"
        and str(ex.get("exact_source_prompt") or "").strip()
    ]
    if not activities:
        return theory

    def _tokens(value: str) -> set:
        return {
            t.lower() for t in re.findall(r"[\w]+", str(value or ""),
                                          flags=re.UNICODE)
            if len(t) >= 2
        }

    concepts = {
        str(c.get("concept_id")): c
        for c in (evidence_map.get("concepts") or [])
        if c.get("concept_id")
    }
    used = set()
    injected = 0

    for act in activities:
        if act.get("student_question"):
            continue
        cid = str(act.get("concept_id") or "")
        concept = concepts.get(cid) or {}
        c_text = " ".join([
            str(concept.get("title") or act.get("title") or ""),
            str(concept.get("normalized_text") or concept.get("raw_text") or ""),
        ])
        c_tokens = _tokens(c_text)
        c_page = int(concept.get("source_page") or 0)

        ranked = []
        for idx, ex in enumerate(verified):
            ex_id = str(ex.get("exercise_id") or f"EX-{idx}")
            e_tokens = _tokens(ex.get("exact_source_prompt") or "")
            overlap = len(c_tokens & e_tokens)
            e_page = int(ex.get("source_page") or 0)
            distance = abs(e_page - c_page) if c_page and e_page else 999
            reuse_penalty = 1 if ex_id in used else 0
            ranked.append((
                reuse_penalty,
                -overlap,
                distance,
                idx,
                ex,
            ))
        if not ranked:
            progress(
                "APPLY_STEP_DEFERRED_NO_VERIFIED_EXERCISE",
                concept_id=cid,
            )
            continue

        ranked.sort(key=lambda row: row[:4])
        ex = ranked[0][4]
        ex_id = str(ex.get("exercise_id") or "")
        used.add(ex_id)
        act["student_apply_prompt"] = {
            "exercise_id": ex_id,
            "number": ex.get("number"),
            "source_page": ex.get("source_page"),
            "prompt": str(ex.get("exact_source_prompt") or "").strip(),
            "verified_against_source": True,
        }
        injected += 1
        progress(
            "PEDAGOGICAL_APPLY_SELF_HEALED",
            concept_id=cid,
            exercise_id=ex_id,
            source_page=ex.get("source_page"),
        )

    if injected:
        theory["activities"] = activities
        progress(
            "PEDAGOGICAL_APPLY_SELF_HEAL_SUMMARY",
            injected=injected,
            concepts=len(activities),
            verified_exercises=len(verified),
        )
    return theory


def _normalize_candidate_before_quality_gates(candidate: dict) -> dict:
    """Deterministic QA middleware for repairable presentation invariants.

    Never changes source evidence, scientific claims, verified solutions,
    formulas or numbers. It repairs only renderer metadata/layout that is
    mechanically reconstructible from the already-rendered lesson.
    """
    page_a = str(candidate.get("page_a_html") or "")
    page_b = str(candidate.get("page_b_html") or "")
    concept_count = len(
        ((candidate.get("evidence_map") or {}).get("concepts") or [])
    )
    if not page_a or not page_b:
        return candidate

    # Keep the existing Apply self-heal as a metadata-only repair.
    section_re = re.compile(
        r'(<section\b[^>]*class="[^"]*\bnabil-concept-card\b[^"]*"[^>]*>)'
        r'(.*?)'
        r'(</section>)',
        re.S | re.I,
    )
    repaired_apply = 0

    def heal_section(match):
        nonlocal repaired_apply
        opener, body, closer = match.groups()
        if 'data-step="application"' in body:
            return match.group(0)
        marker = '<div class="nabil-sci-final"'
        if marker not in body:
            return match.group(0)
        body = body.replace(
            marker,
            '<div class="nabil-sci-final" data-step="application"',
            1,
        )
        repaired_apply += 1
        return opener + body + closer

    healed_a = section_re.sub(heal_section, page_a)

    # QA/mobile self-heal. This is layout-only and costs zero AI calls.
    mobile_css = r"""
<style id="nabilQaMobileSelfHealV2">
#nabilPageLanguage{
  max-width:calc(100vw - 12px)!important;
}
#nabilPageLanguage [data-nabil-lang]{
  min-height:44px!important;
  min-width:44px!important;
  padding:9px 10px!important;
}
button,.q-opt{
  min-height:44px!important;
  min-width:44px!important;
  box-sizing:border-box!important;
  display:inline-flex!important;
  align-items:center!important;
  justify-content:center!important;
  padding-top:10px!important;
  padding-bottom:10px!important;
}
html,body,.container{
  max-width:100%!important;
  min-width:0!important;
}
.nabil-exercise-card,
.nabil-exercise-card>div,
.nabil-exercise-card p,
.nabil-exercise-card li,
.nabil-exercise-card h1,
.nabil-exercise-card h2,
.nabil-exercise-card h3,
[data-nabil-solution-card],
.nabil-solution-fallback{
  min-width:0!important;
  max-width:100%!important;
  overflow-wrap:anywhere!important;
  word-break:break-word!important;
}
.nabil-exercise-card>div:first-child{
  flex-wrap:wrap!important;
  gap:8px!important;
}
.nabil-exercise-card pre,
.nabil-exercise-card code{
  max-width:100%!important;
  white-space:pre-wrap!important;
  overflow-wrap:anywhere!important;
  word-break:break-word!important;
}
.nabil-exercise-card table{
  display:block!important;
  width:100%!important;
  max-width:100%!important;
  overflow-x:auto!important;
}
.nabil-exercise-card svg,
.nabil-exercise-card canvas,
.nabil-exercise-card img,
.nabil-exercise-card iframe,
.nabil-sci-visual-stage svg,
.nabil-sci-visual-stage canvas,
.nabil-sci-visual-stage img{
  max-width:100%!important;
}
mjx-container{
  box-sizing:border-box!important;
  min-width:0!important;
  max-width:100%!important;
  overflow-x:auto!important;
  overflow-y:hidden!important;
  vertical-align:middle!important;
}
mjx-container[display="true"]{
  display:block!important;
  width:100%!important;
  max-width:100%!important;
}
.nabil-exercise-card mjx-container,
.card mjx-container,
.nabil-sci-panel mjx-container{
  max-width:100%!important;
}
</style>
"""

    math_runtime_js = r"""
<script id="nabilMathRuntimeSelfHealV1">
(function(){
  const SUP = {
    '0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹',
    '+':'⁺','-':'⁻','n':'ⁿ','m':'ᵐ','i':'ⁱ','x':'ˣ','y':'ʸ','a':'ᵃ','b':'ᵇ'
  };
  const toSup = value => Array.from(String(value||'')).map(ch => SUP[ch] || ch).join('');
  function readableMathFallbackV2(){
    if (document.querySelector('mjx-container')) return;
    const root = document.body;
    if (!root) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
      const n = walker.currentNode;
      const tag = n.parentElement ? n.parentElement.tagName : '';
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'TEXTAREA') continue;
      const v = n.nodeValue || '';
      if (v.includes('\\(') || v.includes('\\[')) nodes.push(n);
    }
    for (const n of nodes) {
      let t = n.nodeValue || '';
      t = t
        .replace(/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, '($1)/($2)')
        .replace(/\\sqrt\{([^{}]+)\}/g, '√($1)')
        .replace(/\\times/g, '×')
        .replace(/\\div/g, '÷')
        .replace(/\\cdot/g, '·')
        .replace(/\\leq?/g, '≤')
        .replace(/\\geq?/g, '≥')
        .replace(/\\neq/g, '≠')
        .replace(/\\rightarrow/g, '→')
        .replace(/\\left|\\right/g, '')
        .replace(/\^\{([^{}]+)\}/g, (_m,x)=>toSup(x))
        .replace(/\^([0-9+\-nmixtyab]+)/g, (_m,x)=>toSup(x))
        .replace(/_\{([^{}]+)\}/g, '_$1')
        .replace(/\\\(|\\\)|\\\[|\\\]/g, '');
      n.nodeValue = t;
    }
    document.documentElement.dataset.nabilMathRenderer = 'readable-fallback';
    document.documentElement.dataset.nabilMathFallback = 'true';
  }
  window.__NABIL_READABLE_MATH_FALLBACK = readableMathFallbackV2;
})();
</script>
"""

    mathjax_config_repairs = 0

    def heal_page(markup: str) -> str:
        nonlocal mathjax_config_repairs
        fixed = markup.replace(
            'style="min-height:40px"',
            'style="min-height:44px"',
        )

        # Root fix: the cached renderer emitted JS string literals '\\(' as
        # source text '\(' (one slash), which JavaScript interpreted as plain
        # '('; MathJax then treated ordinary parentheses as math delimiters.
        bad_mathjax = (
            "tex: { inlineMath: [['\\(', '\\)']], "
            "displayMath: [['\\[', '\\]']], processEscapes: true },"
        )
        good_mathjax = (
            "tex: { inlineMath: [['\\\\(', '\\\\)']], "
            "displayMath: [['\\\\[', '\\\\]']], processEscapes: true },"
        )
        if bad_mathjax in fixed:
            fixed = fixed.replace(bad_mathjax, good_mathjax, 1)
            mathjax_config_repairs += 1

        injected = mobile_css + "\n" + math_runtime_js
        if 'id="nabilQaMobileSelfHealV2"' not in fixed:
            if "</head>" in fixed:
                fixed = fixed.replace(
                    "</head>", injected + "\n</head>", 1)
            else:
                fixed = injected + fixed
        elif 'id="nabilMathRuntimeSelfHealV1"' not in fixed:
            if "</head>" in fixed:
                fixed = fixed.replace(
                    "</head>", math_runtime_js + "\n</head>", 1)
            else:
                fixed = math_runtime_js + fixed
        return fixed

    healed_a = heal_page(healed_a)
    healed_b = heal_page(page_b)

    changed_a = healed_a != page_a
    changed_b = healed_b != page_b
    if changed_a:
        candidate["page_a_html"] = healed_a
    if changed_b:
        candidate["page_b_html"] = healed_b

    hashes = candidate.get("hashes")
    if isinstance(hashes, dict):
        if changed_a:
            hashes["page_a"] = hashlib.sha256(
                healed_a.encode("utf-8")).hexdigest()
        if changed_b:
            hashes["page_b"] = hashlib.sha256(
                healed_b.encode("utf-8")).hexdigest()

    if repaired_apply:
        progress(
            "QUALITY_GATE_LOCAL_NORMALIZATION_APPLIED",
            gate="TEACHING_FLOW_APPLY_MISSING",
            repaired_concepts=repaired_apply,
            expected_concepts=concept_count,
        )
    if mathjax_config_repairs:
        progress(
            "MATHJAX_DELIMITER_CONFIG_LOCAL_REPAIRED",
            repaired_pages=mathjax_config_repairs,
            inline_delimiters="\\\\( ... \\\\)",
            display_delimiters="\\\\[ ... \\\\]",
        )
    if changed_a or changed_b:
        progress(
            "QA_LAYOUT_LOCAL_NORMALIZATION_APPLIED",
            theory=changed_a,
            exercises=changed_b,
            touch_target_min_px=44,
            math_container_max_width="100%",
        )
    return candidate

def run_all_quality_gates(candidate: dict) -> Dict[str, Any]:
    candidate = _normalize_candidate_before_quality_gates(candidate)
    progress("QUALITY_GATES: Auditing candidate against Real Playwright Chromium Comprehensive QA...")
    report = []

    def check(name: str, cond: bool, severity: str, det: str = ""):
        report.append({"name": name, "passed": bool(cond), "severity": severity, "details": det})
        if not cond and severity == "CRITICAL":
            raise AssertionError(f"QUALITY_GATE_FAILED: {name} -> {det}")

    ev_map = candidate["evidence_map"]
    s_lock = ev_map["source_lock"]
    expected_p = s_lock["end"] - s_lock["start"] + 1
    check("SOURCE_COVERAGE_INCOMPLETE", len(ev_map["pages_evidence"]) == expected_p, "CRITICAL", f"{len(ev_map['pages_evidence'])}/{expected_p} pages")
    completeness = ev_map.get("source_completeness") or {}
    deferred_source_ok = (
        completeness.get("status") == "DEFERRED"
        and completeness.get("backlog_persisted") is True
    )
    check(
        "SOURCE_INVENTORY_COMPLETENESS_FAILED",
        completeness.get("passed") is True or deferred_source_ok,
        "CRITICAL",
        json.dumps(completeness, ensure_ascii=False)[:1200],
    )
    check(
        "SOURCE_ITEMS_DEFERRED_TO_BACKLOG",
        not deferred_source_ok,
        "WARNING",
        json.dumps(completeness, ensure_ascii=False)[:1200],
    )

    exercise_start = ev_map.get("exercise_section_start_page")
    leaked_concepts = [
        {
            "concept_id": concept.get("concept_id"),
            "title": concept.get("title"),
            "source_page": concept.get("source_page"),
        }
        for concept in ev_map.get("concepts", [])
        if exercise_start is not None
        and int(concept.get("source_page") or -1) >= int(exercise_start)
    ]
    check(
        "LESSON_CONCEPT_LEAKED_FROM_EXERCISE_SECTION",
        not leaked_concepts,
        "CRITICAL",
        f"exercise_start_page={exercise_start}, leaked={leaked_concepts}",
    )

    required_unresolved_figures = {
        p["page_num"]: p.get("required_unverified_figure_labels", [])
        for p in ev_map["pages_evidence"]
        if p.get("required_unverified_figure_labels")
    }
    skipped_optional_figures = {
        p["page_num"]: p.get("skipped_unverified_figure_labels", [])
        for p in ev_map["pages_evidence"]
        if p.get("skipped_unverified_figure_labels")
    }
    check("SOURCE_FIGURE_REQUIRED_COVERAGE_INCOMPLETE",
          not required_unresolved_figures, "CRITICAL",
          f"required_unverified_source_figures={required_unresolved_figures}")
    check("OPTIONAL_SOURCE_FIGURE_SKIPPED",
          not skipped_optional_figures, "WARNING",
          f"skipped_unverified_source_figures={skipped_optional_figures}")

    textbook = [
        e for e in candidate["exercises"]
        if e.get("source_origin", "TEXTBOOK") == "TEXTBOOK"
    ]
    generated = [
        e for e in candidate["exercises"]
        if e.get("source_origin") == "AI_ADDITIONAL_PRACTICE"
    ]
    ex_nums = sorted([
        e["number"] for e in textbook
        if e["section_type"] == "EXERCISE"
    ])
    if ex_nums:
        check("EXERCISE_NUMBERING_INVALID",
              all(int(n) > 0 for n in ex_nums)
              and len(ex_nums) == len(set(ex_nums)),
              "CRITICAL", f"Verified exercises: {ex_nums}")
    # Missing numbers are allowed when those page items could not be verified.
    # We never invent/fill a missing textbook exercise.
    # Preserve all verified source exercises. If fewer than 3 are available,
    # add at least 3 gated AI practice exercises in addition to them.
    expected_ai = required_ai_practice_count(len(textbook))
    check("AI_FALLBACK_POLICY_VIOLATION",
          len(generated) == expected_ai, "CRITICAL",
          f"textbook={len(textbook)}, generated={len(generated)}, "
          f"expected_generated={expected_ai}")
    check("NO_PRACTICE_AVAILABLE",
          bool(textbook or generated), "CRITICAL",
          "Neither verified textbook exercises nor gated AI practice exists")

    for e in candidate["exercises"]:
        origin = e.get("source_origin", "TEXTBOOK")
        check("EXERCISE_PROMPT_INVALID",
              len(e["exact_source_prompt"]) >= 10,
              "CRITICAL", f"Ex {e['number']}")
        if origin == "TEXTBOOK":
            check("EXERCISE_FIDELITY_UNVERIFIED",
                  e.get("verified_against_source", False),
                  "CRITICAL", f"Ex {e['number']} source mismatch")
        else:
            check("AI_EXERCISE_SCIENTIFIC_GATE_FAILED",
                  e.get("scientific_gate_passed", False)
                  and bool(e.get("scope_concept_ids")),
                  "CRITICAL", f"Additional practice {e['number']}")
        if e["requires_figure"]:
            has_verified_reconstruction = bool(
                e.get("reconstructed_diagram_verified")
                and e.get("reconstructed_diagram_svg")
                and e.get("reconstructed_diagram_plan")
                and e.get("reconstructed_diagram_method") in {
                    "AI_RECONSTRUCTED_DIAGRAM_FROM_VERIFIED_TEXT",
                    "NABIL_EXPLANATORY_REDRAW_FROM_LOCKED_EVIDENCE",
                }
            )
            check("EXERCISE_DIAGRAM_REQUIRED_MISSING",
                  has_verified_reconstruction,
                  "CRITICAL",
                  f"Ex {e['number']} must have a NABIL redraw; source scan is hidden")

    pre_solved_statuses = [
        e.get("solution_status")
        for e in candidate["exercises"]
        if e.get("solution_mode") == "PRE_SOLVED"
    ]
    check(
        "PRE_SOLVE_STATUS_INVALID",
        all(s in {"SOLVED", "OMITTED_UNVERIFIED"} for s in pre_solved_statuses),
        "CRITICAL",
        f"statuses={pre_solved_statuses}",
    )
    solved_items = [
        e for e in candidate["exercises"]
        if e.get("solution_status") == "SOLVED"
    ]
    check(
        "SOLUTION_SOURCE_SCOPE_AUDIT_MISSING",
        all(
            (e.get("_pre_solved_solution") or {}).get("source_scope_audited") is True
            for e in solved_items
        ),
        "CRITICAL",
        "Every displayed solved exercise must pass text/figure source-scope audit",
    )
    check("WORKSHEET_NOT_GRADABLE", all("correct_index" in q for q in candidate["theory"]["worksheet"]), "CRITICAL", "Worksheet grading keys")
    check("REFERENCE_CARD_CONTENT_INCOMPLETE",
          "goldenReferenceCard" in candidate["page_a_html"],
          "CRITICAL", "Golden reference card missing")
    check("APPROVED_CARD_LAYOUT_MISSING",
          all(x in candidate["page_a_html"] for x in (
              'data-nabil-v18-board="NABIL_V18_SMART_BOARD_V1"',
              'data-nabil-v18-golden="true"',
              "window.NABILScientificCards",
              "nabil-sci-final")),
          "CRITICAL", "V18 smart board + Golden Card engine missing")
    check("TEACHING_FLOW_APPLY_MISSING",
          candidate["page_a_html"].count('data-step="application"') == len(ev_map["concepts"]),
          "CRITICAL", "Every concept must end with Apply")
    # V18: the Golden Card is data embedded in the whole-lesson lab; every source
    # concept must be present in the spec AND the board must embed that spec.
    _golden = candidate["theory"].get("golden_card_spec") or {}
    _spec_ids = sorted(str(x) for x in (_golden.get("concept_ids") or []))
    _expected_concepts = sorted(
        str(c.get("concept_id") or "") for c in ev_map["concepts"])
    check(
        "REFERENCE_CARD_CONCEPT_COVERAGE_INCOMPLETE",
        _spec_ids == _expected_concepts
        and 'data-nabil-v18-golden="true"' in str(
            candidate["theory"].get("whole_lesson_lab_html") or ""),
        "CRITICAL",
        "golden_concepts=" + str(len(_spec_ids))
        + ", concepts=" + str(len(_expected_concepts)),
    )
    lab_index = candidate.get("lab_index") or {}
    concept_lab_index = lab_index.get("concept_labs") or []
    exercise_lab_index = lab_index.get("exercise_labs") or []
    check(
        "PREBUILT_LAB_INDEX_SCHEMA_INVALID",
        lab_index.get("schema") == "nabil-prebuilt-lab-index/v2"
        and lab_index.get("renderer_contract") == REFERENCE_RENDERER_CONTRACT
        and lab_index.get("lesson_id") == candidate.get("lesson_id")
        and lab_index.get("runtime_ai_required_for_indexed_labs") is False,
        "CRITICAL",
        "Standalone/embedded lab index must identify this lesson and declare zero runtime AI for indexed labs",
    )
    whole_lab = lab_index.get("whole_lesson_lab") or {}
    check(
        "WHOLE_LESSON_SMART_LAB_MISSING",
        whole_lab.get("key") == "lesson:whole"
        and whole_lab.get("prebuilt") is True
        and whole_lab.get("active") is True
        and len(whole_lab.get("concept_keys") or []) == len(concept_lab_index)
        and 'data-whole-lesson-smart-lab="true"' in candidate["page_a_html"]
        and 'id="nabilWholeLessonFrame"' in candidate["page_a_html"],
        "CRITICAL",
        "Every lesson must ship one final Smart Board orchestrating all verified concept labs",
    )
    check(
        "TEACHING_ENGINE_SEQUENCE_INCOMPLETE",
        all(
            bool(a.get("teaching_signature"))
            and a.get("teaching_signature", {}).get("autonomous_teacher") is True
            and len(a.get("teaching_steps") or []) >= 3
            and all(
                str(step.get("sentence") or "").strip()
                and str(step.get("lab_key") or "") == "concept:" + str(a.get("concept_id") or "")
                and (step.get("evidence") or {}).get("concept_id") == a.get("concept_id")
                for step in (a.get("teaching_steps") or [])
            )
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "Every concept must carry an age/subject-specific evidence-locked teaching sequence linked to its concept lab",
    )
    geometry_acts = [
        a for a in candidate["theory"].get("activities", [])
        if str((a.get("lab_spec") or {}).get("kind") or "").upper() == "GEOMETRY_PROOF"
    ]
    check(
        "GEOMETRY_VISUAL_PROOF_MARKS_MISSING",
        all(
            'data-proof-marks="evidence-gated"' in str(a.get("lab_html") or "")
            and 'data-teacher-pointer="sentence-synced"' in str(a.get("lab_html") or "")
            and all(
                str(mark.get("evidence_quote") or "").strip()
                for mark in ((a.get("lab_spec") or {}).get("marks") or [])
            )
            and all(
                str(step.get("evidence_quote") or "").strip()
                and isinstance(step.get("target_ids") or [], list)
                for step in ((a.get("lab_spec") or {}).get("proof_steps") or [])
            )
            for a in geometry_acts
        ),
        "CRITICAL",
        "Geometry proof labs must reveal evidence-backed equality/angle/perpendicular/parallel/midpoint/symmetry marks while NABIL explains",
    )
    check(
        "SENTENCE_POINTER_SYNC_MISSING",
        all(
            'data-teacher-pointer="sentence-synced"' in str(a.get("lab_html") or "")
            for a in candidate["theory"].get("activities", [])
            if a.get("has_active_sim")
        )
        and all(
            'data-teacher-pointer="sentence-synced"' in str(
                e.get("_prebuilt_lab_html") or "")
            for e in candidate.get("exercises") or []
            if e.get("_prebuilt_lab_active")
        ),
        "CRITICAL",
        "Every concept/exercise lab must expose sentence-synchronized NABIL pointer behavior",
    )


    check(
        "PREBUILT_CONCEPT_LAB_INDEX_INCOMPLETE",
        len(concept_lab_index) == len(ev_map.get("concepts") or [])
        and all(x.get("prebuilt") is True and x.get("active") is True
                and str(x.get("key") or "").startswith("concept:")
                for x in concept_lab_index),
        "CRITICAL",
        f"indexed_concept_labs={len(concept_lab_index)}, concepts={len(ev_map.get('concepts') or [])}",
    )
    check(
        "PREBUILT_EXERCISE_LAB_INDEX_INCOMPLETE",
        len(exercise_lab_index) == len(candidate.get("exercises") or [])
        and all(x.get("prebuilt") is True and x.get("active") is True
                and str(x.get("key") or "").startswith("exercise:")
                for x in exercise_lab_index),
        "CRITICAL",
        f"indexed_exercise_labs={len(exercise_lab_index)}, exercises={len(candidate.get('exercises') or [])}",
    )
    check(
        "PREBUILT_LAB_INDEX_NOT_EMBEDDED",
        'id="nabilLabIndex"' in candidate["page_a_html"]
        and 'id="nabilLabIndex"' in candidate["page_b_html"],
        "CRITICAL",
        "Both lesson and exercise pages must carry the same prebuilt lab index",
    )
    check(
        "PREBUILT_EXERCISE_LABS_NOT_EMBEDDED",
        candidate["page_b_html"].count(
            'class="nabil-prebuilt-exercise-lab"')
        == len(candidate.get("exercises") or [])
        and candidate["page_b_html"].count(
            'data-nabil-prebuilt-lab="true"')
        == len(candidate.get("exercises") or []),
        "CRITICAL",
        "Every indexed exercise must ship with its ready-to-run lab HTML",
    )
    check(
        "STANDALONE_LAB_INDEX_ARTIFACT_MISSING",
        bool(candidate.get("filename_labs"))
        and bool(candidate.get("lab_index_json"))
        and candidate.get("hashes", {}).get("labs")
        == hashlib.sha256(
            str(candidate.get("lab_index_json") or "").encode("utf-8")
        ).hexdigest(),
        "CRITICAL",
        "Every lesson publish must include a separately hashed --LABS.json artifact",
    )

    check(
        "FORMAL_ARABIC_TEACHING_FAILED",
        all(
            a.get("formal_arabic_verified") is True
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "NABIL-authored Arabic teaching must use clear Modern Standard Arabic only",
    )

    check(
        "GENERATED_CONTENT_SCOPE_AUDIT_MISSING",
        all(
            a.get("generated_content_scope_audited") is True
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "Every generated lesson narrative must pass delete-only source-scope auditing",
    )

    # Quiz coverage applies only to generated question content that survived
    # the independent source-scope audit. Unsafe/out-of-scope generated quiz
    # material is omitted at item level rather than failing the whole lesson.
    concept_count = len(ev_map["concepts"])
    worksheet_count = len(candidate["theory"]["worksheet"])
    quiz_items = candidate["theory"].get("quiz_items") or []
    activities = candidate["theory"].get("activities") or []
    eligible_quiz_count = int(
        candidate["theory"].get("quiz_eligible_count", len(quiz_items)))
    check("QUIZ_VERIFIED_COVERAGE_INCONSISTENT",
          worksheet_count == eligible_quiz_count
          and len(quiz_items) == eligible_quiz_count
          and len(activities) == concept_count,
          "CRITICAL",
          f"worksheet={worksheet_count}, quiz={len(quiz_items)}, "
          f"eligible={eligible_quiz_count}, activities={len(activities)}, "
          f"concepts={concept_count}")

    check("FULL_QUIZ_BLOCK_MISSING",
          (eligible_quiz_count == 0)
          or ("fullQuizBlock" in candidate["page_a_html"]),
          "CRITICAL",
          "Verified quiz items exist but full quiz block is missing from Page A")

    # Every concept must have an explicit lab decision. A technical generation
    # failure is blocked earlier; supported=false is allowed only as a verified
    # "no evidence-backed interaction fits" decision.
    check(
        "LAB_REQUIRED_FOR_EVERY_CONCEPT",
        all(
            isinstance(a.get("lab_spec"), dict)
            and (a.get("lab_spec") or {}).get("supported") is True
            and a.get("has_active_sim") is True
            and bool(a.get("lab_html"))
            for a in activities
        ),
        "CRITICAL",
        "Every lesson concept/paragraph must have a verified interactive lab",
    )

    # Every declared lab must be evidence-validated and genuinely interactive.
    lab_activities = [
        a for a in activities
        if (a.get("lab_spec") or {}).get("supported") is True
    ]
    for act in lab_activities:
        spec = act.get("lab_spec") or {}
        lab_html = act.get("lab_html") or ""
        validate_lab_spec(spec)
        check("LAB_RENDER_MISSING",
              bool(lab_html), "CRITICAL",
              f"concept={act.get('concept_id')}")
        check("LAB_STUB_FORBIDDEN",
              'data-lab-kind=' in lab_html
              and '<script>' in lab_html
              and (
                  '<svg' in lab_html
                  or 'type="number"' in lab_html
                  or 'nabil-seq-step' in lab_html
                  or 'nabil-reveal-item' in lab_html
              )
              and 'nabil:demo' in lab_html,
              "CRITICAL",
              f"concept={act.get('concept_id')}")
        check("LAB_FAKE_NUMERIC_RANGE_FORBIDDEN",
              'type="range"' not in lab_html
              and ' min=' not in lab_html
              and ' max=' not in lab_html,
              "CRITICAL",
              f"concept={act.get('concept_id')}")

        lab_kind = str(spec.get("kind") or "").upper()
        if lab_kind in {"DC_SERIES_CIRCUIT", "OPTICS_REFLECTION", "IONIC_COMPOUND"}:
            check("LAB_TEACHER_POINTER_NOT_SYNCED",
                  'data-teacher-pointer="synced"' in lab_html
                  and 'teacherArrow' in lab_html
                  and 'pointTeacher' in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')} kind={lab_kind}")
        if lab_kind == "DC_SERIES_CIRCUIT":
            check("LAB_OPEN_CIRCUIT_CURRENT_GUARD_MISSING",
                  "OPEN_CIRCUIT_ZERO_CURRENT" in lab_html
                  and "CURRENT_REQUIRES_CLOSED_SWITCH" in lab_html
                  and "switchClosed?V/Rt:0" in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')}")
        elif lab_kind == "OPTICS_REFLECTION":
            check("LAB_OPTICS_NORMAL_REFERENCE_GUARD_MISSING",
                  'data-angle-reference="normal"' in lab_html
                  and "ANGLES_FROM_NORMAL" in lab_html
                  and "I_EQUALS_R" in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')}")
        elif lab_kind == "IONIC_COMPOUND":
            check("LAB_IONIC_NEUTRALITY_GUARD_MISSING",
                  'data-charge-neutral="true"' in lab_html
                  and "CHARGE_NEUTRALITY" in lab_html,
                  "CRITICAL",
                  f"concept={act.get('concept_id')}")

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as tmp_a:
        tmp_a.write(candidate["page_a_html"])
        path_a = tmp_a.name
    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", encoding="utf-8", delete=False) as tmp_b:
        tmp_b.write(candidate["page_b_html"])
        path_b = tmp_b.name

    try:
        qa_a = run_real_playwright_chromium_qa(path_a, "theory")
        qa_b = run_real_playwright_chromium_qa(path_b, "exercises")
    finally:
        Path(path_a).unlink(missing_ok=True)
        Path(path_b).unlink(missing_ok=True)

    qa_a_ok = bool((qa_a or {}).get("passed"))
    qa_b_ok = bool((qa_b or {}).get("passed"))
    qa_ok = qa_a_ok and qa_b_ok
    qa_details = json.dumps(
        {"theory": qa_a, "exercises": qa_b},
        ensure_ascii=False,
    )[:1800]

    check(
        "PLAYWRIGHT_THEORY_QA_FAILED",
        qa_a_ok,
        "CRITICAL",
        json.dumps(qa_a, ensure_ascii=False)[:900],
    )
    check(
        "PLAYWRIGHT_EXERCISES_QA_FAILED",
        qa_b_ok,
        "CRITICAL",
        json.dumps(qa_b, ensure_ascii=False)[:900],
    )

    # A text fallback is allowed to keep the page readable, but Golden publish
    # is not counted as math-rendering success when verified math was present.
    math_renderer_ok = all(
        not bool((row or {}).get("mathPresent"))
        or (
            (row or {}).get("renderer") == "mathjax"
            and int((row or {}).get("mjxCount") or 0) > 0
        )
        for row in (qa_a, qa_b)
    )
    check(
        "MATH_RENDERING_FAILED",
        math_renderer_ok,
        "CRITICAL",
        qa_details,
    )
    check(
        "MOBILE_REAL_PLAYWRIGHT_CHROMIUM_QA_390_844",
        qa_ok,
        "CRITICAL",
        qa_details,
    )

    check(
        "ONLY_VERIFIED_SOLVED_EXERCISES_STUDENT_FACING",
        all(
            e.get("solution_status") == "SOLVED"
            and isinstance(e.get("_pre_solved_solution"), dict)
            and bool(e.get("_prebuilt_lab_key"))
            for e in candidate.get("exercises") or []
        ),
        "CRITICAL",
        "Any exercise that cannot be solved, scientifically verified, and rendered is dropped individually; the lesson remains",
    )
    check(
        "AI_EXERCISE_SCOPE_GATE_REQUIRED",
        all(
            e.get("source_origin") != "AI_ADDITIONAL_PRACTICE"
            or (
                e.get("scientific_gate_passed") is True
                and bool(e.get("scope_concept_ids"))
                and e.get("solution_status") == "SOLVED"
            )
            for e in candidate.get("exercises") or []
        ),
        "CRITICAL",
        "AI practice must be traceable to verified lesson concepts and pass the scientific gate",
    )

    check(
        "STUDENT_SOURCE_SCAN_FORBIDDEN",
        "data:image/" not in candidate["page_a_html"]
        and "data:image/" not in candidate["page_b_html"],
        "CRITICAL",
        "Textbook/source raster images are evidence-only and must not be embedded in student lesson HTML",
    )
    forbidden_raster_tokens = (
        "page_image_url", "figure_image_urls", "originalPageImage",
        "عرض الصورة الأصلية لصفحة الكتاب", "Open original textbook page",
        "Actual scanned page from the indexed government textbook",
    )
    check(
        "STUDENT_SOURCE_RASTER_UI_FORBIDDEN",
        all(
            token not in candidate["page_a_html"]
            and token not in candidate["page_b_html"]
            for token in forbidden_raster_tokens
        ),
        "CRITICAL",
        "Textbook scans/figure pixels may be internal evidence only; student HTML may contain verified NABIL redraws/SVG only",
    )
    translation_report = candidate.get("translation_report") or {}
    # English-source-only pilot has no paid translation bundle. Restrict this
    # exception to the exact owner-approved textbook lesson; it may not
    # suppress mathematical, source, visual, or scientific validation gates.
    source_language_only = (
        candidate.get("source_language_only") is True
        and all(
            (translation_report.get(key) or {}).get("mode")
                == "source_language_no_translation"
            and (translation_report.get(key) or {}).get("complete") is True
            and (translation_report.get(key) or {}).get("languages") in
                (["en"], ["fr"])
            for key in ("page_a", "page_b")
        )
    )
    check(
        "FULL_PAGE_TRANSLATION_INCOMPLETE",
        source_language_only or (
        all(
            (translation_report.get(key) or {}).get("complete") is True
            and (translation_report.get(key) or {}).get("languages")
                == list(REFERENCE_RENDERER_LANGUAGES)
            and all(
                int(((translation_report.get(key) or {}).get(
                    "translated_counts") or {}).get(lang, -1))
                == int((translation_report.get(key) or {}).get(
                    "candidate_strings", -2))
                for lang in REFERENCE_RENDERER_LANGUAGES
            )
            for key in ("page_a", "page_b")
        )
        and all(
            'id="nabilPageLanguage"' in page
            and 'id="nabilPageTranslationBundle"' in page
            and 'data-nabil-translation-complete="true"' in page
            and 'data-nabil-lang="ar"' in page
            and 'data-nabil-lang="en"' in page
            and 'data-nabil-lang="fr"' in page
            for page in (candidate["page_a_html"], candidate["page_b_html"])
        )),
        "CRITICAL",
        "Source-language-only (English/French) mode must be explicit and complete; trilingual mode still needs full prebuilt bundles",
    )

    check(
        "REFERENCE_RENDERER_CONTRACT_MISSING",
        all(
            f'name="nabil-renderer-contract" content="{REFERENCE_RENDERER_CONTRACT}"' in page
            for page in (candidate["page_a_html"], candidate["page_b_html"])
        ),
        "CRITICAL",
        "Both student pages must use the approved content-agnostic golden reference renderer contract",
    )
    check(
        "EXERCISE_SOLUTION_LAB_LINKAGE_INCOMPLETE",
        all(
            bool(e.get("_prebuilt_lab_key"))
            and e.get("_solution_lab_key") == e.get("_prebuilt_lab_key")
            for e in candidate.get("exercises") or []
        )
        and candidate["page_b_html"].count("data-nabil-solution-lab-key=")
            == len(candidate.get("exercises") or []),
        "CRITICAL",
        "Every exercise/solution card must link to exactly its own prebuilt lab key",
    )
    check(
        "SCIENTIFIC_SOLUTION_CARD_LAB_KEY_MISSING",
        all(
            (
                e.get("solution_status") != "SOLVED"
                or str(e.get("_prebuilt_lab_key") or "") in candidate["page_b_html"]
            )
            for e in candidate.get("exercises") or []
        ),
        "CRITICAL",
        "Every displayed solved exercise must carry the same lab key into its Scientific Solution Card",
    )
    check(
        "NABIL_VISUAL_PIPELINE_MISSING",
        all(
            (a.get("has_active_sim") is True)
            or not a.get("source_figure_used_as_hidden_evidence")
            or a.get("visual_method") == "NABIL_EXPLANATORY_REDRAW_FROM_LOCKED_EVIDENCE"
            for a in candidate["theory"].get("activities", [])
        ),
        "CRITICAL",
        "Every concept that used a hidden source figure must teach through a verified NABIL lab/redraw",
    )
    check("NAVIGATION_FAILED", "navigateToExercises" in candidate["page_a_html"] and "returnToLesson" in candidate["page_b_html"], "CRITICAL", "Navigation intact")
    check("E2E_RUNTIME_NOT_WIRED",
          all("nabil_lesson_e2e_runtime_v1.js" in page for page in
              (candidate["page_a_html"], candidate["page_b_html"])),
          "CRITICAL",
          "Generated lesson/exercise pages must load the shared E2E runtime")
    check(
        "BROWSER_TTS_CONTRACT_NOT_WIRED",
        all("nabil_browser_tts_v1.js?v=1" in page for page in
            (candidate["page_a_html"], candidate["page_b_html"])),
        "CRITICAL",
        "All generated student pages must use the free browser SpeechSynthesis voice contract",
    )
    browser_tts_path = ROOT / "app/static/nabil_browser_tts_v1.js"
    browser_tts_source = (
        browser_tts_path.read_text(encoding="utf-8")
        if browser_tts_path.exists() else ""
    )
    check(
        "BROWSER_TTS_CONTRACT_INVALID",
        bool(browser_tts_source)
        and 'engine:"SpeechSynthesis"' in browser_tts_source
        and "SpeechSynthesisUtterance" in browser_tts_source
        and "maleVoicePreferred:true" in browser_tts_source
        and "paidEndpoint:false" in browser_tts_source
        and "/api/tts" not in browser_tts_source
        and "fetch(" not in browser_tts_source,
        "CRITICAL",
        "NABIL lesson voice must be browser SpeechSynthesis only; male voice is preferred when the device supplies one",
    )
    # The audited V18 renderer is delivered as an encoded *inline* payload to
    # preserve executable JS across page translation and HTML normalization.
    # Verify its complete source bytes, not a spoofable substring marker.
    from scripts.nabil_factory.cards.v18_board import verify_v18_scientific_card_inline_engine
    check("SCIENTIFIC_CARD_RENDERER_NOT_WIRED",
          all(verify_v18_scientific_card_inline_engine(page)
              for page in (candidate["page_a_html"], candidate["page_b_html"])),
          "CRITICAL",
          "Generated pages must embed the V18 Scientific Card engine (no external file)")
    if any(e.get("solution_mode") == "PRE_SOLVED" for e in candidate["exercises"]):
        check("PRE_SOLVED_SCIENTIFIC_CARD_MISSING",
              "data-nabil-solution-card" in candidate["page_b_html"],
              "CRITICAL",
              "Verified pre-solved exercises must render through Scientific Solution Card")

    return {"passed": True, "gates": report}


def _scientific_review_projection(candidate: dict) -> dict:
    """Project only the content a student can actually receive.

    Source identity/completeness and evidence-quote traceability are enforced by
    earlier dedicated gates. The independent scientific reviewer must not treat
    noisy OCR, rejected drafts, provider metadata or audit-history strings as if
    they were published scientific claims.
    """
    theory = candidate.get("theory") or {}

    concepts = []
    for act in theory.get("activities") or []:
        concepts.append({
            "concept_id": act.get("concept_id"),
            "title": act.get("title"),
            "source_page": act.get("source_page"),
            "student_facing_explanation": {
                "phenomenon": act.get("phenomenon"),
                "investigation": act.get("investigation"),
                "observation": act.get("observation"),
                "interpretation": act.get("interpretation"),
                "conclusion": act.get("conclusion"),
            },
        })

    def visible_lab(spec):
        if not isinstance(spec, dict):
            return spec
        hidden = {
            "evidence_quote", "evidence_quotes", "evidence_ref",
            "evidence_basis", "ai_provenance", "source_text",
            "source_image_ref", "source_bbox", "verification_status",
        }
        out = {}
        for key, value in spec.items():
            if key in hidden or str(key).startswith("_"):
                continue
            if isinstance(value, dict):
                out[key] = visible_lab(value)
            elif isinstance(value, list):
                out[key] = [
                    visible_lab(v) if isinstance(v, dict) else v
                    for v in value
                ]
            else:
                out[key] = value
        return out

    teaching_steps = []
    for act in theory.get("activities") or []:
        rows = []
        for step in act.get("teaching_steps") or []:
            if not isinstance(step, dict):
                continue
            rows.append({
                "step_id": step.get("step_id"),
                "kind": step.get("kind"),
                "label": step.get("label"),
                "sentence": step.get("sentence"),
                "formula": step.get("formula"),
            })
        teaching_steps.append({
            "concept_id": act.get("concept_id"),
            "steps": rows,
        })

    exercises = []
    for ex in candidate.get("exercises") or []:
        solution = ex.get("_pre_solved_solution") or {}
        exercises.append({
            "exercise_id": ex.get("exercise_id"),
            "section_type": ex.get("section_type"),
            "number": ex.get("number"),
            "source_origin": ex.get("source_origin", "TEXTBOOK"),
            "source_page": ex.get("source_page"),
            "exact_source_prompt": ex.get("exact_source_prompt"),
            "subquestions": ex.get("subquestions") or [],
            "verified_against_source": ex.get("verified_against_source"),
            "displayed_solution": {
                "steps": solution.get("steps") or [],
                "final_answer": solution.get("final_answer"),
                "verification": solution.get("verification") or [],
                "method": solution.get("method"),
            },
        })

    return {
        "concepts": concepts,
        "labs": [
            visible_lab(a.get("lab_spec"))
            for a in theory.get("activities") or []
        ],
        "teaching_steps": teaching_steps,
        "quiz_items": theory.get("quiz_items", []),
        "exercises": exercises,
    }

def run_review(call_reviewer, lesson_text: str, *, retries: int = 2):
    """Return (ReviewerReport | None, reviewed). Never fake a clean report."""
    last_err = None
    attempts = max(1, int(retries) + 1)
    for attempt in range(attempts):
        try:
            raw = call_reviewer(lesson_text)
            report = report_from_json(raw)
            progress(
                "REVIEWER_CALL_SUCCEEDED",
                attempt=attempt + 1,
                issue_count=len(report.issues),
            )
            return report, True
        except Exception as exc:
            last_err = exc
            progress(
                "REVIEWER_CALL_FAILED",
                attempt=attempt + 1,
                error=f"{type(exc).__name__}: {str(exc)[:200]}",
            )
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 8))
    progress(
        "REVIEWER_UNAVAILABLE",
        error=f"{type(last_err).__name__}: {str(last_err)[:200]}"
        if last_err is not None else "unknown",
    )
    return None, False


def independent_scientific_review(entry: dict, candidate: dict) -> dict:
    """Structured reviewer + deterministic local triage.

    The reviewer reports typed issues only; it does not decide PASS/BLOCK.
    If review is unavailable or malformed after bounded retries, deterministic
    checks still run and the lesson is marked UNREVIEWED/needs_review.
    """
    review_payload = _scientific_review_projection(candidate)
    normalized_payload = normalize_payload_strings(review_payload)
    lesson_text = json.dumps(
        normalized_payload,
        ensure_ascii=False,
        sort_keys=True,
    )

    subject = str(entry.get("subject") or "").lower()
    math_rule = (
        "For mathematics, ordinary arithmetic evaluation and direct power "
        "manipulation required by a verified textbook exercise are allowed. "
        "Do not report them as unsupported merely because concept prose does "
        "not restate each arithmetic step. "
        if "math" in subject else ""
    )
    prompt = (
        f"You are an Independent Senior Curriculum Auditor for Lebanese "
        f"{entry['subject'].capitalize()} Grade {entry['grade']}.\n"
        "Inspect ONLY the STUDENT-FACING payload below. For every issue, return "
        "a VERBATIM quote copied from this payload, a category from exactly: "
        "ocr_typo|spacing|symbol|formatting|formula_error|wrong_concept|"
        "false_statement|unclear_evidence, a short message, and confidence 0..1. "
        "Do not decide whether the lesson passes. Do not cite hidden textbook "
        "OCR or prior audit comments; they are not part of the student lesson. "
        + math_rule
        + "Return strict JSON exactly: "
        "{\"issues\":[{\"category\":\"...\","
        "\"quote\":\"verbatim excerpt\","
        "\"message\":\"...\",\"confidence\":0.0}]}.\n"
        f"Lesson Title: {entry['canonical_title']}\n"
        f"STUDENT-FACING PAYLOAD:\n{lesson_text}"
    )

    def _call(_lesson_text: str) -> str:
        return execute_llm_completion(
            prompt,
            json_mode=True,
            temperature=0.0,
            operation=f"scientific_review_{entry.get('lesson_id')}",
            unit_id=str(entry.get("lesson_id") or "lesson"),
        )

    report, reviewed = run_review(
        _call,
        lesson_text,
        retries=int(os.getenv("NABIL_SCI_REVIEW_RETRIES", "2")),
    )

    effective_report = report if report is not None else ReviewerReport()
    gate = scientific_gate(
        lesson_text,
        effective_report,
        emit=progress,
    )

    result = {
        "approved": gate.verdict != "BLOCK",
        "verdict": gate.verdict,
        "needs_review": bool(gate.needs_review or not reviewed),
        "review_status": "REVIEWED" if reviewed else "UNREVIEWED",
        "block_reasons": gate.block_reasons,
        "flagged": gate.flagged,
        "noise_count": gate.noise_count,
        "issues": [
            issue.model_dump()
            for issue in effective_report.issues
        ],
    }

    if gate.verdict == "BLOCK":
        raise ScientificGateBlocked(
            "SCIENTIFIC_REVIEW_REJECTED:"
            + json.dumps(
                gate.block_reasons,
                ensure_ascii=False,
            )
        )

    if not reviewed:
        progress(
            "SCIENTIFIC_REVIEW_CONTINUE_UNREVIEWED",
            lesson_id=str(entry.get("lesson_id") or ""),
            deterministic_verdict=gate.verdict,
            needs_review=True,
        )
    return result

