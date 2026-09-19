/* NABIL open tutor v5 — the blue robot is the only landing page.
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
 '<div id="nabilOpenAnswer" aria-label="بطاقة جواب الأستاذ نبيل">'+
   '<div id="nabilOpenAnswerNav" class="nabil-open-answer-nav" hidden>'+
     '<button id="nabilOpenExplainBtn" type="button">📘 عرض الشرح</button>'+
     '<button id="nabilOpenVisualBtn" type="button" hidden>📐 عرض الرسمة</button>'+
   '</div>'+
   '<div id="nabilOpenLiveType" class="nabil-open-live-type" hidden aria-live="polite"></div>'+
   '<div id="nabilOpenExplanation" class="nabil-open-explanation"></div>'+
   '<div id="nabilOpenVisuals" class="nabil-open-visuals" hidden></div>'+
   '<div id="nabilOpenTools" class="nabil-open-tools"></div>'+
 '</div>'+
 '<div class="nabil-open-composer">'+
   '<textarea id="nabilOpenInput" rows="2" placeholder="اكتب سؤالك هنا… / Type your question… / Écris ta question…"></textarea>'+
   '<button id="nabilOpenTalk" type="button" title="سؤال صوتي">🎙️ سؤال صوتي</button>'+
   '<button id="nabilOpenSend" type="button">➤ إرسال</button>'+
 '</div>'+
 '<label class="nabil-open-pace" for="nabilOpenPace">🔊 سرعة الشرح <input id="nabilOpenPace" aria-label="سرعة صوت الأستاذ نبيل" type="range" min="0.70" max="1.15" step="0.05" value="0.90"><output id="nabilOpenPaceValue">0.90×</output></label>'+ 
 '<div id="nabilOpenStatus" role="status" aria-live="polite">جاهز لسؤالك.</div>';

let homeHost=el("nabilHomeTutorHost");
if(!homeHost){homeHost=document.createElement("div");homeHost.id="nabilHomeTutorHost";home.appendChild(homeHost);}
homeHost.replaceChildren(card);

const status=el("nabilOpenStatus"), board=el("nabilOpenAnswer"), convo=el("nabilOpenConversation"),
      input=el("nabilOpenInput"), talk=el("nabilOpenTalk"), send=el("nabilOpenSend"),
      nav=el("nabilOpenAnswerNav"), explainBtn=el("nabilOpenExplainBtn"), visualBtn=el("nabilOpenVisualBtn"),
      explanation=el("nabilOpenExplanation"), visuals=el("nabilOpenVisuals"), toolsHost=el("nabilOpenTools"), liveType=el("nabilOpenLiveType");
let recorder=null,stream=null,chunks=[],recording=false,busy=false,openConversationId="";
let greetingSpoken=false;
const pace=el("nabilOpenPace"),paceValue=el("nabilOpenPaceValue");
try{
 const saved=Number(localStorage.getItem("nabil_voice_pace"));
 if(Number.isFinite(saved)&&saved>=0.7&&saved<=1.15)pace.value=String(saved);
}catch(_e){}
function syncPace(){
 const v=Math.max(0.7,Math.min(1.15,Number(pace.value)||0.9));
 window.nabilVoicePace=v;
 paceValue.textContent=v.toFixed(2)+"×";
 try{if(typeof nabilNeuralAudio!=="undefined"&&nabilNeuralAudio)nabilNeuralAudio.playbackRate=v}catch(_e){}
 try{localStorage.setItem("nabil_voice_pace",String(v))}catch(_e){}
}
pace.addEventListener("input",syncPace);
syncPace();
function speakGreetingOnce(){
 if(greetingSpoken||home.style.display==="none")return;
 greetingSpoken=true;
 const greeting="أهلًا وسهلًا. أنا الأستاذ نبيل. اسألني كتابة أو صوت، وبشرحلك وبحل معك خطوة خطوة.";
 try{
   const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(greeting):greeting;
   if(typeof nabilSpeakClear==="function")Promise.resolve(nabilSpeakClear(spoken,"العربية",{})).catch(()=>{});
 }catch(_e){}
}

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
 const lang=detectLanguage(text);
 row.dir=lang==="العربية"?"rtl":"ltr";
 row.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
 const who=document.createElement("strong");
 who.textContent=role==="student"?(lang==="English"?"Student: ":lang==="Français"?"Élève : ":"الطالب: "):(lang==="English"?"NABIL: ":lang==="Français"?"NABIL : ":"الأستاذ نبيل: ");
 row.append(who,document.createTextNode(String(text)));
 convo.appendChild(row);
 convo.scrollTop=convo.scrollHeight;
}
function prepareSpeechTypewriter(text,lang){
 const words=String(text||"").replace(/\s+/g," ").trim().split(" ").filter(Boolean);
 let timer=0,index=0,duration=0,started=false;
 const dir=lang==="العربية"?"rtl":"ltr";
 liveType.dir=dir;liveType.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
 liveType.textContent="";liveType.hidden=!words.length;
 const interval=()=>duration>0?Math.max(55,Math.min(420,(duration*1000)/Math.max(words.length,1))):Math.max(75,Math.round(245/(Number(window.nabilVoicePace)||0.9)));
 const tick=()=>{
  if(index>=words.length){finish();return}
  liveType.textContent+=(index?" ":"")+words[index++];
  timer=window.setTimeout(tick,interval());
 };
 const start=()=>{if(started||!words.length)return;started=true;tick()};
 const finish=()=>{if(timer)clearTimeout(timer);timer=0;liveType.textContent=words.join(" ");window.setTimeout(()=>{liveType.hidden=true},700)};
 return {start,finish,setDuration:d=>{if(Number.isFinite(Number(d))&&Number(d)>0)duration=Number(d)}};
}

function renderAnswer(result,question){
 const reply=String(result?.reply||"").trim();
 const figureOnly=!reply&&Array.isArray(result?.drawings)&&result.drawings.length>0;
 if(!reply&&!figureOnly)throw Error("الخادم لم يرجع جوابًا صالحًا.");
 const lang=detectLanguage(question||result?.transcribed_text||reply);
 const dir=lang==="العربية"?"rtl":"ltr";
 board.dir=dir;
 board.lang=lang==='العربية'?'ar':lang==='English'?'en':'fr';
 board.classList.add("has-answer");
 explanation.replaceChildren();
 visuals.replaceChildren();
 toolsHost.replaceChildren();

 // Same academic renderer used by the lesson page. Keep text and drawings in
 // separate panes so the learner can switch between explanation and figure.
 let text=document.createElement("div");
 text.className="nabil-open-answer-text";
 text.dir=dir;
 text.lang=board.lang;
 try{
   if(typeof renderAIText==="function")text.innerHTML=renderAIText(reply);
   else text.innerHTML="<div>"+escapeHTML(reply).replace(/\n/g,"<br>")+"</div>";
 }catch(_e){text.innerHTML="<div>"+escapeHTML(reply).replace(/\n/g,"<br>")+"</div>"}
 if(!figureOnly)explanation.appendChild(text);

 const drawings=Array.isArray(result?.drawings)?result.drawings:[];
 drawings.forEach(d=>{
   try{
     if(typeof renderNabilDiagram!=="function")return;
     const html=renderNabilDiagram(d)||"";
     if(!html)return;
     const pane=document.createElement("div");
     pane.className="nabil-open-visual";
     pane.innerHTML=html;
     visuals.appendChild(pane);
   }catch(_e){}
 });
 const hasVisual=visuals.childElementCount>0;
 const wantsVisual=/draw|plot|graph|figure|diagram|sketch|tracer|dessiner|schéma|schema|ارسم|اعرض الرسم|اعرض الرسمة|ورجيني الرسمة|رسم بياني|مخطط/i.test(String(question||""));
 if(wantsVisual&&!hasVisual){
  const note=document.createElement("p");
  note.className="nabil-open-missing-visual";
  note.textContent=lang==="English"
   ?"No verified drawing was returned. Please provide the function or the figure's givens so I can draw it accurately."
   :lang==="Français"
    ?"Aucun dessin vérifié n’a été retourné. Précise la fonction ou les données de la figure pour la tracer correctement."
    :"ما وصل رسم دقيق لهالسؤال. اكتب الدالة أو معطيات الشكل حتى نرسمه بلا اختراع معلومات.";
  explanation.append(note);
 }
 nav.hidden=false;
 visualBtn.hidden=!hasVisual;
 explanation.hidden=figureOnly;
 visuals.hidden=!figureOnly;
 explainBtn.classList.toggle("active",!figureOnly);
 visualBtn.classList.toggle("active",figureOnly);
 explainBtn.hidden=figureOnly;
 explainBtn.textContent=lang==="English"?"📘 Show explanation":lang==="Français"?"📘 Afficher l’explication":"📘 عرض الشرح";
 visualBtn.textContent=lang==="English"?"📐 Show figure":lang==="Français"?"📐 Afficher le schéma":"📐 عرض الرسمة";

 const showPane=which=>{
   const showVisual=which==="visual"&&hasVisual;
   explanation.hidden=showVisual;
   visuals.hidden=!showVisual;
   explainBtn.classList.toggle("active",!showVisual);
   visualBtn.classList.toggle("active",showVisual);
   (showVisual?visuals:explanation).scrollIntoView({behavior:"smooth",block:"nearest"});
 };
 explainBtn.onclick=()=>showPane("explain");
 visualBtn.onclick=()=>showPane("visual");

 const copy=document.createElement("button");
 copy.type="button";copy.textContent="📋 نسخ الإجابة";
 copy.addEventListener("click",async()=>{
   try{await navigator.clipboard.writeText(reply);copy.textContent="✅ تم النسخ";setTimeout(()=>copy.textContent="📋 نسخ الإجابة",1400)}
   catch(_e){copy.textContent="تعذّر النسخ"}
 });
 const read=document.createElement("button");
 read.type="button";read.textContent=lang==="English"?"🔊 Read answer":lang==="Français"?"🔊 Lire la réponse":"🔊 اقرأ الإجابة";
 read.addEventListener("click",()=>{
   const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(reply):reply;
   Promise.resolve(nabilSpeakClear?.(spoken,lang,{})).catch(()=>{});
 });
 const stop=document.createElement("button");
 stop.type="button";stop.textContent=lang==="English"?"⏹ Stop voice":lang==="Français"?"⏹ Arrêter la voix":"⏹ أوقف الصوت";
 stop.addEventListener("click",()=>{try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}});
 if(!figureOnly)toolsHost.append(copy,read,stop);
 if(hasVisual){
   const preview=document.createElement("button");
   preview.type="button";
   preview.textContent=lang==="English"?"🔎 Enlarge figure":lang==="Français"?"🔎 Agrandir le schéma":"🔎 معاينة الرسمة كبيرة";
   preview.addEventListener("click",()=>{
     const modal=el("drawingPreviewModal"),content=el("drawingPreviewContent");
     if(!modal||!content){visualBtn.click();return}
     content.replaceChildren();
     const clone=visuals.cloneNode(true);
     clone.hidden=false;
     clone.removeAttribute("id");
     clone.querySelectorAll("[id]").forEach(n=>n.removeAttribute("id"));
     clone.classList.add("nabil-open-enlarged-visuals");
     content.appendChild(clone);
     modal.hidden=false;
     el("closeDrawingPreviewBtn")?.focus();
   });
   toolsHost.appendChild(preview);
 }
 try{window.MathJax?.typesetPromise?.([board])}catch(_e){}
 if(!figureOnly)addLine("nabil",reply);
 board.scrollIntoView({behavior:"smooth",block:"nearest"});
 return {reply,lang,hasVisual,figureOnly};
}
function getStudent(){
 try{return typeof getStudentId==="function"?getStudentId():(localStorage.getItem("nabil_student_id")||"nabil_open_student")}
 catch(_e){return "nabil_open_student"}
}
async function request({question="",audio=null}){
 if(busy)return;
 const command=String(question||"").trim();
 const isVisualCommand=/^(?:اعرض|ورجيني|فرجيني|اريني|بدي|show|display|affiche|montre).{0,35}(?:رسم|رسمة|الشكل|graph|figure|drawing|schéma|schema|courbe)/i.test(command);
 const isExplanationCommand=/^(?:اعرض|ورجيني|فرجيني|اريني|بدي|show|display|affiche|montre).{0,35}(?:شرح|حل|explanation|solution|explication)/i.test(command);
 if(!audio&&board.classList.contains("has-answer")&&isExplanationCommand){
   explainBtn.click();setStatus("📘 الشرح ظاهر ببطاقة الأستاذ نبيل.");return;
 }
 if(!audio&&board.classList.contains("has-answer")&&isVisualCommand&&!visualBtn.hidden){
   visualBtn.click();setStatus("📐 الرسمة ظاهرة ببطاقة الأستاذ نبيل.");return;
 }
 if(!audio&&!String(question).trim())return;
 setBusy(true);setStatus(audio?"🧠 عم بفهم التسجيل وبحضّر الجواب…":"🧠 عم بفهم سؤالك وبحضّر الجواب والرسم إذا لازم…");
 try{
   const data=new FormData();
   data.append("student_id",getStudent());
   data.append("activity_mode","general_exercises");
   data.append("teaching_mode","home_live_tutor");
   data.append("language","AUTO");
   if(openConversationId)data.append("conversation_id",openConversationId);
   if(audio){
     const mime=audio.type||"audio/webm",ext=/mp4|m4a/.test(mime)?"m4a":/ogg/.test(mime)?"ogg":"webm";
     data.append("audio",audio,"student_voice."+ext);
   }else{
     data.append("message",String(question).trim());
     addLine("student",String(question).trim());
   }
   const aborter=new AbortController();
   const timeout=setTimeout(()=>aborter.abort(),90000);
   let response;
   try{response=await fetch("/api/chat",{method:"POST",body:data,signal:aborter.signal})}
   finally{clearTimeout(timeout)}
   const result=await response.json().catch(()=>({detail:"الخادم لم يرجع JSON صالحًا"}));
   if(!response.ok)throw Error(String(result.detail||"تعذّر إرسال السؤال").slice(0,200));
   if(result.conversation_id)openConversationId=result.conversation_id;
   const heard=String(result.transcribed_text||question||"").trim();
   if(audio&&heard)addLine("student",heard);
   const shown=renderAnswer(result,heard);
   if(result.student_profile&&window.NABIL130?.mergeProfile)window.NABIL130.mergeProfile(result.student_profile);
   const spoken=typeof nabilBoardPlainSpeech==="function"?nabilBoardPlainSpeech(shown.reply):shown.reply;
   try{stopNabilNeuralVoice?.();speechSynthesis?.cancel?.()}catch(_e){}
   if(!shown.figureOnly&&spoken&&typeof nabilSpeakClear==="function"){
     const typer=prepareSpeechTypewriter(spoken,shown.lang);
     Promise.resolve(nabilSpeakClear(spoken,shown.lang,{
       onduration:d=>typer.setDuration(d),
       onstart:()=>typer.start(),
       onend:()=>typer.finish(),
       onerror:()=>typer.finish()
     })).catch(()=>typer.finish());
   }
   setStatus(shown.figureOnly?"✅ الرسمة ظاهرة. فيك تكبّرها بزر المعاينة.":shown.hasVisual?"✅ الجواب جاهز. فيك تعرض الشرح أو الرسمة من الأزرار فوق البطاقة.":"✅ الجواب جاهز لسؤالك التالي.");
 }catch(e){
   const aborted=e?.name==="AbortError";
   setStatus("⚠️ "+(aborted?"تأخر الجواب أكثر من المتوقع. جرّب إرسال السؤال مرة ثانية.":String(e?.message||"تعذّر الاتصال").slice(0,180)),true)
 }
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
talk.addEventListener("click",()=>{recording?stopRecording():startRecording()});
send.addEventListener("click",()=>{if(recording)return; // Keep one voice question at a time.
 const q=input.value.trim();if(!q)return;input.value="";request({question:q})});
input.addEventListener("input",()=>{
 const lang=detectLanguage(input.value);
 input.dir=lang==="العربية"?"rtl":"ltr";
 input.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
});
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
// Browsers normally block autoplay. Greet on the learner's first intentional interaction,
// using the exact same neural TTS function as the lesson page.
home.addEventListener("pointerdown",e=>{
 // Do not play greeting over microphone recording or while typing a question.
 if(e.target.closest("button,textarea,input,select,label"))return;
 speakGreetingOnce();
},{once:true,passive:true});
input.addEventListener("input",()=>{
 const lang=detectLanguage(input.value);
 input.dir=lang==="العربية"?"rtl":"ltr";
 input.lang=lang==="العربية"?"ar":lang==="English"?"en":"fr";
});
window.NabilOpenTutor={
 start:startRecording,stop:stopRecording,ask:q=>request({question:q}),
 showExplanation:()=>explainBtn.click(),
 showDrawing:()=>{if(!visualBtn.hidden)visualBtn.click();else setStatus("ما في رسمة مرتبطة بآخر جواب. اطلب رسمًا مع معطيات السؤال.",true)},
 setPace:n=>{pace.value=String(n);syncPace()}
};
})();
