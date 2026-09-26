# NABIL AI — AI Collaboration Mailbox

هذا الملف هو قناة المراجعة الرسمية بين:
- **الأستاذ نبيل عقيل** — صاحب المشروع وصاحب القرار النهائي.
- **ChatGPT** — المنفذ البرمجي الحصري: تعديل الكود، commits، الاختبارات، متابعة Railway وGoogle Drive.
- **Claude** — مستشار ومراجع تقني/علمي/تربوي.
- **Gemini** — مستشار ومراجع تقني/علمي/تربوي مستقل.

## قواعد العمل
1. لا يعدّل Claude أو Gemini الكود مباشرة ضمن هذا المسار؛ دورهما مراجعة واقتراح واعتراض.
2. ChatGPT هو المنفذ البرمجي، ولا يعتمد أي اقتراح قبل التحقق من أثره على المصدر، الـFail-Closed، الاختبارات، السرعة، والكلفة.
3. لا تُخفّف أي Quality Gate لمجرد تمرير درس.
4. لا تُختلق معلومة أو رسم أو تمرين أو جواب غير مثبت بالمصدر أو بالمنطق العلمي المطلوب.
5. لا يُعتبر أي متطلب من الـ105 منجزًا إلا مع:
   - STATUS = PASS
   - EVIDENCE
   - IMPLEMENTATION COMMIT
   - LIVE TEST
   - LIVE VERIFIED = YES
6. عند اختلاف Claude وGemini، يوثق الخلاف كما هو، ويصدر ChatGPT قرار التنفيذ مع السبب.
7. لا تُكتب مفاتيح API أو أسرار أو رموز OAuth في هذا الملف.

---

# القالب المعتمد لكل قضية

## ISSUE-XXX — <العنوان>
**الحالة:** OPEN / REVIEWING / IMPLEMENTED / LIVE-VERIFIED / CLOSED  
**الأولوية:** P0 / P1 / P2 / P3  
**المتطلبات المرتبطة:** 105 Matrix IDs  
**الملفات/الـcommits المعنية:**  
**المشكلة أو السؤال:**  

### Claude Review
- التحليل:
- المخاطر:
- الاعتراضات:
- البديل المقترح:
- هل يتطلب تعديل كود؟:

### Gemini Review
- التحليل:
- المخاطر:
- الاعتراضات:
- البديل المقترح:
- هل يتطلب تعديل كود؟:

### ChatGPT Decision
- القرار:
- سبب القرار:
- ما سيتم تنفيذه:
- ما لن يتم تنفيذه:

### Implementation Commit
- commit:
- الملفات المعدلة:
- الاختبارات المحلية/الوحدوية:

### Live Test Evidence
- Railway:
- Google Drive:
- الهاتف 390×844:
- المتصفح:
- المصدر/الكتاب:
- النتيجة:
- LIVE VERIFIED: NO

---

# ISSUE-001 — Golden Pilot: Solids and Liquids
**الحالة:** REVIEWING  
**الأولوية:** P0  
**المتطلبات المرتبطة:** مصنع الدروس، صحة المصدر، الرسومات، التمارين، السرعة، Drive، الاستئناف  
**المصدر:** G 07 physics.pdf  
**الدرس:** G07-PHYSICS-001 — Solids and Liquids  
**الصفحات:** PDF 13–18  
**المشكلة أو السؤال:**  
نريد أول درس كامل منشور فعليًا على Google Drive خلال زمن مستهدف لا يتجاوز 5 دقائق قدر الإمكان، مع الالتزام الكامل بالمصدر وعدم إسقاط أي شكل/تمرين مطلوب. يجب الاستفادة من checkpoints، Smart Failover، OCR المحلي، وحماية الكلفة.

### Claude Review
- بانتظار مراجعة Claude لأحدث البنية والنتيجة الحية للـPilot.

### Gemini Review
- Gemini وافق على دوره كمستشار مستقل صارم، وعلى عدم المجاملة أو تمرير ثغرات Fail-Closed أو تلفيق بيانات.
- المراجعة التفصيلية للـGolden Pilot مطلوبة بعد ظهور النسخة الحية أو أي Blocker جديد.

### ChatGPT Decision
- إبقاء Fail-Closed.
- عدم إعادة العمل المنجز عند توفر checkpoint صالح.
- Groq مزود أول، OpenRouter احتياط عند الحاجة؛ لا Race أعمى يضاعف الاستهلاك.
- حفظ حلول التمارين كـcheckpoints مستقلة.
- عدم اعتبار الدرس ناجحًا قبل نشر HTML فعلي وفحص محتواه على Drive.

### Implementation Commit
- commits الحالية ذات الصلة:
  - 1290ad7e9b4e302333a427f9d87d693dfbb05423 — targeted figure rescue
  - 3427c16398c310f2459afa1b21a0ed53ca707711 — bounded max_tokens
  - efc7a311b9385c15113a9e62264cfa680490f592 — temporary OpenRouter in-flight retry
  - 1eae486b2c98c9db110bb1e308156e956d25c7d5 — per-exercise solution checkpoints
  - 894dfa6a2bfd8dc3b0129733fa40037162993ab8 — solution checkpoint tests
  - adbe8f531b4e660de2aa94afdf8e08e9c85fa120 — keep solved cache out of evidence hashes

### Live Test Evidence
- آخر حالة مؤكدة قبل التشغيل الذاتي: الدرس غير منشور بعد.
- PAGE checkpoints موجودة للصفحات 13، 15، 16، 17، 18.
- الصفحة 14 كانت آخر عقدة في تغطية Fig.1.
- آخر Blocker موثق كان أثناء PRE_SOLVE للتمرين 7 بسبب provider cooldown / OpenRouter availability.
- LIVE VERIFIED: NO

---

# ISSUE-002 — Acceptance Matrix للـ105 متطلبات
**الحالة:** OPEN  
**الأولوية:** P0  
**المشكلة أو السؤال:**  
إنشاء مصفوفة واحدة نهائية تمنع نسيان أي مطلب، وتربط كل بند بالدليل والـcommit والاختبار الحي.

### Claude Review
- مطلوب: اقتراح بنية المصفوفة، وتجميع المتطلبات المتشابهة دون دمجها بطريقة تخفي أي بند مستقل.

### Gemini Review
- مطلوب: مراجعة مستقلة للبنية، مع التركيز على المتطلبات التربوية والعلمية والواجهة وتجربة الطالب.

### ChatGPT Decision
- المصفوفة ستستخدم الحقول التالية كحد أدنى:
  - ID
  - Requirement
  - Category
  - Acceptance Criteria
  - Status
  - Evidence
  - Commit
  - Live Test
  - Blocker
  - Next Action
  - Live Verified

### Implementation Commit
- pending

### Live Test Evidence
- LIVE VERIFIED: NO
