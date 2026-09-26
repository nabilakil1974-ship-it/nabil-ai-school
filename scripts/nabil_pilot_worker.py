"""Autonomous, resumable golden-pilot runner.

Runs exactly the configured first lesson. It never advances to a second lesson:
before every attempt it reads the remote book checkpoint and exits permanently
once the configured lesson is PUBLISHED_VERIFIED.

The runner is safe to restart because page, exercise and solution work is
checkpointed in Drive.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from scripts import nabil_lesson_factory as factory
from scripts.nabil_book_factory import announce, remote_checkpoint, run

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "data" / "nabil_pilot_config.json"


def _truthy(value) -> bool:
    return str(value).strip().lower() not in {"0", "false", "no", "off", ""}


def load_config() -> dict:
    if not CONFIG_PATH.is_file():
        raise RuntimeError("PILOT_CONFIG_MISSING")
    cfg = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    required = ("book_id", "lesson_id", "curriculum_root_id")
    missing = [key for key in required if not str(cfg.get(key, "")).strip()]
    if missing:
        raise RuntimeError("PILOT_CONFIG_INVALID: missing " + ",".join(missing))
    return cfg


def apply_runtime_defaults(cfg: dict) -> None:
    defaults = {
        "NABIL_CURRICULUM_ROOT_ID": cfg["curriculum_root_id"],
        "NABIL_FACTORY_AI_PROVIDER": cfg.get("primary_provider", "groq"),
        "NABIL_FACTORY_AI_FAILOVER_PROVIDERS":
            cfg.get("failover_providers", "openrouter"),
        "GROQ_VISION_MODEL":
            cfg.get("groq_vision_model", "qwen/qwen3.8-27b"),
        "OPENROUTER_VISION_MODEL":
            cfg.get("openrouter_vision_model", "google/gemini-3.6-flash"),
        "OPENROUTER_TEXT_MODEL":
            cfg.get("openrouter_text_model", "google/gemini-3.6-flash"),
        "NABIL_FACTORY_VISION_MAX_OUTPUT_TOKENS":
            str(cfg.get("vision_max_output_tokens", 2048)),
        "NABIL_FACTORY_TEXT_MAX_OUTPUT_TOKENS":
            str(cfg.get("text_max_output_tokens", 4096)),
        "NABIL_FACTORY_MAX_ALL_PROVIDER_WAIT_SECONDS":
            str(cfg.get("max_all_provider_wait_seconds", 30)),
    }
    for key, value in defaults.items():
        os.environ.setdefault(key, str(value))


def configured_lesson_is_published(cfg: dict) -> bool:
    service = factory.get_drive_service()
    state = remote_checkpoint(
        service,
        cfg["curriculum_root_id"],
        cfg["book_id"],
    )
    if not state:
        return False
    row = (state.get("lessons") or {}).get(cfg["lesson_id"]) or {}
    return bool(
        row.get("status") == "PUBLISHED_VERIFIED"
        and row.get("drive_theory_id")
        and row.get("drive_exercises_id")
    )


def run_once(cfg: dict) -> bool:
    if configured_lesson_is_published(cfg):
        announce(
            "AUTONOMOUS_PILOT_ALREADY_PUBLISHED",
            lesson_id=cfg["lesson_id"],
        )
        return True

    announce(
        "AUTONOMOUS_PILOT_ATTEMPT_START",
        lesson_id=cfg["lesson_id"],
        book_id=cfg["book_id"],
    )
    result = run(
        cfg["book_id"],
        index_only=False,
        publish=True,
        max_new_lessons=int(cfg.get("max_new_lessons", 1)),
    )
    if configured_lesson_is_published(cfg):
        announce(
            "AUTONOMOUS_PILOT_PUBLISHED_VERIFIED",
            lesson_id=cfg["lesson_id"],
            status=result.get("status"),
        )
        return True

    raise RuntimeError(
        "AUTONOMOUS_PILOT_DID_NOT_PUBLISH_CONFIGURED_LESSON")


def supervise(stop_event=None) -> None:
    cfg = load_config()
    enabled = _truthy(
        os.getenv("NABIL_AUTO_FACTORY_PILOT", "1")
    ) and bool(cfg.get("enabled", True))
    if not enabled:
        announce("AUTONOMOUS_PILOT_DISABLED")
        return

    apply_runtime_defaults(cfg)
    retry_seconds = max(60, int(cfg.get("retry_seconds", 300)))
    max_attempts = max(
        1, int(os.getenv(
            "NABIL_PILOT_MAX_ATTEMPTS_PER_BOOT",
            str(cfg.get("max_attempts_per_boot", 1)),
        ))
    )
    announce(
        "AUTONOMOUS_PILOT_SUPERVISOR_STARTED",
        lesson_id=cfg["lesson_id"],
        retry_seconds=retry_seconds,
        max_attempts_per_boot=max_attempts,
    )

    attempts = 0
    while attempts < max_attempts:
        if stop_event is not None and stop_event.is_set():
            return
        attempts += 1
        try:
            if run_once(cfg):
                return
        except Exception as exc:
            announce(
                "AUTONOMOUS_PILOT_ATTEMPT_BLOCKED",
                lesson_id=cfg["lesson_id"],
                attempt=attempts,
                max_attempts_per_boot=max_attempts,
                reason=str(exc)[:900],
                retry_seconds=retry_seconds,
            )
        if attempts >= max_attempts:
            announce(
                "AUTONOMOUS_PILOT_PAUSED_BUDGET_GUARD",
                lesson_id=cfg["lesson_id"],
                attempts=attempts,
                reason="wait for code/config change before another paid attempt",
            )
            raise SystemExit(75)
        if stop_event is None:
            time.sleep(retry_seconds)
        elif stop_event.wait(retry_seconds):
            return


def main() -> None:
    supervise()


if __name__ == "__main__":
    main()
