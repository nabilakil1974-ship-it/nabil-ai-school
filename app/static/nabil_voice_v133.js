/* NABIL voice v133 — server transcription, same /api/chat tutor for spoken and typed input. */
(()=>{
"use strict";
const gateway=document.getElementById("nabilProfessorGateway");
if(!gateway)return;
const talk=gateway.querySelector("#nabilGatewayTalk");
const mic=gateway.querySelector("#nabilGatewayMic");
const status=gateway.querySelector("#nabilGatewayStatus");
const transcript=gateway.querySelector("#nabilGatewayTranscript");
const visualBox=gateway.querySelector("#nabilGatewayVisual");
const visualButton=gateway.querySelector("#nabilGatewayVisualBtn");
let recorder=null,stream=null,chunks=[],recording=false,busy=false;
const originalTalk=talk?.textContent||"🎙 تحدث معي الآن";
const setStatus=t=>{if(status)status.textContent=t};
function toggleUI(on){
 recording=on;
 gateway.classList.toggle("gateway-listening",on);
 if(talk)talk.textContent=on?"⏹ إيقاف وإرسال":originalTalk;
 if(mic)mic.textContent=on?"⏹":"🎙";
}
function line(role,text){
 if(!transcript||!text)return;
 const row=document.createElement("div");
 row.className="nabil-gateway-line "+role;
 row.style.whiteSpace="pre-wrap";
 const label=document.createElement("strong");
 label.textContent=role==="student"?"الطالب: ":"الأستاذ نبيل: ";
 row.append(label,document.createTextNode(String(text)));
 transcript.appendChild(row);transcript.scrollTop=transcript.scrollHeight;
 try{window.MathJax?.typesetPromise?.([row])}catch(_e){}
}
const field=(id)=>document.getElementById(id)?.value||"";
function ext(mime){return /ogg/i.test(mime)?"ogg":/mp4|m4a/i.test(mime)?"m4a":"webm"}
async function show(result){
 const text=String(result.reply||"").trim();
 if(!text)throw Error("Empty response from lesson engine");
 line("nabil",text);
 if(result.student_profile&&window.NABIL130?.mergeProfile)
   window.NABIL130.mergeProfile(result.student_profile);
 if(Array.isArray(result.drawings)&&result.drawings.length&&visualBox&&typeof window.renderNabilDiagram==="function"){
   const visuals=result.drawings.map(d=>{try{return window.renderNabilDiagram(d)||""}catch(_e){return""}}).join("");
   if(visuals){visualBox.innerHTML=visuals;visualBox.classList.add("open");visualButton?.classList.add("ready")}
 }
 let spoken=text;
 try{if(typeof window.nabilBoardPlainSpeech==="function")spoken=window.nabilBoardPlainSpeech(text)}catch(_e){}
 try{window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}
 if(typeof window.nabilSpeakClear==="function"){
   try{await window.nabilSpeakClear(spoken,"العربية",{onend:()=>{}})}catch(_e){}
 }
}
async function submit(blob){
 if(busy||!blob?.size)return;
 busy=true;setStatus("🧠 عم حوّل كلامك لسؤال وبحلّه من نفس محرّك الكتابة...");
 try{
   const body=new FormData();
   body.append("audio",blob,"student_voice."+ext(blob.type));
   body.append("student_id",typeof getStudentId==="function"?getStudentId():localStorage.getItem("nabil_student_id")||"student_voice");
   body.append("subject",field("subjectSelect"));
   body.append("grade",field("gradeSelect"));
   body.append("branch",field("branchSelect"));
   body.append("lesson",field("lessonSelect"));
   body.append("language",field("languageSelect")||"العربية");
   body.append("curriculum",field("curriculumSelect")||"المنهج اللبناني الرسمي");
   body.append("activity_mode",field("lessonSelect")?"lesson":"general_exercises");
   body.append("teaching_mode","interactive");
   if(typeof conversationId!=="undefined"&&conversationId)body.append("conversation_id",conversationId);
   const response=await fetch("/api/chat",{method:"POST",body});
   let result;
   try{result=await response.json()}catch(_e){throw Error("الخادم ما رجّع جوابًا مفهومًا")}
   if(!response.ok)throw Error(String(result.detail||"فشل إرسال التسجيل").slice(0,180));
   if(result.conversation_id&&typeof conversationId!=="undefined")conversationId=result.conversation_id;
   const heard=String(result.transcribed_text||"").trim();
   if(heard)line("student",heard);
   await show(result);
   setStatus(heard?"✅ سمعتك: «"+heard.slice(0,110)+"» · فيك تكمّل السؤال كتابة أو صوت.":"✅ جاوبتك؛ فيك تكمّل كتابة أو صوت.");
 }catch(e){setStatus("⚠️ "+String(e?.message||"تعذّر الاتصال").slice(0,160));console.error("NABIL voice v133",e)}
 finally{busy=false}
}
async function start(){
 if(busy||recording)return;
 if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){
   setStatus("الميكروفون غير مدعوم بهالمتصفح؛ اكتب سؤالك أو افتح الموقع عبر HTTPS.");return;
 }
 try{
   stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
   const format=["audio/webm;codecs=opus","audio/mp4","audio/ogg;codecs=opus"].find(t=>MediaRecorder.isTypeSupported?.(t));
   recorder=new MediaRecorder(stream,format?{mimeType:format}:undefined);
   chunks=[];
   recorder.ondataavailable=e=>{if(e.data?.size)chunks.push(e.data)};
   recorder.onstop=()=>{
     const blob=new Blob(chunks,{type:recorder?.mimeType||"audio/webm"});
     chunks=[];stream?.getTracks().forEach(t=>t.stop());stream=null;recorder=null;
     submit(blob);
   };
   try{window.stopNabilNeuralVoice?.();window.speechSynthesis?.cancel?.()}catch(_e){}
   recorder.start();toggleUI(true);
   setStatus("🎙 احكي سؤالك باللهجة اللبنانية أو English أو Français؛ بس تخلص اضغط إيقاف وإرسال.");
 }catch(e){stream?.getTracks().forEach(t=>t.stop());stream=null;toggleUI(false);setStatus("اسمح للميكروفون من إعدادات المتصفح وجرّب مرة ثانية.")}
}
function stop(){
 if(!recording||!recorder)return;
 toggleUI(false);setStatus("⏳ عم برسل التسجيل...");
 try{recorder.stop()}catch(_e){setStatus("تعذّر إنهاء التسجيل. جرّب من جديد.")}
}
// Document capture runs before the legacy gateway button listeners.
// Do not alter typed-input handlers; both modalities use /api/chat.
document.addEventListener("click",e=>{
 if(!gateway.contains(e.target))return;
 if(!(e.target.closest("#nabilGatewayTalk")||e.target.closest("#nabilGatewayMic")))return;
 e.preventDefault();e.stopImmediatePropagation();
 if(recording)stop();else start();
},true);
window.nabilVoiceV133={start,stop};
})();
