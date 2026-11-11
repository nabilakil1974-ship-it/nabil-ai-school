"""Dedicated Railway worker: science PDF indexing with restart-safe DB checkpoints.

Deploy this as a SEPARATE Railway service from the same GitHub repo,
Dockerfile=/Dockerfile, Start Command=python -m scripts.science_worker.
Web deployments will not interrupt it; worker redeploys resume missing pages.
"""
import os
import time
import traceback

from sqlalchemy import text
from app.db.session import engine

from scripts.index_science_textbooks import run_manifest

RETRY_SECONDS = int(os.getenv("NABIL_SCIENCE_RETRY_SECONDS", "900"))


def main():
    print("SCIENCE_WORKER_STARTED chemistry -> physics -> biology", flush=True)
    while True:
        failures = []
        # Coordinate with scripts.index_science_textbooks: both paths use
        # the same PostgreSQL session advisory lock to avoid duplicate OCR.
        with engine.connect() as connection:
            locked = False
            if connection.dialect.name == "postgresql":
                print("SCIENCE_WORKER_WAITING_FOR_EXCLUSIVE_LOCK", flush=True)
                connection.execute(text("SELECT pg_advisory_lock(728168120)"))
                connection.commit()
                locked = True
                print("SCIENCE_WORKER_LOCK_ACQUIRED", flush=True)
            try:
                for name in ("chemistry", "physics", "biology"):
                    print(f"SCIENCE_WORKER_SUBJECT_START {name}", flush=True)
                    try:
                        run_manifest(name)
                    except Exception as exc:
                        print(f"SCIENCE_WORKER_SUBJECT_FAILED {name}: {exc}", flush=True)
                        traceback.print_exc()
                        failures.append(name)
                    else:
                        print(f"SCIENCE_WORKER_SUBJECT_COMPLETE {name}", flush=True)
            finally:
                if locked:
                    connection.execute(text("SELECT pg_advisory_unlock(728168120)"))
                    connection.commit()
                    print("SCIENCE_WORKER_LOCK_RELEASED", flush=True)
        if not failures:
            print(
                "SCIENCE_WORKER_ALL_COMPLETE; sleeping and ready to resume "
                "automatically if this worker is redeployed.",
                flush=True,
            )
            # No need to download every PDF repeatedly after completion.
            # Railway restart/redeploy naturally starts main() again.
            while True:
                time.sleep(3600)
        print(
            f"SCIENCE_WORKER_RETRY in {RETRY_SECONDS}s: "
            + ", ".join(failures),
            flush=True,
        )
        time.sleep(RETRY_SECONDS)


if __name__ == "__main__":
    main()
