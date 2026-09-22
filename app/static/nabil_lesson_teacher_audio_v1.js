/* Offline-ready authored teacher explanations and exact-text read aloud. No AI API calls. */
(()=>{
"use strict";
function init(){
 if(document.getElementById("nabil-teacher-audio")||!document.querySelector("#lesson-language"))return;
 const synth=window.speechSynthesis,select=document.getElementById("lesson-language");
 const fr=[
 "Regarde : une résistance possède deux bornes. Si on inverse ses bornes, sa valeur ne change pas. Le sens du courant peut changer, mais pas la résistance du conducteur ohmique.",
 "On fait varier la tension et on mesure le courant. Pour un conducteur ohmique, la tension est proportionnelle à l’intensité. La formule à retenir est U égale R fois I. Attention aux unités : volt, ampère et ohm.",
 "Pour mesurer directement la résistance, on utilise un multimètre en position ohmmètre, symbole oméga. On coupe l’alimentation avant la mesure. On peut comparer la valeur lue avec U divisé par I.",
 "En série, le même courant traverse les deux résistances. Les tensions s’additionnent et la résistance équivalente vaut R un plus R deux. Essaie les valeurs du schéma et vérifie la somme.",
 "En dérivation, la tension est la même aux bornes de chaque résistance. Le courant se partage entre les branches. La résistance équivalente est inférieure à chacune des deux résistances."
 ];
 const en=[
 "Look: a resistor has two terminals. Reversing the terminals does not change its resistance. The direction of current may reverse, but the ohmic resistance stays the same.",
 "We vary the voltage and measure the current. For an ohmic conductor, voltage is proportional to current. Remember U equals R times I. Use volts, amperes and ohms.",
 "To measure resistance directly, set the multimeter to the ohmmeter position, marked omega. Disconnect the power supply before measuring. Compare the reading with U divided by I.",
 "In series, the same current flows through both resistors. The voltages add, and equivalent resistance equals R one plus R two. Check the values in the diagram.",
 "In parallel, each resistor has the same voltage. Current divides between the branches. The equivalent resistance is smaller than either individual resistance."
 ];
 const ar=[
 "شوفوا يا أبطال، عنا مقاومة إلها طرفين. إذا بدّلنا الطرف الأول بالثاني، قيمة المقاومة ما بتتغيّر. يعني اتجاه مرور التيار ما بيغيّر قيمة المقاومة الأومية.",
 "هلق منغيّر التوتر ومنقيس شدة التيار. بالناقل الأومي، كل ما زاد التوتر زادت شدة التيار بنفس النسبة. قانون أوم هو U تساوي R ضرب I. انتبهوا: التوتر بالفولت، التيار بالأمبير، والمقاومة بالأوم.",
 "إذا بدنا نقيس المقاومة مباشرة، منحط جهاز الملتيميتر على وضع الأوميتر، رمز أوميغا. لازم نفصل التغذية الكهربائية قبل قياس المقاومة، ومنقارن النتيجة مع R تساوي U على I.",
 "هلق شو عنا بالرسم؟ عنا مقاومتين موصولتين على التوالي: R واحد تساوي ميتين وعشرين أوم، وR اتنين تساوي تمانين أوم، ومصدر توتره اتناش فولت. بالـ series، نفس التيار بيمر بالمقاومتين، والمقاومة المكافئة R E تساوي R واحد زائد R اتنين، يعني ميتين وعشرين زائد تمانين، النتيجة تلاتمية أوم. هلق منطبّق قانون أوم: I تساوي U على R E، يعني اتناش على تلاتمية، فبيطلع صفر فاصلة صفر أربعة أمبير، أو أربعين ميلي أمبير. ومنتأكد كمان إن U واحد زائد U اتنين بيساووا اتناش فولت.",
 "هون اختلف التوصيل: المقاومتين على التفرّع، parallel. التوتر نفسه على كل فرع، يعني U واحد تساوي U اتنين تساوي اتناش فولت. التيار بيتوزّع: I واحد تساوي اتناش على ميتين وعشرين، وI اتنين تساوي اتناش على تمانين. المقاومة المكافئة R E منحسبها من واحد على R E تساوي واحد على R واحد زائد واحد على R اتنين. وبما إن عنا مقاومتين، R E تساوي R واحد ضرب R اتنين على مجموعهن، يعني ميتين وعشرين ضرب تمانين على تلاتمية، وبتطلع تقريبًا تمانية وخمسين فاصلة سبعة أوم. انتبهوا: بالموازي المقاومة المكافئة أصغر من أصغر مقاومة."
 ];
 const exerciseArabic={
  4:"التمرين أربعة. المعطيات: U تساوي اتناش فولت، و I تساوي خمسة فاصلة خمسة ميلي أمبير. المطلوب نحسب المقاومة R. أول شي منحوّل الميلي أمبير لأمبير: I تساوي صفر فاصلة صفر صفر خمسة خمسة أمبير. من قانون أوم R تساوي U على I، يعني اتناش على صفر فاصلة صفر صفر خمسة خمسة، والنتيجة تقريبًا ألفين ومية واثنين وتمانين أوم، أو اتنين فاصلة تمنتعش كيلو أوم.",
  6:"التمرين ستة. المعطيات: U تساوي أربعة وعشرين فولت، و R تساوي مية أوم. المطلوب شدة التيار I. من قانون أوم I تساوي U على R، يعني أربعة وعشرين على مية، والنتيجة صفر فاصلة أربعة وعشرين أمبير.",
  7:"التمرين سبعة. المعطيات: I تساوي ميتين ميلي أمبير، و R تساوي واحد وخمسين أوم. المطلوب التوتر U. منحوّل التيار لصفر فاصلة اتنين أمبير، ومنطبّق U تساوي R ضرب I، يعني واحد وخمسين ضرب صفر فاصلة اتنين، والنتيجة عشرة فاصلة اتنين فولت.",
  14:"التمرين أربعة عشر. شو عطانا؟ مقاومتين على التوالي، التوتر الكلي اتناش فولت، R واحد ميتين وعشرين أوم، و U واحد تمانية فاصلة تمانية فولت. شو المطلوب؟ التيار I، والتوتر U اتنين، والمقاومة R اتنين. أولًا التيار I تساوي U واحد على R واحد، يعني تمانية فاصلة تمانية على ميتين وعشرين، النتيجة صفر فاصلة صفر أربعة أمبير. ثانيًا U اتنين تساوي U ناقص U واحد، يعني اتناش ناقص تمانية فاصلة تمانية، النتيجة تلاتة فاصلة اتنين فولت. ثالثًا R اتنين تساوي U اتنين على I، يعني تلاتة فاصلة اتنين على صفر فاصلة صفر أربعة، النتيجة تمانين أوم.",
  15:"التمرين خمستعش. أول شي منقرأ المعطيات: عنا مقاومتين على التوالي، R واحد تساوي مية أوم، و R اتنين تساوي ميتين أوم، والتوتر الكلي U تساوي اتناش فولت. المطلوب تلات شغلات: المقاومة المكافئة R E، وشدة التيار I، والتوتر على المقاومة التانية U اتنين. الخطوة الأولى: R E تساوي R واحد زائد R اتنين، يعني مية زائد ميتين، فبتطلع تلاتمية أوم. الخطوة التانية: I تساوي U على R E، يعني اتناش على تلاتمية، النتيجة صفر فاصلة صفر أربعة أمبير، أي أربعين ميلي أمبير. الخطوة التالتة: U اتنين تساوي R اتنين ضرب I، يعني ميتين ضرب صفر فاصلة صفر أربعة، فبتطلع تمانية فولت. ومنتأكد: التوتر على المقاومة الأولى أربعة فولت، وأربعة زائد تمانية يساوي اتناش فولت، متل المعطى."
 };
 let chosen=null,paused=false,utterance=null;
 const box=document.createElement("aside");box.id="nabil-teacher-audio";
 box.style.cssText="position:fixed;bottom:96px;right:4px;z-index:2147483000;width:48px;max-height:calc(100dvh - 130px);overflow-y:auto;overflow-x:hidden;background:#09253c;border:2px solid #46c7ee;border-radius:14px;padding:5px;color:#f2fbff;box-shadow:0 5px 25px #000a;font:14px/1.5 system-ui,Arial;direction:ltr";
 box.innerHTML='<div style="font-weight:700;margin-bottom:7px">🎓 NABIL · Lecture et explication / Read & explain</div><div id="nabil-audio-selected" style="font-size:12px;color:#a9e9ff;margin-bottom:8px"></div><div id="nabil-audio-buttons" style="display:flex;flex-wrap:wrap;gap:6px"></div><div id="nabil-audio-explanation" style="display:none;margin-top:9px;max-height:130px;overflow:auto;white-space:pre-wrap;border-top:1px solid #4a7890;padding-top:8px"></div>';
 const actions=box.querySelector("#nabil-audio-buttons"),info=box.querySelector("#nabil-audio-selected"),explain=box.querySelector("#nabil-audio-explanation");
 box.querySelector("div").style.display="none";info.style.display="none";explain.style.display="none";
 actions.style.cssText="display:flex;flex-direction:column;gap:5px;align-items:center";
 let inlineExplanation=null;
 function showExplanation(t,dir){
  inlineExplanation?.remove();
  const target=chosen?.closest("main .row,main section.card,main article.card")||section();
  if(!target)return;
  inlineExplanation=document.createElement("aside");inlineExplanation.id="nabil-inline-teacher-explanation";
  inlineExplanation.dir=dir;inlineExplanation.style.cssText="position:relative;display:block;clear:both;margin:12px 0;padding:14px;background:#143a4b;border:2px solid #69e5ce;border-radius:12px;color:#fff;line-height:1.9;white-space:pre-wrap;overflow-wrap:anywhere";
  const heading=document.createElement("strong");heading.textContent=dir==="rtl"?"🎓 شرح نبيل خطوة بخطوة":"🎓 NABIL · Explanation";heading.style.cssText="display:block;color:#a9ffe7;margin-bottom:8px";
  const body=document.createElement("div");body.textContent=t;inlineExplanation.append(heading,body);target.append(inlineExplanation);
  inlineExplanation.scrollIntoView({behavior:"smooth",block:"nearest"});
 }
 const add=(label,fn)=>{const b=document.createElement("button");b.type="button";b.textContent=label;b.style.cssText="width:35px;height:39px;padding:2px;background:#1768a8;color:white;border:1px solid #66c9ee;border-radius:8px;cursor:pointer;font-size:17px;flex-shrink:0";b.title=label;b.setAttribute("aria-label",label);b.onclick=fn;actions.append(b);return b;};
 function section(){
  return chosen?.closest("section.card,article.card")||chosen?.closest("section,article")||document.querySelector("main .card");
 }
 function sectionText(){
  const s=section();if(!s)return "";
  return [...s.querySelectorAll("h1,h2,p,.formula")].filter(e=>!e.closest("#nabil-teacher-audio")).map(e=>e.innerText.trim()).filter(Boolean).join(". ").slice(0,2400);
 }
 function speak(t,langOverride){
  if(!t)return;
  if(!synth||!window.SpeechSynthesisUtterance){info.textContent="Audio unavailable in this browser";return;}
  synth.cancel();paused=false;
  utterance=new SpeechSynthesisUtterance(t);
  utterance.lang=langOverride|| (select.value==="en"?"en-US":"fr-FR");utterance.rate=.9;
  const voices=synth.getVoices();
  const lang=utterance.lang.slice(0,2);
  const voice=voices.find(v=>v.lang.toLowerCase().startsWith(lang)&&v.localService)||voices.find(v=>v.lang.toLowerCase().startsWith(lang));
  if(voice)utterance.voice=voice;
  synth.speak(utterance);
 }
 function index(){
  const cards=[...document.querySelectorAll("main section.card,main article.card")].filter(e=>e.querySelector("h2"));
  return cards.indexOf(section());
 }
 function explanation(langOverride){
  const row=chosen?.closest(".row");
  const heading=row?.querySelector("h3")?.textContent||"";
  const exerciseNumber=Number((heading.match(/(?:Exercice|Exercise)\s*(\d+)/i)||[])[1]);
  if(langOverride==="ar"&&exerciseArabic[exerciseNumber])return exerciseArabic[exerciseNumber];
  if(row&&langOverride==="ar")return "منقرأ المعطيات والمطلوب أولًا، ومنختار القانون المناسب، ومنعوّض القيم مع وحداتها، ومنتأكد من النتيجة.";
  const n=index(),t=(langOverride==="ar"?ar:select.value==="en"?en:fr)[n];
  if(t)return t;
  if(langOverride==="ar")return "اختار فقرة من أفكار الدرس الخمس، أو اسأل نبيل عن أي تمرين إضافي.";
  return select.value==="en"?"Read the displayed text for this section, then try its exercise. Use the question box to ask NABIL for a new explanation.":"Lis le texte affiché dans cette section, puis essaie son exercice. Pour une explication nouvelle, pose ta question à NABIL.";
 }
 function refresh(){
  const s=section();const h=s?.querySelector("h1,h2");
  info.textContent=(select.value==="en"?"Selected idea: ":"Idée choisie : ")+(h?.innerText||"Conducteurs ohmiques");box.title=info.textContent;
 }
 add("🔊 Lire / Read",()=>{refresh();speak(sectionText());});
 add("🎓 Expliquer / Explain",()=>{refresh();const t=explanation();showExplanation(t,"ltr");speak(t);});
 add("🇱🇧 اشرح بالعربي",()=>{refresh();const t=explanation("ar");showExplanation(t,"rtl");speak(t,"ar-LB");});
 add("⏯",()=>{if(!synth)return;if(synth.paused){synth.resume();paused=false;}else if(synth.speaking){synth.pause();paused=true;}});
 add("⏹",()=>{synth?.cancel();paused=false;});
 add("✕",()=>{synth?.cancel();box.style.display="none";open.style.display="block";});
 for(const [i,b] of [...actions.children].entries())b.textContent=["🔊","🎓","🇱🇧","⏯","⏹","✕"][i];
 const open=document.createElement("button");open.type="button";open.textContent="🎓";
 open.setAttribute("aria-label","Open NABIL lesson audio");
 open.style.cssText="display:none;position:fixed;right:4px;bottom:96px;z-index:2147483000;background:#1768a8;color:white;border:2px solid #72d6fa;border-radius:10px;padding:8px;cursor:pointer";
 open.onclick=()=>{box.style.display="block";open.style.display="none";};
 document.body.append(box,open);
 document.addEventListener("click",e=>{
  if(e.target.closest("#nabil-teacher-audio,#nabil-sticky-language,#lesson-language,#nabil-inline-teacher-explanation"))return;
  const target=e.target.closest("main .row,main section.card,main article.card");
  if(e.target.closest("button,input,select,a"))return;
  if(target){chosen=target;refresh();}
 });
 select.addEventListener("change",()=>{synth?.cancel();refresh();explain.style.display="none";});
 refresh();
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init);else init();
})();