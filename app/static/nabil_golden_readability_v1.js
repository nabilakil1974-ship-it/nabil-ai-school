/* NABIL Golden Readability v1 — structured, calm classroom typography for every Golden lesson. */
(()=>{"use strict";
if(window.NABILGoldenReadabilityInstalled)return;window.NABILGoldenReadabilityInstalled=true;
const css=`
:root{--nabil-reading-width:820px}
.card{padding:clamp(18px,4vw,34px)!important}
.card>h2{margin:8px auto 28px!important;max-width:var(--nabil-reading-width);line-height:1.35!important}
.line,.turn,.lab,.reference-visual,.golden-block{max-width:var(--nabil-reading-width);margin-left:auto!important;margin-right:auto!important}
.line{display:block;margin-top:0!important;margin-bottom:22px!important;font-size:clamp(18px,3.7vw,22px)!important;line-height:2!important;letter-spacing:.01em;white-space:pre-wrap;overflow-wrap:break-word!important}
.turn{margin-top:28px!important;margin-bottom:30px!important;padding:18px 20px!important}
.turn b{display:block;margin-bottom:13px;font-size:clamp(18px,3.8vw,22px);line-height:1.5}
.turn p{margin:0!important;font-size:clamp(18px,3.7vw,22px)!important;line-height:2!important;white-space:pre-wrap;overflow-wrap:break-word!important}
.turn.nabil{margin-top:34px!important;margin-bottom:34px!important;background:#061e32!important}
.turn.nabil b{color:#73e9ff!important}
.nabil-formula{direction:ltr!important;text-align:center!important;unicode-bidi:isolate!important;display:block;max-width:720px;margin:26px auto!important;padding:17px 18px;border:1px solid #315d79;border-radius:12px;background:#03111d;font-family:"Cambria Math","STIX Two Math",serif;font-size:clamp(21px,4.5vw,30px)!important;line-height:1.55!important;overflow-wrap:anywhere}
.nabil-section-gap{height:10px}
.student{margin-top:34px!important;margin-bottom:34px!important}
.check{margin-top:28px!important;margin-bottom:28px!important}
nav{margin-top:32px!important;padding-top:18px!important;border-top:1px solid #194663}
@media(max-width:600px){main{padding:10px!important}.card{padding:18px 14px!important}.card>h2{padding-right:48px!important;margin-bottom:24px!important}.line,.turn p{font-size:19px!important;line-height:1.95!important}.turn{padding:16px!important}.nabil-formula{font-size:23px!important;margin:24px 0!important;padding:16px 10px}.count{font-size:12px}}
`;
const style=document.createElement("style");style.id="nabilGoldenReadabilityStyle";style.textContent=css;document.head.appendChild(style);
const formulaLike=s=>{const t=String(s||"").trim();if(!t||t.length>180)return false;if(/[=≤≥<>±∞√∫∑∆Δ]/.test(t))return true;if(/^(?:f|g|h|y|x|D[fF]?|lim)\s*\(/i.test(t))return true;if(/^(?:domain|range)\s*[:=]/i.test(t))return true;return false;};
function splitDenseParagraph(p){if(!p||p.dataset.nabilReadable)return;p.dataset.nabilReadable="1";const text=(p.textContent||"").trim();if(!text)return;if(formulaLike(text)){p.classList.add("nabil-formula");return;}if(text.length<150)return;const parts=text.split(/(?<=[.!؟?])\s+(?=[^\s])/).map(x=>x.trim()).filter(Boolean);if(parts.length<2)return;p.textContent="";parts.forEach((part,i)=>{const span=document.createElement("span");span.style.display="block";span.style.marginBottom=i===parts.length-1?"0":"14px";span.textContent=part;p.appendChild(span);});}
function enhance(root=document){root.querySelectorAll?.(".line,.turn p,.golden-block p").forEach(splitDenseParagraph);root.querySelectorAll?.(".line").forEach(p=>{if(formulaLike(p.textContent))p.classList.add("nabil-formula")});}
function boot(){enhance();const mo=new MutationObserver(ms=>ms.forEach(m=>m.addedNodes.forEach(n=>{if(n.nodeType===1)enhance(n)})));mo.observe(document.body,{childList:true,subtree:true});}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",boot,{once:true});else boot();
})();
