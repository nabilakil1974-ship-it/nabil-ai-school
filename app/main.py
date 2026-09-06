from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
import os

app = FastAPI(title="منصة الأستاذ نبيل التعليمية")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>الأستاذ نبيل - المنصة التعليمية</title>
        <style>
            body { background-color: #1b262c; color: white; font-family: Tahoma; text-align: center; padding-top: 50px; }
            h1 { color: #bbe1fa; }
        </style>
    </head>
    <body>
        <h1>أهلاً بك في منصة الأستاذ نبيل الذكية للمنهج اللبناني 🇱🇧</h1>
        <p>السيرفر يعمل الآن بنجاح تام!</p>
    </body>
    </html>
    """
    return html_content

@app.post("/api/chat")
async def chat_api(message: str = Form(...), subject: str = Form(...)):
    reply = f"أهلاً بك يا بطل! لقد تلقيت سؤالك في مادة ({subject}):\n\n1. الخطوة الأولى: تحليل المعطيات بدقة حسب المنهج اللبناني.\n2. الخطوة الثانية: التطبيق القانوني والبرهنة خطوة بخطوة.\n3. النتيجة النهائية: الإجابة صحيحة ومفصلة تماماً مثل سلم التصحيح الرسمي."
    return JSONResponse({"reply": reply})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
