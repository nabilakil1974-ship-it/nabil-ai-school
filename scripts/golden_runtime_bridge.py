"""Compatibility installer for the canonical Golden catalogue.

The old route monkey-patch is retired. Production startup still imports this function,
so it now performs one idempotent normal FastAPI include_router() until app/main.py is
cleaned up to own the registration directly.
"""


def install_golden_runtime_bridge():
    from app.main import app
    from app.services import golden_catalogue

    marker = "_nabil_golden_catalogue_registered"
    if getattr(app.state, marker, False):
        return app

    # Do not duplicate canonical routes if a future app/main.py registers them first.
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
