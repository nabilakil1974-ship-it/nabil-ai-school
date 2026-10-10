from __future__ import annotations

"""Owner-authorized ONE lesson acceptance production; no Grade 7 batch."""

import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts import nabil_book_factory


if __name__ == "__main__":
    # Explicitly reproduce the one deleted Powers lesson, not five lessons.
    # Explicit, source-English-only pilot: skip expensive AR/FR translation calls.
    os.environ["NABIL_POWERS_ENGLISH_ONLY"] = "1"
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
    raise SystemExit(nabil_book_factory.main())
