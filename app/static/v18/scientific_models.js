(function(global){
'use strict';
function lnxOverX(x){return x>0?Math.log(x)/x:NaN;}
function lnxOverXDerivative(x){return x>0?(1-Math.log(x))/(x*x):NaN;}
function tangentGeom(P,O={x:305,y:225},R=88){
let dx=P.x-O.x,dy=P.y-O.y,d2=dx*dx+dy*dy,d=Math.sqrt(d2);const min=R+42;
if(d<min){const s=min/Math.max(d,.001);P={x:O.x+dx*s,y:O.y+dy*s};dx=P.x-O.x;dy=P.y-O.y;d2=dx*dx+dy*dy;}
const l=R*R/d2,m=R*Math.sqrt(d2-R*R)/d2,bx=O.x+l*dx,by=O.y+l*dy;
return {P,T1:{x:bx-m*dy,y:by+m*dx},T2:{x:bx+m*dy,y:by-m*dx}};
}
function countAtoms(formula){const out={};const re=/([A-Z][a-z]?)(\d*)/g;let m;while((m=re.exec(formula))){out[m[1]]=(out[m[1]]||0)+(m[2]?Number(m[2]):1);}return out;}
function scaledCounts(parts){const out={};for(const p of parts){const c=countAtoms(p.formula);for(const [k,v] of Object.entries(c))out[k]=(out[k]||0)+v*(p.coeff||1);}return out;}
function ohmCurrent(V,R){return Number(R)>0?Number(V)/Number(R):NaN;}
function ohmResistance(V,I){return Number(I)!==0?Number(V)/Number(I):NaN;}
function copperHydroxidePrecipitation(){return {reactants:'CuSO4 + 2NaOH',product:'Cu(OH)2',molecular:'CuSO4 + 2NaOH -> Cu(OH)2 + Na2SO4',netIonic:'Cu2+ + 2OH- -> Cu(OH)2',precipitate:true};}
function heartCycleState(step){const states=[{phase:'venous-return',blue:['body','right-atrium','right-ventricle'],red:[]},{phase:'to-lungs',blue:['right-ventricle','pulmonary-artery','lungs'],red:[]},{phase:'oxygenation',blue:['lungs'],red:['lungs']},{phase:'left-return',blue:[],red:['lungs','left-atrium','left-ventricle']},{phase:'to-body',blue:[],red:['left-ventricle','aorta','body']}];return states[Math.max(0,Math.min(states.length-1,Number(step)||0))];}
const api={lnxOverX,lnxOverXDerivative,tangentGeom,countAtoms,scaledCounts,ohmCurrent,ohmResistance,copperHydroxidePrecipitation,heartCycleState};
if(typeof module!=='undefined'&&module.exports)module.exports=api;global.NabilScientificModels=api;
})(typeof window!=='undefined'?window:globalThis);
