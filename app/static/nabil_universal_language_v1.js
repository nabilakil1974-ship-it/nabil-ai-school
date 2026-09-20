/* NABIL universal student language preference — one selector for every activity. */
(()=>{"use strict";if(window.nabilGlobalLanguageReady)return;window.nabilGlobalLanguageReady=true;
const KEY="nabil.student.explanation.language.v1";
const choices=[["auto","🌐 وفق لغة السؤال / الكتاب"],["en","🇬🇧 English only"],["fr","🇫🇷 Français uniquement"],["ar","🇱🇧 العربية"]];
const norm=s=>/fran|français|french/i.test(s)?"fr":/english|انجليزي|إنجليزي/i.test(s)?"en":/عرب|arabic/i.test(s)?"ar":"auto";
const languageValue={en:"English",fr:"Français",ar:"العربية"};
function get(){let saved="auto";try{saved=localStorage.getItem(KEY)||"auto"}catch(_){}return choices.some(x=>x[0]===saved)?saved:"auto";}
function selectNative(lang){
 const el=document.getElementById("languageSelect");if(!el||lang==="auto")return;
 const options=[...el.options];const found=options.find(x=>norm(x.value)===lang)||options.find(x=>norm(x.textContent)===lang);
 if(found&&el.value!==found.value){el.value=found.value;el.dispatchEvent(new Event("change",{bubbles:true}));}
}
function mount(){
 if(document.getElementById("nabilUniversalLanguage"))return;
 const native=document.getElementById("languageSelect");if(!native)return;
 const box=document.createElement("label");box.id="nabilUniversalLanguage";
 box.style.cssText="display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:10px;margin:10px 0;max-width:100%;background:#12324b;color:#fff;border:1px solid #38bdf8;border-radius:12px;font:14px Arial,sans-serif;box-sizing:border-box";
 const label=document.createElement("span");label.textContent="🗣️ لغة شرح الأستاذ نبيل:";
 const input=document.createElement("select");input.id="nabilUniversalLanguageChoice";
 input.style.cssText="min-width:160px;max-width:100%;padding:8px;border-radius:8px;color:#102a43;background:#fff";
 choices.forEach(([value,name])=>{const opt=document.createElement("option");opt.value=value;opt.textContent=name;input.appendChild(opt)});
 input.value=get();input.onchange=()=>{try{localStorage.setItem(KEY,input.value)}catch(_){}selectNative(input.value)};
 box.append(label,input);
 const parent=native.closest("label")||native.parentElement;parent?.insertAdjacentElement("afterend",box);
 selectNative(get());
 native.addEventListener("change",()=>{const mode=get();if(mode!=="auto"&&norm(native.value)!==mode){input.value="auto";try{localStorage.setItem(KEY,"auto")}catch(_){}}});
}
const originalFetch=window.fetch.bind(window);
window.fetch=(input,options)=>{
 const url=typeof input==="string"?input:(input?.url||"");
 const body=options?.body;
 if(/\\/?api\\/chat(?:\\?|$)/.test(url)&&body instanceof FormData){
   const mode=get();if(mode!=="auto"){body.set("language",languageValue[mode]);body.set("nabil_explanation_language",mode)}
 }
 return originalFetch(input,options);
};
window.nabilExplanationLanguage=()=>get();
const observer=new MutationObserver(mount);observer.observe(document.documentElement,{childList:true,subtree:true});mount();
})();