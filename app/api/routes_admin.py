import os
import base64
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# تهيئة عميل Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/chat")
async def chat(
    message: str = Form(None),
    image: UploadFile = File(None)
):
    try:
        # تحديد النموذج المناسب حسب وجود صورة أو عدمه
        if image and image.filename:
            model_name = "llama-3.2-11b-vision-preview"
            image_bytes = await image.read()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": message if message else "اشرح هذه الصورة بالتفصيل لل curriculum اللبناني."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ]
        else:
            # استخدمنا النموذج الأقوى للنصوص مع شخصية أستاذ نبيل
            model_name = "llama-3.3-70b-versatile"
            messages = [
                {
                    "role": "system",
                    "content": "أنت أستاذ نبيل، مرشد تعليمي وخبير بالمنهج اللبناني. حافظ على ردود دقيقة، واضحة ومباشرة."
                },
                {
                    "role": "user", 
                    "content": message if message else "مرحباً"
                }
            ]

        # تم رفع max_tokens إلى 4000 لتفادي أي اقتطاع أو تفريغ للاستجابة بسبب وسوم التفكير
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=4000
        )
        
        reply = response.choices[0].message.content
        return {"reply": reply}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
