/* NABIL student entry — minimal welcome, then grade only. No developer labels. */
(() => {
  "use strict";
  const byId = (id) => document.getElementById(id);
  let overlay, card, originalParent, originalNext, gradeSelect, stage = "welcome";

  function styleOverlay() {
    overlay = document.createElement("main");
    overlay.id = "nabilStudentEntry";
    overlay.setAttribute("role", "main");
    overlay.style.cssText = [
      "position:fixed","inset:0","z-index:2147483000","display:flex",
      "align-items:center","justify-content:center","padding:22px",
      "box-sizing:border-box","background:#071d32","color:#eef8ff",
      "font-family:Tahoma,Arial,sans-serif","direction:rtl"
    ].join(";");
    card = document.createElement("section");
    card.style.cssText = [
      "box-sizing:border-box","width:min(100%,520px)","padding:28px 22px",
      "border-radius:18px","border:1px solid #145f91","background:#0a2238",
      "text-align:center","box-shadow:0 18px 55px #0005"
    ].join(";");
    overlay.appendChild(card);
    document.body.appendChild(overlay);
  }

  function button(label, action) {
    const b = document.createElement("button");
    b.type = "button";
    b.textContent = label;
    b.style.cssText = [
      "display:block","width:100%","min-height:50px","margin-top:20px",
      "padding:12px 18px","border:0","border-radius:12px",
      "background:#0b6de5","color:white","font:700 18px Tahoma,Arial,sans-serif",
      "cursor:pointer"
    ].join(";");
    b.addEventListener("click", action);
    return b;
  }

  function showWelcome() {
    stage = "welcome";
    card.replaceChildren();
    const greeting = document.createElement("p");
    greeting.textContent = "أنا الأستاذ نبيل، أهلًا بكم، لنبدأ الدرس.";
    greeting.style.cssText = "margin:0;font-size:clamp(22px,5vw,30px);line-height:1.8;font-weight:700";
    card.append(greeting, button("لنبدأ الدرس", showGrade));
  }

  function showGrade() {
    stage = "grade";
    card.replaceChildren();
    const label = document.createElement("label");
    label.textContent = "اختر الصف";
    label.htmlFor = "nabilStudentGradeSelect";
    label.style.cssText = "display:block;margin:0 0 16px;font-size:24px;font-weight:700";
    gradeSelect = byId("gradeSelect");
    if (!gradeSelect) {
      const msg = document.createElement("p");
      msg.textContent = "اختيار الصف غير متاح حاليًا.";
      card.append(msg, button("العودة", showWelcome));
      return;
    }
    if (!originalParent) {
      originalParent = gradeSelect.parentNode;
      originalNext = gradeSelect.nextSibling;
    }
    gradeSelect.id = "nabilStudentGradeSelect";
    gradeSelect.setAttribute("aria-label", "اختر الصف");
    gradeSelect.style.setProperty("display", "block", "important");
    gradeSelect.style.setProperty("width", "100%", "important");
    gradeSelect.style.setProperty("min-height", "52px", "important");
    gradeSelect.style.setProperty("font-size", "18px", "important");
    gradeSelect.style.setProperty("padding", "10px", "important");
    gradeSelect.style.setProperty("box-sizing", "border-box", "important");
    card.append(label, gradeSelect);
    const note = document.createElement("p");
    note.textContent = "اختر صفك للمتابعة.";
    note.style.cssText = "margin:12px 0 0;color:#bad6e9;font-size:14px";
    card.append(note, button("متابعة", continueToLessons));
    gradeSelect.focus();
  }

  function restoreGradeSelect() {
    if (!gradeSelect || !originalParent) return;
    gradeSelect.id = "gradeSelect";
    if (originalNext && originalNext.parentNode === originalParent) {
      originalParent.insertBefore(gradeSelect, originalNext);
    } else {
      originalParent.appendChild(gradeSelect);
    }
    gradeSelect.style.removeProperty("display");
    gradeSelect.style.removeProperty("width");
    gradeSelect.style.removeProperty("min-height");
    gradeSelect.style.removeProperty("font-size");
    gradeSelect.style.removeProperty("padding");
    gradeSelect.style.removeProperty("box-sizing");
    gradeSelect.removeAttribute("aria-label");
  }

  function continueToLessons() {
    if (!gradeSelect || !String(gradeSelect.value || "").trim()) {
      const old = card.querySelector("[data-grade-error]");
      if (!old) {
        const error = document.createElement("p");
        error.dataset.gradeError = "1";
        error.textContent = "يرجى اختيار الصف أولًا.";
        error.style.cssText = "margin:12px 0 0;color:#ffd44f";
        card.appendChild(error);
      }
      return;
    }
    const chosen = gradeSelect.value;
    restoreGradeSelect();
    gradeSelect.value = chosen;
    overlay.remove();
    document.body.classList.remove("nabil-home-lock");
    // Refresh the real curriculum selectors after restoring the original DOM.
    gradeSelect.dispatchEvent(new Event("change", { bubbles: true }));
    stage = "lessons";
  }

  function init() {
    // Remove the extra whiteboard-branded shortcut and any accidental diagnostics.
    byId("nabil-start-whiteboard")?.remove();
    byId("nabilGoldenDiagnostic")?.remove();
    byId("nabilGoldenLessonHost")?.remove();
    styleOverlay();
    showWelcome();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
