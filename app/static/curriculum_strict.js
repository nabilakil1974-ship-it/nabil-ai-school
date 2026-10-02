(() => {
  "use strict";

  // NABIL AI — strict curriculum selector
  // Golden lesson routing ready.
  // Backward-compatible with:
  //   lessons: ["Inverse Function", ...]
  // and:
  //   lessons: [
  //     { title: "Inverse Function", lesson_id: "G12-MATH-GS-002" },
  //     ...
  //   ]

  const byId = id => document.getElementById(id);

  const grade = () => byId("gradeSelect");
  const subject = () => byId("subjectSelect");
  const language = () => byId("languageSelect");
  const branch = () => byId("branchSelect");
  const lesson = () => byId("lessonSelect");

  let requestSeq = 0;
  let bindSeq = 0;

  function clean(value) {
    return String(value ?? "").trim();
  }

  function resetLessons(message = "اختر الدرس") {
    const el = lesson();
    if (!el) return;

    el.innerHTML = "";

    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = message;
    opt.dataset.lessonId = "";

    el.appendChild(opt);

    // Never leave a stale Golden lesson id after grade/subject/language changes.
    el.dataset.lessonId = "";
    el.dataset.strictCurriculum = "1";
  }

  function normalizeLessonItem(item) {
    // Legacy API:
    // "Inverse Function"
    if (typeof item === "string") {
      const title = clean(item);

      if (!title) return null;

      return {
        title,
        lessonId: ""
      };
    }

    if (!item || typeof item !== "object") {
      return null;
    }

    // Support current/future catalog field names without breaking the UI.
    const title = clean(
      item.title ??
      item.lesson ??
      item.name ??
      item.canonical_title
    );

    if (!title) return null;

    const lessonId = clean(
      item.lesson_id ??
      item.lessonId ??
      item.id
    );

    return {
      title,
      lessonId
    };
  }

  function syncSelectedLessonIdentity() {
    const el = lesson();
    if (!el) return;

    const opt = el.options?.[el.selectedIndex];

    el.dataset.lessonId = clean(
      opt?.dataset?.lessonId
    );

    // Expose the selected identity to the legacy chat page without changing
    // lessonSelect.value, which remains the human-readable lesson title.
    window.NABILSelectedLesson = {
      title: clean(el.value),
      lesson_id: clean(el.dataset.lessonId)
    };

    // Optional event for any other frontend component that wants to react
    // to a curriculum lesson selection.
    try {
      window.dispatchEvent(
        new CustomEvent("nabil:lesson-selected", {
          detail: {
            title: window.NABILSelectedLesson.title,
            lesson_id: window.NABILSelectedLesson.lesson_id
          }
        })
      );
    } catch (_) {
      // CustomEvent failure must never break curriculum selection.
    }
  }

  async function fetchCurriculumLessons(queryString) {
    let res = await fetch(
      "/api/chat/curriculum/lessons?" + queryString,
      { cache: "no-store" }
    );

    // Some deployments mount the chat router without the /chat prefix.
    if (res.status === 404) {
      res = await fetch(
        "/api/curriculum/lessons?" + queryString,
        { cache: "no-store" }
      );
    }

    return res;
  }

  async function refreshStrictLessons() {
    const g = clean(grade()?.value);
    const s = clean(subject()?.value);
    const l = clean(language()?.value);
    const b = clean(branch()?.value);

    const seq = ++requestSeq;

    resetLessons();

    if (
      g.startsWith("الثالث ثانوي") &&
      !g.includes(" - ") &&
      !b
    ) {
      resetLessons("اختر فرع الثالث ثانوي أولًا");
      return;
    }

    if (!g || !s || !l) {
      return;
    }

    const q = new URLSearchParams({
      grade: g,
      subject: s,
      language: l
    });

    if (b) {
      q.set("branch", b);
    }

    try {
      const res = await fetchCurriculumLessons(
        q.toString()
      );

      if (!res.ok) {
        throw new Error(
          "curriculum " + res.status
        );
      }

      const data = await res.json();

      // Ignore stale network responses after the user changes another select.
      if (seq !== requestSeq) {
        return;
      }

      const el = lesson();

      if (!el) {
        return;
      }

      const rawLessons = Array.isArray(data?.lessons)
        ? data.lessons
        : [];

      const normalized = [];
      const seen = new Set();

      for (const raw of rawLessons) {
        const item = normalizeLessonItem(raw);

        if (!item) continue;

        // Prefer lesson_id as identity when available.
        // Fall back to title only for the legacy API.
        const key = item.lessonId
          ? "id:" + item.lessonId
          : "title:" + item.title.toLocaleLowerCase();

        if (seen.has(key)) {
          continue;
        }

        seen.add(key);
        normalized.push(item);
      }

      resetLessons(
        normalized.length
          ? "اختر الدرس"
          : "لا توجد دروس موثقة بهذه اللغة"
      );

      for (const item of normalized) {
        const opt = document.createElement("option");

        // IMPORTANT:
        // Keep value = title so every existing part of NABIL AI that expects
        // lessonSelect.value to be the lesson title continues to work.
        opt.value = item.title;
        opt.textContent = item.title;

        // Golden identity travels separately.
        opt.dataset.lessonId = item.lessonId;

        el.appendChild(opt);
      }

      el.dataset.strictCurriculum = "1";
      syncSelectedLessonIdentity();

    } catch (err) {
      if (seq !== requestSeq) {
        return;
      }

      console.error(
        "NABIL strict curriculum:",
        err
      );

      resetLessons(
        "لا توجد دروس موثقة لهذا الاختيار"
      );
    }
  }

  function bindLessonSelect() {
    const el = lesson();

    if (!el || el.dataset.nabilLessonIdentityBound) {
      return;
    }

    el.dataset.nabilLessonIdentityBound = "1";

    el.addEventListener(
      "change",
      syncSelectedLessonIdentity
    );

    syncSelectedLessonIdentity();
  }

  function bindCurriculumSelectors() {
    for (const el of [
      grade(),
      subject(),
      language(),
      branch()
    ]) {
      if (
        !el ||
        el.dataset.strictCurriculumBound
      ) {
        continue;
      }

      el.dataset.strictCurriculumBound = "1";

      el.addEventListener(
        "change",
        () => {
          setTimeout(
            refreshStrictLessons,
            0
          );
        }
      );
    }

    bindLessonSelect();
  }

  function bind() {
    ++bindSeq;

    bindCurriculumSelectors();

    setTimeout(
      refreshStrictLessons,
      250
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      bind
    );
  } else {
    bind();
  }

  /*
   * The legacy page can rebuild the curriculum selects asynchronously.
   * Re-bind after those mutations.
   *
   * We intentionally do not use a permanent MutationObserver here:
   * rebuilding lesson options ourselves would trigger it and could create
   * refresh loops.
   */
  setTimeout(
    () => {
      bindCurriculumSelectors();
      refreshStrictLessons();
    },
    1200
  );

  setTimeout(
    () => {
      bindCurriculumSelectors();
      refreshStrictLessons();
    },
    1800
  );

  /*
   * Public compatibility API.
   *
   * Existing code can continue calling:
   *   window.NABILStrictCurriculum.refresh()
   *
   * New chat code can call:
   *   window.NABILStrictCurriculum.getSelectedLessonId()
   */
  window.NABILStrictCurriculum = {
    refresh: refreshStrictLessons,

    getSelectedLessonId() {
      const el = lesson();

      if (!el) return "";

      const opt = el.options?.[el.selectedIndex];

      return clean(
        opt?.dataset?.lessonId ||
        el.dataset.lessonId
      );
    },

    getSelectedLesson() {
      const el = lesson();

      if (!el) {
        return {
          title: "",
          lesson_id: ""
        };
      }

      const opt = el.options?.[el.selectedIndex];

      return {
        title: clean(el.value),
        lesson_id: clean(
          opt?.dataset?.lessonId ||
          el.dataset.lessonId
        )
      };
    }
  };
})();
