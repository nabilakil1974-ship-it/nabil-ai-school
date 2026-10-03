"""Production entrypoint that installs the Golden Drive bridge before Uvicorn.

Import the FastAPI app in this process, install the bridge on that exact object,
then make the generic server serve the already-patched object.  This avoids a
second string-based ``app.main:app`` import from bypassing the runtime patch.
"""
from scripts.golden_runtime_bridge import install_golden_runtime_bridge

# Import the application first so the bridge and Uvicorn operate on the same
# FastAPI object in the same process.
from app.main import app
import scripts.start_server as _server


def _run_patched_app(*args, **kwargs):
    """Replace only Uvicorn's app target; preserve all server settings."""
    original = _server.uvicorn.run

    def run(target, *run_args, **run_kwargs):
        if target == "app.main:app":
            target = app
        # Passing an app object cannot be used with reload/workers; this server
        # does not request either, so behaviour is otherwise identical.
        return original(target, *run_args, **run_kwargs)

    _server.uvicorn.run = run
    try:
        return _server.main(*args, **kwargs)
    finally:
        _server.uvicorn.run = original


if __name__ == "__main__":
    install_golden_runtime_bridge()
    _run_patched_app()
