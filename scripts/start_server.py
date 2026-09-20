"""Start the web server and optionally supervise resumable science indexing.

Railway replaces containers on deploy. Book progress is saved per PDF page in
PostgreSQL. The optional background indexer is relaunched after nonzero exits
instead of silently stopping forever. A separate Railway worker is preferred
where CPU/RAM are limited.
"""
import os
import subprocess
import sys
import threading

import uvicorn

SCIENCE_COMMAND = (
    sys.executable, "-u", "-m", "scripts.index_science_textbooks", "all"
)

MATH_COMMAND = (sys.executable, "-u", "-m", "scripts.index_math_textbooks")


def _supervise_science(stop: threading.Event) -> None:
    retry_seconds = max(
        30, int(os.environ.get("NABIL_SCIENCE_RETRY_SECONDS", "120"))
    )
    # Give the public web app time to start responding before indexing.
    if stop.wait(15):
        return
    while not stop.is_set():
        try:
            worker = subprocess.Popen(
                SCIENCE_COMMAND,
                cwd="/app",
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )
            print(
                f"SCIENCE_INDEX_AUTO_RESUME started pid={worker.pid}; "
                "chemistry -> physics -> biology; resume ONLY missing pages",
                flush=True,
            )
            while not stop.is_set():
                try:
                    exit_code = worker.wait(timeout=2)
                    break
                except subprocess.TimeoutExpired:
                    continue
            else:
                exit_code = None
            if stop.is_set():
                if worker.poll() is None:
                    worker.terminate()
                    try:
                        worker.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        worker.kill()
                        worker.wait()
                return
            if exit_code == 0:
                print("SCIENCE_INDEX_ALL_COMPLETE; worker exited normally", flush=True)
                return
            print(
                f"SCIENCE_INDEX_WORKER_EXITED code={exit_code}; "
                f"restarting in {retry_seconds}s from PostgreSQL checkpoints",
                flush=True,
            )
        except Exception as exc:
            print(
                f"SCIENCE_INDEX_WORKER_ERROR {type(exc).__name__}: {exc}; "
                f"retry in {retry_seconds}s",
                flush=True,
            )
        if stop.wait(retry_seconds):
            return


def _supervise_math(stop: threading.Event) -> None:
    retry_seconds = max(
        30, int(os.environ.get("NABIL_MATH_RETRY_SECONDS", "120"))
    )
    # Give the public web app time to start responding before indexing.
    if stop.wait(30):
        return
    while not stop.is_set():
        try:
            worker = subprocess.Popen(
                MATH_COMMAND,
                cwd="/app",
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
            )
            print(
                f"MATH_INDEX_AUTO_RESUME started pid={worker.pid}; "
                "resume ONLY missing mathematics pages",
                flush=True,
            )
            while not stop.is_set():
                try:
                    exit_code = worker.wait(timeout=2)
                    break
                except subprocess.TimeoutExpired:
                    continue
            else:
                exit_code = None
            if stop.is_set():
                if worker.poll() is None:
                    worker.terminate()
                    try:
                        worker.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        worker.kill()
                        worker.wait()
                return
            if exit_code == 0:
                print("MATH_INDEX_ALL_COMPLETE; worker exited normally", flush=True)
                return
            print(
                f"MATH_INDEX_WORKER_EXITED code={exit_code}; "
                f"restarting in {retry_seconds}s from PostgreSQL checkpoints",
                flush=True,
            )
        except Exception as exc:
            print(
                f"MATH_INDEX_WORKER_ERROR {type(exc).__name__}: {exc}; "
                f"retry in {retry_seconds}s",
                flush=True,
            )
        if stop.wait(retry_seconds):
            return


def main() -> None:
    raw_port = os.environ.get("PORT") or "8080"
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise SystemExit(f"Invalid PORT environment variable: {raw_port!r}") from exc
    if not 1 <= port <= 65535:
        raise SystemExit(f"PORT out of range: {port}")

    stop = threading.Event()
    auto_index = os.environ.get("NABIL_AUTO_INDEX_SCIENCE", "0").strip().lower()
    supervisor = None
    if auto_index not in {"0", "false", "no", "off"}:
        supervisor = threading.Thread(
            target=_supervise_science, args=(stop,), daemon=True,
            name="nabil-science-index-supervisor",
        )
        supervisor.start()
        print("SCIENCE_INDEX_SUPERVISOR enabled", flush=True)

    auto_math = os.environ.get("NABIL_AUTO_INDEX_MATH", "1").strip().lower()
    math_supervisor = None
    if auto_math not in {"0", "false", "no", "off"}:
        math_supervisor = threading.Thread(
            target=_supervise_math, args=(stop,), daemon=True,
            name="nabil-math-index-supervisor",
        )
        math_supervisor.start()
        print("MATH_INDEX_SUPERVISOR enabled", flush=True)

    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=port)
    finally:
        stop.set()
        if supervisor is not None:
            supervisor.join(timeout=15)
        if math_supervisor is not None:
            math_supervisor.join(timeout=15)


if __name__ == "__main__":
    main()
