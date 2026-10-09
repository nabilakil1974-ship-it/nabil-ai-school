from __future__ import annotations

"""Railway entrypoint for Grade 7 Mathematics Golden production."""

import sys

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
