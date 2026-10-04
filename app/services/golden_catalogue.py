def _catalogue(grade, subject, language="", branch=""):
    gn, sc, bc, lc = _grade(grade), _subject(subject), _branch(branch), _lang(language)
    out = []
    if not gn or not sc:
        return out
    for row in _registry_rows():
        m = _meta(row["lesson_id"])
        if not m:
            continue
        # مطابقة الصف والمادة بدقة لكي تظهر دروس الصف المختار فقط
        if m["grade"] and gn and m["grade"] != gn:
            continue
        if m["subject"] and sc and m["subject"] != sc:
            continue
        if bc and m["branch"] and m["branch"] != bc:
            continue
        rl = m["language"] or _lang(row.get("language"))
        if lc and rl and lc != rl:
            continue
        out.append({k: row[k] for k in ("lesson_id", "title", "version", "language", "golden")})
    return out
