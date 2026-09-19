(() => {
  "use strict";
  // deploy-trigger: 2026-09-18 textbook grounding rollout
  const byId = id => document.getElementById(id);
  const grade = () => byId("gradeSelect");
  const subject = () => byId("subjectSelect");
  const language = () => byId("languageSelect");
  const branch = () => byId("branchSelect");
  const lesson = () => byId("lessonSelect");
  let requestSeq = 0;

  function resetLessons(message = "اختر الدرس") {
    const el = lesson();
    if (!el) return;
    el.innerHTML = "";
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = message;
    el.appendChild(opt);
  }

  async function refreshStrictLessons() {
    const g = grade()?.value?.trim() || "";
    const s = subject()?.value?.trim() || "";
    const l = language()?.value?.trim() || "";
    const b = branch()?.value?.trim() || "";
    const seq = ++requestSeq;
    resetLessons();
    if (g.startsWith("الثالث ثانوي") && !g.includes(" - ") && !b) {
      resetLessons("اختر فرع الثالث ثانوي أولًا");
      return;
    }
    if (!g || !s || !l) return;

    const q = new URLSearchParams({grade:g, subject:s, language:l});
    if (b) q.set("branch", b);
    try {
      let res = await fetch("/api/chat/curriculum/lessons?" + q.toString(), {cache:"no-store"});
      // Some deployments mount the chat router without the /chat prefix.
      if (res.status === 404) {
        res = await fetch("/api/curriculum/lessons?" + q.toString(), {cache:"no-store"});
      }
      if (!res.ok) throw new Error("curriculum " + res.status);
      const data = await res.json();
      if (seq !== requestSeq) return;
      const el = lesson();
      if (!el) return;
      resetLessons(Array.isArray(data.lessons) && data.lessons.length ? "اختر الدرس" : "لا توجد دروس موثقة بهذه اللغة");
      for (const title of (data.lessons || [])) {
        const opt = document.createElement("option");
        opt.value = title;
        opt.textContent = title;
        el.appendChild(opt);
      }
      el.dataset.strictCurriculum = "1";
    } catch (err) {
      if (seq !== requestSeq) return;
      console.error("NABIL strict curriculum:", err);
      resetLessons("لا توجد دروس موثقة لهذا الاختيار");
    }
  }

  function bind() {
    for (const el of [grade(), subject(), language(), branch()]) {
      if (!el || el.dataset.strictCurriculumBound) continue;
      el.dataset.strictCurriculumBound = "1";
      el.addEventListener("change", () => setTimeout(refreshStrictLessons, 0));
    }
    setTimeout(refreshStrictLessons, 250);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", bind);
  else bind();

  // The legacy page rebuilds selects during curriculum loading; keep the strict
  // grade+subject+language result authoritative after those mutations.
  setTimeout(bind, 1200);
  setTimeout(refreshStrictLessons, 1800);
  window.NABILStrictCurriculum = { refresh: refreshStrictLessons };
})();
