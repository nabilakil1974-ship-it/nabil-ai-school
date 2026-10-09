from __future__ import annotations

"""Railway entrypoint for Grade 7 Mathematics Golden production."""

import sys
from pathlib import Path

# Be robust whether Railway invokes this as a module
# (`python -m scripts.run_g07_math`) or by file path
# (`python scripts/run_g07_math.py`).  Direct file execution otherwise puts
# /app/scripts on sys.path and makes `import scripts` fail.
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
        "--max-new-lessons", "5",
    ]
    nabil_book_factory.main()
