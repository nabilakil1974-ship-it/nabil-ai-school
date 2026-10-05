import { parseLessonText } from './nabil_parser.js';
import { renderCard } from './nabil_cards.js';
import { mountVerifiedLabs } from './nabil_labs.js';
function escapeTitle(v){const d=document.createElement('div');d.textContent=String(v||'');return d.innerHTML;}
window.NABILReferenceClassroomV16={mount(root,text,title,meta={}){const sections=parseLessonText(text);root.innerHTML='<div class="nrc"><main class="nrc-wrap"><h1 class="nrc-title">'+escapeTitle(title)+'</h1><article class="nrc-lesson">'+sections.map((c,i)=>renderCard(c,i)).join('')+'</article></main></div>';root.dataset.lessonId=meta.lesson_id||'';root.dataset.renderer='reference-v16-modular';mountVerifiedLabs(root,meta);},parse:parseLessonText};
