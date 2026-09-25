"""Dedicated Railway source-book worker. Never run inside the student web process.

Set NABIL_FACTORY_INBOX_FOLDER_ID and, for otherwise unregistered PDFs in that
intake folder, NABIL_FACTORY_INBOX_GRADE, NABIL_FACTORY_INBOX_SUBJECT and
NABIL_FACTORY_INBOX_LANGUAGE. Existing manifested books retain their labels.
Configure NABIL_FACTORY_AI_PROVIDER and a scoped source-sharing consent before
processing scanned pages with an external vision model.

Start command: python -m scripts.nabil_factory_worker
"""
import os
import sys

from scripts.nabil_book_factory import run_folder, announce


def main():
    folder_id = os.getenv("NABIL_FACTORY_INBOX_FOLDER_ID", "").strip()
    if not folder_id:
        raise RuntimeError("NABIL_FACTORY_INBOX_FOLDER_ID_NOT_CONFIGURED")
    interval = int(os.getenv("NABIL_FACTORY_POLL_SECONDS", "300"))
    announce("FACTORY_WORKER_STARTED", poll_seconds=interval, folder_configured=True)
    run_folder(
        folder_id,
        grade=os.getenv("NABIL_FACTORY_INBOX_GRADE", ""),
        subject=os.getenv("NABIL_FACTORY_INBOX_SUBJECT", ""),
        language=os.getenv("NABIL_FACTORY_INBOX_LANGUAGE", ""),
        branch=os.getenv("NABIL_FACTORY_INBOX_BRANCH", ""),
        watch=True,
        poll_seconds=interval,
    )


if __name__ == "__main__":
    sys.exit(main())
