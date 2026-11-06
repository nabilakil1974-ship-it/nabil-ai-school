"""Lightweight standalone API for school timetable analysis."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
