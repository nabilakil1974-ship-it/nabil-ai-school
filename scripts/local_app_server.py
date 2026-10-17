"""Run the real platform app locally for browser tests (port 8765).
Only Google client libraries are stubbed (not installed in the sandbox); every route, page and script is the real one."""
import os, sys, types
from unittest import mock
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

class _Dummy(types.ModuleType):
    def __getattr__(self, k):
        if k.startswith("__"):
            raise AttributeError(k)
        return mock.MagicMock()

for m in ["googleapiclient", "googleapiclient.discovery", "googleapiclient.http", "googleapiclient.errors", "google",
          "google.oauth2", "google.oauth2.service_account", "google.oauth2.credentials", "google.auth",
          "google.auth.transport", "google.auth.transport.requests"]:
    sys.modules.setdefault(m, _Dummy(m))
import uvicorn
from app.main import app
uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", "8765")), log_level="warning")
