"""P1 — source identity, textbook evidence and source-completeness gates."""

from .source_completeness import (
    attach_and_verify_source_completeness,
    build_independent_source_inventory,
)

__all__ = [
    "attach_and_verify_source_completeness",
    "build_independent_source_inventory",
]
