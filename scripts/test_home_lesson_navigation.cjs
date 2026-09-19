"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const source=fs.readFileSync("app/static/nabil_open_tutor_v1.js","utf8");
const css=fs.readFileSync("app/static/nabil_reference_theme.css","utf8");
const start=source.indexOf("function showStructuredLesson(){");
const end=source.indexOf("window.nabilShowProfessorGateway=showBlueRobotHome;",start);
assert(start>=0&&end>start,"test real navigation code");
const styles={};
const home={hidden:false,attributes:{},style:{
  setProperty:(k,v)=>{styles[k]=v},removeProperty:k=>delete styles[k],
  set display(v){styles.display=v},get display(){return styles.display},
  set opacity(v){styles.opacity=v}
},setAttribute:(k,v)=>{home.attributes[k]=v},removeAttribute:k=>delete home.attributes[k]};
const classes=new Set(["nabil-home-lock"]);
const body={classList:{add:c=>classes.add(c),remove:c=>classes.delete(c),contains:c=>classes.has(c)}};
const callbacks={};
const document={body,addEventListener:(type,fn)=>{callbacks[type]=fn}};
const window={scrollTo:()=>{}};
const stage={hidden:false},homeHost={style:{display:"block"}};
const returnHome={addEventListener:()=>{}};
vm.runInNewContext(source.slice(start,end+"window.nabilShowProfessorGateway=showBlueRobotHome;".length),
  {home,homeHost,stage,document,window,returnHome});
function click(id){
 let prevented=false,stopped=false;
 const event={target:{closest:sel=>sel.split(",").some(s=>s.trim()==="#"+id)?{}:null},
 preventDefault:()=>{prevented=true},stopImmediatePropagation:()=>{stopped=true}};
 callbacks.click(event);
 return {prevented,stopped};
}
let e=click("homeStartShortcut");
assert(e.prevented&&e.stopped,"consume stale grade-splash legacy click listeners");
assert.equal(home.hidden,true);
assert.equal(styles.display,"none");
assert.equal(homeHost.style.display,"none");
assert.equal(stage.hidden,true);
assert(classes.has("nabil-lesson-active")&&!classes.has("nabil-home-lock"));
e=click("backToInterfaceBtn");
assert(e.prevented&&e.stopped,"consume legacy Home listeners");
assert.equal(home.hidden,false);
assert.equal(styles.display,"block");
assert.equal(homeHost.style.display,"block");
assert(classes.has("nabil-home-lock")&&!classes.has("nabil-lesson-active"));
assert(css.includes("OWNER_STABLE_TWO_VIEWS_V10"));
assert(css.includes("body.nabil-lesson-active::before{display:none!important"));
assert(css.includes("#nabilHome[hidden]"));
assert(css.includes("body:not(.nabil-lesson-active) #nabilHome #homeStartShortcut"));
assert(css.includes("position:fixed!important;top:auto!important;left:auto!important"));
assert(css.includes("bottom:max(15px,env(safe-area-inset-bottom))!important"));
console.log("NABIL lesson/home real navigation + bottom-right Start Lesson: PASS");
