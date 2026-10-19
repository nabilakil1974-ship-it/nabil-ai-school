import re,json
h=open('lesson_v4.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global h
    assert h.count(a)==cnt,(a[:70],h.count(a)); h=h.replace(a,b)
# 1) bidi: Arabic prefix split + more math symbols + trailing Arabic punctuation
rep("const words=String(text).match(/\\S+\\s*/g)||[];\n  const isMath=w=>/[0-9^{}=+×÷−<>≤≥≠≈√]/.test(w);\n  const isLatin=w=>/^[A-Za-z][A-Za-z'’-]*[.,;:!?]?\\s*$/.test(w);",
"""const words=[];(String(text).match(/\\S+\\s*/g)||[]).forEach(w=>{const m=w.match(/^([\\u0600-\\u06ff]{1,3})([^\\u0600-\\u06ff\\s][\\s\\S]*)$/);if(m){words.push(m[1]);words.push(m[2])}else words.push(w)});
  const isMath=w=>/[0-9^{}=+×÷−<>≤≥≠≈√∠△°≅⟂↔∥]/.test(w)&&!/[\\u0600-\\u06ff]/.test(w.replace(/[،؛]/g,''));
  const isLatin=w=>/^[A-Za-z][A-Za-z'’-]*[.,;:!?،؛]?\\s*$/.test(w);
  const endsRun=w=>/[،؛.:!?]\\s*$/.test(w);""")
rep("while(j<words.length&&(isMath(words[j])||isLatin(words[j]))){buf+=words[j];j++}\n      const b=bdiOf(buf.replace(/\\s+$/,''));units.push(b);",
"while(j<words.length&&(isMath(words[j])||isLatin(words[j]))){buf+=words[j];j++;if(endsRun(words[j-1]))break}\n      const tailP=(buf.match(/[،؛.:!?]+\\s*$/)||[''])[0];buf=buf.slice(0,buf.length-tailP.length);\n      const b=bdiOf(buf.replace(/\\s+$/,''));units.push(b);if(tailP){const tp=document.createElement('span');tp.textContent=tailP.trim();units.push(tp)}")
# 2) srcBox
rep("const clipId='nb-source-'+id+'-'+index;","srcBox={x,y,w,h};const clipId='nb-source-'+id+'-'+index;")
rep("async function sourceFigure(id,args){","let srcBox=null;\nasync function sourceFigure(id,args){")
# 3) congruenceCases misplaced label
rep("      label(k==='ASA'?'∠B = ∠N':'∠B = ∠N',p[0][0]+12,p[0][1]-25,'#b42e61');\n","")
# 4) annotate + twoTri
fn=r"""
async function annotate(id,a){
  const img=a.on==='image'&&srcBox;
  const T=p=>img?[srcBox.x+p[0]*srcBox.w,srcBox.y+p[1]*srcBox.h]:p;
  const S=img?0.8:1;
  const pt=async p=>{if(FAST)return true;svgPoint(p[0],p[1]);return await wait(300,id)};
  const ang=(o,p)=>Math.atan2(p[1]-o[1],p[0]-o[0]);
  for(const it of a.items||[]){
    if(id!==run)return false;
    const c=it.c||'#d6336c';
    if(it.kind==='equal'){
      const n=Math.max(1,it.n||1);
      for(const sg of it.segs){
        const p=T(sg[0]),q=T(sg[1]),mx=(p[0]+q[0])/2,my=(p[1]+q[1])/2,L=Math.hypot(q[0]-p[0],q[1]-p[1])||1,ux=(q[0]-p[0])/L,uy=(q[1]-p[1])/L,nx=-uy,ny=ux;
        if(!await pt([mx,my]))return false;
        for(let i=0;i<n;i++){const o=(i-(n-1)/2)*9*S;el('line',{x1:mx+ux*o-nx*12*S,y1:my+uy*o-ny*12*S,x2:mx+ux*o+nx*12*S,y2:my+uy*o+ny*12*S,stroke:c,'stroke-width':4,'stroke-linecap':'round'})}
        if(!await wait(FAST?0:250,id))return false}}
    else if(it.kind==='arc'){
      const O=T(it.at),P=T(it.from),Q=T(it.to),n=Math.max(1,it.n||1);
      if(!await pt(O))return false;
      let a1=ang(O,P),a2=ang(O,Q),d=a2-a1;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;
      const r0=(it.r||30)*S;
      for(let i=0;i<n;i++){const r=r0+i*8*S;el('path',{d:'M'+(O[0]+r*Math.cos(a1))+' '+(O[1]+r*Math.sin(a1))+' A'+r+' '+r+' 0 0 '+(d>0?1:0)+' '+(O[0]+r*Math.cos(a1+d))+' '+(O[1]+r*Math.sin(a1+d)),fill:'none',stroke:c,'stroke-width':3.6,'stroke-linecap':'round'})}
      if(it.text){const r=r0+(n-1)*8*S+24*S,m=a1+d/2;el('text',{x:O[0]+r*Math.cos(m)-18*S,y:O[1]+r*Math.sin(m)+8*S,'font-size':24*S,fill:c,'font-weight':'bold'},it.text)}
      if(!await wait(FAST?0:300,id))return false}
    else if(it.kind==='seg'){const p=T(it.a),q=T(it.b);if(!await pt(p))return false;if(!await drawLine(p[0],p[1],q[0],q[1],c,id,it.dash||''))return false}
    else if(it.kind==='poly'){const ps=it.pts.map(T);if(!await pt(ps[0]))return false;for(let i=0;i<ps.length;i++){const p=ps[i],q=ps[(i+1)%ps.length];if(!await drawLine(p[0],p[1],q[0],q[1],c,id,'10 6'))return false}}
    else if(it.kind==='right'){const O=T(it.at),u=T(it.u),v=T(it.v),d=16*S,nu=Math.hypot(u[0]-O[0],u[1]-O[1])||1,nv=Math.hypot(v[0]-O[0],v[1]-O[1])||1,a1=[O[0]+(u[0]-O[0])/nu*d,O[1]+(u[1]-O[1])/nu*d],a2=[O[0]+(v[0]-O[0])/nv*d,O[1]+(v[1]-O[1])/nv*d];
      if(!await pt(O))return false;el('path',{d:'M'+a1+' L'+[a1[0]+a2[0]-O[0],a1[1]+a2[1]-O[1]]+' L'+a2,fill:'none',stroke:c,'stroke-width':3.6})}
    else if(it.kind==='ring'){const p=T(it.p);if(!await pt(p))return false;const e=el('circle',{cx:p[0],cy:p[1],r:(it.r||16)*S,fill:'none',stroke:c,'stroke-width':4});if(!await wait(FAST?0:450,id))return false}
    else if(it.kind==='label'){const p=T(it.p);if(!await pt(p))return false;el('text',{x:p[0],y:p[1],'font-size':26*S,fill:c,'font-weight':'bold'},it.text)}
  }
  return id===run}
async function twoTri(id,a){
  ink.replaceChildren();
  const T1=a.t1,T2=a.t2;
  for(const [T,names,col] of [[T1,'ABC','#1762aa'],[T2,'PMN','#159b7b']]){
    for(let j=0;j<3;j++)if(!await drawLine(...T[j],...T[(j+1)%3],col,id))return false;
    const cx=(T[0][0]+T[1][0]+T[2][0])/3,cy=(T[0][1]+T[1][1]+T[2][1])/3;
    for(let j=0;j<3;j++){const dx=T[j][0]-cx,dy=T[j][1]-cy,L=Math.hypot(dx,dy)||1;label(names[j],T[j][0]+dx/L*28-10,T[j][1]+dy/L*28+9,col)}}
  return id===run}
"""
rep("const DRAW={triEl,","const DRAW={annotate,twoTri,triEl,")
i=h.find("const DRAW={annotate");h=h[:i]+fn+h[i:]
# 5) draw step with speech
rep("else if(step.t==='draw'){setBoardMode('dual',{preserveState:true});await new Promise(r=>requestAnimationFrame(r));if(!await doDraw(step,id))return}",
"else if(step.t==='draw'){setBoardMode('dual',{preserveState:true});await new Promise(r=>requestAnimationFrame(r));const hv=step.speech?speakText(step.speech,id):null;if(!await doDraw(step,id))return;if(hv&&!await waitVoice(hv,id))return}")
# 6) data
m=re.search(r'(<script id="nabilV6Data" type="application/json">)(.*?)(</script>)',h,re.S)
D=json.loads(m.group(2))
def A(speech,items,on='board'):return {"t":"draw","draw":"annotate","args":{"on":on,"items":items},"speech":speech}
BL,GR,PK,OR='#1c7ed6','#2f9e44','#d6336c','#e8590c'
# scene 9 SAS
sc=D['scenes'][9];st=sc['steps']
cs=st[1]
A0,B0,C0=[225,325],[390,325],[305,155];M0,N0,P0=[530,325],[695,325],[610,155]
new=[st[0],cs,
 A("الضلع AB يساوي الضلع MN. نضع على كل منهما علامة واحدة.",[{"kind":"equal","segs":[[A0,B0],[M0,N0]],"n":1,"c":BL}]),
 A("والضلع BC يساوي الضلع NP. نضع على كل منهما علامتين.",[{"kind":"equal","segs":[[B0,C0],[N0,P0]],"n":2,"c":GR}]),
 A("والزاوية B تساوي الزاوية N، وهي محصورة بين الضلعين المعلَّمين. نرسم عليها القوس نفسه.",[{"kind":"arc","at":B0,"from":A0,"to":C0,"n":1,"c":PK,"r":34},{"kind":"arc","at":N0,"from":M0,"to":P0,"n":1,"c":PK,"r":34}])]+st[2:]
sc['steps']=new
# scene 29 ex12
sc=D['scenes'][29];st=sc['steps']
A1,B1,C1=[210,420],[440,420],[239.7,251.8];P1,M1,N1=[520,420],[750,420],[549.7,251.8]
new=[st[0],{"t":"draw","draw":"twoTri","args":{"t1":[A1,B1,C1],"t2":[P1,M1,N1]}},
 A("المعطى: الضلع AB يساوي الضلع PM. نضع على كل منهما علامة.",[{"kind":"equal","segs":[[A1,B1],[P1,M1]],"n":1,"c":BL}]),
 A("الزاوية A تساوي ثمانين درجة، وهي ضعف الزاوية B التي تساوي أربعين درجة.",[{"kind":"arc","at":A1,"from":B1,"to":C1,"n":2,"c":PK,"text":"80°","r":34},{"kind":"arc","at":B1,"from":A1,"to":C1,"n":1,"c":GR,"text":"40°","r":34}]),
 A("وفي المثلث الثاني: الزاوية M تساوي أربعين درجة، فالزاوية P ضعفها: ثمانون درجة.",[{"kind":"arc","at":P1,"from":M1,"to":N1,"n":2,"c":PK,"text":"80°","r":34},{"kind":"arc","at":M1,"from":P1,"to":N1,"n":1,"c":GR,"text":"40°","r":34}])]+st[1:]
sc['steps']=new
# scene 31 ex14
sc=D['scenes'][31];st=sc['steps']
fA,fB,fC,fE,fF=[.161,.334],[.625,.334],[.625,.719],[.279,.175],[.821,.431]
new=[st[0],
 A("نلاحظ في الشكل علامتَي التساوي: الضلع AB يساوي الضلع BC.",[{"kind":"ring","p":[.407,.334],"c":PK,"r":16},{"kind":"ring","p":[.633,.525],"c":PK,"r":16}],'image'),
 st[1],
 A("نحدد المثلث ABE. فيه زاوية قائمة عند E، والزاوية عند B تساوي ثلاثين درجة.",[{"kind":"poly","pts":[fA,fB,fE],"c":OR},{"kind":"ring","p":fE,"c":OR,"r":16}],'image'),
 A("الزاوية الثالثة عند A تساوي ستين درجة.",[{"kind":"arc","at":fA,"from":fB,"to":fE,"n":1,"c":OR,"text":"60°","r":34}],'image'),
 st[2],
 A("وفي المثلث BCF: الزاوية CBF تساوي ستين درجة، والزاوية BCF تساوي ثلاثين درجة.",[{"kind":"poly","pts":[fB,fC,fF],"c":GR},{"kind":"arc","at":fB,"from":fC,"to":fF,"n":1,"c":GR,"text":"60°","r":30},{"kind":"arc","at":fC,"from":fB,"to":fF,"n":1,"c":GR,"text":"30°","r":34}],'image')]+st[3:]
sc['steps']=new
# scene 38 problem2
sc=D['scenes'][38];st=sc['steps']
pA,pM,pN,pK,pL=[.471,.173],[.377,.419],[.55,.419],[.286,.419],[.648,.419]
new=[st[0],
 A("المعطى AM يساوي AN. نضع على كل منهما علامة واحدة.",[{"kind":"equal","segs":[[pA,pM],[pA,pN]],"n":1,"c":BL}],'image'),
 A("وKM يساوي NL. نضع على كل منهما علامتين.",[{"kind":"equal","segs":[[pK,pM],[pN,pL]],"n":2,"c":GR}],'image'),
 st[1],
 A("لنرى المثلثين AMK وANL، نكمل الرسم: نصل النقطة A بالنقطة K، وA بالنقطة L.",[{"kind":"seg","a":pA,"b":pK,"c":PK},{"kind":"seg","a":pA,"b":pL,"c":PK}],'image'),
 st[2],
 A("الزاويتان الخارجيتان AMK وANL متساويتان. نرسم عليهما القوس نفسه.",[{"kind":"arc","at":pM,"from":pA,"to":pK,"n":1,"c":OR,"r":28},{"kind":"arc","at":pN,"from":pA,"to":pL,"n":1,"c":OR,"r":28}],'image')]+st[3:]
sc['steps']=new
h=h[:m.start(2)]+json.dumps(D,ensure_ascii=False)+h[m.end(2):]
open('lesson_v5.html','w',encoding='utf-8').write(h)
print('ok')
