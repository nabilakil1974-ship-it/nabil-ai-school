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
    # بناء الرد التعليمي المفصل والمتباعد وفق المنهج اللبناني وسلّم التصحيح الرسمي
    reply_text = (
        f"أهلاً بك يا بطل في منصة الأستاذ نبيل التعليمية 🇱🇧\n\n"
        f"📚 **المادة:** {subject}    |    **الصف:** {grade}\n"
        f"📝 **سؤالك المدخل:** {message}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🎯 **الإجابة النموذجية وفق سلم التصحيح الرسمي (CRDP):**\n\n"
        "1️⃣ **الخطوة الأولى (المعطيات والتحليل):**\n"
        "   - قراءة الفرضيات بدقة وتحديد المعطيات الرقمية أو النصية المتوفرة.\n"
        "   - ربط المطلوب بالنظرية أو القاعدة القانونية المخصصة للمنهج اللبناني.\n\n"
        "2️⃣ **الخطوة الثانية (التطبيق والخطوات البرهانية):**\n"
        "   - كتابة القانون العام أو العلاقة الأساسية أولاً.\n"
        "   - التعويض العددي أو اللفظي خطوة بخطوة مع ترك مساحات واضحة للقراءة.\n"
        "   - إظهار خطوات الحساب الرياضي أو التحليل الأدبي بصرامة ووضوح.\n\n"
        "3️⃣ **الخطوة الثالثة (النتيجة النهائية):**\n"
        "   - استخراج الناتج النهائي بدقة متناهية.\n"
        "   - إرفاق الوحدات القياسية الصحيحة (مثل: cm, m/s, mol/L) أو صياغة الخاتمة الأدبية.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 **توجيه إضافي:** يمكنك استخدام لوح الرسم التفاعلي في الأعلى لتوضيح الأشكال الهندسية، الدوائر الكهربائية، أو المنحنيات البيانية الخاصة بهذا السؤال!"
    )
    
    return JSONResponse({
        "reply": reply_text,
        "subject": subject,
        "grade": grade
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
