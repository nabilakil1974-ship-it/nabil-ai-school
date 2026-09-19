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
assert(js.includes("renderVerifiedSphereFallback(d)||primary"),"text-only placeholders must be replaced with SVG fallback");
assert(js.includes(".replace(/\\bDRAWINGS?_JSON"),"transport JSON should not reach student board");
console.log("NABIL verified 3D-style sphere SVG + safe landing protocol: PASS");
