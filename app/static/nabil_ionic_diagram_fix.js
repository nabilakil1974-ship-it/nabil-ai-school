/* Source-aware ionic visual safety patch. Loaded after the legacy visual engine.
   Electron counts and ionic ratios are calculated, never requested from a model.
   Two arrows are valid for MgCl2 (2 e-), ONE arrow for NaCl (1 e-).
*/
(()=>{
"use strict";
const ELEMENTS={
 Li:{shells:[2,1],charge:1,metal:true},Na:{shells:[2,8,1],charge:1,metal:true},
 Mg:{shells:[2,8,2],charge:2,metal:true},Ca:{shells:[2,8,8,2],charge:2,metal:true},
 Cl:{shells:[2,8,7],charge:1,metal:false},F:{shells:[2,7],charge:1,metal:false},
 O:{shells:[2,6],charge:2,metal:false},S:{shells:[2,8,6],charge:2,metal:false}
};
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const sum=a=>a.reduce((x,y)=>x+y,0);
const gcd=(a,b)=>b?gcd(b,a%b):a;
function ionicLesson(){
 const subject=String(document.getElementById("subjectSelect")?.value||"");
 const lesson=String(document.getElementById("lessonSelect")?.value||"");
 const open=typeof generalExercisesMode!=="undefined"&&generalExercisesMode;
 return !open && /كيمياء|chemistry|chimie/i.test(subject)
   && /ionic|ionique|أيون/i.test(lesson);
}
function atom(x,y,symbol,shells,transferred=0){
 let out="";
 shells.forEach((n,i)=>{
  const radius=19+i*20;
  out+=`<circle cx="${x}" cy="${y}" r="${radius}" fill="none" stroke="#38bdf8" stroke-width="1.8"/>`;
  for(let k=0;k<n;k++){
   const angle=(-Math.PI/2)+(2*Math.PI*k)/n;
   const px=x+radius*Math.cos(angle),py=y+radius*Math.sin(angle);
   const gained=i===shells.length-1 && k>=n-transferred && transferred>0;
   out+=`<circle cx="${px.toFixed(2)}" cy="${py.toFixed(2)}" r="3.6" fill="${gained?"#ff7070":"#b8f6ff"}"/>`;
  }
 });
 out+=`<circle cx="${x}" cy="${y}" r="15" fill="#8b5cf6" stroke="#f5d0fe" stroke-width="1.5"/>
 <text x="${x}" y="${y+5}" text-anchor="middle" fill="#fff" font-size="16" font-weight="800">${esc(symbol)}</text>`;
 return out;
}
function doublets(x,y,symbol,charge,gained=0){
 let s=`<text x="${x}" y="${y+10}" text-anchor="middle" fill="#fff" font-size="39" font-weight="800">${esc(symbol)}</text>`;
 const pts=[[-8,-40],[8,-40],[-8,42],[8,42],[-46,-6],[-46,10],[46,-6],[46,10]];
 if(gained>0)pts.slice(0,8).forEach(([dx,dy],i)=>{
  s+=`<circle cx="${x+dx}" cy="${y+dy}" r="4" fill="${i>=8-gained?"#ff7070":"#8deaff"}"/>`;
 });
 s+=`<path d="M${x-60} ${y-50} h-9 v100 h9 M${x+60} ${y-50} h9 v100 h-9" fill="none" stroke="#e7f7ff" stroke-width="2.7"/>
 <text x="${x+77}" y="${y-42}" fill="#f8fafc" font-size="22" font-weight="700">${esc(charge)}</text>`;
 return s;
}
function renderIonic(spec){
 const metal=String(spec?.chemistry?.cation?.symbol||spec?.labels?.metal||"").trim();
 const nonmetal=String(spec?.chemistry?.anion?.symbol||spec?.labels?.nonmetal||"").trim();
 const m=ELEMENTS[metal],a=ELEMENTS[nonmetal];
 if(!m?.metal||a?.metal!==false)return "";
 const loss=m.charge,gain=a.charge,g=gcd(loss,gain),mc=gain/g,ac=loss/g;
 // Avoid pretending this generic figure is the exact figure scanned from a book.
 const formula=metal+(mc>1?mc:"")+nonmetal+(ac>1?ac:"");
 const beforeM=m.shells, beforeA=a.shells;
 const afterM=beforeM.slice(), afterA=beforeA.slice();
 afterM[afterM.length-1]-=loss;if(afterM.at(-1)===0)afterM.pop();
 afterA[afterA.length-1]+=gain;
 const W=1120,H=715;let svg=`<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Electron transfer and Lewis dot pairs for ${esc(formula)}" style="display:block;width:100%;height:auto;background:#081d32">
 <defs><marker id="nabilIonElectronArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10Z" fill="#ffdc5c"/></marker></defs>
 <rect x="9" y="9" width="1102" height="697" rx="20" fill="#081d32" stroke="#39baff" stroke-width="2"/>
 <text x="560" y="51" text-anchor="middle" fill="#7be6ff" font-size="27" font-weight="800">Ionic bonding: ${esc(formula)}</text>
 <text x="560" y="79" text-anchor="middle" fill="#d5eefb" font-size="16">Electron transfer • Bohr shells • Lewis doublets</text>
 <rect x="28" y="103" width="1064" height="362" rx="17" fill="#0b2b44" stroke="#2e8ab6"/>
 <text x="300" y="140" text-anchor="middle" fill="#fff" font-size="22" font-weight="800">Before transfer</text>
 <text x="839" y="140" text-anchor="middle" fill="#fff" font-size="22" font-weight="800">After transfer</text>`;
 const before=[],after=[];
 const ys=n=>n===1?[292]:n===2?[215,366]:Array.from({length:n},(_,i)=>190+i*(205/(n-1)));
 for(let i=0;i<mc;i++){before.push({x:155,y:ys(mc)[i],s:metal,arr:beforeM});after.push({x:685,y:ys(mc)[i],s:metal+"⁺".repeat(loss),arr:afterM});}
 for(let i=0;i<ac;i++){before.push({x:390,y:ys(ac)[i],s:nonmetal,arr:beforeA});after.push({x:915,y:ys(ac)[i],s:nonmetal+"⁻".repeat(gain),arr:afterA});}
 before.forEach(v=>{svg+=atom(v.x,v.y,v.s.replace(/[⁺⁻]/g,""),v.arr);svg+=`<text x="${v.x}" y="${v.y+92}" text-anchor="middle" fill="#fff" font-size="15">${v.arr.join(", ")}</text>`;});
 after.forEach((v,i)=>{svg+=atom(v.x,v.y,v.s.replace(/[⁺⁻]/g,""),v.arr,i>=mc?gain:0);svg+=`<text x="${v.x}" y="${v.y+92}" text-anchor="middle" fill="#fff" font-size="15">${esc(v.s)}: ${v.arr.join(", ")}</text>`;});
 // Transfer arrows from each donor's electron to each acceptor's vacancy.
 // MgCl2: upper and lower arrows. NaCl: one arrow, never invent a second e-.
 for(let k=0;k<mc*loss;k++){
  const di=Math.floor(k/loss),ai=Math.floor(k/gain);
  const donor=before[di],receiver=before[mc+ai], top=(k%2===0);
  const sy=donor.y+(top?-38:38),ey=receiver.y+(top?-38:38);
  const controlY=top?Math.min(sy,ey)-67:Math.max(sy,ey)+67;
  svg+=`<path d="M${donor.x+43} ${sy} Q270 ${controlY} ${receiver.x-47} ${ey}" stroke="#ffdc5c" fill="none" stroke-width="3.2" marker-end="url(#nabilIonElectronArrow)"/>
  <text x="274" y="${controlY+(top?-5:20)}" text-anchor="middle" fill="#ffdc5c" font-size="18">e⁻</text>`;
 }
 svg+=`<rect x="28" y="483" width="1064" height="212" rx="17" fill="#0b2b44" stroke="#2e8ab6"/>
 <text x="560" y="520" text-anchor="middle" fill="#7be6ff" font-size="22" font-weight="800">Lewis representation — pairs (doublets)</text>`;
 const items=[];for(let i=0;i<mc;i++)items.push({symbol:metal,charge:loss===1?"+":loss+"+",an:false});
 for(let i=0;i<ac;i++)items.push({symbol:nonmetal,charge:gain===1?"−":gain+"−",an:true});
 const gap=920/(items.length+1);
 items.forEach((item,i)=>{
  const x=100+gap*(i+1);
  if(item.an)svg+=doublets(x,595,item.symbol,item.charge,gain);
  else svg+=`<text x="${x}" y="605" text-anchor="middle" fill="#fff" font-size="39" font-weight="800">[${esc(item.symbol)}]</text><text x="${x+46}" y="563" fill="#fff" font-size="23">${esc(item.charge)}</text>`;
 });
 svg+=`<text x="560" y="678" text-anchor="middle" fill="#d5eefb" font-size="16">Each ${esc(nonmetal)} ion has four electron pairs (8 outer-shell electrons).</text></svg>`;
 return `<div class="nabil-visual nabil-ionic-verified" style="width:100%;max-width:100%;overflow:auto;background:#081d32;border:1px solid #2e8ab6;border-radius:15px">
 <div class="nabil-visual-title" style="color:#7be6ff">Ionic bond — ${esc(formula)}</div>${svg}</div>`;
}
function install(){
 const old=window.renderNabilDiagram;
 if(typeof old!=="function"||old.__ionicScientificFix)return false;
 const wrapped=function(spec){
  const t=String(spec?.type||"").toLowerCase();
  if(ionicLesson()&&/^(function|coordinate_plane|orthonormal_plane|graph)$/.test(t)){
   console.warn("NABIL_IONIC_REJECT_UNRELATED_FUNCTION_GRAPH",t);
   return "";
  }
  if(["ionic_bond","electron_transfer","ion_formation","lewis_structure"].includes(t)){
   const scientific=renderIonic(spec);
   if(scientific)return scientific;
  }
  return old.apply(this,arguments);
 };
 wrapped.__ionicScientificFix=true;
 window.renderNabilDiagram=wrapped;
 return true;
}
if(!install())window.addEventListener("load",install,{once:true});
})();
