
var T=$("#teacher");
function tel(tag,attrs,txt){var e=document.createElementNS(NS,tag);for(var k in attrs)e.setAttribute(k,attrs[k]);if(txt!=null)e.textContent=txt;T.appendChild(e);return e}
var SK="#c98a64",SKd="#a96e4b",HAIR="#17110d",SH="#14171d",SHl="#232832";
var td=tel("defs",{});
var sg=document.createElementNS(NS,"linearGradient");sg.setAttribute("id","shirt");sg.setAttribute("x1","0");sg.setAttribute("y1","0");sg.setAttribute("x2","1");sg.setAttribute("y2","0");
sg.innerHTML='<stop offset="0" stop-color="#0d0f14"/><stop offset=".7" stop-color="#1a1e27"/><stop offset="1" stop-color="#232937"/>';
td.appendChild(sg);
/* back arm (resting) */
tel("path",{d:"M95 480 C60 560 70 700 110 790 L170 780 C150 700 150 590 190 500Z",fill:"#10131a"});
/* torso */
tel("path",{d:"M40 941 C28 760 36 560 92 420 C120 372 190 346 262 352 C330 360 366 410 372 480 C380 620 390 800 388 941Z",fill:"url(#shirt)"});
tel("path",{d:"M150 380 C190 360 250 352 300 372 C250 380 205 392 170 420Z",fill:SHl,opacity:.7});
tel("path",{d:"M120 430 C150 600 160 780 150 941",fill:"none",stroke:"#262c38","stroke-width":3,opacity:.7});
/* neck */
tel("path",{d:"M196 300 L196 372 C210 392 250 394 272 372 L272 296Z",fill:SKd});
/* collar */
tel("path",{d:"M178 364 L226 410 L270 364 L292 380 L230 440 L160 388Z",fill:"#1d222c"});
/* head (facing right) */
tel("path",{d:"M178 214 C176 150 220 112 266 118 C312 124 336 168 336 214 C338 250 330 288 298 312 C268 330 214 322 196 292 C182 270 178 242 178 214Z",fill:SK});
tel("path",{d:"M334 214 L352 236 L334 244Z",fill:SK});            /* nose */
tel("path",{d:"M184 188 C184 120 232 92 276 98 C316 104 338 140 338 178 C320 150 290 140 262 144 C228 148 200 168 192 206Z",fill:HAIR});
tel("path",{d:"M172 190 C170 160 180 140 196 126 C204 150 200 176 204 206Z",fill:HAIR});
/* beard */
tel("path",{d:"M196 246 C200 296 226 332 276 330 C316 326 336 296 338 262 C328 276 312 284 296 280 C282 268 256 266 238 276 C220 272 208 262 202 240Z",fill:HAIR});
tel("path",{d:"M270 272 C290 266 312 268 326 262",fill:"none",stroke:"#3a2a22","stroke-width":3,"stroke-linecap":"round"});
tel("path",{d:"M306 274 q12 4 22 -2",fill:"none",stroke:"#7a4a3a","stroke-width":3,"stroke-linecap":"round"}); /* mouth */
/* ear and eye */
tel("ellipse",{cx:206,cy:232,rx:12,ry:22,fill:SKd});
tel("ellipse",{cx:300,cy:206,rx:8,ry:5,fill:"#fff"});
tel("circle",{cx:304,cy:206,r:3.4,fill:"#1b1411"});
tel("path",{d:"M284 190 Q302 180 322 190",fill:"none",stroke:HAIR,"stroke-width":6,"stroke-linecap":"round"});
/* arm group */
var arm=tel("path",{d:"",fill:"none",stroke:"#171b23","stroke-width":58,"stroke-linecap":"round","stroke-linejoin":"round"});
var armHl=tel("path",{d:"",fill:"none",stroke:"#262d3a","stroke-width":14,"stroke-linecap":"round","stroke-linejoin":"round",opacity:.7});
var hand=tel("ellipse",{cx:0,cy:0,rx:25,ry:21,fill:SK});
var pen=tel("line",{x1:0,y1:0,x2:0,y2:0,stroke:"#f5f7ff","stroke-width":9,"stroke-linecap":"round"});
var penTip=tel("circle",{cx:0,cy:0,r:6,fill:"#ffe14d",filter:""});
var SHD={x:310,y:410},L1=215,L2=215;
var cur={x:560,y:330},target=[585,330],t0=0;
function solve(tx,ty){
  var dx=tx-SHD.x,dy=ty-SHD.y,d=Math.hypot(dx,dy),max=L1+L2-6;
  if(d>max){dx*=max/d;dy*=max/d;d=max}
  if(d<110){dx*=110/d;dy*=110/d;d=110}
  var a=Math.atan2(dy,dx),c=(L1*L1+d*d-L2*L2)/(2*L1*d);
  var ang=Math.acos(Math.max(-1,Math.min(1,c)));
  var ea=a+ang; /* elbow below the line (positive y) */
  var ex=SHD.x+L1*Math.cos(ea),ey=SHD.y+L1*Math.sin(ea);
  return {ex:ex,ey:ey,wx:SHD.x+dx,wy:SHD.y+dy};
}
function frame(ts){
  cur.x+=(target[0]-cur.x)*.07;cur.y+=(target[1]-cur.y)*.07;
  var wob=Math.sin(ts/380)*2.2;
  var s=solve(cur.x-67+wob,cur.y+57+wob*.4);
  var d="M"+SHD.x+" "+SHD.y+" Q"+(SHD.x+10)+" "+(SHD.y+60)+" "+s.ex+" "+s.ey+" L"+s.wx+" "+s.wy;
  arm.setAttribute("d",d);armHl.setAttribute("d",d);
  var fa=Math.atan2(s.wy-s.ey,s.wx-s.ex);
  hand.setAttribute("cx",s.wx);hand.setAttribute("cy",s.wy);
  var px=cur.x+wob,py=cur.y+wob*.4;
  pen.setAttribute("x1",s.wx);pen.setAttribute("y1",s.wy);pen.setAttribute("x2",px);pen.setAttribute("y2",py);
  penTip.setAttribute("cx",px);penTip.setAttribute("cy",py);
  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);
/* shoulder cap drawn above the arm start */
tel("circle",{cx:SHD.x,cy:SHD.y,r:30,fill:"#171b23"});

