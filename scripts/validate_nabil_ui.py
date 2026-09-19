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

    # Reject known regressions that previously exposed code or reintroduced
    # a stand-alone grade splash.
    if ".selection-stage{display:none!important}" not in theme.replace(" ", ""):
        raise SystemExit("theme: grade-only landing stage must remain hidden")
    if "replaceChildren();stage.hidden=true" not in open_tutor.replace(" ", ""):
        raise SystemExit("open tutor: legacy grade landing must remain retired")
    if 'html.replace("</body>"' in main_py:
        raise SystemExit("main.py: global </body> replacement can leak raw JS")

    print("NABIL UI contract: PASS")
    print(" - owner reference blue palette")
    print(" - one robot landing, no grade-only splash")
    print(" - typed/voice open tutor shares /api/chat + renderer + neural TTS")
    print(" - same voice/pace and LTR foreign-language answer board")
    print(" - verified diagrams and full-size preview, paced visible transcript")
    print(" - smart learning actions render real results below answer tools")


if __name__ == "__main__":
    main()
