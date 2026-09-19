"""Run NABIL AI and resume science PDF ingestion after Railway restarts.

Every Railway deploy replaces its container, so a manually started Console job
cannot survive it. Launch ingestion with the server instead, with durable
per-page progress in PostgreSQL and a cross-container advisory lock.
"""
import os
import subprocess
import sys

import uvicorn


def main() -> None:
    raw_port = os.environ.get("PORT") or "8080"
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise SystemExit(f"Invalid PORT environment variable: {raw_port!r}") from exc
    if not 1 <= port <= 65535:
        raise SystemExit(f"PORT out of range: {port}")

    worker = None
    auto_index = os.environ.get("NABIL_AUTO_INDEX_SCIENCE", "1").strip().lower()
    if auto_index not in {"0", "false", "no", "off"}:
        try:
            worker = subprocess.Popen(
                [sys.executable, "-u", "-m", "scripts.index_science_textbooks", "all"],
                cwd="/app",
                env={**os.environ, "PYTHONUNBUFFERED": "1"},
                stdout=None,  # worker progress appears in Railway Deploy Logs
                stderr=None,
            )
            print(
                f"SCIENCE_INDEX_AUTO_RESUME started pid={worker.pid}; "
                "chemistry -> physics -> biology; PostgreSQL checkpoints enabled",
                flush=True,
            )
        except Exception as exc:
            # Ingestion must not take down the student-facing website.
            print(f"SCIENCE_INDEX_START_FAILED: {exc}", flush=True)

    try:
        uvicorn.run("app.main:app", host="0.0.0.0", port=port)
    finally:
        if worker is not None and worker.poll() is None:
            worker.terminate()
            try:
                worker.wait(timeout=12)
            except subprocess.TimeoutExpired:
                worker.kill()
                worker.wait()


if __name__ == "__main__":
    main()
