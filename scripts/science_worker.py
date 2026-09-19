"""Dedicated Railway worker: science PDF indexing with restart-safe DB checkpoints.

Deploy this as a SEPARATE Railway service from the same GitHub repo,
Dockerfile=/Dockerfile, Start Command=python -m scripts.science_worker.
Web deployments will not interrupt it; worker redeploys resume missing pages.
"""
import os
import time
import traceback

from scripts.index_science_textbooks import run_manifest

RETRY_SECONDS = int(os.getenv("NABIL_SCIENCE_RETRY_SECONDS", "900"))


def main():
    print("SCIENCE_WORKER_STARTED chemistry -> physics -> biology", flush=True)
    while True:
        failures = []
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
