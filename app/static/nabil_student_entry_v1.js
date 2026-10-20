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

  function isGradeSeven() {
    const value = String(gradeSelect?.value || "");
    const option = gradeSelect?.options?.[gradeSelect.selectedIndex];
    const label = String(option?.textContent || "");
    const combined = (value + " " + label).replace(/[٠-٩]/g, d => String("٠١٢٣٤٥٦٧٨٩".indexOf(d)));
    return /(?:^|\\D)7(?:\\D|$)/.test(combined)
      || /(?:grade|class|eb|g)\\s*0?7/i.test(combined)
      || /السابع|seventh|septieme/i.test(combined);
  }

  function showUnavailable() {
    let status = card.querySelector("[data-no-approved-lesson]");
    if (!status) {
      status = document.createElement("p");
      status.dataset.noApprovedLesson = "1";
      status.style.cssText = "margin:16px 0 0;color:#ffd44f;font-size:16px;line-height:1.8";
      card.appendChild(status);
    }
    status.textContent = "لا يوجد درس جاهز ومعتمد لهذا الصف حاليًا.";
  }

  function onGradeChange() {
    if (!gradeSelect || !String(gradeSelect.value || "").trim()) {
      card.querySelector("[data-no-approved-lesson]")?.remove();
      return;
    }
    if (isGradeSeven()) {
      // The only lesson approved for student-facing release is Grade 7 v4.
      window.location.assign("/static/NABIL_G07_EN004_method14_v4.html");
      return;
    }
    showUnavailable();
  }

  function showGrade() {
    stage = "grade";
    card.replaceChildren();
    const label = document.createElement("label");
    label.textContent = "اختر الصف";
    label.htmlFor = "gradeSelect";
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
    gradeSelect.setAttribute("aria-label", "اختر الصف");
    gradeSelect.style.setProperty("display", "block", "important");
    gradeSelect.style.setProperty("width", "100%", "important");
    gradeSelect.style.setProperty("min-height", "52px", "important");
    gradeSelect.style.setProperty("font-size", "18px", "important");
    gradeSelect.style.setProperty("padding", "10px", "important");
    gradeSelect.style.setProperty("box-sizing", "border-box", "important");
    card.append(label, gradeSelect);
    if (!gradeSelect.dataset.nabilStudentEntryBound) {
      gradeSelect.dataset.nabilStudentEntryBound = "1";
      gradeSelect.addEventListener("change", onGradeChange);
    }
    gradeSelect.focus();
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
