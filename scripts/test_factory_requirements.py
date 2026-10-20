"""Regression guard: capabilities the user made mandatory for every lesson (docs/NABIL_LESSONS_LEARNED.md)."""
import pathlib,sys
A=pathlib.Path(__file__).parent/'nabil_factory/cards/assets'
js=(A/'golden_v6_engine.js').read_text(encoding='utf8')
need={'LL-07/12 annotate':'async function annotate','LL-17 constructTools':'async function constructTools','LL-17 compass':'function compass(',
 'LL-17 protractor':'function protractor(','LL-18 congruent speech':'is congruent to','LL-18 arabic congruent':'يطابق','LL-19 hat':'\\u0302','LL-silent':'step.silent'}
bad=[k for k,v in need.items() if v not in js]
print('missing:',bad);sys.exit(1 if bad else 0)
