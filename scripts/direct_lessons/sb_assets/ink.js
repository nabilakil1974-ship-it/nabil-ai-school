
var cv=$("#ink"),cx=cv.getContext("2d");
var tool="pen",color="#ffffff",size=5,shapeKind=null,ops=[],redo=[],drawing=null;
var COLORS=["#ffffff","#ffe14d","#ff5252","#39d98a","#6fd3ff","#ff9f1c","#d58cff"];
var swBox=$("#sws");
COLORS.forEach(function(c,i){var s=document.createElement("span");s.className="sw"+(i===0?" sel":"");s.style.background=c;s.onclick=function(){color=c;$$(".sw").forEach(function(x){x.classList.remove("sel")});s.classList.add("sel");if(tool==="eraser")setTool("pen")};swBox.appendChild(s)});
$("#size").oninput=function(){size=+this.value};
function pos(e){var r=stage.getBoundingClientRect();return {x:(e.clientX-r.left)/scale,y:(e.clientY-r.top)/scale}}
function drawOp(o,c){
  c.save();c.lineCap="round";c.lineJoin="round";c.lineWidth=o.w;c.strokeStyle=o.c;
  if(o.k==="erase"){c.globalCompositeOperation="destination-out";c.lineWidth=o.w*4}
  if(o.k==="pen"||o.k==="erase"){
    c.beginPath();c.moveTo(o.p[0].x,o.p[0].y);
    if(o.p.length===1)c.lineTo(o.p[0].x+.1,o.p[0].y);
    for(var i=1;i<o.p.length;i++)c.lineTo(o.p[i].x,o.p[i].y);
    c.stroke();
  }else{
    var a=o.a,b=o.b;c.beginPath();
    if(o.k==="line"||o.k==="arrow"){c.moveTo(a.x,a.y);c.lineTo(b.x,b.y);
      if(o.k==="arrow"){var an=Math.atan2(b.y-a.y,b.x-a.x),h=14+o.w*2;
        c.moveTo(b.x,b.y);c.lineTo(b.x-h*Math.cos(an-.45),b.y-h*Math.sin(an-.45));
        c.moveTo(b.x,b.y);c.lineTo(b.x-h*Math.cos(an+.45),b.y-h*Math.sin(an+.45))}}
    else if(o.k==="rect"){c.rect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(b.x-a.x),Math.abs(b.y-a.y))}
    else if(o.k==="circle"){c.ellipse((a.x+b.x)/2,(a.y+b.y)/2,Math.abs(b.x-a.x)/2,Math.abs(b.y-a.y)/2,0,0,7)}
    else if(o.k==="tri"){c.moveTo((a.x+b.x)/2,a.y);c.lineTo(b.x,b.y);c.lineTo(a.x,b.y);c.closePath()}
    c.stroke();
  }
  c.restore();
}
window.__repaint=function(){repaint()};
function repaint(extra){cx.clearRect(0,0,cv.width,cv.height);ops.forEach(function(o){drawOp(o,cx)});if(extra)drawOp(extra,cx)}
cv.addEventListener("pointerdown",function(e){
  if(tool==="select")return;
  cv.setPointerCapture(e.pointerId);closePops();
  var p=pos(e);redo=[];
  if(tool==="shape")drawing={k:shapeKind||"line",c:color,w:size,a:p,b:p};
  else drawing={k:tool==="eraser"?"erase":"pen",c:color,w:size,p:[p]};
  repaint(drawing);
});
cv.addEventListener("pointermove",function(e){
  if(!drawing)return;var p=pos(e);
  if(drawing.p)drawing.p.push(p);else drawing.b=p;
  repaint(drawing);
});
function endDraw(){if(!drawing)return;ops.push(drawing);drawing=null;repaint()}
cv.addEventListener("pointerup",endDraw);cv.addEventListener("pointercancel",endDraw);
function setTool(t){
  tool=t;
  $$("[data-tool]").forEach(function(b){b.classList.toggle("act",b.dataset.tool===t)});
  $("#tShape").classList.toggle("act",t==="shape");
  cv.style.pointerEvents=(t==="select")?"none":"auto";
  cv.style.cursor=t==="eraser"?"cell":"crosshair";
}
$$("[data-tool]").forEach(function(b){b.onclick=function(){closePops();setTool(b.dataset.tool)}});
$("#tShape").onclick=function(){togglePop("popShapes")};
$$("[data-shape]").forEach(function(b){b.onclick=function(){shapeKind=b.dataset.shape;setTool("shape");closePops()}});
$("#tUndo").onclick=function(){if(ops.length){redo.push(ops.pop());repaint()}};
$("#tRedo").onclick=function(){if(redo.length){ops.push(redo.pop());repaint()}};
$("#clearInk").onclick=function(){ops=[];redo=[];repaint()};
setTool("select");

