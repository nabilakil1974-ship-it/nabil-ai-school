/* NABIL AI shared lab voice helper — browser-cached, zero server TTS cost. */
(() => {
  "use strict";
  if (window.NABILLabVoice) return;
  let token = 0, timer = 0;
  function stop(){ token++; if(timer){clearTimeout(timer);timer=0;} try{window.NABILLessonE2E?.stopSpeech?.();}catch(_){} try{window.NABILBrowserTTS?.stop?.();}catch(_){} try{window.speechSynthesis?.cancel?.();}catch(_){} }
  function speak(text, lang, onDone){
    const mine = token;
    const finish = () => { if(mine === token && typeof onDone === "function") onDone(); };
    try{
      if(window.NABILLessonE2E?.speak){ Promise.resolve(window.NABILLessonE2E.speak(text,lang)).then(finish).catch(finish); return; }
      if(window.NABILBrowserTTS?.speak){ Promise.resolve(window.NABILBrowserTTS.speak(text,lang)).then(finish).catch(finish); return; }
    }catch(_){}
    const words=String(text||"").trim().split(/\s+/).filter(Boolean).length;
    timer=setTimeout(finish,Math.max(1700,words*390));
  }
  function play(cues, lang, point){
    stop(); const mine=token; let i=0; const rows=Array.isArray(cues)?cues:[];
    const next=()=>{ if(mine!==token||i>=rows.length)return; const cue=rows[i++]||{}; try{point?.(cue.target);}catch(_){} speak(cue.text||"",lang,next); };
    next();
  }
  window.NABILLabVoice={stop,speak,play};
})();
