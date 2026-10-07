"""Compatibility installer for the canonical Golden runtime.

Migration contract:
  canonical catalogue -> local reviewed Golden package -> renderer.
Drive/AI are production-time concerns only and are forbidden from student runtime.
"""


def install_golden_runtime_bridge():
    from app.main import app
    from app.services import golden_catalogue
    from app.services.golden_package_store import lesson_source

    marker = "_nabil_golden_catalogue_registered"
    if getattr(app.state, marker, False):
        return app

    # During migration golden_catalogue still owns the HTTP routes and renderer.
    # Replace only its source resolver so opening a lesson can never call Drive.
    def _local_source(entry):
        lid = str((entry or {}).get("lesson_id") or "").strip().upper()
        found = lesson_source(lid)
        if not found:
            raise RuntimeError(f"LOCAL_GOLDEN_PACKAGE_MISSING: {lid}")
        _catalogue_entry, text, source = found
        return text, source

    golden_catalogue._source = _local_source

    canonical_paths = {
        "/api/curriculum/lessons",
        "/api/chat/curriculum/lessons",
        "/api/interactive-lessons/resolve",
        "/api/interactive-lessons/golden-classroom",
    }
    existing = {getattr(route, "path", "") for route in app.routes}
    if not canonical_paths.issubset(existing):
        app.include_router(
            golden_catalogue.build_router(),
            prefix="/api",
            tags=["golden-catalogue"],
        )
    setattr(app.state, marker, True)
    return app
