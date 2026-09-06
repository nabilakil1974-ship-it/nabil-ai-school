from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="منصة الأستاذ نبيل التعليمية")

if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=FileResponse)
async def read_root():
    return "app/static/chat.html"

@app.post("/api/chat")
async def chat_api(message: str = Form(...), subject: str = Form(...), grade: str = Form(...)):
    # تنسيق الرد بأسطر متباعدة وواضحة جداً مطابقة لسلم التصحيح
    reply_text = (
        f"أهلاً بك يا بطل في منصة الأستاذ نبيل التعليمية!\n\n"
        f"📚 **المادة:** {subject}  |  **الصف:** {grade}\n"
        f"💬 **سؤالك:** {message}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 **خطوات الحل النموذجية (وفق سلم التصحيح الرسمي - CRDP):**\n\n"
        "1️⃣ **الخطوة الأولى:** تحديد المعطيات الأساسية وشروط المسألة بدقة متناهية واستخراج المتغيرات.\n\n"
        "2️⃣ **الخطوة الثانية:** كتابة القوانين الرياضية أو العلمية المعتمدة وتطبيقها خطوة بخطوة مع التعليل.\n\n"
        "3️⃣ **الخطوة الثالثة:** حساب الناتج النهائي وإبراز الإجابة بشكل نهائي ومنسق مع الوحدات الصحيحة.\n\n"
        "✨ *نصيحة الأستاذ نبيل:* يمكنك استخدام لوح الرسم التفاعلي في الأعلى لمراجعة المنحنيات والأشكال البيانية بدقة!"
    )
    
    return JSONResponse({
        "reply": reply_text,
        "subject": subject,
        "grade": grade
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
