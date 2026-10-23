from __future__ import annotations

"""Owner-authorized FULL Grade-7 Mathematics production (first lesson to last).

The source book is downloaded once to the persistent volume (/data/nabil) and
reused; progress is checkpointed to Drive after every lesson, so a restart
skips already-published lessons and never starts from the beginning.
"""

import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts import nabil_book_factory


if __name__ == "__main__":
    # No single-lesson restriction: whole book, resume from the checkpoint.
    os.environ.pop("NABIL_ONLY_LESSON_ID", None)
    os.environ.pop("NABIL_REBUILD_LESSON_ID", None)
    sys.argv = [
        sys.argv[0],
        "--book-id", os.getenv("NABIL_G07_BOOK_ID", "1E-nj01QlpvZCa_kHy92qQDlm6ko1ba_D"),
        "--grade", "7",
        "--subject", "mathematics",
        "--language", "en",
        "--max-new-lessons", "0",
    ]
    raise SystemExit(nabil_book_factory.main())
