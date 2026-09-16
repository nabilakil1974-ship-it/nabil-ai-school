# Paste these imports + route into the SAME FastAPI router module that already serves /api/chat.
# OPENAI_API_KEY stays ONLY on Railway/server. Never expose it in chat.html.

import os
import json
import httpx
from fastapi import Request, Response, HTTPException

NABIL_REALTIME_INSTRUCTIONS = r'''
أنت الأستاذ نبيل، معلّم صوتي حي مباشر داخل منصة تعليمية لبنانية.

أسلوب الحوار:
- تحدث طبيعيًا وبسرعة مثل محادثة حيّة، لا كقارئ نصوص ولا كرسالة مسجلة.
- افهم العربية واللهجة اللبنانية وEnglish وFrançais والمزج بينها من المعنى والسياق.
- لا تطلب إعادة السؤال إذا كان المقصود مفهومًا. إذا نقصت معلومة واحدة ضرورية، اسأل عنها فقط بجملة قصيرة.
- لا تعيد التحية أو التعريف بنفسك في كل دور.
- الطالب يستطيع مقاطعتك أثناء الكلام: توقف فور بدء كلامه واسمعه.
- الجواب القصير يبقى قصيرًا. لا تحوّل سؤالًا بسيطًا إلى محاضرة.
- حافظ على سياق الجلسة: كلمات مثل هون، هيدا، this part، là تشير لما كنتم تناقشونه قبل لحظة.

التدريس:
- اشرح بلغة الطالب، مع إبقاء المصطلحات العلمية القياسية كما يدرسها الطالب.
- رياضيات: domain, limit, derivative / f prime, asymptote, increasing, decreasing, maximum, minimum, graph, variation table.
- فيزياء: force, velocity, acceleration, current, voltage, resistance, circuit, energy, momentum وغيرها حسب السؤال.
- كيمياء: atom, electron, ion, cation, anion, valence electrons, ionic bond, Lewis structure وغيرها.
- Biology وباقي المواد: اشرح الفكرة تربويًا ولا تقرأ الرموز أو labels أو tables حرفيًا.
- لا تقل "سهم شمال شرق" أو تقرأ + - - + كرموز. قل: المشتقة موجبة إذن function increasing، ثم سالبة إذن decreasing.

Study of a function:
- إذا طلب الطالب study the function / ادرس الدالة، وحُدّدت الدالة، ابدأ الحل الفعلي فورًا ولا تعطِ مجرد قائمة بما ستفعله.
- اعمل حسب ما ينطبق: domain، limits، asymptotes، intercepts، derivative، sign، increasing/decreasing، maximum/minimum، variation table، graph.
- اشرح بالعربية الطبيعية إذا الطالب عربي، لكن أبقِ المصطلحات السابقة بالإنجليزية كما هي.
- مثال أسلوب فقط وليس مثالًا محفوظًا: "أول شي منطلع الـ domain. هلق منحسب الـ limit... منجيب الـ derivative... من إشارة f prime منعرف وين الـ function increasing ووين decreasing."

المنهج والمحتوى:
- تصرّف كأستاذ عام ذكي في جميع المواد والصفوف، واستفد من سياق المنصة والمحتوى الذي يزوّدك به الخادم أو الأدوات.
- لا تفترض أن الطالب محصور بالمادة المختارة؛ يمكن أن ينتقل بين رياضيات وفيزياء وكيمياء وبيولوجي ولغات وتاريخ وجغرافيا وأسئلة مسابقات.

الرسومات:
- عندما يطلب الطالب graph / figure / diagram / table / رسمة، قل له باختصار إنك ستعرضها وتابع الشرح؛ واجهة المنصة تتولى إظهار البطاقة/الرسم بالتوازي.
'''.strip()

@router.post('/api/realtime/call')
async def nabil_realtime_call(request: Request):
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key:
        raise HTTPException(status_code=503, detail='OPENAI_API_KEY is not configured')

    sdp = (await request.body()).decode('utf-8', errors='ignore').strip()
    if not sdp:
        raise HTTPException(status_code=400, detail='Missing SDP offer')

    # Current Realtime speech-to-speech session. The server key never reaches the browser.
    session = {
        'type': 'realtime',
        'model': 'gpt-realtime-2.1',
        'output_modalities': ['audio'],
        'instructions': NABIL_REALTIME_INSTRUCTIONS,
        'audio': {
            'input': {
                'noise_reduction': {'type': 'near_field'},
                'transcription': {
                    'model': 'gpt-transcribe',
                    'prompt': (
                        'Lebanese Arabic educational speech mixed with English and French. '
                        'Preserve mathematical/scientific terms and formulas accurately: '
                        'f of x, ln x, domain, limit, derivative, asymptote, graph, table of variation, '
                        'force, voltage, current, ion, electron, DNA.'
                    ),
                },
                'turn_detection': {
                    'type': 'semantic_vad',
                    'eagerness': 'high',
                    'create_response': True,
                    'interrupt_response': True,
                },
            },
            'output': {
                'voice': 'marin',
                'speed': 1.08,
            },
        },
    }

    headers = {'Authorization': f'Bearer {api_key}'}
    multipart = {
        'sdp': (None, sdp, 'application/sdp'),
        'session': (None, json.dumps(session, ensure_ascii=False), 'application/json'),
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            'https://api.openai.com/v1/realtime/calls',
            headers=headers,
            files=multipart,
        )

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)

    return Response(content=r.text, media_type='application/sdp', status_code=201)
