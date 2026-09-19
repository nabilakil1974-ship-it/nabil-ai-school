/* Actual isolated SVG renderer regression without a browser or AI key. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const js=fs.readFileSync("app/static/nabil_open_tutor_v1.js","utf8");
const start=js.indexOf("function renderVerifiedSphereFallback(d){");
const end=js.indexOf("\nfunction detectLanguage(",start);
assert(start>=0 && end>start,"fallback must be in real landing tutor source");
const escapeHTML=t=>String(t??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const render=vm.runInNewContext(js.slice(start,end)+"\nrenderVerifiedSphereFallback",{escapeHTML,Number,String});
for(const radius of [3,5]){
 const fig=render({type:"sphere",radius,radius_label:"r = "+radius+" cm",title:"Sphere"});
 assert.match(fig,/<svg\b/);
 assert.match(fig,/viewBox="0 0 680 520"/);
 assert.match(fig,new RegExp("r = "+radius+" cm"));
 assert.match(fig,/<circle\b/);
 assert.match(fig,/<path\b/);
 assert.match(fig,/<line\b/);
 assert.match(fig,/#[0-9a-fA-F]{6}/);
}
assert.equal(render({type:"sphere"}),"","never invent radius");
assert.equal(render({type:"sphere",radius:0}),"","reject zero radius");
assert.equal(render({type:"cylinder",radius:3}),"","don't fabricate other figures");
const unsafe=render({type:"sphere",radius:3,title:"<script>danger</script>"});
assert(!unsafe.includes("<script>"),"SVG title must escape markup");
assert(js.includes("renderVerifiedSphereFallback(d)||renderVerifiedCoordinateFallback(d)"),"text-only placeholders must be replaced with SVG fallback");
assert(js.includes(".replace(/\\bDRAWINGS?_JSON"),"transport JSON should not reach student board");

const languageStart=js.indexOf("function detectLanguage(q){");
const languageEnd=js.indexOf("\nfunction addLine(",languageStart);
assert(languageStart>=0&&languageEnd>languageStart,"test real language detection source");
const detect=vm.runInNewContext(js.slice(languageStart,languageEnd)+"\ndetectLanguage");
assert.equal(detect("Draw a sphere with radius 3 cm. Only the figure."),"English");
assert.equal(detect("بدي study the function ln x"),"English");
assert.equal(detect("هلق derivative and increasing"),"English");
assert.equal(detect("Étudie la fonction ln(x)"),"Français");
assert.equal(detect("بدي étudier la fonction"),"Français");
assert.equal(detect("اشرح الدرس بالعربية"),"العربية");
const css=fs.readFileSync("app/static/nabil_reference_theme.css","utf8");
const backend=fs.readFileSync("app/api/routes_chat.py","utf8");
assert(css.includes("OWNER_PHONE_ANSWER_FIRST_V9"),"mobile answer-first override required");
assert(css.includes("height:clamp(90px,27vw,138px)!important"),"avatar must shrink after answer");
assert(css.includes("max-height:none!important;overflow:visible!important"),"mobile solution must not clip");
assert(backend.includes("FOREIGN_LANGUAGE_FIRST_TUTOR_V3"),"foreign language must dominate all subjects");
assert(backend.includes("For EVERY grade and subject"),"must be universal rather than math-only");

console.log("NABIL verified 3D-style sphere SVG + safe landing protocol: PASS");
