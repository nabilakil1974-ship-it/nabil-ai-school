"""Install the canonical Golden HTTP runtime.

The catalogue service now natively reads golden_package_store, so no monkey
patching and no Drive/AI runtime fallback are required.
"""


def install_golden_runtime_bridge():
    from app.main import app
    from app.services import golden_catalogue

    marker = "_nabil_golden_catalogue_registered"
    if getattr(app.state, marker, False):
        return app

    canonical_paths = {
        "/api/curriculum/lessons",
        "/api/chat/curriculum/lessons",
        "/api/interactive-lessons/resolve",
        "/api/interactive-lessons/golden-classroom",
        "/api/interactive-lessons/verified-labs",
        "/api/interactive-lessons/verified-lab",
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
