
/**
 * NABIL AI — Fallback Drawings Engine
 * Version: 1.0.0
 *
 * Guarantees pedagogically-required visuals for indexed lessons, exercises,
 * assessment questions, and solution steps even when AI omits DRAWINGS_JSON.
 *
 * Host integration:
 * - If available, uses window.renderNabilDiagram(spec).
 * - Never invents numeric data, coordinates, measurements, or labels.
 * - Specific drawings have priority over generic concept maps.
 */

(function(global){
  "use strict";

  const HARD_VISUAL_KEYWORDS = [
    "draw","sketch","plot","graph","diagram","figure","represent","construct",
    "circuit","triangle","circle","tangent","field lines","magnetic field","magnet",
    "atom","molecule","cell","ray diagram","table of variation","variation table",
    "sign table","coordinate plane","orthonormal system","free body diagram",
    "tracer","représenter","schéma","courbe","graphique","construire","champ magnétique",
    "aimant","atome","molécule","cellule","tableau de variation","tableau de signe",
    "repère","lentille","miroir",
    "ارسم","مثّل","مثل","أنشئ","مخطط","شكل","رسم","منحنى","جدول تغيرات","جدول إشارة",
    "دارة","مثلث","دائرة","مماس","مجال مغناطيسي","مغناطيس","ذرة","جزيء","خلية",
    "معلم","إحداثيات","عدسة","مرآة","قوى"
  ];

  const HARD_VISUAL_LESSONS = [
    /magnetic field created by a magnet/i,
    /magnetic field/i,
    /champ magnétique/i,
    /electromagnetic induction/i,
    /induction électromagnétique/i,
    /structure of the atom/i,
    /atomic structure/i,
    /structure de l['’]atome/i,
    /cell structure/i,
    /structure de la cellule/i,
    /distance between two points/i,
    /length of a segment.*orthonormal/i,
    /coordinate geometry/i,
    /logarithmic.*function/i,
    /exponential.*function/i,
    /variation table/i,
    /table of variation/i,
    /electric circuit/i,
    /ray optics/i,
    /pythagoras/i,
    /tangent.*circle/i,
    /المجال المغناطيسي/i,
    /بنية الذرة/i,
    /تركيب الخلية/i,
    /المسافة بين نقطتين/i,
    /جدول التغيرات/i,
    /دارة كهربائية/i,
    /فيثاغورس/i
  ];

  const REGISTRY = {
    math: [
      { topic:"right_triangle", rx:/pythag|فيثاغورس|théorème de pythagore/i },
      { topic:"circle_tangent", rx:/circle|tangent|دائرة|مماس|cercle|tangente/i },
      { topic:"coordinate_plane", rx:/coordinate|orthonormal|repère|إحداثيات|معلم|cartesian/i },
      { topic:"function_graph", rx:/function|graph|curve|دالة|تابع|منحنى|fonction|courbe|logarith|exponential/i },
      { topic:"variation_table", rx:/variation|monotonic|جدول تغير|variation table|tableau de variations/i },
      { topic:"sign_table", rx:/sign table|tableau de signe|جدول إشارة/i },
      { topic:"statistics_graph", rx:/statistics|statistic|إحصاء|statistique/i },
      { topic:"probability_tree", rx:/probability|احتمال|probabilité/i },
      { topic:"vector_plane", rx:/vector|متجه|vecteur/i },
      { topic:"triangle", rx:/triangle|مثلث/i },
      { topic:"rectangle", rx:/rectangle|مستطيل/i },
      { topic:"square", rx:/square|مربع|carré/i },
      { topic:"cylinder", rx:/cylinder|أسطوانة|اسطوانة|cylindre/i },
      { topic:"cone", rx:/cone|مخروط|cône/i },
      { topic:"sphere", rx:/sphere|كرة|sphère/i }
    ],

    physics: [
      { topic:"magnetic_field", rx:/magnetic field|bar magnet|magnet|champ magnétique|aimant|مجال مغناطيسي|مغناطيس/i },
      { topic:"electromagnetic_induction", rx:/electromagnetic induction|induction électromagnétique|حث كهرومغناطيسي/i },
      { topic:"electric_series", rx:/series circuit|circuit en série|دارة توالي/i },
      { topic:"electric_parallel", rx:/parallel circuit|circuit en parallèle|دارة توازي/i },
      { topic:"electric_circuit", rx:/electric circuit|circuit électrique|دارة كهربائية|current|voltage|resistor/i },
      { topic:"inclined_plane", rx:/inclined plane|plan incliné|سطح مائل/i },
      { topic:"free_body", rx:/free body|force|newton|قوة|قوى/i },
      { topic:"ray_diagram", rx:/ray|lens|mirror|optics|شعاع|عدسة|مرآة|optique/i },
      { topic:"wave", rx:/wave|oscillation|موجة|اهتزاز|onde/i },
      { topic:"motion_graph", rx:/motion|velocity|acceleration|حركة|سرعة|تسارع/i },
      { topic:"spring", rx:/spring|hooke|نابض/i }
    ],

    chemistry: [
      { topic:"atom_model", rx:/atom|atomic|ذرة|atomique/i },
      { topic:"ionic_bond", rx:/ionic bond|liaison ionique|رابطة أيونية|رابطه ايونيه/i },
      { topic:"molecule", rx:/molecule|molecular|جزيء|molécule/i },
      { topic:"periodic_table", rx:/periodic table|الجدول الدوري|tableau périodique/i },
      { topic:"titration_setup", rx:/titration|معايرة|titrage/i },
      { topic:"reaction_rate_graph", rx:/reaction rate|kinetic|سرعة التفاعل|cinétique/i },
      { topic:"energy_diagram", rx:/energy diagram|enthalpy|طاقة التفاعل|enthalpie/i },
      { topic:"electrochemistry", rx:/electrochem|electrolysis|كهرباء كيميائية|électrochim/i },
      { topic:"ph_scale", rx:/acid|base|ph|حمض|قاعدة|acide|base/i },
      { topic:"lab_setup", rx:/lab|apparatus|experiment|مختبر|تجربة|laboratoire/i },
      { topic:"states_of_matter", rx:/states of matter|حالات المادة|états de la matière/i }
    ],

    biology: [
      { topic:"cell_diagram", rx:/cell|خلية|cellule/i },
      { topic:"dna_diagram", rx:/dna|gene|chromosome|وراثة|جين|كروموسوم/i },
      { topic:"cell_division", rx:/mitosis|meiosis|انقسام|mitose|méiose/i },
      { topic:"digestive_system", rx:/digest|هضم|digestif/i },
      { topic:"respiratory_system", rx:/respirat|تنفس|respiratoire/i },
      { topic:"circulatory_system", rx:/circulat|دوران|circulatoire/i },
      { topic:"nervous_system", rx:/nervous|عصبي|nerveux/i },
      { topic:"reproductive_system", rx:/reproduction|تكاثر|reproduction/i },
      { topic:"food_chain", rx:/food chain|سلسلة غذائية|chaîne alimentaire/i },
      { topic:"ecosystem", rx:/ecosystem|بيئة|écosystème/i },
      { topic:"life_cycle", rx:/life cycle|دورة حياة|cycle de vie/i }
    ],

    geography: [
      { topic:"climate_graph", rx:/climate|مناخ|climat/i },
      { topic:"population_graph", rx:/population|سكان|population/i },
      { topic:"map", rx:/map|خريطة|carte/i },
      { topic:"relief_map", rx:/relief|تضاريس|relief/i },
      { topic:"statistics_graph", rx:/economic|اقتصاد|économ/i }
    ],

    history: [
      { topic:"timeline", rx:/timeline|chronology|تسلسل زمني|chronologie/i },
      { topic:"map", rx:/map|خريطة|carte/i },
      { topic:"document_panel", rx:/document|وثيقة|source/i }
    ],

    language: [
      { topic:"picture_prompt", rx:/picture|image|وصف صورة|description d['’]image|visual comprehension/i },
      { topic:"grammar_map", rx:/grammar|قواعد|grammaire/i },
      { topic:"sentence_structure", rx:/sentence structure|تركيب الجملة|structure de phrase/i }
    ]
  };

  const REQUIRED_ELEMENTS = {
    magnetic_field: ["magnet","north_label","south_label","field_lines","direction_arrows"],
    right_triangle: ["point_a","point_b","point_c","right_angle"],
    coordinate_plane: ["x_axis","y_axis"],
    function_graph: ["x_axis","y_axis","curve"],
    variation_table: ["row_x","row_derivative","row_function","trend_arrows"],
    sign_table: ["row_x","sign_row"],
    electric_circuit: ["source","wires","components"],
    electric_series: ["source","wires","components"],
    electric_parallel: ["source","wires","components"],
    atom_model: ["nucleus","electrons"],
    ionic_bond: ["ions","charge_labels"],
    cell_diagram: ["cell_outline","nucleus"],
    map: ["map_shape"],
    timeline: ["timeline_axis"]
  };

  function normalize(text){
    return String(text || "")
      .toLowerCase()
      .normalize("NFKD")
      .replace(/[\u064B-\u065F]/g, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function subjectFamily(subject){
    const s = normalize(subject);

    if(/math|رياضيات|mathématique/.test(s)) return "math";
    if(/physics|فيزياء|physique/.test(s)) return "physics";
    if(/chemistry|كيمياء|chimie/.test(s)) return "chemistry";
    if(/biology|life science|علوم الحياة|أحياء|biologie/.test(s)) return "biology";
    if(/science|علوم/.test(s)) return "science";
    if(/geography|جغرافيا|géographie/.test(s)) return "geography";
    if(/history|تاريخ|histoire/.test(s)) return "history";
    if(/arabic|english|french|français|لغة|عربي|فرنسي|إنكليزي|انكليزي/.test(s)) return "language";

    return "default";
  }

  function classifyVisualTopic(meta = {}){
    const family = subjectFamily(meta.subject);
    const combined = normalize(`${meta.lessonTitle || meta.lesson || ""} ${meta.text || ""}`);

    const rules = REGISTRY[family] || [];
    for(const rule of rules){
      if(rule.rx.test(combined)){
        return {
          primaryTopic: rule.topic,
          secondaryTopics: [],
          confidence: 0.95,
          family
        };
      }
    }

    if(family === "science"){
      if(/magnet|مغناطيس/.test(combined)) return {primaryTopic:"magnetic_field",secondaryTopics:[],confidence:0.9,family};
      if(/electric|circuit|كهرباء|دارة/.test(combined)) return {primaryTopic:"electric_circuit",secondaryTopics:[],confidence:0.9,family};
      if(/cell|خلية/.test(combined)) return {primaryTopic:"cell_diagram",secondaryTopics:[],confidence:0.9,family};
      if(/states|matter|مادة|حالات/.test(combined)) return {primaryTopic:"states_of_matter",secondaryTopics:[],confidence:0.85,family};
      if(/light|ضوء/.test(combined)) return {primaryTopic:"ray_diagram",secondaryTopics:[],confidence:0.85,family};
      if(/force|قوة/.test(combined)) return {primaryTopic:"free_body",secondaryTopics:[],confidence:0.85,family};
    }

    return {
      primaryTopic: null,
      secondaryTopics: [],
      confidence: 0,
      family
    };
  }

  function detectVisualNeed(meta = {}){
    const lessonTitle = String(meta.lessonTitle || meta.lesson || "");
    const text = String(meta.text || "");
    const combined = normalize(`${lessonTitle} ${text}`);

    if(HARD_VISUAL_LESSONS.some(rx => rx.test(combined))){
      return {
        needsVisual: true,
        visualPriority: "required",
        reason: "hard_visual_lesson"
      };
    }

    const matchedKeywords = HARD_VISUAL_KEYWORDS.filter(k => combined.includes(normalize(k)));
    if(matchedKeywords.length){
      return {
        needsVisual: true,
        visualPriority: "required",
        reason: "keyword_match",
        matchedKeywords
      };
    }

    const family = subjectFamily(meta.subject);
    if(["math","physics","chemistry","biology","science"].includes(family)){
      const classified = classifyVisualTopic(meta);
      if(classified.primaryTopic){
        return {
          needsVisual: true,
          visualPriority: "recommended",
          reason: "subject_topic_match",
          topic: classified.primaryTopic
        };
      }
    }

    return {
      needsVisual: false,
      visualPriority: "none",
      reason: "no_match"
    };
  }

  function getDrawingConfig(topic){
    return {
      topic,
      mandatoryElements: REQUIRED_ELEMENTS[topic] || [],
      source: "fallback"
    };
  }

  function drawingNodeLooksUsable(node){
    if(!node) return false;

    const svg = node.matches?.("svg") ? node : node.querySelector?.("svg");
    if(!svg) return false;

    const meaningful = svg.querySelectorAll(
      "path,line,polyline,polygon,circle,ellipse,rect,text"
    ).length;

    const semantic = svg.querySelectorAll(
      "path,polyline,polygon,circle,ellipse,rect,text"
    ).length;

    return meaningful >= 4 && semantic >= 2;
  }

  function validateDrawingCompleteness(topic, drawingStateOrNode){
    if(!drawingStateOrNode) return false;

    if(drawingStateOrNode.nodeType === 1){
      if(!drawingNodeLooksUsable(drawingStateOrNode)) return false;

      const text = normalize(drawingStateOrNode.textContent || "");

      if(topic === "magnetic_field"){
        return /\bn\b/.test(text) &&
               /\bs\b/.test(text) &&
               drawingStateOrNode.querySelectorAll("path,polyline").length >= 2;
      }

      if(topic === "function_graph"){
        return drawingStateOrNode.querySelectorAll("path,polyline").length >= 1;
      }

      if(topic === "right_triangle"){
        return drawingStateOrNode.querySelectorAll("circle,text").length >= 3;
      }

      return true;
    }

    const required = REQUIRED_ELEMENTS[topic] || [];
    if(!required.length) return true;

    return required.every(key => Boolean(drawingStateOrNode[key]));
  }

  function buildFallbackSpec(meta = {}){
    const classified = classifyVisualTopic(meta);
    const lessonTitle = String(meta.lessonTitle || meta.lesson || "");

    if(classified.primaryTopic){
      return {
        type: classified.primaryTopic,
        title: lessonTitle || meta.title || "Educational Visual",
        source: "fallback-engine"
      };
    }

    const need = detectVisualNeed(meta);
    if(need.needsVisual){
      return {
        type: "concept_map",
        title: lessonTitle || meta.title || "Educational Visual",
        source: "fallback-engine"
      };
    }

    return null;
  }

  function findExistingVisual(container){
    if(!container) return null;

    const candidates = [
      ...container.querySelectorAll(".nabil-visual"),
      ...container.querySelectorAll("svg")
    ];

    return candidates.find(drawingNodeLooksUsable) || null;
  }

  function ensureVisual(meta = {}, options = {}){
    const container = options.container || meta.container;
    const render = options.render || global.renderNabilDiagram || null;

    const need = detectVisualNeed(meta);

    if(!need.needsVisual){
      return {
        needsVisual: false,
        source: "none",
        valid: true,
        topic: null,
        visualElement: null
      };
    }

    const classified = classifyVisualTopic(meta);
    const topic = classified.primaryTopic;

    // Exercises/solutions must never recycle a visual from an older card/lesson.
    // Only accept a visual already inside the CURRENT exercise/solution container.
    // If the model omitted an exact drawing, do not inject a generic fallback that
    // can misrepresent the student's actual data.
    const strictExercise = ["exercise", "solution"].includes(String(meta.contentType || "").toLowerCase());
    const existing = findExistingVisual(container);

    if(existing && (!topic || validateDrawingCompleteness(topic, existing))){
      return {
        needsVisual: true,
        source: "ai",
        valid: true,
        topic,
        visualElement: existing
      };
    }

    const spec = buildFallbackSpec(meta);

    if(strictExercise){
      return {
        needsVisual: true,
        source: "model-required",
        valid: false,
        topic: topic || spec?.type || null,
        spec: null,
        visualElement: null,
        reason: "no_exact_exercise_drawing"
      };
    }

    if(!spec || typeof render !== "function"){
      return {
        needsVisual: true,
        source: "fallback",
        valid: false,
        topic: spec?.type || topic || null,
        spec: spec || null,
        visualElement: null
      };
    }

    const rendered = render(spec);

    if(!rendered){
      return {
        needsVisual: true,
        source: "fallback",
        valid: false,
        topic: spec.type,
        spec,
        visualElement: null
      };
    }

    let host = options.host || container?.querySelector?.(".lesson-visuals");

    if(!host && container){
      host = document.createElement("div");
      host.className = "lesson-visuals";
      container.appendChild(host);
    }

    if(host){
      host.insertAdjacentHTML(
        "beforeend",
        `<div class="nabil-fallback-drawing" data-fallback-topic="${spec.type}">${rendered}</div>`
      );
    }

    const inserted = host?.lastElementChild || null;
    const valid = inserted ? validateDrawingCompleteness(spec.type, inserted) : false;

    return {
      needsVisual: true,
      source: "fallback",
      valid,
      topic: spec.type,
      spec,
      visualElement: inserted
    };
  }

  function prepareCard(card, lessonMeta = {}, options = {}){
    return ensureVisual({
      ...lessonMeta,
      contentType: "lesson",
      text: card?.innerText || card?.textContent || "",
      container: card
    }, {
      ...options,
      container: card
    });
  }

  function prepareExerciseVisual(exercise, lessonMeta = {}, options = {}){
    return ensureVisual({
      ...lessonMeta,
      contentType: "exercise",
      text: exercise?.innerText || exercise?.textContent || "",
      container: exercise
    }, {
      ...options,
      container: exercise
    });
  }

  function prepareAssessmentQuestionVisual(question, assessmentMeta = {}, options = {}){
    return ensureVisual({
      ...assessmentMeta,
      contentType: "assessment",
      text: question?.innerText || question?.textContent || "",
      container: question
    }, {
      ...options,
      container: question
    });
  }

  function prepareSolutionVisual(step, questionMeta = {}, options = {}){
    return ensureVisual({
      ...questionMeta,
      contentType: "solution",
      text: step?.innerText || step?.textContent || "",
      container: step
    }, {
      ...options,
      container: step
    });
  }

  function auditContainer(container, meta = {}, options = {}){
    if(!container) return [];

    const results = [];

    const lessonCards = [...container.querySelectorAll(".lesson-concept-card")];
    lessonCards.forEach(card => {
      results.push({
        type: "lesson-card",
        result: prepareCard(card, meta, options)
      });
    });

    const exercises = [...container.querySelectorAll(
      ".exercise-board,.exercise-card,.general-exercise-card"
    )];
    exercises.forEach(exercise => {
      results.push({
        type: "exercise",
        result: prepareExerciseVisual(exercise, meta, options)
      });
    });

    return results;
  }

  function debugLog(label, data){
    try{
      console.log(`[NABIL DRAWING ENGINE] ${label}`, data);
    }catch(_e){}
  }

  global.NabilFallbackDrawingsEngine = {
    version: "1.0.0",
    REGISTRY,
    HARD_VISUAL_KEYWORDS,
    HARD_VISUAL_LESSONS,
    detectVisualNeed,
    classifyVisualTopic,
    getDrawingConfig,
    validateDrawingCompleteness,
    drawingNodeLooksUsable,
    buildFallbackSpec,
    ensureVisual,
    prepareCard,
    prepareExerciseVisual,
    prepareAssessmentQuestionVisual,
    prepareSolutionVisual,
    auditContainer,
    debugLog
  };

})(window);
