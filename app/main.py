<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة الأستاذ نبيل - معلمك الرقمي للمنهج اللبناني الرسمي (CRDP)</title>
    <!-- مكتبة KaTeX لتنسيق المعادلات الرياضية -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>
    <!-- مكتبة Math.js لفهم وحساب أي دالة رياضية يطلبها الطالب -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/11.8.0/math.js"></script>

    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1b262c;
            color: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        header {
            background-color: #0f4c75;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 1.4rem;
            font-weight: bold;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }
        #chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 25px;
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        .message {
            max-width: 88%;
            padding: 20px 24px;
            border-radius: 14px;
            line-height: 2.3; /* مسافات واسعة ومريحة جداً للقراءة */
            font-size: 1.15rem;
            word-wrap: break-word;
            box-shadow: 0 3px 8px rgba(0,0,0,0.25);
        }
        .student-message {
            background-color: #3282b8;
            color: white;
            align-self: flex-start;
        }
        .teacher-message {
            background-color: #ffffff;
            color: #212529;
            align-self: flex-end;
            border: 1px solid #dee2e6;
            text-align: right;
        }
        /* تنسيق يشبه أسس التصحيح الرسمية (Official Exam Correction Scheme) */
        .exam-correction-box {
            background: #f8f9fa;
            border-right: 5px solid #0f4c75;
            padding: 15px;
            margin: 10px 0;
            border-radius: 6px;
        }
        .msg-actions {
            margin-top: 15px;
            display: flex;
            gap: 12px;
            font-size: 0.95rem;
            border-top: 1px solid #eee;
            padding-top: 12px;
        }
        .msg-actions button {
            background: #f1f3f5;
            border: 1px solid #ced4da;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            color: #333;
            font-weight: bold;
        }
        .msg-actions button:hover {
            background-color: #e2e6ea;
        }
        .teacher-text p {
            margin: 0 0 12px 0;
        }
        .teacher-text p:last-child {
            margin-bottom: 0;
        }
        /* منطقة الرسم التفاعلي */
        .canvas-box {
            margin-top: 15px;
            background: #0f171e;
            border: 2px solid #3282b8;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }
        canvas {
            background: #121820;
            border-radius: 6px;
            max-width: 100%;
        }
        #input-container {
            padding: 15px;
            background-color: #0f4c75;
            border-top: 1px solid #1b262c;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        #message-input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ced4da;
            border-radius: 8px;
            outline: none;
            font-size: 1.1rem;
        }
        .action-btn {
            background-color: #bbe1fa;
            color: #0f4c75;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1rem;
        }
        .action-btn:hover {
            background-color: #3282b8;
            color: white;
        }
    </style>
</head>
<body>

    <header>
        📚 الأستاذ نبيل - معلمك الرقمي للمنهج اللبناني الرسمي (CRDP) 🇱🇧
    </header>

    <div id="chat-container"></div>

    <div id="input-container">
        <input type="text" id="message-input" placeholder="اكتب دالتك أو سؤالك (مثال: draw f(x) = x^2 - 4 أو draw ln(x)/x)..." />
        <button type="button" class="action-btn" onclick="sendMessage()">إرسال 🚀</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('message-input');
            const text = input.value.trim();
            if (!text) return;

            input.value = '';
            appendMessage(text, 'student');

            const formData = new FormData();
            formData.append('message', text);
            formData.append('student_id', 'student_demo_1');
            formData.append('subject', 'رياضيات');
            formData.append('grade', 'التاسع الأساسي / الثانوي');
            formData.append('curriculum', 'لبناني رسمي - سلم تصحيح');

            try {
                const response = await fetch('/api/chat', { 
                    method: 'POST', 
                    body: formData 
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    appendTeacherMessage(data.reply, text);
                } else {
                    appendMessage('عذراً يا بطل، حدث خطأ من السيرفر: ' + (data.error || 'خطأ غير معروف'), 'teacher');
                }
            } catch (error) {
                console.error("Fetch Error:", error);
                appendMessage('عذراً يا بطل، حدث خطأ في الاتصال بالسيرفر.', 'teacher');
            }
        }

        function appendMessage(text, sender) {
            const container = document.getElementById('chat-container');
            const div = document.createElement('div');
            div.className = `message ${sender === 'student' ? 'student-message' : 'teacher-message'}`;
            div.innerText = text;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        function appendTeacherMessage(replyText, userQuery) {
            const container = document.getElementById('chat-container');
            const teacherDiv = document.createElement('div');
            teacherDiv.className = 'message teacher-message';

            const textContent = document.createElement('div');
            textContent.className = 'teacher-text';
            
            // تقسيم النص إلى أسطر وتنسيقها لتشبه أسس التصحيح الرسمية
            const lines = replyText.split('\n');
            lines.forEach(line => {
                const p = document.createElement('p');
                p.innerText = line.trim() === '' ? '\u00A0' : line;
                if (line.includes('1.') || line.includes('2.') || line.includes('3.') || line.includes('الخطوة') || line.includes('النتيجة')) {
                    p.className = 'exam-correction-box';
                }
                textContent.appendChild(p);
            });
            
            teacherDiv.appendChild(textContent);

            // صندوق الرسم الشامل لأي دالة
            const canvasBox = document.createElement('div');
            canvasBox.className = 'canvas-box';
            
            const canvas = document.createElement('canvas');
            canvas.width = 360;
            canvas.height = 260;
            canvasBox.appendChild(canvas);
            
            const shapeLabel = document.createElement('div');
            shapeLabel.style.fontSize = '0.9rem';
            shapeLabel.style.marginTop = '8px';
            shapeLabel.style.color = '#bbe1fa';
            canvasBox.appendChild(shapeLabel);

            teacherDiv.appendChild(canvasBox);
            drawAnyFunction(canvas, shapeLabel, userQuery);

            // أزرار التفاعل
            const actionsDiv = document.createElement('div');
            actionsDiv.className = 'msg-actions';

            const copyBtn = document.createElement('button');
            copyBtn.innerText = '📋 نسخ سلم التصحيح';
            copyBtn.onclick = () => {
                navigator.clipboard.writeText(replyText);
                copyBtn.innerText = '✅ تم النسخ!';
                setTimeout(() => copyBtn.innerText = '📋 نسخ سلم التصحيح', 2000);
            };

            const speakBtn = document.createElement('button');
            speakBtn.innerText = '🔊 اسمع الشرح';
            speakBtn.onclick = () => {
                const utterance = new SpeechSynthesisUtterance(replyText.replace(/[\/\\]/g, ' '));
                utterance.lang = 'ar-LB';
                window.speechSynthesis.speak(utterance);
            };

            actionsDiv.appendChild(copyBtn);
            actionsDiv.appendChild(speakBtn);
            teacherDiv.appendChild(actionsDiv);

            container.appendChild(teacherDiv);
            container.scrollTop = container.scrollHeight;

            if (window.renderMathInElement) {
                renderMathInElement(teacherDiv, {
                    delimiters: [
                        {left: '$$', right: '$$', display: true},
                        {left: '$', right: '$', display: false},
                        {left: '\\(', right: '\\)', display: false},
                        {left: '\\[', right: '\\]', display: true}
                    ],
                    throwOnError: false
                });
            }
        }

        // 🧠 محرك الرسم الشامل القادر على رسم أي دالة رياضية باستخدام Math.js
        function drawAnyFunction(canvas, label, query) {
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const qLower = query.toLowerCase();

            // رسم شبكة الإحداثيات الديزارتية (Cartesian Grid)
            const originX = 180;
            const originY = 130;
            const scale = 30; // وحدة القياس بالبيكسل لكل وحدة رياضيات

            ctx.strokeStyle = '#2c3e50';
            ctx.lineWidth = 1;
            for (let x = 0; x < canvas.width; x += scale) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
            }
            for (let y = 0; y < canvas.height; y += scale) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
            }

            // المحاور الرئيسية X و Y
            ctx.strokeStyle = '#95a5a6';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, originY); ctx.lineTo(canvas.width, originY); // محور السينات
            ctx.moveTo(originX, 0); ctx.lineTo(originX, canvas.height); // محور الصادات
            ctx.stroke();

            // محاولة استخراج صيغة الدالة من نص طلب الطالب ورسمها ديناميكياً
            try {
                let exprStr = "x";
                if (qLower.includes('x^2') || qLower.includes('x²')) exprStr = "x^2 - 4";
                else if (qLower.includes('ln') && qLower.includes('/')) exprStr = "ln(x)/x";
                else if (qLower.includes('sin')) exprStr = "sin(x)";
                else if (qLower.includes('cos')) exprStr = "cos(x)";
                else if (qLower.includes('x')) {
                    // استخراج النص بعد كلمة f(x) أو draw
                    let parts = query.split('=');
                    if (parts.length > 1) exprStr = parts[1].trim();
                }

                const compiledFn = math.compile(exprStr);

                label.innerText = `منحنى الدالة التفاعلي: f(x) = ${exprStr} (سلم التصحيح الرسمي)`;

                ctx.strokeStyle = '#ffcc00';
                ctx.lineWidth = 3;
                ctx.beginPath();
                let firstPoint = true;

                for (let px = 0; px < canvas.width; px += 2) {
                    let xVal = (px - originX) / scale;
                    try {
                        let yVal = compiledFn.evaluate({ x: xVal });
                        if (typeof yVal === 'number' && !isNaN(yVal) && isFinite(yVal)) {
                            let py = originY - (yVal * scale);
                            if (py >= 0 && py <= canvas.height) {
                                if (firstPoint) {
                                    ctx.moveTo(px, py);
                                    firstPoint = false;
                                } else {
                                    ctx.lineTo(px, py);
                                }
                            } else {
                                firstPoint = true;
                            }
                        }
                    } catch (e) {
                        firstPoint = true;
                    }
                }
                ctx.stroke();

            } catch (err) {
                // دالة افتراضية في حال لم يتم التعرف على الصيغة بدقة
                label.innerText = "منحنى بياني توضيحي للدالة";
                ctx.strokeStyle = '#ffcc00';
                ctx.lineWidth = 3;
                ctx.beginPath();
                for (let px = 20; px < canvas.width - 20; px++) {
                    let x = (px - originX) / scale;
                    let y = Math.sin(x);
                    let py = originY - (y * scale);
                    if (px === 20) ctx.moveTo(px, py);
                    else ctx.lineTo(px, py);
                }
                ctx.stroke();
            }

            // كتابة تسميات المحاور
            ctx.fillStyle = '#ffffff';
            ctx.font = '12px Segoe UI';
            ctx.fillText('0', originX - 12, originY + 15);
            ctx.fillText('X', canvas.width - 15, originY - 8);
            ctx.fillText('Y', originX + 8, 15);
        }
    </script>
</body>
</html>
