"""Regression guard: capabilities the user made mandatory for every lesson (docs/NABIL_LESSONS_LEARNED.md)."""
import pathlib,sys
A=pathlib.Path(__file__).parent/'nabil_factory/cards/assets'
js=(A/'golden_v6_engine.js').read_text(encoding='utf8')
need={'LL-07/12 annotate':'async function annotate','LL-17 constructTools':'async function constructTools','LL-17 compass':'function compass(',
 'LL-17 protractor':'function protractor(','LL-18 congruent speech':'is congruent to','LL-18 arabic congruent':'يطابق','LL-19 hat':'\\u0302','LL-silent':'step.silent','LL-24 construct':'async function construct(','LL-26 lang buttons':'function setLang(','LL-26 french speech':'est isométrique à','LL-26 greeting':'Commençons la leçon'}
bad=[k for k,v in need.items() if v not in js]
print('missing:',bad)

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from scripts.nabil_factory.factory.student_clean_gate import audit_student_text
assert audit_student_text([{"steps":[{"t":"text","text":"Student p.43 Golden"}]}])["verdict"]=="FAIL"
assert audit_student_text([{"steps":[{"t":"text","text":"Draw AB."}]}])["verdict"]=="PASS"
from app.services.exercise_solver import _clean_construct
assert _clean_construct({"points":{"A":[0,0],"B":[1,0]},"ops":[{"op":"ruler","a":"A","b":"B"}]})
pl=(A/'golden_v6_plan.js').read_text(encoding='utf8')
for k,v in {'LL-28 plan follows board language':'viewLang','LL-28 plan twins':'PLAN.tw','LL-29 13-section CRDP-based plan':'const S13=','LL-29 plan disclaimer':'not an official unified template'}.items():
    if v not in pl: bad.append(k)
print('missing:',bad)
sys.exit(1 if bad else 0)
