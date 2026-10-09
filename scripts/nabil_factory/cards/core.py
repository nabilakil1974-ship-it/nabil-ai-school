from __future__ import annotations

# ==============================================================================
# GOLDEN REFERENCE RENDERER CONTRACT — CONTENT-AGNOSTIC
# ==============================================================================
# This is the visual/interaction contract distilled from the approved golden
# reference lesson.  It contains NO lesson-specific science.  Scientific data
# comes only from Evidence Map -> audited narrative/solution -> verified lab.
REFERENCE_RENDERER_CONTRACT = "NABIL_REFERENCE_RENDERER_V1"
REFERENCE_RENDERER_LANGUAGES = ("ar", "en", "fr")
REFERENCE_MOBILE_VIEWPORT = (390, 844)



# ==============================================================================
# 4. MATHEMATICAL RENDERING ENGINE (PURE PLAIN-TEXT MATHJAX URL)
# ==============================================================================
class MathRenderingEngine:
    @staticmethod
    def render_inline(expr: str) -> str:
        return f"\\({expr.strip()}\\)"

    @staticmethod
    def render_display(expr: str) -> str:
        return f"\\[\n{expr.strip()}\n\\]"

    @staticmethod
    def normalize_math(text: str, source_page: int, bbox: List[float], image_ref: str) -> Tuple[str, bool, List[Dict[str, Any]]]:
        if not text:
            return text, True, []

        verified = True
        math_records = []

        for m in re.finditer(r'(?<!\w)(\d+|[a-zA-Z])\s*/\s*(\d+|[a-zA-Z])(?!\w)', text):
            math_records.append({
                "raw": m.group(0),
                "raw_source_text": text,
                "normalized_math": f"\\frac{{{m.group(1)}}}{{{m.group(2)}}}",
                "latex": f"\\frac{{{m.group(1)}}}{{{m.group(2)}}}",
                "verified": True,
                "source_page": source_page,
                "source_bbox": bbox,
                "source_image_ref": image_ref,
                "verification_status": "VERIFIED"
            })

        for m in re.finditer(r'\b([a-zA-Z])\s*=\s*([^,\n\.]+)', text):
            raw_eq = m.group(0)
            is_balanced = raw_eq.count('(') == raw_eq.count(')') and raw_eq.count('{') == raw_eq.count('}')
            status = "VERIFIED" if is_balanced else "MATH_EXPRESSION_UNVERIFIED"
            math_records.append({
                "raw": raw_eq,
                "raw_source_text": text,
                "normalized_math": f"{m.group(1)} = {m.group(2).strip()}",
                "latex": f"{m.group(1)} = {m.group(2).strip()}",
                "verified": is_balanced,
                "source_page": source_page,
                "source_bbox": bbox,
                "source_image_ref": image_ref,
                "verification_status": status
            })
            if not is_balanced:
                verified = False

        try:
            text = re.sub(r'\(\s*([^()]+)\s*\)\s*/\s*\(\s*([^()]+)\s*\)', r'\\(\\frac{\1}{\2}\\)', text)
            text = re.sub(r'(?<!\w)(\d+|[a-zA-Z])\s*/\s*(\d+|[a-zA-Z])(?!\w)', r'\\(\\frac{\1}{\2}\\)', text)
            text = re.sub(r'\bsqrt\s*\(\s*([^()]+)\s*\)', r'\\(\\sqrt{\1}\\)', text)
            text = re.sub(r'\broot\[\s*(\d+)\s*\]\s*\(\s*([^()]+)\s*\)', r'\\(\\sqrt[\1]{\2}\\)', text)
            text = re.sub(r'\blim_\{\s*([^}]+)\s*\}', r'\\(\\lim_{\1}\\)', text)
            text = re.sub(r'\bint\s+([^$]+?)\s+d([a-zA-Z])\b', r'\\(\\int \1 \\, d\2\\)', text)
            text = re.sub(r'\bvec\(\s*([a-zA-Z]{1,2})\s*\)', r'\\(\\vec{\1}\\)', text)
            text = re.sub(r'\b(cm|m|mm|kg|g|s|mol|N|J|W|Pa)3\b', r'\1\\(^3\\)', text)
            text = re.sub(r'\b(cm|m|mm|kg|g|s|mol|N|J|W|Pa)2\b', r'\1\\(^2\\)', text)
            text = re.sub(r'\b([a-zA-Z])\^(\d+|\{[^}]+\})', r'\1\\(^{\2}\\)', text)
            text = re.sub(r'\b([A-Z][a-z]?)(\d+)\b', r'\1\\(_{\2}\\)', text)
            text = re.sub(r'\s*->\s*', r' \\(\\rightarrow\\) ', text)
        except Exception:
            verified = False

        return text, verified, math_records

    @staticmethod
    def inject_mathjax_head() -> str:
        return '''<script>
window.MathJax = {
  tex: { inlineMath: [['\\\\(', '\\\\)']], displayMath: [['\\\\[', '\\\\]']], processEscapes: true },
  options: { renderActions: { addMenu: [] } },
  chtml: { scale: 0.95 }
};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
'''



# ==============================================================================
# PREBUILT FULL-PAGE AR / EN / FR TRANSLATION
# ==============================================================================
def _looks_like_formula_only(value: str) -> bool:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if not text:
        return True
    letters = re.findall(r"[A-Za-zÀ-ÿ\u0600-\u06ff]", text)
    operators = re.findall(r"[=+\-×÷*/^∠⊥≅≤≥<>√∞]", text)
    # Mathematical labels/formulas stay canonical and are never sent through
    # translation. This protects point labels, equations and symbolic results.
    return bool(operators) and len(letters) <= max(5, len(text) // 5)


def _is_translatable_display_string(value: str) -> bool:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if len(text) < 2 or len(text) > 1200:
        return False
    if _looks_like_formula_only(text):
        return False
    if "://" in text or text.startswith(("#", ".", "/", "{", "}", "[", "]")):
        return False
    if re.search(r"</?[A-Za-z][^>]*>", text):
        return False
    if re.fullmatch(r"[A-Za-z0-9_.:/#-]+", text):
        # Keep human one-word labels, reject ids/paths/camelCase/code tokens.
        if any(ch in text for ch in "_./:#") or re.search(r"[a-z][A-Z]", text):
            return False
        if "-" in text and text.lower() not in {"step-by-step"}:
            return False
    if not re.search(r"[A-Za-zÀ-ÿ\u0600-\u06ff]", text):
        return False
    return True


def _extract_translation_candidates(markup: str) -> List[str]:
    """Collect static/dynamic display strings using Python stdlib only."""
    from html.parser import HTMLParser

    ordered: List[str] = []
    seen = set()
    script_chunks: List[str] = []

    def add(value):
        text = re.sub(r"\s+", " ", str(value or "")).strip()
        if text and text not in seen and _is_translatable_display_string(text):
            seen.add(text)
            ordered.append(text)

    class Collector(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.skip_depth = 0
            self.in_script = False

        def handle_starttag(self, tag, attrs):
            lower = tag.lower()
            if lower == "script":
                self.in_script = True
                return
            if lower in {"style", "noscript"}:
                self.skip_depth += 1
                return
            if self.skip_depth == 0:
                amap = dict(attrs)
                for attr in ("title", "placeholder", "aria-label"):
                    add(amap.get(attr))

        def handle_endtag(self, tag):
            lower = tag.lower()
            if lower == "script":
                self.in_script = False
            elif lower in {"style", "noscript"} and self.skip_depth:
                self.skip_depth -= 1

        def handle_data(self, data):
            if self.in_script:
                script_chunks.append(data)
            elif self.skip_depth == 0:
                add(data)

    parser = Collector()
    parser.feed(markup)
    parser.close()

    # Labs/whole-lesson/proof engines keep some display strings in JS data and
    # reveal them later. Include human-readable literals so the runtime
    # MutationObserver translates those dynamic updates too.
    source = "\n".join(script_chunks)
    for match in re.finditer(r'"((?:\\.|[^"\\])*)"', source):
        raw = match.group(1)
        try:
            value = json.loads('"' + raw + '"')
        except Exception:
            value = raw.replace('\\"', '"').replace("\\n", " ")
        add(value)
    for match in re.finditer(r"'((?:\\.|[^'\\])*)'", source):
        raw = match.group(1)
        if "\\" in raw and not re.search(r"\\[nrt'\\]", raw):
            continue
        add(raw.replace("\\'", "'").replace("\\n", " "))
    return ordered

def _translation_integrity_tokens(value: str) -> Tuple[List[str], List[str]]:
    text = str(value or "")
    numbers = re.findall(r"(?<![\w])[-+]?\d+(?:[.,]\d+)?(?:%|°)?", text)
    protected = re.findall(
        r"(?:[A-Z][A-Za-z]?\d{0,3}|[A-Z]{1,4}\d*|"
        r"[A-Za-z]\d*[₀₁₂₃₄₅₆₇₈₉]*|"
        r"Ω|V|A|mA|kΩ|kg|g|m|cm|mm|s|ms|mol|Pa|N|J|W|Hz)"
        r"(?=\b|[^A-Za-zÀ-ÿ])",
        text,
    )
    return numbers, protected


_TRANSLATION_LOCK_RE = re.compile(
    r"(?<![\\w])[-+]?\\d+(?:[.,]\\d+)?(?:%|°)?"
    r"|(?:[A-Z][A-Za-z]?\\d{0,3}|[A-Z]{1,4}\\d*|"
    r"[A-Za-z]\\d*[₀₁₂₃₄₅₆₇₈₉]*|"
    r"Ω|V|A|mA|kΩ|kg|g|m|cm|mm|s|ms|mol|Pa|N|J|W|Hz)"
    r"(?=\\b|[^A-Za-zÀ-ÿ])"
)


def _lock_scientific_translation_tokens(value: str, item_id: str):
    text = str(value or "")
    # Lock scientific tokens only when the string is actually mathematical/
    # scientific. Plain prose is left untouched.
    if not re.search(r"[=+\\-×÷*/^∠⊥≅Ω₀₁₂₃₄₅₆₇₈₉]|\\d", text):
        return text, []
    locks = []
    def repl(match):
        key = f"__NABIL_LOCK_{item_id}_{len(locks):03d}__"
        locks.append((key, match.group(0)))
        return key
    return _TRANSLATION_LOCK_RE.sub(repl, text), locks


def _restore_scientific_translation_tokens(
        translated: str, locks: List[Tuple[str, str]],
        target_lang: str, item_id: str) -> str:
    value = str(translated or "")
    for key, original in locks:
        if value.count(key) != 1:
            raise RuntimeError(
                f"PAGE_TRANSLATION_LOCK_CHANGED:{target_lang}:{item_id}")
        value = value.replace(key, original)
    return value


def _translate_strings_batch(
        strings: List[str], source_lang: str, target_lang: str,
        purpose: str) -> Dict[str, str]:
    if target_lang == source_lang:
        return {value: value for value in strings}
    if not strings:
        return {}
    target_name = {"ar": "Modern Standard Arabic", "en": "English",
                   "fr": "French"}[target_lang]
    source_name = {"ar": "Modern Standard Arabic", "en": "English",
                   "fr": "French"}.get(source_lang, source_lang)
    output: Dict[str, str] = {}
    batch_size = 55
    for start in range(0, len(strings), batch_size):
        batch = strings[start:start + batch_size]
        items = []
        lock_maps = {}
        for i, value in enumerate(batch):
            item_id = str(start + i)
            wire_text, locks = _lock_scientific_translation_tokens(
                value, item_id)
            items.append({"id": item_id, "text": wire_text})
            lock_maps[item_id] = locks
        prompt = (
            "You are a strict translation-only engine for a school lesson. "
            f"Translate each item from {source_name} to {target_name}. "
            "Do not add, omit, explain, simplify or correct scientific content. "
            "Preserve every number exactly as written. Preserve mathematical "
            "expressions, point/segment labels, variable names, chemical formulas, "
            "units and standard symbols exactly. Any token shaped like "
            "__NABIL_LOCK_000_000__ is immutable: copy it byte-for-byte, "
            "exactly once, in the translated item. Keep NABIL as NABIL. "
            "Use clear school-level Modern Standard Arabic when target is Arabic. "
            "Return strict JSON exactly as {\"items\":[{\"id\":\"...\",\"text\":\"...\"}]}. "
            "The item count and ids must match.\nITEMS:\n" +
            json.dumps(items, ensure_ascii=False)
        )
        result = _execute_llm_json_strict(
            prompt,
            purpose=f"{purpose}_{target_lang}_{start}",
            max_attempts=3,
        )
        translated = result.get("items") if isinstance(result, dict) else None
        if not isinstance(translated, list) or len(translated) != len(items):
            raise RuntimeError(
                f"PAGE_TRANSLATION_SCHEMA_INVALID:{target_lang}:{start}")
        by_id = {
            str(row.get("id")): str(row.get("text") or "").strip()
            for row in translated if isinstance(row, dict)
        }
        for item in items:
            item_id = item["id"]
            source = batch[int(item_id) - start]
            value = by_id.get(item_id, "")
            if not value:
                raise RuntimeError(
                    f"PAGE_TRANSLATION_EMPTY:{target_lang}:{item_id}")
            value = _restore_scientific_translation_tokens(
                value, lock_maps.get(item_id, []),
                target_lang, item_id)
            src_numbers, src_protected = _translation_integrity_tokens(source)
            dst_numbers, dst_protected = _translation_integrity_tokens(value)
            if src_numbers != dst_numbers:
                raise RuntimeError(
                    f"PAGE_TRANSLATION_NUMBER_CHANGED:{target_lang}:{item['id']}")
            # Protected token order may contain ordinary one-letter words in
            # prose. Enforce exact preservation only when the source looks
            # mathematical/scientific enough to make those tokens meaningful.
            if (
                re.search(r"[=+\-×÷*/^∠⊥≅Ω₀₁₂₃₄₅₆₇₈₉]", source)
                and src_protected != dst_protected
            ):
                # Locked transport should make this unreachable. If a provider
                # still mutates a scientific token, fail only this translation
                # item with an explicit diagnostic instead of silently changing
                # mathematics.
                raise RuntimeError(
                    f"PAGE_TRANSLATION_SYMBOL_CHANGED:{target_lang}:{item_id}")
            if target_lang == "ar":
                _assert_formal_arabic_text(
                    value, purpose=f"{purpose}_ar_{item['id']}")
            output[source] = value
    return output


def build_trilingual_page_translation(
        markup: str, source_lang_code: str, purpose: str
        ) -> Tuple[str, Dict[str, Any]]:
    source_lang = (
        source_lang_code if source_lang_code in REFERENCE_RENDERER_LANGUAGES
        else "en"
    )
    candidates = _extract_translation_candidates(markup)
    bundles = {source_lang: {value: value for value in candidates}}
    for target in REFERENCE_RENDERER_LANGUAGES:
        if target == source_lang:
            continue
        bundles[target] = _translate_strings_batch(
            candidates, source_lang, target, purpose)
    if any(len(bundles.get(lang, {})) != len(candidates)
           for lang in REFERENCE_RENDERER_LANGUAGES):
        raise RuntimeError("FULL_PAGE_TRANSLATION_COVERAGE_INCOMPLETE")

    payload = json.dumps(
        {
            "source": source_lang,
            "languages": list(REFERENCE_RENDERER_LANGUAGES),
            "strings": bundles,
        },
        ensure_ascii=False, separators=(",", ":"),
    ).replace("</", "<\\/")

    language_bar = r'''
<div id="nabilPageLanguage" data-nabil-page-language="true"
 style="position:sticky;top:4px;z-index:2147482000;display:flex;gap:6px;
 align-items:center;justify-content:center;flex-wrap:wrap;margin:0 auto 8px;
 width:max-content;max-width:100%;background:#061725;border:1px solid #2b6485;
 border-radius:13px;padding:6px 8px;box-shadow:0 7px 22px #0007;direction:ltr">
 <span aria-hidden="true">🌐</span>
 <button type="button" data-nabil-lang="ar" style="min-height:40px">العربية</button>
 <button type="button" data-nabil-lang="en" style="min-height:40px">English</button>
 <button type="button" data-nabil-lang="fr" style="min-height:40px">Français</button>
</div>
'''
    runtime = r'''
<script id="nabilPageTranslationRuntime">
(()=>{
"use strict";
const data=JSON.parse(document.getElementById("nabilPageTranslationBundle").textContent);
const source=data.source,strings=data.strings||{},langs=data.languages||["ar","en","fr"];
const originals=new WeakMap();
const reverse={};
langs.forEach(lang=>{reverse[lang]=new Map(Object.entries(strings[lang]||{}).map(([a,b])=>[String(b),a]))});
function trimmedParts(v){const m=String(v||"").match(/^(\s*)([\s\S]*?)(\s*)$/);return m||["","","",""]}
function baseFor(value){
 const t=String(value||"").trim();if(!t)return "";
 if((strings[source]||{})[t]!==undefined)return t;
 for(const lang of langs){const hit=reverse[lang]?.get(t);if(hit!==undefined)return hit}
 return t;
}
function translateNode(node,lang){
 if(!node||node.nodeType!==Node.TEXT_NODE)return;
 const p=node.parentElement;if(!p||["SCRIPT","STYLE","NOSCRIPT"].includes(p.tagName))return;
 const parts=trimmedParts(node.nodeValue),current=parts[2];if(!current)return;
 let base=originals.get(node);
 const inferred=baseFor(current);
 if(!base||(strings[source]||{})[inferred]!==undefined&&current!==((strings[lang]||{})[base]||base)){
   base=inferred;originals.set(node,base);
 }
 const out=(strings[lang]||{})[base];
 if(out!==undefined&&current!==out)node.nodeValue=parts[1]+out+parts[3];
}
function translateAttrs(root,lang){
 (root.querySelectorAll?.("[title],[placeholder],[aria-label]")||[]).forEach(el=>{
  ["title","placeholder","aria-label"].forEach(attr=>{
   if(!el.hasAttribute(attr))return;
   const key="__nabilBase_"+attr.replace("-","_");
   let base=el.dataset[key]||baseFor(el.getAttribute(attr));
   el.dataset[key]=base;
   const out=(strings[lang]||{})[base];if(out!==undefined)el.setAttribute(attr,out);
  })
 })
}
const frameObservers=new WeakMap();
function translateRoot(root,lang){
 if(!root)return;
 const walker=(root.ownerDocument||document).createTreeWalker(root,NodeFilter.SHOW_TEXT);
 const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
 nodes.forEach(n=>translateNode(n,lang));translateAttrs(root,lang);
}
function watchFrame(frame){
 try{
  const doc=frame.contentDocument;if(!doc?.body)return;
  translateRoot(doc.body,current);
  if(frameObservers.has(frame))frameObservers.get(frame).disconnect();
  const obs=new MutationObserver(records=>{
   if(applying)return;applying=true;
   for(const rec of records){
    if(rec.type==="characterData")translateNode(rec.target,current);
    for(const added of rec.addedNodes||[]){
     if(added.nodeType===Node.TEXT_NODE)translateNode(added,current);
     else if(added.nodeType===Node.ELEMENT_NODE)translateRoot(added,current);
    }
   }
   applying=false;
  });
  obs.observe(doc.body,{subtree:true,childList:true,characterData:true});
  frameObservers.set(frame,obs);
 }catch(_e){}
}
function translateFrames(lang){
 document.querySelectorAll("iframe").forEach(frame=>{
  try{watchFrame(frame)}catch(_e){}
  if(!frame.dataset.nabilTranslationWatch){
   frame.dataset.nabilTranslationWatch="1";
   frame.addEventListener("load",()=>watchFrame(frame));
  }
 })
}
let applying=false,current=source;
function apply(lang){
 if(!langs.includes(lang))lang=source;
 applying=true;current=lang;
 document.documentElement.lang=lang;
 document.documentElement.dir=lang==="ar"?"rtl":"ltr";
 translateRoot(document.body,lang);translateFrames(lang);
 document.querySelectorAll("#nabilPageLanguage [data-nabil-lang]").forEach(b=>{
  const on=b.dataset.nabilLang===lang;b.setAttribute("aria-pressed",String(on));
  b.style.background=on?"#0b84bd":"#153955";b.style.borderColor=on?"#7af3ff":"#426d8b";
 });
 try{localStorage.setItem("nabil.lesson.page.language",lang)}catch(_e){}
 applying=false;
 window.dispatchEvent(new CustomEvent("nabil:page-language-change",{detail:{language:lang}}));
}
document.getElementById("nabilPageLanguage")?.addEventListener("click",e=>{
 const b=e.target.closest("[data-nabil-lang]");if(b)apply(b.dataset.nabilLang)
});
const observer=new MutationObserver(records=>{
 if(applying)return;applying=true;
 for(const rec of records){
  if(rec.type==="characterData")translateNode(rec.target,current);
  for(const added of rec.addedNodes||[]){
   if(added.nodeType===Node.TEXT_NODE)translateNode(added,current);
   else if(added.nodeType===Node.ELEMENT_NODE){
    translateRoot(added,current);
    if(added.tagName==="IFRAME")watchFrame(added);
    else added.querySelectorAll?.("iframe").forEach(watchFrame);
   }
  }
 }
 applying=false;
});
observer.observe(document.body,{subtree:true,childList:true,characterData:true});
let initial=source;try{const saved=localStorage.getItem("nabil.lesson.page.language");if(langs.includes(saved))initial=saved}catch(_e){}
apply(initial);
window.NABILPageLanguage={
 apply,get:()=>current,source,
 translateText:(value,lang=current)=>{
  const raw=String(value||""),base=baseFor(raw.trim());
  const out=(strings[lang]||{})[base];
  return out===undefined?raw:out;
 }
};
})();
</script>
'''
    bundle_script = (
        '<script id="nabilPageTranslationBundle" type="application/json">'
        + payload + '</script>'
    )
    if "<body" not in markup.lower():
        raise RuntimeError("FULL_PAGE_TRANSLATION_BODY_MISSING")
    markup = re.sub(
        r"(<body[^>]*>)",
        lambda m: (
            m.group(1)
            + '\n<div data-nabil-translation-complete="true" hidden></div>\n'
            + language_bar + bundle_script
        ),
        markup, count=1, flags=re.I,
    )
    markup = re.sub(
        r"</body>", lambda m: runtime + "\n" + m.group(0),
        markup, count=1, flags=re.I,
    )
    report = {
        "source_language": source_lang,
        "languages": list(REFERENCE_RENDERER_LANGUAGES),
        "candidate_strings": len(candidates),
        "translated_counts": {
            lang: len(bundles.get(lang, {}))
            for lang in REFERENCE_RENDERER_LANGUAGES
        },
        "complete": True,
    }
    return markup, report



# ==============================================================================
# 9. TWIN-PAGE HTML COMPILATION
# ==============================================================================
def render_lesson_page_a(entry: dict, theory: dict, ev_map: dict, lab_index: Optional[dict] = None) -> str:
    clean_title = html.escape(re.sub(r'^\s*\d{2,3}\s*(?:--|[-_ ]+)\s*', '', entry["canonical_title"]))
    clean_title = html.escape(re.sub(r'\s+\d{2,3}$', '', clean_title).strip())
    lang = entry.get("language", "en")
    page_a_lang_code = resolve_lang_code(lang)

    acts_html = ""
    for act in theory["activities"]:
        q = act.get("student_question")
        question_html = ""
        if q:
            opts = "".join([
                f'<button onclick="gradeStep(this, {i == q["correct_index"]}, '
                f'\'{html.escape(q["feedback"])}\')" class="q-opt">'
                f'{html.escape(o)}</button>'
                for i, o in enumerate(q["options"])
            ])
            question_html = f'''
          <div style="background:#f1f5f9; padding:12px; border-radius:6px; margin-top:12px;">
            <div style="font-weight:600; font-size:14px; margin-bottom:8px;">{ui_t(page_a_lang_code, "check_understanding")}: {html.escape(q["q"])}</div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">{opts}</div>
            <div class="step-fb" style="margin-top:8px; font-size:13px; font-weight:600; display:none;"></div>
          </div>'''
        flow_labels = {
            "ar": {
                "phenomenon": "👀 شوف",
                "investigation": "🖐️ جرّب",
                "observation": "🔎 لاحظ",
                "interpretation": "💡 فكّر",
                "conclusion": "✅ استنتج",
            },
            "fr": {
                "phenomenon": "👀 Observe",
                "investigation": "🖐️ Essaie",
                "observation": "🔎 Remarque",
                "interpretation": "💡 Réfléchis",
                "conclusion": "✅ Conclus",
            },
            "en": {
                "phenomenon": "👀 See",
                "investigation": "🖐️ Try",
                "observation": "🔎 Notice",
                "interpretation": "💡 Think",
                "conclusion": "✅ Conclude",
            },
        }.get(page_a_lang_code, {})
        generated_rows = []
        for field in (
            "phenomenon",
            "investigation",
            "observation",
            "interpretation",
            "conclusion",
        ):
            value = str(act.get(field) or "").strip()
            if value:
                label = flow_labels.get(field, field.title())
                generated_rows.append(
                    '<div class="nabil-flow-row ' + ('nabil-conclude' if field == 'conclusion' else '') + '" data-step="' + html.escape(field) + '">'
                    '<b>' + html.escape(label) + ':</b> ' + html.escape(value) + '</div>'
                )
        apply_text = str(act.get("student_question") or "").strip()
        if apply_text:
            apply_label = {"ar":"✍️ طبّق","fr":"✍️ Applique","en":"✍️ Apply"}.get(page_a_lang_code,"✍️ Apply")
            generated_rows.append(
                '<div class="nabil-flow-row nabil-apply" data-step="application"><b>'
                + html.escape(apply_label) + ':</b> ' + html.escape(apply_text) + '</div>'
            )
        generated_html = "".join(generated_rows)
        concept_badge = {"ar":"بطاقة فكرة","fr":"Carte concept","en":"Concept Card"}.get(page_a_lang_code,"Concept Card")
        analysis_label = {"ar":"📘 الشرح","fr":"📘 Explication","en":"📘 Explanation"}.get(page_a_lang_code,"📘 Explanation")
        visual_label = {"ar":"🧪 الرسم والمختبر","fr":"🧪 Visuel et laboratoire","en":"🧪 Visual & Lab"}.get(page_a_lang_code,"🧪 Visual & Lab")
        teacher_note = {"ar":"شاهد، جرّب، لاحظ، فكّر، استنتج، ثم طبّق.","fr":"Observe, essaie, remarque, réfléchis, conclus puis applique.","en":"See, Try, Notice, Think, Conclude, then Apply."}.get(page_a_lang_code,"See, Try, Notice, Think, Conclude, then Apply.")
        acts_html += f"""
        <section class="nabil-sci-card nabil-concept-card" data-nabil-concept-id="{html.escape(str(act["concept_id"]))}">
          <div class="nabil-sci-top">
            <div><div class="nabil-sci-brand">NABIL AI | منصة نبيل التعليمية الذكية</div>
            <h2 class="nabil-sci-title">{act["activity_num"]}. {html.escape(act["title"])}</h2></div>
            <div class="nabil-sci-badge">{html.escape(concept_badge)}</div>
          </div>
          <div class="nabil-sci-grid">
            <div class="nabil-sci-panel nabil-sci-analysis"><h3>{html.escape(analysis_label)}</h3>{generated_html}</div>
            <div class="nabil-sci-panel nabil-sci-visual"><h3>{html.escape(visual_label)}</h3>
              <div class="nabil-sci-visual-stage">{act["visual_html"]}{act.get("lab_html","")}</div>
            </div>
            <div class="nabil-sci-panel nabil-sci-teacher-panel"><div class="nabil-sci-teacher">
              <img class="nabil-sci-avatar" src="/static/nabil-profile.jpg" alt="NABIL AI" onerror="this.style.display='none'">
              <div><strong>NABIL AI</strong><p>{html.escape(teacher_note)}</p></div>
            </div></div>
          </div>
          <div class="nabil-sci-final"><h3>{html.escape({"ar":"✍️ طبّق وتحقق","fr":"✍️ Applique et vérifie","en":"✍️ Apply & Check"}.get(page_a_lang_code,"✍️ Apply & Check"))}</h3>{question_html}</div>
        </section>"""


    ws_items = ""
    for idx, item in enumerate(theory["worksheet"]):
        opts = "".join([f'<button onclick="gradeWs(this, {i == item["correct_index"]}, \'{html.escape(item["explanation"])}\')" class="q-opt">{html.escape(o)}</button>' for i, o in enumerate(item["options"])])
        ws_items += f'''
        <div class="ws-item" style="margin-bottom:14px; padding:12px; background:#fff; border:1px solid #e2e8f0; border-radius:6px;">
          <div style="font-weight:600; margin-bottom:6px;">{html.escape(ui_t(page_a_lang_code, "question_label"))} {idx+1}: {html.escape(item["question"])}</div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">{opts}</div>
          <div class="ws-fb" style="margin-top:6px; font-size:12px; font-weight:600; display:none;"></div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="{html.escape(lang)}" dir="{html_dir_attr(page_a_lang_code)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="nabil-lesson-id" content="{html.escape(entry['lesson_id'])}">
<meta name="nabil-canonical-title" content="{clean_title}">
<meta name="nabil-grade" content="{entry.get('grade', 7)}">
<meta name="nabil-subject" content="{html.escape(entry.get('subject', 'Physics'))}">
<meta name="nabil-source-book-id" content="{html.escape(entry['book_id'])}">
<meta name="nabil-source-pages" content="{entry['pdf_start_page']}-{entry['pdf_end_page']}">
<meta name="nabil-renderer-contract" content="{REFERENCE_RENDERER_CONTRACT}">
<meta name="nabil-translation-languages" content="ar,en,fr">
<title>{clean_title} - NABIL Universal Engine</title>
{MathRenderingEngine.inject_mathjax_head()}
<script defer src="/static/nabil_browser_tts_v1.js?v=1"></script>\n<script defer src="/static/nabil_lab_voice_v1.js?v=1"></script>\n<script defer src="/static/nabil_scientific_solution_cards_e2e.js?v=4"></script>
<script defer src="/static/nabil_lesson_e2e_runtime_v1.js?v=4"></script>
<script defer src="/static/nabil_smart_lab_bridge_v1.js?v=3"></script>
<style>
{reference_renderer_css()}
#zoomModal {{ display:none; position:fixed; z-index:9999; inset:0; background:rgba(0,0,0,.88); justify-content:center; align-items:center; cursor:zoom-out; }}
#zoomModal img {{ max-width:92%; max-height:92%; border-radius:10px; }}
</style>
</head>
<body>
{_lab_index_script(lab_index or build_prebuilt_lab_index(entry, theory, []))}
<div class="container">
  <div class="header">
    <h1 style="margin:0; font-size:22px;">{clean_title}</h1>
    <div class="header-actions" style="display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;">
      <button type="button" id="nabilExplainWholeLessonLabs" class="nav-btn" style="background:#0f766e;">🧪 {html.escape({"ar":"اشرح الدرس كاملًا بالمختبرات","fr":"Expliquer toute la leçon avec les laboratoires","en":"Explain the whole lesson with labs"}.get(page_a_lang_code,"Explain the whole lesson with labs"))}</button>
      <button type="button" onclick="document.getElementById('goldenReferenceCard')?.scrollIntoView({{behavior:'smooth',block:'start'}})" class="nav-btn" style="background:#7c3aed;">📌 {html.escape({"ar":"البطاقة النهائية","fr":"Carte finale","en":"Final reference card"}.get(page_a_lang_code,"Final reference card"))}</button>
      <button onclick="navigateToExercises()" class="nav-btn">{html.escape(ui_t(page_a_lang_code, "view_exercises"))}</button>
    </div>
  </div>
  {acts_html}
  <div class="card" style="margin-top:24px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h3 style="margin:0; color:#0284c7;">{html.escape(ui_t(page_a_lang_code, "worksheet_title"))}</h3>
      <div id="wsScoreBadge" style="font-size:13px; font-weight:bold; color:#059669;">{html.escape(ui_t(page_a_lang_code, "score_label"))}: 0 / {len(theory['worksheet'])}</div>
    </div>
    <div style="width:100%; background:#e2e8f0; height:6px; border-radius:3px; margin:12px 0;">
      <div id="wsProgressBar" style="width:0%; background:#0284c7; height:6px; border-radius:3px; transition:width 0.3s ease;"></div>
    </div>
    {ws_items}
  </div>
  {theory.get("quiz_html", "")}
  {theory.get("whole_lesson_lab_html", "")}
  {theory.get("reference_card_html", "")}
</div>
<div id="zoomModal" onclick="this.style.display='none'"><img id="zoomImg" src=""></div>
<script>
let answeredCount = 0;
let score = 0;
const totalQuestions = {len(theory['worksheet'])};

function zoomImage(img) {{
  const modal = document.getElementById('zoomModal');
  const modalImg = document.getElementById('zoomImg');
  modal.style.display = 'flex';
  modalImg.src = img.src;
}}

function startNABILWholeLesson() {{
  const lab = document.getElementById('nabilWholeLessonSmartLab');
  if (!lab) return;
  lab.scrollIntoView({{behavior:'smooth', block:'start'}});
  setTimeout(() => {{
    if (window.NABILWholeLessonOrchestrator?.play) {{
      window.NABILWholeLessonOrchestrator.play();
    }} else {{
      document.getElementById('nabilWholePlay')?.click();
    }}
  }}, 280);
}}
document.getElementById('nabilExplainWholeLessonLabs')?.addEventListener('click', startNABILWholeLesson);

function nabilReadFinalCard(){{
  try{{
    const n=document.getElementById('nabilFinalCardSpeech'); if(!n)return;
    const d=JSON.parse(n.textContent||'{{}}'), spoken=String(d.text||'').trim(); if(!spoken)return;
    try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}
    if(window.NABILLessonE2E?.speak){{window.NABILLessonE2E.speak(spoken,d.lang||'en');return;}}
    if('speechSynthesis' in window){{window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(spoken);u.lang=d.lang==='ar'?'ar':d.lang==='fr'?'fr-FR':'en-US';window.speechSynthesis.speak(u);}}
  }}catch(_e){{}}
}}
function nabilStopFinalCard(){{try{{window.NABILLessonE2E?.stopSpeech?.()}}catch(_e){{}}try{{window.speechSynthesis?.cancel?.()}}catch(_e){{}}}}

function navigateToExercises() {{
  const url = new URL(window.location.href);
  if (url.searchParams.has('lesson')) {{
    url.searchParams.set('view', 'exercises');
    window.location.href = url.toString();
  }} else {{
    const cur = window.location.pathname.split('/').pop();
    window.location.href = cur.replace('.html', '--EXERCISES.html');
  }}
}}
function gradeStep(btn, isCorrect, fb) {{
  const box = btn.parentElement.nextElementSibling;
  box.style.display = 'block';
  box.style.color = isCorrect ? '#059669' : '#dc2626';
  box.innerHTML = (isCorrect ? '✓ ' : '✗ ') + fb;
}}
function gradeWs(btn, isCorrect, exp) {{
  const parent = btn.parentElement;
  if (parent.dataset.answered) return;
  parent.dataset.answered = 'true';
  answeredCount++;
  if (isCorrect) score++;

  const box = parent.nextElementSibling;
  box.style.display = 'block';
  box.style.color = isCorrect ? '#059669' : '#dc2626';
  box.innerHTML = (isCorrect ? '{html.escape(ui_t(page_a_lang_code, "ws_correct"))}' : '{html.escape(ui_t(page_a_lang_code, "ws_incorrect"))}') + exp;

  document.getElementById('wsProgressBar').style.width = ((answeredCount / totalQuestions) * 100) + '%';
  document.getElementById('wsScoreBadge').innerText = '{html.escape(ui_t(page_a_lang_code, "score_label"))}: ' + score + ' / ' + totalQuestions;
}}
</script>
</body>
</html>'''



def _deterministic_evidence_reveal_spec(
        evidence_id: str, title: str, source_text: str, lang_code: str) -> dict:
    """No-LLM fallback: a real interactive lab using only supplied evidence."""
    quote = str(source_text or "").strip()[:1200]
    if not quote:
        raise RuntimeError("PREBUILT_LAB_SOURCE_EMPTY")
    return {
        "supported": True,
        "kind": "EVIDENCE_REVEAL",
        "title": str(title or "NABIL Interactive Explanation"),
        "instructions": {
            "ar": "استكشف المعطيات مع نبيل خطوة خطوة.",
            "fr": "Explore les données avec NABIL étape par étape.",
            "en": "Explore the givens with NABIL step by step.",
        }.get(lang_code, "Explore the givens with NABIL step by step."),
        "observation": {
            "ar": "هذا المختبر مبني فقط على المعطيات الموثقة.",
            "fr": "Ce laboratoire utilise uniquement les données vérifiées.",
            "en": "This lab uses only the verified givens.",
        }.get(lang_code, "This lab uses only the verified givens."),
        "evidence_ref": evidence_id,
        "evidence_basis": "text",
        "evidence_quote": quote,
        "items": [{
            "label": str(title or "Verified task"),
            "evidence_quote": quote,
        }],
        "prebuilt": True,
        "teacher_script": [
            {"say": str(title or "Read the verified task."), "target_ids": ["evidence:0"], "action": "point",
             "state_before": {"revealed_index": -1}, "state_after": {"revealed_index": 0},
             "scientific_constraints": ["Use only verified exercise evidence."], "evidence_quote": quote},
            {"say": "Focus on the verified task.", "target_ids": ["evidence:0"], "action": "highlight",
             "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
             "scientific_constraints": ["Use only verified exercise evidence."], "evidence_quote": quote},
            {"say": str(title or "Work from the verified givens."), "target_ids": ["evidence:0"], "action": "explain",
             "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
             "scientific_constraints": ["Do not introduce unsupported givens or relations."], "evidence_quote": quote},
            {"say": "Keep the result tied to the verified task.", "target_ids": ["evidence:0"], "action": "conclude",
             "state_before": {"revealed_index": 0}, "state_after": {"revealed_index": 0},
             "scientific_constraints": ["Do not introduce unsupported givens or relations."], "evidence_quote": quote},
        ],
    }


def prepare_prebuilt_exercise_labs(
        entry: dict, exercises: list, profile: dict, ev_map: dict) -> None:
    """Generate every exercise lab ONCE during lesson production.

    Student runtime never needs an LLM for an indexed exercise. Richer lab
    kinds are attempted from the exact verified prompt; if no richer kind is
    justified, an evidence-only interactive reveal is prebuilt deterministically.
    """
    lang_code = resolve_lang_code(entry.get("language", "en"))
    for ex in exercises:
        evidence_id = str(ex.get("exercise_id") or
                          f"{entry['lesson_id']}-EX-{ex.get('number')}")
        source_text = (
            str(ex.get("exact_source_prompt") or "").strip()
            + "\n"
            + "\n".join(str(x) for x in (ex.get("subquestions") or []))
        ).strip()
        figure_paths = []
        figure_refs = list(ex.get("figure_refs") or [])
        if figure_refs:
            for page_item in ev_map.get("pages_evidence", []):
                if int(page_item.get("page_num") or -1) != int(
                        ex.get("source_page") or -2):
                    continue
                for fig in page_item.get("figures") or []:
                    if (fig.get("figure_id") in figure_refs
                            and fig.get("image_path")
                            and Path(fig["image_path"]).is_file()):
                        figure_paths.append(str(fig["image_path"]))

        figure_image_base64 = None
        if figure_paths:
            from PIL import Image
            pics = []
            for filename in figure_paths[:4]:
                with Image.open(filename) as image:
                    pic = image.convert("RGB")
                    pic.thumbnail((1100, 850))
                    pics.append(pic.copy())
            if pics:
                canvas = Image.new(
                    "RGB",
                    (max(im.width for im in pics),
                     sum(im.height for im in pics) + 8 * (len(pics) - 1)),
                    "white",
                )
                top = 0
                for pic in pics:
                    canvas.paste(pic, (0, top))
                    top += pic.height + 8
                buf = io.BytesIO()
                canvas.save(buf, format="PNG")
                figure_image_base64 = base64.b64encode(
                    buf.getvalue()).decode("ascii")

        pseudo_concept = {
            "concept_id": evidence_id,
            "title": (
                f"{ex.get('section_type', 'EXERCISE')} {ex.get('number', '')}"
            ).strip(),
            "source_page": ex.get("source_page"),
            "raw_text": source_text,
            "normalized_text": source_text,
            "figure_refs": figure_refs,
            "math_records": [],
        }
        minimal_narrative = {
            "phenomenon": "",
            "investigation": "",
            "observation": "",
            "interpretation": "",
            "conclusion": "",
            "distractor_1": "",
            "distractor_2": "",
            "formulas": [],
            "units": [],
            "_scope_audited": True,
        }
        try:
            spec = build_verified_lab_spec(
                entry, pseudo_concept, minimal_narrative, profile,
                figure_image_base64=figure_image_base64,
                vision_context={
                    "lesson_id": entry.get("lesson_id"),
                    "book_id": entry.get("book_id"),
                    "pdf_page": ex.get("source_page"),
                } if figure_image_base64 else None)
        except Exception as exc:
            progress(
                "EXERCISE_RICH_LAB_FALLBACK_TO_PREBUILT_REVEAL",
                exercise_id=evidence_id,
                reason=str(exc)[:240],
            )
            spec = _deterministic_evidence_reveal_spec(
                evidence_id,
                pseudo_concept["title"],
                source_text,
                lang_code,
            )
        if spec.get("supported") is not True:
            spec = _deterministic_evidence_reveal_spec(
                evidence_id,
                pseudo_concept["title"],
                source_text,
                lang_code,
            )
        # Exercise lab provenance is canonicalized to the exercise index key.
        spec["evidence_ref"] = evidence_id
        try:
            lab_html, active = render_verified_lab(
                spec, lang_code, evidence_id)
        except Exception as exc:
            ex["_exercise_render_rejected"] = True
            ex["_exercise_render_rejection_reason"] = str(exc)[:500]
            progress(
                "EXERCISE_DROPPED_LAB_RENDER_FAILED_NOT_LESSON",
                exercise_id=evidence_id, reason=str(exc)[:240])
            continue
        if not active or not lab_html:
            ex["_exercise_render_rejected"] = True
            ex["_exercise_render_rejection_reason"] = (
                f"PREBUILT_EXERCISE_LAB_RENDER_FAILED:{evidence_id}")
            progress(
                "EXERCISE_DROPPED_LAB_RENDER_FAILED_NOT_LESSON",
                exercise_id=evidence_id)
            continue
        ex["_prebuilt_lab_spec"] = spec
        ex["_prebuilt_lab_html"] = lab_html
        ex["_prebuilt_lab_active"] = True
        ex["_prebuilt_lab_key"] = f"exercise:{evidence_id}"
        progress(
            "PREBUILT_EXERCISE_LAB_READY",
            exercise_id=evidence_id,
            kind=spec.get("kind"),
        )


def build_prebuilt_lab_index(entry: dict, theory: dict, exercises: list) -> dict:
    """Serializable concept/exercise/solution lab directory shipped once.

    Contract:
      concept id -> lab key
      exercise id -> solution card -> SAME lab key
    Indexed students never regenerate these labs at runtime.
    """
    concept_labs = []
    for act in theory.get("activities", []):
        spec = act.get("lab_spec") or {}
        key = f"concept:{act.get('concept_id')}"
        concept_labs.append({
            "key": key,
            "artifact": "theory",
            "concept_id": act.get("concept_id"),
            "title": act.get("title"),
            "kind": spec.get("kind"),
            "renderer_contract": REFERENCE_RENDERER_CONTRACT,
            "translation_languages": list(REFERENCE_RENDERER_LANGUAGES),
            "teacher_pointer": "sentence_synced",
            "teaching_mode": (act.get("teaching_signature") or {}).get("mode"),
            "teaching_level": (act.get("teaching_signature") or {}).get("level"),
            "secondary_year_contract": (
                act.get("teaching_signature") or {}
            ).get("secondary_year_contract"),
            "teaching_steps_count": len(act.get("teaching_steps") or []),
            "prebuilt": True,
            "active": bool(act.get("has_active_sim")),
        })
    exercise_labs = []
    for ex in exercises:
        spec = ex.get("_prebuilt_lab_spec") or {}
        key = str(ex.get("_prebuilt_lab_key") or "")
        ex["_solution_lab_key"] = key
        exercise_labs.append({
            "key": key,
            "solution_lab_key": key,
            "artifact": "exercises",
            "exercise_id": ex.get("exercise_id"),
            "number": ex.get("number"),
            "section_type": ex.get("section_type"),
            "kind": spec.get("kind"),
            "renderer_contract": REFERENCE_RENDERER_CONTRACT,
            "translation_languages": list(REFERENCE_RENDERER_LANGUAGES),
            "teacher_pointer": "sentence_synced",
            "prebuilt": True,
            "active": bool(ex.get("_prebuilt_lab_active")),
        })
    return {
        "schema": "nabil-prebuilt-lab-index/v2",
        "renderer_contract": REFERENCE_RENDERER_CONTRACT,
        "lesson_id": entry.get("lesson_id"),
        "grade": entry.get("grade"),
        "subject": entry.get("subject"),
        "translation_languages": list(REFERENCE_RENDERER_LANGUAGES),
        "voice": {
            "engine": "SpeechSynthesis",
            "paid_endpoint": False,
            "male_voice_preferred": True,
            "male_voice_guaranteed": False,
        },
        "mobile_reference_viewport": {
            "width": REFERENCE_MOBILE_VIEWPORT[0],
            "height": REFERENCE_MOBILE_VIEWPORT[1],
        },
        "concept_labs": concept_labs,
        "exercise_labs": exercise_labs,
        "whole_lesson_lab": {
            "key": "lesson:whole",
            "artifact": "theory",
            "renderer_contract": REFERENCE_RENDERER_CONTRACT,
            "concept_keys": [x["key"] for x in concept_labs],
            "teaching_story": True,
            "prebuilt": True,
            "active": bool(theory.get("whole_lesson_lab_active")),
        },
        "runtime_ai_required_for_indexed_labs": False,
    }


def _lab_index_script(lab_index: dict) -> str:
    payload = json.dumps(lab_index, ensure_ascii=False, separators=(",", ":"))
    payload = payload.replace("</", "<\\/")
    return (
        '<script id="nabilLabIndex" type="application/json">'
        + payload + '</script>'
    )


def render_lesson_page_b(entry: dict, exercises: list, profile: dict, ev_map: dict, lab_index: Optional[dict] = None) -> str:
    clean_title = html.escape(re.sub(r'^\s*\d{2,3}\s*(?:--|[-_ ]+)\s*', '', entry["canonical_title"]))
    clean_title = html.escape(re.sub(r'\s+\d{2,3}$', '', clean_title).strip())
    lesson_id = entry["lesson_id"]
    lang = entry.get("language", "en")
    page_b_lang_code = resolve_lang_code(lang)
    connecting_js = ui_t(page_b_lang_code, "connecting_solver")
    verified_js = ui_t(page_b_lang_code, "verified_solution")
    error_js = ui_t(page_b_lang_code, "solution_error")
    network_error_js = ui_t(page_b_lang_code, "network_error")
    final_answer_js = ui_t(page_b_lang_code, "final_answer_label")

    ex_cards = ""
    for ex in exercises:
        ex_num = ex["number"]
        sec_type = ex["section_type"]
        source_origin = ex.get("source_origin", "TEXTBOOK")
        localized_sec_type = (
            ui_t(page_b_lang_code, "exercise_label") if sec_type == "EXERCISE"
            else ui_t(page_b_lang_code, "problem_label") if sec_type == "PROBLEM"
            else sec_type
        )
        if source_origin == "TEXTBOOK":
            provenance_html = (
                '<span style="font-size:12px; color:#059669;">'
                '✓ ' + html.escape({
                    "ar": "موثّق من المصدر",
                    "fr": "Vérifié à la source",
                    "en": "Source verified",
                }.get(page_b_lang_code, "Source verified")) + '</span>'
            )
            card_title = f"{localized_sec_type} {ex_num}"
        else:
            provenance_html = (
                f'<span style="font-size:12px; color:#64748b;">'
                f'{ui_t(page_b_lang_code, "additional_practice_note")}</span>'
            )
            card_title = f"{ui_t(page_b_lang_code, 'additional_practice')} {ex_num}"

        ex_fig_html = ""
        if ex.get("reconstructed_diagram_verified") and ex.get("reconstructed_diagram_svg"):
            note = {
                "ar": "رسم تخطيطي معاد بناؤه من النص الموثق — ليس صورة الكتاب الأصلية",
                "fr": "Schéma reconstruit à partir du texte vérifié — ce n’est pas la figure originale du manuel",
                "en": "Schematic reconstructed from verified text — not the original textbook figure",
            }.get(page_b_lang_code, "Schematic reconstructed from verified text — not the original textbook figure")
            ex_fig_html = (
                '<div style="text-align:center; margin:12px 0;">'
                + str(ex["reconstructed_diagram_svg"])
                + '<div style="font-size:11px;color:#64748b;margin-top:4px;">'
                + html.escape(note) + '</div></div>'
            )
        # Original textbook figure pixels are deliberately not student-facing.
        # A verified NABIL redraw is required when the exercise needs a figure.

        if ex["solution_mode"] == "PRE_SOLVED":
            if ex.get("solution_status") == "OMITTED_UNVERIFIED":
                omitted_note = {
                    "ar": "لم يُعرض الحل الآلي لأن كل ادعاء فيه لم يمكن توثيقه بأمان من نص الدرس/الشكل الأصلي.",
                    "fr": "La solution automatique n'est pas affichée car toutes ses affirmations n'ont pas pu être vérifiées à partir du texte/figure source.",
                    "en": "Automatic solution omitted because every claim could not be safely verified against the lesson text/source figure.",
                }.get(
                    page_b_lang_code,
                    "Automatic solution omitted because every claim could not be safely verified against the lesson text/source figure."
                )
                sol_box = (
                    '<div style="margin-top:10px;padding:12px;background:#fff7ed;'
                    'border:1px solid #fed7aa;border-radius:6px;font-size:13px;'
                    'color:#9a3412;line-height:1.6;">'
                    + html.escape(omitted_note) + '</div>'
                )
            else:
                sol = ex.get("_pre_solved_solution")
                if sol is None:
                    sol = grounded_subject_solver(ex, ev_map, profile)
                    ex["_pre_solved_solution"] = sol
                step_label = ui_t(page_b_lang_code, "step_label")
                steps_html = "<br>".join([
                    f"• <b>{step_label}:</b> {html.escape(str(step))}"
                    for step in sol["steps"]
                ])
                card_spec = build_factory_solution_card_spec(entry, ex, sol)
                card_json = html.escape(
                    json.dumps(card_spec, ensure_ascii=False), quote=True)
                sol_box = f'''
                <div data-nabil-solution-card="{card_json}" style="margin-top:10px;">
                  <div class="nabil-solution-fallback" style="padding:12px; background:#ecfdf5; border-radius:6px; font-size:13px; color:#065f46; line-height:1.6;">
                    {verified_js}<br>
                    {steps_html}<br>
                    • <b>{final_answer_js}:</b> {html.escape(str(sol["final_answer"]))}
                  </div>
                </div>'''
        else:
            solve_label = ui_t(page_b_lang_code, "solve_on_demand", sec=sec_type, num=ex_num)
            sol_box = f'''
            <div id="demandBox_{sec_type}_{ex_num}" style="margin-top:10px;">
              <button onclick="requestServerSolution('{lesson_id}', '{sec_type}', {ex_num})" class="nav-btn" style="background:#475569; padding:8px 14px; font-size:12px;">{html.escape(solve_label)}</button>
              <div id="demandAns_{sec_type}_{ex_num}" style="display:none; margin-top:8px; padding:12px; background:#eff6ff; border-radius:6px; font-size:13px; color:#1e40af; line-height:1.6;"></div>
            </div>'''

        sub_html = ""
        if ex.get("subquestions"):
            sub_items = "".join([f"<li style='margin-top:4px;'>{html.escape(sq)}</li>" for sq in ex["subquestions"]])
            sub_html = f"<ul style='margin:6px 0 0 16px; padding:0; font-size:13px; color:#334155;'>{sub_items}</ul>"

        ex_cards += f'''
        <div class="card nabil-exercise-card" data-nabil-exercise-number="{ex_num}" data-nabil-section-type="{html.escape(sec_type)}" data-nabil-solution-lab-key="{html.escape(str(ex.get("_solution_lab_key") or ex.get("_prebuilt_lab_key") or ""))}" style="margin-top:16px;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0; font-size:16px;">{card_title}</h3>
            {provenance_html}
          </div>
          <p class="nabil-exercise-prompt" style="margin:10px 0; font-size:14px; line-height:1.5;">{html.escape(ex["exact_source_prompt"])}</p>
          <button type="button" class="nabil-explain-lab-btn nav-btn" data-nabil-prebuilt-lab="true" style="background:#0f766e;margin:2px 0 8px;">🧪 {html.escape({"ar":"اشرح هذا التمرين بالمختبر","fr":"Expliquer cet exercice avec un laboratoire","en":"Explain this exercise with a lab"}.get(page_b_lang_code,"Explain this exercise with a lab"))}</button>
          <div class="nabil-prebuilt-exercise-lab" data-lab-key="{html.escape(str(ex.get("_prebuilt_lab_key") or ""))}" hidden>
            {ex.get("_prebuilt_lab_html", "")}
          </div>
          {ex_fig_html}
          {sub_html}
          {sol_box}
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="{html.escape(lang)}" dir="{html_dir_attr(page_b_lang_code)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="nabil-lesson-id" content="{html.escape(entry['lesson_id'])}">
<meta name="nabil-canonical-title" content="{clean_title}">
<meta name="nabil-grade" content="{entry.get('grade', 7)}">
<meta name="nabil-subject" content="{html.escape(entry.get('subject', 'Physics'))}">
<meta name="nabil-source-book-id" content="{html.escape(entry['book_id'])}">
<meta name="nabil-source-pages" content="{entry['pdf_start_page']}-{entry['pdf_end_page']}">
<meta name="nabil-renderer-contract" content="{REFERENCE_RENDERER_CONTRACT}">
<meta name="nabil-translation-languages" content="ar,en,fr">
<title>{clean_title} - Official Exercises</title>
{MathRenderingEngine.inject_mathjax_head()}
<script defer src="/static/nabil_browser_tts_v1.js?v=1"></script>\n<script defer src="/static/nabil_lab_voice_v1.js?v=1"></script>\n<script defer src="/static/nabil_scientific_solution_cards_e2e.js?v=4"></script>
<script defer src="/static/nabil_lesson_e2e_runtime_v1.js?v=4"></script>
<script defer src="/static/nabil_smart_lab_bridge_v1.js?v=3"></script>
<style>
{reference_renderer_css()}
#zoomModal {{ display:none; position:fixed; z-index:9999; inset:0; background:rgba(0,0,0,.88); justify-content:center; align-items:center; cursor:zoom-out; }}
#zoomModal img {{ max-width:92%; max-height:92%; border-radius:10px; }}
</style>
</head>
<body>
{_lab_index_script(lab_index or build_prebuilt_lab_index(entry, {"activities": []}, exercises))}
<div class="container">
  <div class="header">
    <h1 style="margin:0; font-size:20px;">{html.escape(ui_t(page_b_lang_code, "exercises_page_title", title=html.unescape(clean_title)))}</h1>
    <button onclick="returnToLesson()" class="nav-btn" style="background:#475569;">{html.escape(ui_t(page_b_lang_code, "back_to_lesson"))}</button>
  </div>
  {ex_cards}
</div>
<div id="zoomModal" onclick="this.style.display='none'"><img id="zoomImg" src=""></div>
<script>
function zoomImage(img) {{
  const modal = document.getElementById('zoomModal');
  const modalImg = document.getElementById('zoomImg');
  modal.style.display = 'flex';
  modalImg.src = img.src;
}}

function returnToLesson() {{
  const url = new URL(window.location.href);
  if (url.searchParams.has('view')) {{
    url.searchParams.delete('view');
    window.location.href = url.toString();
  }} else {{
    const cur = window.location.pathname.split('/').pop();
    window.location.href = cur.replace('--EXERCISES.html', '.html');
  }}
}}

async function requestServerSolution(lessonId, secType, exNum) {{
  const ansBox = document.getElementById('demandAns_' + secType + '_' + exNum);
  ansBox.style.display = 'block';
  ansBox.innerHTML = '<i>{connecting_js}</i>';

  try {{
    const resp = await fetch('/api/interactive-lessons/solve-on-demand', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ lesson_id: lessonId, section_type: secType, exercise_number: exNum }})
    }});
    const data = await resp.json();
    if (data.status === 'SUCCESS') {{
      const sol = data.solution;
      if (data.solution_card && window.NABILScientificCards?.renderCard) {{
        window.NABILScientificCards.renderCard(data.solution_card, ansBox);
      }} else {{
        let stepsHtml = sol.steps.map(s => '• ' + s).join('<br>');
        ansBox.innerHTML = '{verified_js}' + stepsHtml + '<br><b>{final_answer_js}:</b> ' + sol.final_answer;
      }}
    }} else {{
      ansBox.innerHTML = '{error_js}' + (data.error || 'Unable to retrieve solution');
      ansBox.style.color = '#dc2626';
    }}
  }} catch (err) {{
    ansBox.innerHTML = '{network_error_js}';
    ansBox.style.color = '#dc2626';
  }}
}}
</script>
</body>
</html>'''
