/* Real photo of the teacher + a glowing teaching pointer that moves over the board */
var T=$("#teacher");
function tel(tag,attrs,txt){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!=null)e.textContent=txt;T.appendChild(e);return e}
var td=tel("defs",{});
td.innerHTML='<filter id="pg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
var beam=tel("path",{d:"",fill:"none",stroke:"#ffe14d","stroke-width":4,"stroke-dasharray":"2 12","stroke-linecap":"round",opacity:.85,filter:"url(#pg)"});
var ring=tel("circle",{cx:0,cy:0,r:26,fill:"none",stroke:"#ffe14d","stroke-width":4,filter:"url(#pg)"});
var dot=tel("circle",{cx:0,cy:0,r:9,fill:"#ffe14d",filter:"url(#pg)"});
var head=tel("path",{d:"M0 0 L-30 -14 L-24 0 L-30 14 Z",fill:"#ffe14d",stroke:"#7a5b00","stroke-width":2,filter:"url(#pg)"});
var speaking=false;
var cur={x:585,y:330},target=[585,330];
function frame(ts){
  cur.x+=(target[0]-cur.x)*.08;cur.y+=(target[1]-cur.y)*.08;
  var ox=PORTRAIT?410:352,oy=PORTRAIT?250:330;
  var wob=Math.sin(ts/330)*3,tx=cur.x+wob,ty=cur.y+wob*.6;
  var mx=(ox+tx)/2,my=Math.min(oy,ty)-70;
  beam.setAttribute("d","M"+ox+" "+oy+" Q"+mx+" "+my+" "+tx+" "+ty);
  ring.setAttribute("cx",tx);ring.setAttribute("cy",ty);ring.setAttribute("r",24+Math.sin(ts/260)*5);
  dot.setAttribute("cx",tx);dot.setAttribute("cy",ty);
  var ang=Math.atan2(ty-my,tx-mx)*180/Math.PI;
  head.setAttribute("transform","translate("+(tx-4)+","+(ty-4)+") rotate("+ang+") translate(-18,0)");
  var u=$("#ustaz");if(u)u.classList.toggle("talk",speaking);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
