"""Stateful conversation engine for the school principal (no external AI, deterministic).

Each utterance is turned into explicit OPERATIONS (type / target / old / new / reason / clarity / validation) that are validated and
applied to ONE school state. Nothing is guessed: unclear scope -> a single clear question and NO change. Every change is logged and
can be undone (snapshot stack). Understanding is rule-based; it covers the patterns tested in tests/test_timetable_ops.py and nothing is
claimed beyond them.
"""
from __future__ import annotations
import copy, re
from typing import Any

DAY_ORDER = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"]
DAY_KEYS = {"احد": "الأحد", "اثنين": "الاثنين", "تلات": "الثلاثاء", "ثلاثاء": "الثلاثاء", "تلاتاء": "الثلاثاء", "اربعاء": "الأربعاء", "اربعا": "الأربعاء",
            "خميس": "الخميس", "جمعه": "الجمعة", "جمعة": "الجمعة", "سبت": "السبت"}
NUM = {"واحد": 1, "واحده": 1, "حصه": 1, "اول": 1, "حصتين": 2, "حصتان": 2, "اثنين": 2, "تنتين": 2, "ثلاث": 3, "ثلاثه": 3, "تلات": 3, "تلاته": 3,
       "اربع": 4, "اربعه": 4, "خمس": 5, "خمسه": 5, "ست": 6, "سته": 6, "سبع": 7, "سبعه": 7, "ثماني": 8, "تمان": 8, "تمانيه": 8, "ثمانيه": 8,
       "تسع": 9, "تسعه": 9, "عشر": 10, "عشره": 10}
GRADES = {"الاول": "1", "الثاني": "2", "التاني": "2", "الثالث": "3", "التالت": "3", "الرابع": "4", "الخامس": "5", "السادس": "6", "السابع": "7",
          "الثامن": "8", "التامن": "8", "التاسع": "9", "العاشر": "10", "الحادي عشر": "11", "الثاني عشر": "12"}
LETTERS = {"الف": "أ", "ا": "أ", "باء": "ب", "ب": "ب", "جيم": "ج", "ج": "ج", "دال": "د", "د": "د", "هاء": "هـ", "ه": "هـ"}
SUBJECTS = ["رياضيات", "علوم", "عربي", "لغه عربيه", "انكليزي", "انجليزي", "فرنسي", "تاريخ", "جغرافيا", "فيزياء", "كيمياء", "احياء", "تربيه", "معلوماتيه", "فن", "رياضه", "موسيقى", "اجتماعيات", "تربيه وطنيه", "دين"]
SUBJECT_CANON = {"علوم": "علوم", "عربي": "لغة عربية", "لغه عربيه": "لغة عربية", "انجليزي": "إنكليزي", "انكليزي": "إنكليزي", "فرنسي": "فرنسي", "احياء": "أحياء", "تربيه": "تربية", "تربيه وطنيه": "تربية وطنية",
                 "معلوماتيه": "معلوماتية", "رياضه": "رياضة", "اجتماعيات": "اجتماعيات", "دين": "دين", "رياضيات": "رياضيات", "تاريخ": "تاريخ", "جغرافيا": "جغرافيا", "فيزياء": "فيزياء", "كيمياء": "كيمياء", "فن": "فن", "موسيقى": "موسيقى"}


def norm(t: str) -> str:
    t = re.sub(r"[ً-ٰٟـ]", "", str(t or ""))
    t = t.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ى", "ي").replace("ة", "ه")
    t = t.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    t = re.sub(r"[«»؟?!]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def new_state() -> dict[str, Any]:
    return {"days": [], "periods_per_day": None, "teachers": {}, "context": {"teacher": None}, "log": [], "undo": []}


AR = "\u0621-\u064a"


def _days_in(text: str) -> list[str]:
    out = []
    for k, v in DAY_KEYS.items():
        if re.search(r"(?<![" + AR + r"])(?:ال|لل|و|ب|ل|وال|ولل)?" + k + r"(?![" + AR + r"])", text) and v not in out: out.append(v)
    return [d for d in DAY_ORDER if d in out]


def _num(tok: str) -> int | None:
    tok = tok.strip()
    if tok.isdigit(): return int(tok)
    return NUM.get(tok)


def _canon_subject(text: str) -> str | None:
    for s in sorted(SUBJECTS, key=len, reverse=True):
        if re.search(r"(?<![^\W\d_])(?:ال)?" + s + r"(?![^\W\d_])", text): return SUBJECT_CANON.get(s, s)
    return None


def _sections(text: str) -> list[str]:
    """'للسابع ألف وباء وجيم، وللثامن باء' -> ['7أ','7ب','7ج','8ب']; a bare grade gives '7*' (unresolved, must be asked)."""
    t = " " + text.replace("،", " ").replace(",", " ") + " "
    t = re.sub(r"(?<![" + AR + r"])(?:و)?لل", " ال", t)          # للسابع / وللثامن -> السابع / الثامن
    t = re.sub(r"(?<![" + AR + r"])و(?=ال)", " ", t)              # والثامن -> الثامن
    toks = t.split(); out: list[str] = []; i = 0; grade = None
    while i < len(toks):
        tk = toks[i]
        g = None
        for name in sorted(GRADES, key=len, reverse=True):
            parts = name.split()
            if toks[i:i + len(parts)] == parts: g = (GRADES[name], len(parts)); break
        if g:
            grade = g[0]; i += g[1]; got = False
            while i < len(toks):
                x = toks[i]; x2 = x[1:] if x.startswith("و") and x[1:] in LETTERS else x
                if x2 in LETTERS and x != "ه":
                    sec = grade + LETTERS[x2]
                    if sec not in out: out.append(sec)
                    got = True; i += 1
                elif x == "و" and i + 1 < len(toks) and toks[i + 1] in LETTERS: i += 1
                else: break
            if not got: out.append(grade + "*")
            continue
        i += 1
    return out


def _clone(st): return copy.deepcopy({k: v for k, v in st.items() if k != "undo"})


def _teacher_key(st, name: str) -> str | None:
    n = norm(name)
    for t in st["teachers"]:
        if norm(t) == n or norm(t).startswith(n) or n.startswith(norm(t)): return t
    return None


def load_of(st, teacher: str) -> dict[str, int]:
    t = st["teachers"][teacher]
    required = sum((a["per_section"] or 0) * len(a["sections"]) for a in t["assignments"])
    return {"required": required, "assignments": len(t["assignments"])}


def missing(st) -> list[str]:
    m = []
    if not st["days"]: m.append("أيام الدوام غير محددة")
    if not st["periods_per_day"]: m.append("عدد الحصص اليومية غير محدد")
    for n, t in st["teachers"].items():
        if not t["assignments"]: m.append(f"الأستاذ {n}: لا مواد مسندة")
        for a in t["assignments"]:
            if not a["sections"]: m.append(f"الأستاذ {n} - {a['subject']}: الشعب غير محددة")
            elif not a["per_section"]: m.append(f"الأستاذ {n} - {a['subject']}: عدد الحصص لكل شعبة غير محدد")
            if any(s.endswith("*") for s in a["sections"]): m.append(f"الأستاذ {n} - {a['subject']}: الشعبة غير محددة للصف")
    return m


def _teacher_from(st, text: str, create: bool):
    m = re.search(r"(?:الاستاذه|الاستاذ|استاذه|استاذ|المعلمه|المعلم|معلم|مس)\s+([^\W\d_]+)", text)
    name = None
    if m:
        name = m.group(1)
        if name in ("ال",): name = None
    if not name:  # "نبيل بيدرس ..." / "خالد عنده"
        m2 = re.match(r"^(?:نبيل،?\s*)?([^\W\d_]+)\s+(?:بيدرس|يدرس|بتدرس|تدرس)", text)
        if m2: name = m2.group(1)
    if not name: return None
    key = _teacher_key(st, name)
    if key: return key
    if create:
        st["teachers"][name] = {"free": {}, "assignments": []}
        return name
    return None


def _free_clause(st, teacher, text, log, mode):
    day = _days_in(text)
    if not day: return False
    text = re.sub(r"(?:،\s*)?(?:مش|مو|وليس|ليس|مش)\s+\S+(?:\s+حص\w+)?", " ", text)   # drop the negated alternative ("مش حصتين")
    m = re.search(r"اول\s+(\w+)\s*(?:حصص|حصه|حصتين)?", text)
    n = 1
    if re.search(r"حصتين", text): n = 2
    elif m and _num(m.group(1)): n = _num(m.group(1))
    if re.search(r"اول\s+حصه(?!\s*\w*\s*حصه)", text) and not re.search(r"حصتين", text): n = 1
    t = st["teachers"][teacher]
    for d in day:
        old = t["free"].get(d, [])
        new = list(range(1, n + 1)) if mode == "replace" else sorted(set(old) | set(range(1, n + 1)))
        t["free"][d] = new
        log.append({"type": "free_" + mode, "target": f"{teacher}/{d}", "old": old, "new": new, "reason": "وقت فراغ المعلم (لا تدريس)", "clarity": "clear", "valid": True})
    return True


def apply(state: dict[str, Any], text: str) -> dict[str, Any]:
    """Apply one utterance (may hold several clauses). Returns {state, changes, questions, answer}."""
    st = copy.deepcopy(state or new_state())
    st.setdefault("undo", []); st.setdefault("log", []); st.setdefault("context", {"teacher": None})
    changes: list[dict] = []; questions: list[str] = []; answers: list[str] = []
    snapshot = _clone(st)
    clauses = [c.strip(" ،") for c in re.split(r"[.\n]+|\s*،\s*(?=و?(?:خلي|ضيف|شيل|احذف|الغ|عدل|غير|رجع|ارجع|فرجيني|قديش|شو)\b)|\s+و(?=(?:خلي|ضيف|شيل|احذف|الغ|عدل|غير|رجع|فرجيني|قديش|شو)\b)", norm(text).replace("،", "،")) if c and c.strip(" ،")]
    for clause in clauses:
        c = clause
        if re.search(r"^(?:لا\s*)?(?:تراجع|ارجع عن|رجع (?:اخر|القيمه)|رجعلي اخر)", c) or re.search(r"(?:ارجع|رجع|تراجع)\w*\s+(?:عن\s+)?(?:اخر|القيمه السابقه)", c):
            if not st["undo"]: answers.append("لا يوجد تعديل للتراجع عنه."); continue
            prev = st["undo"].pop(); keep = st["undo"]; st.clear(); st.update(prev); st["undo"] = keep
            st["log"].append({"type": "undo", "target": "last", "reason": "تراجع بطلب المدير", "clarity": "clear", "valid": True}); changes.append({"type": "undo"}); continue
        if re.search(r"(?:قديش|كم)\s+(?:صار\s+)?(?:نصاب|حصص)", c) or re.search(r"شو (?:بعد )?ناقص", c):
            if re.search(r"نصاب", c):
                t = _teacher_from(st, c, False) or st["context"].get("teacher")
                if t and t in st["teachers"]: l = load_of(st, t); answers.append(f"نصاب {t} المطلوب: {l['required']} حصة أسبوعياً ({l['assignments']} تعيين).")
                else: questions.append("نصاب أي معلم تقصد؟")
            if re.search(r"ناقص", c):
                ms = missing(st); answers.append("الناقص: " + "؛ ".join(ms) if ms else "لا يوجد نقص في البيانات الحالية.")
            continue
        ctx = st["context"]
        if not re.search(r"فراغ|فاضي", c) and not (_days_in(c) and re.search(r"اول", c)): ctx["last"] = None
        # ---- days of work / periods per day
        if re.search(r"دوام|ضيف .*(?:ال?(?:احد|اثنين|ثلاثاء|اربعاء|خميس|جمعه|سبت))|شيل .*(?:ال?(?:احد|اثنين|ثلاثاء|اربعاء|خميس|جمعه|سبت))", c) and not re.search(r"فراغ|عن\s+\w+|للاستاذ|لاستاذ", c):
            ds = _days_in(c)
            if ds:
                if re.search(r"شيل|احذف|الغ|امسح|ما بدي|الا\s", c) and not re.search(r"^(?:عنا|عندنا)", c):
                    old = list(st["days"]); st["days"] = [d for d in st["days"] if d not in ds]
                    changes.append({"type": "days_remove", "target": "days", "old": old, "new": st["days"], "reason": "طلب حذف يوم", "clarity": "clear", "valid": True})
                elif re.search(r"ضيف|زيد|كمان|سجل|حط", c) and st["days"]:
                    old = list(st["days"]); st["days"] = [d for d in DAY_ORDER if d in set(st["days"]) | set(ds)]
                    changes.append({"type": "days_add", "target": "days", "old": old, "new": st["days"], "reason": "إضافة يوم دون المساس بالموجود", "clarity": "clear", "valid": True})
                else:
                    old = list(st["days"]); st["days"] = [d for d in DAY_ORDER if d in ds]
                    changes.append({"type": "days_set", "target": "days", "old": old, "new": st["days"], "reason": "تحديد أيام الدوام", "clarity": "clear", "valid": True})
            m = re.search(r"(?:كل يوم|يوميا|في اليوم)\s+(\w+)\s+حصص?", c)
            if m and _num(m.group(1)):
                old = st["periods_per_day"]; st["periods_per_day"] = _num(m.group(1))
                changes.append({"type": "periods_per_day", "target": "periods_per_day", "old": old, "new": st["periods_per_day"], "reason": "عدد الحصص اليومية", "clarity": "clear", "valid": True})
            if ds or m: continue
        # ---- delete subject / section
        m = re.search(r"(?:احذف|شيل|الغ|امسح)\s+(?:ال?)?(\S+(?:\s+\S+)?)\s+عن\s+(.+)", c)
        if m:
            subj = _canon_subject(m.group(1)); target = m.group(2)
            secs = _sections(target)
            t = _teacher_key(st, re.sub(r"^(?:الاستاذه|الاستاذ|استاذ|استاذه)\s+", "", target.split("،")[0].split(" و")[0].strip())) if not secs else None
            if t and subj:
                before = len(st["teachers"][t]["assignments"])
                st["teachers"][t]["assignments"] = [a for a in st["teachers"][t]["assignments"] if a["subject"] != subj]
                if len(st["teachers"][t]["assignments"]) == before: questions.append(f"لا أجد مادة {subj} عند {t}.")
                else:
                    changes.append({"type": "subject_remove", "target": f"{t}/{subj}", "old": subj, "new": None, "reason": "حذف المادة فقط؛ المعلم وأوقات فراغه باقية", "clarity": "clear", "valid": True}); ctx["teacher"] = t
                continue
            if secs and subj:
                hit = 0
                for tn, tv in st["teachers"].items():
                    for a in tv["assignments"]:
                        if a["subject"] == subj and any(s in a["sections"] for s in secs):
                            a["sections"] = [s for s in a["sections"] if s not in secs]; hit += 1
                if hit: changes.append({"type": "section_remove", "target": f"{subj}/{','.join(secs)}", "old": secs, "new": None, "reason": "إزالة شعبة من المادة فقط", "clarity": "clear", "valid": True})
                else: questions.append(f"لا أجد مادة {subj} مسندة للشعب {'، '.join(secs)}.")
                continue
        # ---- add subject to existing teacher
        m = re.search(r"ضيف\s+(?:لل|ل)?(?:ال)?(?:استاذه|استاذ)\s+(\S+)\s+ماده\s+(.+)", c)
        if m:
            t = _teacher_key(st, m.group(1))
            if not t: questions.append(f"لا أجد معلماً باسم «{m.group(1)}». هل تريد إضافته كمعلم جديد؟"); continue
            subj = _canon_subject(m.group(2))
            if not subj: questions.append("ما المادة؟"); continue
            secs = _sections(m.group(2))
            if not any(a["subject"] == subj for a in st["teachers"][t]["assignments"]):
                st["teachers"][t]["assignments"].append({"subject": subj, "sections": secs, "per_section": None})
                changes.append({"type": "subject_add", "target": f"{t}/{subj}", "old": None, "new": {"sections": secs}, "reason": "مادة جديدة لمعلم موجود (لم يُنشأ معلم جديد)", "clarity": "clear" if secs else "needs_sections", "valid": True})
                if not secs: questions.append(f"لأي شعب يدرّس {t} مادة {subj}؟")
            ctx["teacher"] = t; continue
        # ---- teaching assignment
        m = re.search(r"(?:بيدرس|يدرس|بتدرس|تدرس)\s+(.+)", c)
        if m:
            t = _teacher_from(st, c, True)
            if not t: questions.append("ما اسم المعلم؟"); continue
            subj = _canon_subject(m.group(1))
            if not subj: questions.append(f"ما المادة التي يدرّسها {t}؟"); ctx["teacher"] = t; continue
            secs = _sections(m.group(1))
            ex = next((a for a in st["teachers"][t]["assignments"] if a["subject"] == subj), None)
            if ex:
                old = list(ex["sections"]); ex["sections"] = sorted(set(ex["sections"]) | set(secs)) if re.search(r"كمان|ضيف", c) else secs
                changes.append({"type": "assignment_update", "target": f"{t}/{subj}", "old": old, "new": ex["sections"], "reason": "تحديث شعب المادة", "clarity": "clear", "valid": True})
            else:
                st["teachers"][t]["assignments"].append({"subject": subj, "sections": secs, "per_section": None})
                changes.append({"type": "assignment_add", "target": f"{t}/{subj}", "old": None, "new": secs, "reason": "ربط المعلم بالمادة والشعب", "clarity": "clear" if secs and not any(s.endswith('*') for s in secs) else "needs_sections", "valid": True})
            ctx["teacher"] = t
            if any(s.endswith("*") for s in secs): questions.append("حدّد الشعب (ألف، باء...) للصفوف المذكورة.")
            mp = re.search(r"لكل شعبه\s+(\w+)\s+حصص?", c)
            if mp and _num(mp.group(1)):
                for a in st["teachers"][t]["assignments"]:
                    if a["subject"] == subj: a["per_section"] = _num(mp.group(1))
            continue
        # ---- periods per section ("خلي لكل شعبة خمس حصص" / "خلي الرياضيات خمس حصص")
        m = re.search(r"(?:خلي|خلّي|حط|سجل)\s+(?:لكل شعبه|(?:ال)?(\S+))\s+(\w+)\s+حصص?", c)
        if m:
            n = _num(m.group(2)); t = ctx.get("teacher")
            subj = _canon_subject(m.group(1) or "") if m.group(1) else None
            if not n: questions.append("كم حصة بالضبط؟"); continue
            if not t: questions.append("لأي معلم تقصد؟"); continue
            tgt = [a for a in st["teachers"][t]["assignments"] if (subj is None and a["per_section"] is None) or a["subject"] == subj]
            if not tgt: tgt = [a for a in st["teachers"][t]["assignments"] if subj is None] if subj is None else []
            if not tgt: questions.append("لأي مادة تقصد؟"); continue
            for a in tgt:
                old = a["per_section"]; a["per_section"] = n
                changes.append({"type": "periods_per_section", "target": f"{t}/{a['subject']}", "old": old, "new": n, "reason": "نصاب لكل شعبة من الشعب المذكورة في السياق", "clarity": "clear", "valid": True})
            continue
        # ---- free time (teacher free periods, NOT teaching time)
        if re.search(r"فراغ|فاضي|فاضيه", c) or (ctx.get("last") == "free" and _days_in(c) and re.search(r"اول", c)):
            t = _teacher_from(st, c, False) or ctx.get("teacher")
            if not t: questions.append("فراغ أي معلم؟"); continue
            mode = "replace" if re.search(r"قصدي|مش|فقط|بس", c) else ("add" if re.search(r"كمان|ضيف|زيد", c) else "replace_if_new")
            if mode == "replace_if_new":
                mode = "add"
            if _free_clause(st, t, c, changes, mode): ctx["teacher"] = t; ctx["last"] = "free"
            else: questions.append("أي يوم؟")
            continue
        # ---- unknown clause: never guess
        questions.append(f"لم أفهم: «{clause}». أعد الصياغة أو اكتبها بأسماء الأيام/المعلم/المادة.")
    # validation layer: refuse to commit an invalid state
    problems = _validate(st)
    if problems:
        return {"state": state, "changes": [], "questions": questions + ["رُفض التعديل لأن البيانات صارت غير صالحة: " + "؛ ".join(problems)], "answers": answers}
    effective = [ch for ch in changes if ch.get("type") != "undo" or True]
    if changes and not any(ch["type"] == "undo" for ch in changes):
        st["undo"].append(snapshot); st["undo"] = st["undo"][-30:]
    st["log"].extend(changes); st["log"] = st["log"][-200:]
    return {"state": st, "changes": effective, "questions": questions, "answers": answers}


def _validate(st) -> list[str]:
    p = []
    for n, t in st["teachers"].items():
        seen = set()
        for a in t["assignments"]:
            if a["subject"] in seen: p.append(f"{n}: مادة {a['subject']} مكررة")
            seen.add(a["subject"])
            if a["per_section"] is not None and not (1 <= a["per_section"] <= 20): p.append(f"{n}: عدد حصص غير معقول")
        if st["periods_per_day"]:
            for d, ps in t["free"].items():
                if any(x > st["periods_per_day"] for x in ps): p.append(f"{n}: فراغ يتجاوز عدد حصص اليوم")
    return p
