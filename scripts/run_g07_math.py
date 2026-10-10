from __future__ import annotations

"""Single-lesson Grade 7 mathematics acceptance run. No batch production."""

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from scripts import nabil_book_factory


if __name__ == "__main__":
    sys.argv = [
        sys.argv[0],
        "--book-id", "1E-nj01QlpvZCa_kHy92qQDlm6ko1ba_D",
        "--grade", "7",
        "--subject", "mathematics",
        "--language", "en",
        "--max-new-lessons", "1",
    ]
    raise SystemExit(nabil_book_factory.main())
