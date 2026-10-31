/* Real photo of the teacher + a glowing teaching pointer that moves over the board */
var T=$("#teacher");
function tel(tag,attrs,txt){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!=null)e.textContent=txt;T.appendChild(e);return e}
var td=tel("defs",{});
td.innerHTML='<filter id="pg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
var beam=tel("path",{d:"",fill:"none",stroke:"#e8c27a","stroke-width":9,"stroke-linecap":"round",opacity:1});
var ring=tel("circle",{cx:0,cy:0,r:26,fill:"none",stroke:"#ffe14d","stroke-width":4,filter:"url(#pg)"});
var dot=tel("circle",{cx:0,cy:0,r:9,fill:"#ffe14d",filter:"url(#pg)"});
var head=tel("path",{d:"M0 0 L-30 -14 L-24 0 L-30 14 Z",fill:"#ffe14d",stroke:"#7a5b00","stroke-width":2,filter:"url(#pg)"});
var speaking=false,lastSp=null,uv=$("#uv");
if(uv){uv.addEventListener("playing",function(){$("#ustaz").classList.add("vid")});uv.addEventListener("error",function(){})}
var cur={x:585,y:330},target=[585,330];
function frame(ts){
  cur.x+=(target[0]-cur.x)*.08;cur.y+=(target[1]-cur.y)*.08;
  var ox=340,oy=430;
  var wob=Math.sin(ts/330)*3,tx=cur.x+wob,ty=cur.y+wob*.6;
  var mx=(ox+tx)/2,my=Math.min(oy,ty)-70;
  var dx=tx-ox,dy=ty-oy,dl=Math.hypot(dx,dy)||1,ex=tx-dx/dl*16,ey=ty-dy/dl*16;beam.setAttribute("d","M"+ox+" "+oy+" L"+ex+" "+ey);
  ring.setAttribute("cx",tx);ring.setAttribute("cy",ty);ring.setAttribute("r",24+Math.sin(ts/260)*5);
  dot.setAttribute("cx",tx);dot.setAttribute("cy",ty);
  var ang=Math.atan2(ty-my,tx-mx)*180/Math.PI;
  head.setAttribute("opacity",0);head.setAttribute("transform","translate("+(tx-4)+","+(ty-4)+") rotate("+ang+") translate(-18,0)");
  var u=$("#ustaz");if(u)u.classList.toggle("talk",speaking);
  if(speaking!==lastSp){lastSp=speaking;if(uv){try{if(speaking){var pr=uv.play();if(pr&&pr.catch)pr.catch(function(){})}else uv.pause()}catch(e){}}}
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
