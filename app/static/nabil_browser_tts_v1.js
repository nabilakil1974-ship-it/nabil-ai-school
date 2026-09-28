/* NABIL AI — Browser TTS Contract v1
 * Student-facing NABIL speech uses the browser SpeechSynthesis API only.
 * No paid/neural TTS endpoint is called from this contract.
 * Male voices are preferred when the browser/OS provides one; availability
 * depends on the device, so gender cannot be guaranteed on every device.
 */
(()=>{
"use strict";
if(window.NABILBrowserTTS?.version)return;

const MALE_HINTS={
 ar:["hamed","naayf","maged","tarik","male","ذكر"],
 en:["guy","david","mark","ryan","george","male"],
 fr:["henri","paul","claude","male"]
};
let token=0;

function codeOf(value){
 const v=String(value||"").toLowerCase();
 if(/fr|fran/.test(v))return "fr";
 if(/ar|عرب/.test(v))return "ar";
 return "en";
}
function localeOf(code){return code==="ar"?"ar-SA":code==="fr"?"fr-FR":"en-US"}
function voices(){try{return window.speechSynthesis?.getVoices?.()||[]}catch(_e){return []}}
function voiceFor(code){
 const scoped=voices().filter(v=>String(v.lang||"").toLowerCase().startsWith(code));
 const hints=MALE_HINTS[code]||[];
 return scoped.find(v=>hints.some(h=>String(v.name||"").toLowerCase().includes(h)))
     ||scoped.find(v=>v.localService)||scoped[0]||null;
}
async function waitVoices(){
 if(voices().length)return;
 await new Promise(resolve=>{
  let done=false;
  const finish=()=>{if(done)return;done=true;resolve()};
  try{speechSynthesis.addEventListener("voiceschanged",finish,{once:true})}catch(_e){}
  setTimeout(finish,650);
 });
}
function splitMixed(text,base){
 const raw=String(text||"").trim();
 if(base!=="ar")return raw?[{text:raw,code:base}]:[];
 const parts=raw.split(/([A-Za-z][A-Za-z0-9_.+-]*(?:\s+[A-Za-z][A-Za-z0-9_.+-]*)*)/g).filter(Boolean);
 return parts.map(part=>({text:part,code:/[A-Za-z]/.test(part)&&!/[\u0600-\u06FF]/.test(part)?"en":"ar"})).filter(x=>x.text.trim());
}
function stop(){
 token++;
 try{window.speechSynthesis?.cancel?.()}catch(_e){}
}
async function speak(text,language,options={}){
 const raw=String(text||"").trim();
 if(!raw)return;
 const synth=window.speechSynthesis;
 if(!synth||!window.SpeechSynthesisUtterance){
  options.onerror?.(new Error("SPEECH_SYNTHESIS_UNAVAILABLE"));
  return;
 }
 stop();
 const mine=token;
 await waitVoices();
 if(mine!==token)return;
 const base=codeOf(language);
 const segments=splitMixed(raw,base);
 const words=raw.split(/\s+/).filter(Boolean).length;
 const estimated=Math.max(900,Math.round(words*360/Math.max(.72,Math.min(1.12,Number(window.nabilVoicePace||.9)))));
 try{options.onduration?.(estimated)}catch(_e){}
 return await new Promise(resolve=>{
  let i=0,started=false;
  const next=()=>{
   if(mine!==token){resolve();return}
   if(i>=segments.length){
    try{options.onend?.()}catch(_e){}
    resolve();return;
   }
   const seg=segments[i++];
   const u=new SpeechSynthesisUtterance(seg.text);
   u.lang=localeOf(seg.code);
   u.voice=voiceFor(seg.code);
   u.rate=Math.max(.72,Math.min(1.12,Number(window.nabilVoicePace||.9)));
   u.pitch=.94;
   u.onstart=()=>{if(!started){started=true;try{options.onstart?.()}catch(_e){}}};
   u.onboundary=e=>{try{options.onboundary?.(e)}catch(_e){}};
   u.onend=next;
   u.onerror=event=>{
    if(mine!==token){resolve();return}
    try{options.onsegmenterror?.(event)}catch(_e){}
    next();
   };
   synth.speak(u);
  };
  next();
 });
}

window.NABILBrowserTTS={
 version:"1.0.1",
 engine:"SpeechSynthesis",
 paidEndpoint:false,
 maleVoicePreferred:true,
 maleVoiceGuaranteed:false,
 speak,stop,voiceFor,codeOf
};
window.nabilSpeakClear=(spoken,language,options={})=>speak(spoken,language,options);
window.stopNabilNeuralVoice=stop;

// Keep teacher-lab stop events synchronized with browser speech.
// Speaking itself remains owned by the verified teacher_script renderer.
document.addEventListener("nabil:teacher-stopped",stop);
document.addEventListener("nabil:teach-stop",stop);
})();
