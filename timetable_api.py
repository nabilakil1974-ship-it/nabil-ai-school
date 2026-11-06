"""Lightweight standalone API for school timetable analysis."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
from app.api import routes_timetable

app = FastAPI(title="NABIL School Timetable Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes_timetable.router, prefix="/api")

@app.api_route("/", methods=["GET", "HEAD"], include_in_schema=False)
def school_app():
    index = Path(__file__).parent / "timetable" / "index.html"
    if not index.is_file():
        return {"error": "NABIL school interface is not installed"}
    return FileResponse(index, media_type="text/html; charset=utf-8")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NABIL timetable analyzer", "nabil_engine_configured": bool(os.getenv("NABIL_EXECUTIVE_API_URL") and os.getenv("NABIL_EXECUTIVE_API_KEY"))}

# Serve the school-facing web app from the same public Render URL.
# Keep this mount last so it cannot shadow the /api routes above.
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "timetable"), html=True), name="school-timetable")
