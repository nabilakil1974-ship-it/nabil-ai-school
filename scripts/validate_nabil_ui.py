"""Static UI contract checks for NABIL AI production builds.

This intentionally avoids browser automation; it catches accidental regressions
in the exact owner-requested wiring before a Railway image is accepted.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str, *needles: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise SystemExit(f"{path}: missing required contract strings: {missing}")
    return text


def main() -> None:
    theme = require(
        "app/static/nabil_reference_theme.css",
        "--nabil-ref-page:#05172d",
        "--nabil-ref-header:#002973",
        "--nabil-ref-panel:#081e33",
        "--nabil-ref-green:#009e48",
        "#nabilHomeTutorHost",
        "#nabilLearningDock",
        ".nabil-visual",
    )
    open_tutor = require(
        "app/static/nabil_open_tutor_v1.js",
        'data.append("activity_mode","general_exercises")',
        'fetch("/api/chat"',
        "MediaRecorder",
        "renderNabilDiagram",
        "nabilSpeakClear",
        "stage.hidden=true",
        "speakGreetingOnce",
        "prepareSpeechTypewriter",
        "nabilOpenPace",
        "nabilOpenLiveType",
        "drawingPreviewModal",
        "home_live_tutor",
        "board.dir=dir",
    )
    learning = require(
        "app/static/nabil_learning_v132.js",
        'data-nv132=',
        '["checkpoint"',
        '["explain_another_way"',
        '["adaptive_practice"',
        '["flashcards"',
        '["quick_quiz"',
        '["study_plan"',
        '["dashboard"',
        "sendToAI",
        "nv132Result",
        "placeDock",
        "awaitingAnswer",
    )
    main_py = require(
        "app/main.py",
        "gateway_marker",
        "bootstrapNabilHome(){ return;",
        "nabil_reference_theme.css",
        "nabil_learning_v132.js",
        "nabil_open_tutor_v1.js",
        "pace_browser_new",
        "pace_neural_new",
        'rfind("</body>")',
    )

    lesson_runtime = require(
        "app/static/nabil_lesson_e2e_runtime_v1.js",
        "#nabilE2ETools",
        "#nabilE2EStatus",
        "#nabilE2ESend",
        "#nabilE2EReadPage",
        "SpeechSynthesisUtterance",
        "speechSynthesis",
        "stopSpeech",
    )
    smart_lab = require(
        "app/static/nabil_smart_lab_bridge_v1.js",
        "/api/smart-labs/from-question",
        "nabil:teach-all",
        "nabil:teach-stop",
        "nabil:teacher-complete",
        "#nabilSmartLabFrame",
    )
    lab_voice = require(
        "app/static/nabil_lab_voice_v1.js",
        "speechSynthesis",
        "NABILLessonE2E",
        "NABILBrowserTTS",
    )
    mobile_lab = require(
        "app/static/nabil_mobile_lab_fix_v15.css",
        "#nabilSmartLabModal",
        "#nabilSmartLabShell",
        "#nabilSmartLabFrame",
        "height:0!important",
        "100dvh",
        ".nabil-solution-runtime-lab iframe",
    )

    if ".selection-stage{display:none!important}" not in theme.replace(" ", ""):
        raise SystemExit("theme: grade-only landing stage must remain hidden")
    if "replaceChildren();stage.hidden=true" not in open_tutor.replace(" ", ""):
        raise SystemExit("open tutor: legacy grade landing must remain retired")
    if 'html.replace("</body>"' in main_py:
        raise SystemExit("main.py: global </body> replacement can leak raw JS")

    compact_mobile = "".join(mobile_lab.split())
    required_mobile_frame = "#nabilSmartLabFrame{flex:11 0!important;width:100%!important;height:0!important;min-height:0!important;max-height:none!important;}"
    if required_mobile_frame not in compact_mobile:
        raise SystemExit("mobile lab: Smart Lab frame must consume the remaining phone viewport")

    print("NABIL UI contract: PASS")
    print(" - owner reference blue palette")
    print(" - one robot landing, no grade-only splash")
    print(" - typed/voice open tutor shares /api/chat + renderer + neural TTS")
    print(" - same voice/pace and LTR foreign-language answer board")
    print(" - verified diagrams and full-size preview, paced visible transcript")
    print(" - smart learning actions render real results below answer tools")
    print(" - lesson diagnostic panel + status/read/send controls are wired")
    print(" - Smart Lab teach/stop/completion bridge is wired")
    print(" - lesson/lab speech contracts are wired")
    print(" - phone Smart Lab keeps a real remaining-viewport height")


if __name__ == "__main__":
    main()
