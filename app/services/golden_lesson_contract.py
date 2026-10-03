"""Fail-closed pedagogical contract for NABIL Golden lessons.

Point 4: a Golden lesson is a complete teaching journey, not arbitrary chunks.
The source lesson must cover the journey from entry/hook through teaching,
student application and assessment, and MUST finish with a visual summary card.
Optional discovery/lab/proof stages are required only when appropriate to the
lesson, but the structural spine and final summary are mandatory.
"""
from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class GoldenSection:
    key: str
    label: str
    aliases: tuple[str, ...]
    required: bool = False

SECTIONS=(
 GoldenSection('prerequisites','Prerequisites',('prerequisites','prior knowledge','what you need','قبل أن نبدأ','المتطلبات السابقة')),
 GoldenSection('hook','Hook',('hook','warm up','warm-up','think first','فكر معي','لنبدأ','مدخل','تمهيد'),True),
 GoldenSection('discover','Discover',('discover','observe','notice','explore','اكتشف','لاحظ','استكشف')),
 GoldenSection('explain','Explain',('explain','idea','concept','learn','شرح','الفكرة','نفهم'),True),
 GoldenSection('visualize','Visualize',('visualize','visual','diagram','figure','graph','رسم','شاهد','تصور')),
 GoldenSection('manipulate','Manipulate / Experiment',('manipulate','experiment','interactive','lab','مختبر','جرّب','حرّك')),
 GoldenSection('conjecture','Conjecture',('conjecture','predict','what do you notice','توقع','ماذا تلاحظ')),
 GoldenSection('rule','Rule / Definition',('rule','definition','theorem','formula','property','قاعدة','تعريف','نظرية','خاصية'),True),
 GoldenSection('why','Why / Proof',('why','proof','reason','justify','لماذا','برهان','تبرير')),
 GoldenSection('worked_example','Worked Example',('worked example','example','مثال محلول','مثال'),True),
 GoldenSection('deeper_example','Deeper Example',('deeper example','advanced example','مثال أعمق','مثال مركب')),
 GoldenSection('checkpoint','Checkpoint',('checkpoint','check your understanding','quick check','تحقق من فهمك','نقطة تحقق')),
 GoldenSection('common_mistake','Common Mistake',('common mistake','mistake','error detective','خطأ شائع','انتبه')),
 GoldenSection('student_try','Student Try',('student turn','your turn','try','دورك','جرّب بنفسك'),True),
 GoldenSection('hint','Hint',('hint','تلميح')),
 GoldenSection('solution','Full NABIL Solution',('full nabil solution','solution','nabil solution','الحل الكامل','حل نبيل'),True),
 GoldenSection('practice','Practice',('practice','exercises','تمارين','تدريب'),True),
 GoldenSection('challenge','Challenge / Lab',('challenge','transfer','lab','تحدي','مختبر')),
 GoldenSection('assessment','Assessment',('assessment','exit assessment','exit ticket','اختبار ختامي','تقييم'),True),
 GoldenSection('visual_summary','Final Visual Summary',('visual summary','final summary','golden card','summary card','بطاقة نهائية','الخلاصة البصرية','خلاصة الدرس'),True),
)

HEADER_RE=re.compile(r'^\s*(?:#{1,6}\s*|\d+[.)]\s*)?(.{2,100}?)\s*:?\s*$',re.I)

def _norm(s:str)->str:
    return re.sub(r'\s+',' ',str(s or '').strip().casefold())

def classify(line:str)->str|None:
    m=HEADER_RE.match(line or '')
    if not m:return None
    h=_norm(m.group(1))
    for sec in SECTIONS:
        if any(a in h for a in sec.aliases):return sec.key
    return None

def parse_sections(text:str)->list[tuple[str,list[str]]]:
    out=[]; current=''; body=[]
    for raw in str(text or '').replace('\r','').split('\n'):
        line=raw.strip()
        if not line:continue
        key=classify(line)
        if key:
            if body:out.append((current or 'explain',body))
            current=key;body=[]
        else:body.append(line)
    if body:out.append((current or 'explain',body))
    # Merge adjacent same-type sections without changing pedagogical order.
    merged=[]
    for key,lines in out:
        if merged and merged[-1][0]==key:merged[-1][1].extend(lines)
        else:merged.append((key,list(lines)))
    return merged

def validate_golden_lesson(text:str)->dict:
    sections=parse_sections(text);keys=[k for k,_ in sections]
    missing=[s.key for s in SECTIONS if s.required and s.key not in keys]
    errors=[]
    if missing:errors.append('MISSING_REQUIRED_SECTIONS:'+','.join(missing))
    if not sections:errors.append('EMPTY_TEACHING_SEQUENCE')
    if sections and sections[-1][0]!='visual_summary':errors.append('FINAL_CARD_MUST_BE_LAST')
    # Mandatory spine must progress forward; repeated explanatory cards remain OK.
    order={s.key:i for i,s in enumerate(SECTIONS)};seen=-1
    for key,_ in sections:
        idx=order.get(key,seen)
        if key in {'hook','explain','rule','worked_example','student_try','solution','practice','assessment','visual_summary'}:
            if idx<seen:errors.append('PEDAGOGICAL_ORDER_INVALID:'+key);break
            seen=idx
    return {'valid':not errors,'errors':errors,'sections':sections,'section_keys':keys}

def require_golden_lesson(text:str)->dict:
    result=validate_golden_lesson(text)
    if not result['valid']:
        raise ValueError('GOLDEN_LESSON_CONTRACT_FAILED|'+'|'.join(result['errors']))
    return result
