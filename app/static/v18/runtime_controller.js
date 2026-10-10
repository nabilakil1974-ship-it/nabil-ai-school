(function(global){
'use strict';
const S=()=>global.NabilP3LabStandardV12?.STANDARD;
class TeacherPlaybackController{
constructor(opts={}){
const std=S(); const langCode=opts.langCode||'en';
const lang=global.NabilP3LabStandardV12?.getLanguage(langCode)||{speech:'en-US'};
this.onStep=opts.onStep||(()=>{});this.onState=opts.onState||(()=>{});
this.langCode=langCode;this.lang=opts.lang||lang.speech||'en-US';
this.rate=opts.rate??std?.teacher?.speech?.rate??0.72;
this.pitch=opts.pitch??std?.teacher?.speech?.pitch??1;
this.volume=opts.volume??std?.teacher?.speech?.volume??1;
this.lineMs=opts.lineMs??std?.teacher?.typewriter?.line_ms??65;
this.titleMs=opts.titleMs??std?.teacher?.typewriter?.title_ms??90;
this.textMs=opts.textMs??std?.teacher?.typewriter?.text_ms??34;
this.pauseAfterLine=opts.pauseAfterLine??std?.teacher?.typewriter?.pause_after_line_ms??420;
this.pauseAfterStep=opts.pauseAfterStep??std?.teacher?.typewriter?.pause_after_step_ms??1200;
this.token=0;this.timer=null;this.playing=false;this.voiceEnabled=opts.voiceEnabled!==false;
}
setLanguage(code){this.langCode=code||'en';const lang=global.NabilP3LabStandardV12?.getLanguage(this.langCode);if(lang?.speech)this.lang=lang.speech;this.onState({language:this.langCode,lang:this.lang});}
setVoiceEnabled(v){this.voiceEnabled=!!v;if(!this.voiceEnabled)this.cancelSpeech();this.onState({voiceEnabled:this.voiceEnabled});}
cancelSpeech(){try{if(global.speechSynthesis)global.speechSynthesis.cancel();}catch(e){}}
stop(){this.playing=false;this.token++;if(this.timer)clearTimeout(this.timer);this.timer=null;this.cancelSpeech();this.onState({playing:false});}
speak(text,lang){
if(!this.voiceEnabled||!text||!global.speechSynthesis||!global.SpeechSynthesisUtterance)return Promise.resolve();
this.cancelSpeech();
return new Promise(resolve=>{
try{const u=new global.SpeechSynthesisUtterance(String(text));u.lang=lang||this.lang;u.rate=this.rate;u.pitch=this.pitch;u.volume=this.volume;u.onend=resolve;u.onerror=resolve;global.speechSynthesis.speak(u);}catch(e){resolve();}
});
}
async typeText(text,onChar,speed){
const mine=this.token;const s=String(text||'');
for(let i=0;i<=s.length;i++){if(mine!==this.token||!this.playing)return false;onChar?.(s.slice(0,i));await new Promise(r=>this.timer=setTimeout(r,speed));}
return true;
}
async runTeacherStep(step,index){
this.onStep(index,step);this.onState({playing:true,index,event:'STEP_START'});
if(step.title){await this.typeText(step.title,v=>this.onState({event:'WRITE_TITLE',index,value:v}),step.titleMs||this.titleMs);}
const lines=step.lines?.length?step.lines:[step.formula||step.text].filter(Boolean);
const voices=step.voices||[];
for(let i=0;i<lines.length;i++){
const ok=await this.typeText(lines[i],v=>this.onState({event:'WRITE_LINE',index,line:i,value:v}),step.lineMs||this.lineMs);
if(!ok)return false;
await new Promise(r=>this.timer=setTimeout(r,this.pauseAfterLine));
await this.speak(voices[i]||step.speech||step.text,step.lang||this.lang);
if(!this.playing)return false;
this.onState({event:'LINE_DONE',index,line:i});
}
if(step.visualEvent)this.onState({event:'ANIMATE',index,visualEvent:step.visualEvent});
if(step.lockResult!==undefined)this.onState({event:'LOCK_RESULT',index,result:step.lockResult});
await new Promise(r=>this.timer=setTimeout(r,step.pauseAfterMs||this.pauseAfterStep));
return true;
}
async play(steps,startIndex=0){
this.stop();this.playing=true;this.token++;this.onState({playing:true,index:startIndex});
for(let i=startIndex;i<steps.length;i++){if(!this.playing)return;const ok=await this.runTeacherStep(steps[i],i);if(!ok)return;}
this.playing=false;this.onState({playing:false,finished:true});
}
}
const api={TeacherPlaybackController};if(typeof module!=='undefined'&&module.exports)module.exports=api;global.NabilRuntime=api;
})(typeof window!=='undefined'?window:globalThis);
