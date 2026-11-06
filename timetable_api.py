"""Lightweight standalone API for school timetable analysis."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api import routes_timetable

app = FastAPI(title="NABIL School Timetable Analyzer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes_timetable.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "NABIL timetable analyzer"}

# Serve the school-facing web app from the same public Render URL.
# Keep this mount last so it cannot shadow the /api routes above.
app.mount("/", StaticFiles(directory=str(Path(__file__).parent / "timetable"), html=True), name="school-timetable")
