/* Main-page open tutor: one /api/chat engine and one lesson TTS voice.
   Grade, subject and lesson fields deliberately omitted in open question mode.
*/
(()=>{
"use strict";
const el=id=>document.getElementById(id);
const card=document.createElement("section");
card.id="nabilOpenTutor";
card.setAttribute("aria-label","الأستاذ نبيل — سؤال مفتوح");
card.innerHTML='<h2>👋 أهلًا! أنا الأستاذ نبيل</h2>'+
 '<p>اسألني كتابةً أو صوتًا باللهجة اللبنانية، English أو Français. ما في داعي تختار صفًا أو مادة لتسألني.</p>'+
 '<div class="nabil-open-actions"><button id="nabilOpenTalk" type="button">🎙️ سؤال صوتي</button>'+
 '<button id="nabilOpenFocus" type="button">✍️ اكتب سؤالك</button></div>'+
 '<div id="nabilOpenStatus" role="status" aria-live="polite">جاهز نحل سوا، خطوة بخطوة.</div>'+
 '<div id="nabilOpenAnswer" aria-label="بطاقة جواب الأستاذ نبيل"></div>';
const main=document.querySelector(".lesson-main-column");
const chat=el("chat");
if(!main||!chat)return;
main.insertBefore(card,chat);
const button=el("nabilOpenTalk"),status=el("nabilOpenStatus"),board=el("nabilOpenAnswer");
let recorder=null,stream=null,chunks=[],busy=false,recording=false;
const update=(message,error=false)=>{status.textContent=message;status.classList.toggle("error",error)};
const questionLanguage=q=>{
 const t=String(q||"").trim();
 if(/[\u0600-\u06ff]/.test(t))return "العربية";
 if(/\b(bonjour|explique|étudie|etudie|fonction|dérivée|derivee|tracer|tracé|courbe|résoudre|resoudre|dessine|dessiner)\b/i.test(t))return "Français";
 if(/[a-z]/i.test(t))return "English";
 return el("languageSelect")?.value||"العربية";
};
function showReply(result,spokenQuestion){
 const reply=String(result?.reply||"").trim();
 if(!reply)throw Error("ما وصل جواب صالح من الخادم.");
 if(result.conversation_id&&typeof conversationId!=="undefined")conversationId=result.conversation_id;
 if(result.student_profile&&window.NABIL130?.mergeProfile)window.NABIL130.mergeProfile(result.student_profile);
 const heard=String(result.transcribed_text||spokenQuestion||"").trim();
 if(heard&&typeof addMessage==="function")addMessage("student",heard);
 if(typeof addMessage==="function")addMessage("teacher",reply,result.sources||[]);
 board.replaceChildren();
 const text=document.createElement("div");
 text.className="nabil-open-answer-text";
 if(typeof renderAIText==="function")text.innerHTML=renderAIText(reply);
 else text.textContent=reply;
 board.appendChild(text);
 if(Array.isArray(result.drawings)&&typeof renderNabilDiagram==="function"){
  for(const drawing of result.drawings){
   try{
    const visual=renderNabilDiagram(drawing);
    if(!visual)continue;
    const pane=document.createElement("div");
    pane.className="nabil-open-visual";
    pane.innerHTML=visual;board.appendChild(pane);
   }catch(err){console.warn("Unsupported or invalid drawing",err)}
  }
 }
 try{window.MathJax?.typesetPromise?.([board])}catch(_){}
 board.scrollIntoView({behavior:"smooth",block:"nearest"});
 const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(reply):reply;
 const lang=questionLanguage(heard);
 if(typeof nabilSpeakClear==="function"){
  Promise.resolve(nabilSpeakClear(spoken,lang,{})).catch(()=>{});
 }
 update("✅ جاهز لسؤالك التالي، صوتيًا أو كتابيًا.");
}
function freeMode(){
 // Selecting a lesson explicitly still returns to normal lesson mode.
 if(typeof nabilActivityMode!=="undefined")nabilActivityMode="general_exercises";
}
el("nabilOpenFocus")?.addEventListener("click",()=>{
 freeMode();
 const input=el("messageInput");
 input?.focus();input?.scrollIntoView({behavior:"smooth",block:"center"});
});
function closeStream(){if(stream){stream.getTracks().forEach(t=>t.stop());stream=null}}
function stop(){
 if(!recorder||!recording)return;
 recording=false;button.textContent="⏳ جارٍ الإرسال";
 try{recorder.stop()}catch(e){busy=false;closeStream();update("تعذّر إنهاء التسجيل؛ حاول مجددًا.",true)}
}
async function submit(blob){
 if(!blob?.size){busy=false;button.textContent="🎙️ سؤال صوتي";update("ما وصل صوت. جرّب تسجيل السؤال مرة تانية.",true);return}
 update("🧠 عم بفهم سؤالك وبحضّر الحل والرسم إذا لازم...");
 try{
  const data=new FormData();
  const mime=blob.type||"audio/webm";
  const ext=/mp4|m4a/.test(mime)?"m4a":/ogg/.test(mime)?"ogg":"webm";
  data.append("audio",blob,"question."+ext);
  data.append("student_id",typeof getStudentId==="function"?getStudentId():localStorage.getItem("nabil_student_id")||"nabil_voice");
  data.append("activity_mode","general_exercises");
  data.append("teaching_mode","interactive");
  // NO grade/subject/lesson: topic and reply language inferred from utterance.
  data.append("language","Auto");
  if(typeof conversationId!=="undefined"&&conversationId)data.append("conversation_id",conversationId);
  const response=await fetch("/api/chat",{method:"POST",body:data});
  const result=await response.json().catch(()=>({detail:"الخادم لم يرجع JSON صالحًا"}));
  if(!response.ok)throw Error(String(result.detail||"تعذّر إرسال السؤال"));
  freeMode();
  showReply(result,"");
 }catch(e){update("⚠️ "+String(e?.message||"تعذّر الاتصال").slice(0,180),true)}
 finally{busy=false;button.textContent="🎙️ سؤال صوتي";}
}
async function start(){
 if(busy||recording)return;
 if(!navigator.mediaDevices?.getUserMedia||!window.MediaRecorder){update("الميكروفون غير مدعوم؛ اكتب سؤالك أو استخدم HTTPS.",true);return}
 busy=true;
 try{
  stream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:true,noiseSuppression:true,autoGainControl:true}});
  const mime=["audio/webm;codecs=opus","audio/mp4","audio/ogg;codecs=opus"].find(x=>MediaRecorder.isTypeSupported(x));
  recorder=new MediaRecorder(stream,mime?{mimeType:mime}:undefined);
  chunks=[];
  recorder.ondataavailable=e=>{if(e.data?.size)chunks.push(e.data)};
  recorder.onerror=()=>{recording=false;busy=false;closeStream();button.textContent="🎙️ سؤال صوتي";update("توقف التسجيل بسبب خطأ؛ حاول مجددًا.",true)};
  recorder.onstop=()=>{
   const audio=new Blob(chunks,{type:recorder.mimeType||"audio/webm"});
   chunks=[];closeStream();recorder=null;submit(audio);
  };
  try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_){}
  recorder.start();recording=true;
  button.textContent="⏹ إيقاف وإرسال";
  update("🎙️ احكي السؤال براحتك، واضغط إيقاف وإرسال وقت تخلص.");
 }catch(e){busy=false;closeStream();button.textContent="🎙️ سؤال صوتي";update("اسمح للميكروفون من المتصفح وجرب مجددًا.",true)}
}
button.addEventListener("click",()=>recording?stop():start());
// The former browser SpeechRecognition only handles the UI language.
// Reuse the same server transcription and TTS for the lesson-page microphone.
document.addEventListener("click",event=>{
 const mic=event.target.closest?.("#micBtn");
 if(!mic)return;
 event.preventDefault();event.stopImmediatePropagation();
 if(recording)stop();else start();
},true);
window.NabilOpenTutor={start,stop,freeMode};
})();
