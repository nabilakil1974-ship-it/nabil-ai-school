from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="منصة الأستاذ نبيل التعليمية")

# التأكد من تقديم الملفات الثابتة بشكل صحيح
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=FileResponse)
async def read_root():
    return "app/static/chat.html"

@app.post("/api/chat")
async def chat_api(message: str = Form(...), subject: str = Form(...), grade: str = Form(...)):
    # الرد الذكي المنسق وفق سلم التصحيح الرسمي للشهادات الرسمية في لبنان (CRDP)
    reply_text = (
        f"أهلاً بك يا بطل في منصة الأستاذ نبيل! بناءً على سؤالك في مادة ({subject}) للصف ({grade}):\n\n"
        f"📌 **السؤال المدخل:** {message}\n\n"
        "1️⃣ **الخطوة الأولى (المعطيات والشروط):** تحديد المعطيات الأساسية بدقة واستخراج المتغيرات المطلوبة.\n"
        "2️⃣ **الخطوة الثانية (القوانين المعتمدة):** تطبيق القوانين الرسمية للمنهج اللبناني خطوة بخطوة مع التعليل العلمي.\n"
        "3️⃣ **الخطوة الثالثة (النتيجة النهائية):** حساب الناتج النهائي بدقة مع الوحدات الصحيحة وفق سلم التصحيح الرسمي.\n\n"
        "💡 *تذكير:* يمكنك دائماً استخدام لوح الرسم التفاعلي أعلاه لتوضيح الأشكال الهندسية أو المنحنيات!"
    )
    
    return JSONResponse({
        "reply": reply_text,
        "subject": subject,
        "grade": grade
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
