"""Start NABIL AI with a validated runtime port; no shell expansion required."""
import os

import uvicorn


def main() -> None:
    raw_port = os.environ.get("PORT") or "8080"
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise SystemExit(f"Invalid PORT environment variable: {raw_port!r}") from exc
    if not 1 <= port <= 65535:
        raise SystemExit(f"PORT out of range: {port}")
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
