"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const source=fs.readFileSync("app/static/nabil_open_tutor_v1.js","utf8");
const css=fs.readFileSync("app/static/nabil_reference_theme.css","utf8");
assert(source.includes('returnHome.textContent="Home"'),"the navigation label must be just Home");
assert(source.includes('lessonHeader.appendChild(returnHome)'),"Home must be in the header, not on Send");
assert(!source.includes('returnHome.textContent="⌂ الرئيسية"'),"retire Arabic floating label");
assert(css.includes("OWNER HOME NAV FIX"),"non-overlapping Home position is required");
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
const newDock=css.slice(css.indexOf("OWNER_HOME_BUTTONS_OPPOSITE_ANSWER_V12"));
assert(newDock.startsWith("OWNER_HOME_BUTTONS_OPPOSITE_ANSWER_V12"),"owner's LEFT-side button dock must exist");
assert(newDock.includes("#nabilHome #homeStartShortcut,") && newDock.includes("#nabilHome #homeVoiceBtn{"),"dock both controls rather than navigation only");
assert(newDock.includes("left:max(14px,env(safe-area-inset-left))!important"),"green control at left of robot side");
assert(newDock.includes("left:calc(max(14px,env(safe-area-inset-left)) + 142px)!important"),"red control beside green");
assert(newDock.includes("display:flex!important;visibility:visible!important;pointer-events:auto!important"),"voice cannot stay hidden on mobile");
assert(newDock.includes("width:min(42vw,145px)!important"),"both buttons must fit 320px phone");
assert(newDock.includes("padding-bottom:125px!important"),"reserve scroll space for mobile answer composer");
console.log("NABIL lesson/home real navigation + LEFT-side unobscured Start and Voice controls: PASS");
