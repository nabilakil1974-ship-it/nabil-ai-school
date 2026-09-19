/* Direct lesson entry — the owner retired BOTH introductory screens.
 * Keep the original lesson DOM and its dropdowns/avatar/microphone intact.
 * Never navigate to the obsolete robot splash or welcome gateway.
 */
(function () {
  "use strict";

  function enterLessonDirectly() {
    const splash = document.getElementById("nabilHome");
    const gateway = document.getElementById("nabilProfessorGateway");
    if (splash) {
      splash.style.setProperty("display", "none", "important");
      splash.setAttribute("aria-hidden", "true");
    }
    if (gateway) {
      gateway.style.setProperty("display", "none", "important");
      gateway.classList.add("closed");
      gateway.setAttribute("aria-hidden", "true");
    }
    document.body.classList.remove("nabil-home-lock");

    // Legacy "Home" buttons must return to the main lesson selectors,
    // never resurrect the retired first or second intro screens.
    window.nabilShowProfessorGateway = enterLessonDirectly;
  }

  enterLessonDirectly();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enterLessonDirectly, {once: true});
  }
  window.addEventListener("load", enterLessonDirectly, {once: true});
})();
