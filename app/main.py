from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
import os

app = FastAPI(title="منصة الأستاذ نبيل التعليمية")

@app.get("/", response_class=FileResponse)
async def read_root():
    return "app/static/chat.html"

@app.post("/api/chat")
async def chat_api(message: str = Form(...), subject: str = Form(...), grade: str = Form(...)):
    reply = f"Hello! Request received for subject: {subject}, grade: {grade}. The system is working perfectly!"
    return JSONResponse({"reply": reply})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
