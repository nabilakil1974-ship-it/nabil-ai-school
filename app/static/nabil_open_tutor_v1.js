/* NABIL open tutor v2 — the blue robot is the only landing page.
   Spoken and typed questions use the SAME /api/chat reasoning path, renderer and TTS.
   Open mode is intentionally independent from grade/subject/lesson selectors.
*/
(()=>{
"use strict";
const el=id=>document.getElementById(id);
const home=el("nabilHome"), main=document.querySelector(".lesson-main-column"), chat=el("chat");
if(!home||!main||!chat)return;

// Remove the obsolete separate gateway if legacy HTML created it before this script.
el("nabilProfessorGateway")?.remove();
const gatewayStyle=el("nabil-v105-startup-style");
if(gatewayStyle)gatewayStyle.disabled=true;

// The landing page never asks for a grade. Grade/subject/language/lesson remain
// available only after the learner explicitly enters the lesson page.
const stage=el("homeStage");
if(stage){stage.replaceChildren();stage.hidden=true;}

const card=document.createElement("section");
card.id="nabilOpenTutor";
card.setAttribute("aria-label","NABIL AI — open tutor");
card.innerHTML=
 '<div class="nabil-open-head">'+
   '<img class="nabil-open-mini-avatar" src="/static/nabil-lesson-avatar.png" alt="NABIL AI robot">'+
   '<div><h2>أهلًا! أنا الأستاذ نبيل 👋</h2>'+
   '<p>اسألني مباشرة كتابةً أو صوتًا. بفهم اللبناني، English وFrançais، وبجاوب بلغة السؤال.</p></div>'+
 '</div>'+
 '<div id="nabilOpenConversation" class="nabil-open-conversation" aria-live="polite">'+
   '<div class="nabil-open-welcome">جاهز نحل ونشرح ونرسم سوا — من دون اختيار صف أو مادة.</div>'+
 '</div>'+
 '<div id="nabilOpenAnswer" aria-label="بطاقة جواب الأستاذ نبيل"></div>'+
 '<div class="nabil-open-composer">'+
   '<textarea id="nabilOpenInput" rows="2" placeholder="اكتب سؤالك هنا… / Type your question… / Écris ta question…"></textarea>'+
   '<button id="nabilOpenTalk" type="button" title="سؤال صوتي">🎙️ سؤال صوتي</button>'+
   '<button id="nabilOpenSend" type="button">➤ إرسال</button>'+
 '</div>'+
 '<div id="nabilOpenStatus" role="status" aria-live="polite">جاهز لسؤالك.</div>';

let homeHost=el("nabilHomeTutorHost");
if(!homeHost){homeHost=document.createElement("div");homeHost.id="nabilHomeTutorHost";home.appendChild(homeHost);}
homeHost.replaceChildren(card);

const status=el("nabilOpenStatus"), board=el("nabilOpenAnswer"), convo=el("nabilOpenConversation"),
      input=el("nabilOpenInput"), talk=el("nabilOpenTalk"), send=el("nabilOpenSend");
let recorder=null,stream=null,chunks=[],recording=false,busy=false,openConversationId="";

const setStatus=(t,error=false)=>{status.textContent=t;status.classList.toggle("error",!!error)};
const setBusy=x=>{busy=x;send.disabled=x;talk.disabled=x&&!recording;card.classList.toggle("is-busy",x)};
const escapeHTML=t=>String(t??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

function detectLanguage(q){
 const t=String(q||"").trim();
 if(/[\u0600-\u06ff]/.test(t))return "العربية";
 if(/\b(bonjour|explique|étudie|etudie|fonction|dérivée|derivee|tracer|courbe|résoudre|resoudre|dessine|dessiner|calcule|montrer|démontrer|demontrer)\b/i.test(t))return "Français";
 if(/[a-z]/i.test(t))return "English";
 return "العربية";
}
function addLine(role,text){
 if(!text)return;
 const row=document.createElement("div");
 row.className="nabil-open-line "+role;
 const who=document.createElement("strong");
 who.textContent=role==="student"?"الطالب: ":"الأستاذ نبيل: ";
 row.append(who,document.createTextNode(String(text)));
 convo.appendChild(row);
 convo.scrollTop=convo.scrollHeight;
}
function renderAnswer(result,question){
 const reply=String(result?.reply||"").trim();
 if(!reply)throw Error("الخادم لم يرجع جوابًا صالحًا.");
 board.replaceChildren();

 const lang=detectLanguage(question||result?.transcribed_text||reply);
 const dir=lang==="العربية"?"rtl":"ltr";
 board.dir=dir;

 const drawingHTML=(Array.isArray(result?.drawings)?result.drawings:[]).map(d=>{
   try{return typeof renderNabilDiagram==="function"?(renderNabilDiagram(d)||""):""}catch(_e){return""}
 }).filter(Boolean);

 let rendered="";
 try{
   if(typeof renderGeneralExerciseBoards==="function"){
     rendered=renderGeneralExerciseBoards(reply,drawingHTML,dir,lang,question||"");
   }
 }catch(err){console.warn("NABIL open board renderer",err)}
 if(rendered){
   board.innerHTML=rendered;
 }else{
   const text=document.createElement("div");
   text.className="nabil-open-answer-text";
   if(typeof renderAIText==="function")text.innerHTML=renderAIText(reply);
   else text.innerHTML="<div>"+escapeHTML(reply).replace(/\n/g,"<br>")+"</div>";
   board.appendChild(text);
   drawingHTML.forEach(html=>{const pane=document.createElement("div");pane.className="nabil-open-visual";pane.innerHTML=html;board.appendChild(pane)});
 }

 const tools=document.createElement("div");
 tools.className="nabil-open-tools";
 const copy=document.createElement("button");copy.type="button";copy.textContent="📋 نسخ الإجابة";
 copy.addEventListener("click",async()=>{
   try{await navigator.clipboard.writeText(reply);copy.textContent="✅ تم النسخ";setTimeout(()=>copy.textContent="📋 نسخ الإجابة",1400)}
   catch(_e){copy.textContent="تعذّر النسخ"}
 });
 const read=document.createElement("button");read.type="button";read.textContent=lang==="English"?"🔊 Read answer":lang==="Français"?"🔊 Lire la réponse":"🔊 اقرأ الإجابة";
 read.addEventListener("click",()=>{const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(reply):reply;Promise.resolve(nabilSpeakClear?.(spoken,lang,{})).catch(()=>{})});
 tools.append(copy,read);board.appendChild(tools);
 try{window.MathJax?.typesetPromise?.([board])}catch(_e){}
 addLine("nabil",reply);
 board.scrollIntoView({behavior:"smooth",block:"nearest"});
 return {reply,lang};
}
function getStudent(){
 try{return typeof getStudentId==="function"?getStudentId():(localStorage.getItem("nabil_student_id")||"nabil_open_student")}
 catch(_e){return "nabil_open_student"}
}
async function request({question="",audio=null}){
 if(busy)return;
 if(!audio&&!String(question).trim())return;
 setBusy(true);setStatus(audio?"🧠 عم بفهم التسجيل وبحضّر الجواب…":"🧠 عم بفهم سؤالك وبحضّر الجواب والرسم إذا لازم…");
 try{
   const data=new FormData();
   data.append("student_id",getStudent());
   data.append("activity_mode","general_exercises");
   data.append("teaching_mode","interactive");
   data.append("language","AUTO");
   if(openConversationId)data.append("conversation_id",openConversationId);
   if(audio){
     const mime=audio.type||"audio/webm",ext=/mp4|m4a/.test(mime)?"m4a":/ogg/.test(mime)?"ogg":"webm";
     data.append("audio",audio,"student_voice."+ext);
   }else{
     data.append("message",String(question).trim());
     addLine("student",String(question).trim());
   }
   const response=await fetch("/api/chat",{method:"POST",body:data});
   const result=await response.json().catch(()=>({detail:"الخادم لم يرجع JSON صالحًا"}));
   if(!response.ok)throw Error(String(result.detail||"تعذّر إرسال السؤال").slice(0,200));
   if(result.conversation_id)openConversationId=result.conversation_id;
   const heard=String(result.transcribed_text||question||"").trim();
   if(audio&&heard)addLine("student",heard);
   const shown=renderAnswer(result,heard);
   if(result.student_profile&&window.NABIL130?.mergeProfile)window.NABIL130.mergeProfile(result.student_profile);
   const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(shown.reply):shown.reply;
   try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}
   if(typeof nabilSpeakClear==="function")Promise.resolve(nabilSpeakClear(spoken,shown.lang,{})).catch(()=>{});
   setStatus("✅ جاهز لسؤالك التالي.");
 }catch(e){setStatus("⚠️ "+String(e?.message||"تعذّر الاتصال").slice(0,180),true)}
 finally{setBusy(false);send.disabled=false;talk.disabled=false;if(!recording)talk.textContent="🎙️ سؤال صوتي"}
}
async function startRecording(){
 if(busy||recording)return;
 if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){setStatus("الميكروفون غير مدعوم؛ اكتب سؤالك أو افتح الموقع عبر HTTPS.",true);return}
 try{
   stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
   const mime=["audio/webm;codecs=opus","audio/mp4","audio/ogg;codecs=opus"].find(x=>MediaRecorder.isTypeSupported?.(x));
   recorder=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);chunks=[];
   recorder.ondataavailable=e=>{if(e.data?.size)chunks.push(e.data)};
   recorder.onstop=()=>{const blob=new Blob(chunks,{type:recorder?.mimeType||"audio/webm"});chunks=[];stream?.getTracks().forEach(t=>t.stop());stream=null;recorder=null;recording=false;request({audio:blob})};
   try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}
   recorder.start();recording=true;send.disabled=true;talk.textContent="⏹ إيقاف وإرسال";setStatus("🎙️ احكي براحتك، وبس تخلص اضغط إيقاف وإرسال.");
 }catch(_e){stream?.getTracks().forEach(t=>t.stop());stream=null;setStatus("اسمح للميكروفون من إعدادات المتصفح وجرّب مرة ثانية.",true)}
}
function stopRecording(){if(!recording||!recorder)return;talk.textContent="⏳ جارٍ الإرسال";setStatus("⏳ عم برسل التسجيل…");try{recorder.stop()}catch(_e){recording=false;setStatus("تعذّر إنهاء التسجيل.",true)}}
talk.addEventListener("click",()=>recording?stopRecording():startRecording());
send.addEventListener("click",()=>{if(recording)return; // Keep one voice question at a time.
 const q=input.value.trim();if(!q)return;input.value="";request({question:q})});
input.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send.click()}});

// Suppress the old home browser-SpeechRecognition handler; the landing microphone
// must always use server transcription exactly like the platform voice path.
document.addEventListener("click",e=>{
 const old=e.target.closest?.("#homeVoiceBtn");
 if(!old)return;
 e.preventDefault();e.stopImmediatePropagation();
 if(recording)stopRecording();else startRecording();
},true);

// Keep legacy red microphone as a large, accessible shortcut to the same recorder.
const legacyMic=el("homeVoiceBtn");
if(legacyMic){legacyMic.hidden=false;legacyMic.title="سؤال صوتي — نفس محرّك الأستاذ نبيل";legacyMic.querySelector("span:last-child")?.replaceChildren("سؤال صوتي")}

// The green button enters the actual lesson page. It does not show another grade splash.
document.addEventListener("click",e=>{
 if(!e.target.closest?.("#homeStartShortcut"))return;
 stage&&(stage.hidden=true);
 homeHost.style.display="none";
},true);

// If user returns Home from the lesson page, restore exactly this landing card.
window.nabilShowProfessorGateway=()=>{
 home.style.display="block";home.style.opacity="1";homeHost.style.display="block";stage&&(stage.hidden=true);
 document.body.classList.add("nabil-home-lock");
};
try{if(typeof nabilActivityMode!=="undefined")nabilActivityMode="general_exercises"}catch(_e){}
// Do not let the retired home script speak using a second browser-only voice.
try{if(typeof homeWelcomeSpoken!=="undefined")homeWelcomeSpoken=true}catch(_e){}
document.body.classList.add("nabil-home-lock");
window.NabilOpenTutor={start:startRecording,stop:stopRecording,ask:q=>request({question:q})};
})();
