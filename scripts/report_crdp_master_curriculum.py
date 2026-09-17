import json, sys
from pathlib import Path

p = Path(sys.argv[1] if len(sys.argv) > 1 else "app/static/crdp_master_curriculum_index.json")
d = json.loads(p.read_text(encoding="utf-8"))
print(json.dumps(d.get("coverage", {}), ensure_ascii=False, indent=2))
for grade, gnode in d.get("catalog", {}).items():
    subjects = gnode.get("subjects", {})
    n = 0
    for snode in subjects.values():
        for lnode in snode.get("languages", {}).values():
            n += len(lnode.get("lessons", []))
    print(f"{grade}: {n} lessons | {', '.join(subjects.keys()) if subjects else 'NO DATA'}")
