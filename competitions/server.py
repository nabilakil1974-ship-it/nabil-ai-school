from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

from competitions.routes import router

ROOT = Path(__file__).resolve().parent

app = FastAPI(title="NABIL AI Competition Generator")
app.include_router(router, prefix="/api")

@app.get("/", include_in_schema=False)
def competition_home():
    return FileResponse(ROOT / "index.html", media_type="text/html",
                        headers={"Cache-Control": "no-store"})

@app.get("/health", include_in_schema=False)
def health():
    return {"ok": True, "service": "nabil-competitions"}
