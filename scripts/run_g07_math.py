from __future__ import annotations

"""Grade 7 Powers production with fail-closed runtime diagnostics."""

import faulthandler
import json
import os
import signal
import sys
import time
import traceback
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_STAGE = "BOOT"
_STARTED = time.monotonic()


def report(event: str, **fields) -> None:
    """Emit stage-only diagnostics; never log credentials or raw exceptions."""
    payload = {
        "event": event,
        "stage": _STAGE,
        "elapsed_seconds": round(time.monotonic() - _STARTED, 2),
        **fields,
    }
    print("NABIL_G07_DIAGNOSTIC " + json.dumps(payload, ensure_ascii=True), flush=True)


def mark(stage: str) -> None:
    global _STAGE
    _STAGE = stage
    report("STAGE_ENTER")


def _on_signal(signum, frame):
    report("PROCESS_SIGNAL", signal=signal.Signals(signum).name)
    if frame is not None:
        traceback.print_stack(frame, file=sys.stderr)
    sys.stderr.flush()
    raise SystemExit(128 + signum)


def _uncaught(exc_type, exc_value, exc_tb):
    report("UNCAUGHT_EXCEPTION", exception_type=exc_type.__name__)
    traceback.print_exception(exc_type, exc_value, exc_tb, file=sys.stderr)
    sys.stderr.flush()


sys.excepthook = _uncaught
faulthandler.enable(file=sys.stderr)
for _sig in (signal.SIGTERM, signal.SIGINT):
    signal.signal(_sig, _on_signal)

mark("IMPORT_BOOK_FACTORY")
try:
    from scripts import nabil_book_factory
except BaseException as exc:
    report("IMPORT_FAILED", exception_type=type(exc).__name__)
    traceback.print_exc(file=sys.stderr)
    raise
report("IMPORT_OK")

if __name__ == "__main__":
    mark("CONFIGURE_LESSON")
    os.environ["NABIL_ONLY_LESSON_ID"] = "G07-MATHEMATICS-69B7C840-001"
    os.environ["NABIL_REBUILD_LESSON_ID"] = "G07-MATHEMATICS-69B7C840-001"
    sys.argv = [
        sys.argv[0],
        "--book-id", "1E-nj01QlpvZCa_kHy92qQDlm6ko1ba_D",
        "--grade", "7",
        "--subject", "mathematics",
        "--language", "en",
        "--max-new-lessons", "1",
    ]
    mark("RUN_BOOK_FACTORY")
    try:
        exit_code = nabil_book_factory.main()
    except BaseException as exc:
        report("FACTORY_EXCEPTION", exception_type=type(exc).__name__)
        traceback.print_exc(file=sys.stderr)
        raise
    report("FACTORY_EXIT", exit_code=exit_code)
    raise SystemExit(exit_code)
