(function(global){
'use strict';
const SUBJECTS=['math','physics','chemistry','biology'];
function norm(v){return String(v||'').trim().toLowerCase();}
function has(text,words){text=norm(text);return words.some(w=>text.includes(w));}
function routeLesson(lesson){
const subject=norm(lesson.subject),kind=norm(lesson.kind),text=[lesson.title,lesson.content,lesson.topic,lesson.expression].join(' ').toLowerCase();
if(subject==='math'||subject==='mathematics'){
if(kind.includes('function')||has(text,['ln','function','derivative','limit','variation','asymptote','curve','graph']))return {renderer:'math-function',reason:'function/analysis signals'};
if(kind.includes('geometry')||kind.includes('proof')||has(text,['tangent','circle','triangle','symmetry','proof','geometry']))return {renderer:'math-geometry-proof',reason:'geometry/proof signals'};
if(has(text,['vector','matrix','coordinate']))return {renderer:'math-vector',reason:'vector/coordinate signals'};
return {renderer:'scientific-schematic',reason:'generic mathematics'};
}
if(subject==='physics'){
if(kind.includes('ohm')||has(text,['ohm law',"ohm's law",'i ∝ v','v/i']))return {renderer:'physics-ohm',reason:'ohm-law signals'};
if(kind.includes('circuit')||has(text,['circuit','resistor','battery','current','voltage']))return {renderer:'physics-circuit',reason:'electric-circuit signals'};
if(kind.includes('wave')||has(text,['wave','frequency','wavelength','lens','mirror','ray','optics']))return {renderer:'physics-wave-optics',reason:'wave/optics signals'};
return {renderer:'physics-mechanics',reason:'default physics mechanics/vector model'};
}
if(subject==='chemistry'){
if(kind.includes('precip')||has(text,['precipitate','precipitation','cuso4','cu(oh)2']))return {renderer:'chemistry-precipitation',reason:'precipitation signals'};
if(kind.includes('reaction')||has(text,['reaction','equation','reactant','product','→','->']))return {renderer:'chemistry-reaction',reason:'chemical-reaction signals'};
if(kind.includes('molecule')||has(text,['molecule','bond','atom','electron','lewis']))return {renderer:'chemistry-structure',reason:'molecular-structure signals'};
return {renderer:'chemistry-lab',reason:'default chemistry lab/schematic'};
}
if(subject==='biology'){
if(kind.includes('heart')||has(text,['heart','atrium','ventricle','aorta','pulmonary','circulation']))return {renderer:'biology-heart',reason:'heart/circulation signals'};
return {renderer:'biology-diagram',reason:'biology diagram/process'};
}
return {renderer:'scientific-schematic',reason:'fallback'};
}
const api={routeLesson,SUBJECTS};if(typeof module!=='undefined'&&module.exports)module.exports=api;global.NabilScientificVisualRouter=api;
})(typeof window!=='undefined'?window:globalThis);
