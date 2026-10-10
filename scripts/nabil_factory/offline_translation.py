"""Offline English/French translation, with zero paid API fallback.

Argos Translate language packs must be provisioned once by an operator.
Missing models fail closed rather than substituting the source text.
"""
from __future__ import annotations
import re
from bs4 import BeautifulSoup, NavigableString

class OfflineTranslationUnavailable(RuntimeError):
    pass

SKIP_TAGS = {"script", "style", "code", "pre", "math", "svg", "textarea", "noscript"}
# Preserve MathJax delimiters, numbers and symbols as immutable placeholders.
MATH = re.compile(r"(\\\\\[.*?\\\\\]|\\\\\(.*?\\\\\)|\\$\\$.*?\\$\\$|\\$[^$\\n]+\\$)", re.S)

class HelsinkiOpusTranslator:
    """Commercially permissible Apache-2.0 Marian EN<->FR translation.
    
    Model weights must be downloaded once into a persistent local HF cache.
    Loading uses local_files_only=True: NEVER silently make an internet or API
    call during factory production, and NEVER substitute paid model inference.
    """
    MODELS = {
        ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
        ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
    }

    def __init__(self, source: str, target: str):
        import os
        model_name = self.MODELS.get((source, target))
        if not model_name:
            raise OfflineTranslationUnavailable("OPUS_UNSUPPORTED_LANGUAGE_PAIR")
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        except ImportError as exc:
            raise OfflineTranslationUnavailable("OPUS_DEPENDENCIES_MISSING") from exc
        model_dir = os.getenv("NABIL_OPUS_MODEL_DIR", "").strip()
        local_name = (model_dir + "/" + source + "-" + target) if model_dir else model_name
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(local_name, local_files_only=True)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                local_name, local_files_only=True)
        except Exception as exc:
            raise OfflineTranslationUnavailable("OPUS_MODEL_NOT_PREINSTALLED") from exc
        self.model.eval()

    def translate(self, text: str) -> str:
        import torch
        tokens = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=384)
        with torch.inference_mode():
            output = self.model.generate(**tokens, max_new_tokens=512, num_beams=4)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)


def get_free_translator(source: str, target: str, backend: str = "opus"):
    """Choose explicitly; missing free models never invoke a paid provider."""
    if backend == "opus":
        return HelsinkiOpusTranslator(source, target)
    if backend == "argos":
        return _installed_translator(source, target)
    raise OfflineTranslationUnavailable("UNKNOWN_OFFLINE_BACKEND")


def _installed_translator(src: str, dst: str):
    if src not in ("en", "fr") or dst not in ("en", "fr") or src == dst:
        raise OfflineTranslationUnavailable("EN_FR_ONLY: unsupported translation pair")
    try:
        from argostranslate import translate
    except ImportError as exc:
        raise OfflineTranslationUnavailable("ARGOS_NOT_INSTALLED") from exc
    langs = {lang.code: lang for lang in translate.get_installed_languages()}
    if src not in langs or dst not in langs:
        raise OfflineTranslationUnavailable("ARGOS_LANGUAGE_PACK_MISSING")
    try:
        return langs[src].get_translation(langs[dst])
    except Exception as exc:
        raise OfflineTranslationUnavailable("ARGOS_LANGUAGE_PACK_MISSING") from exc

def translate_scientific_text(text: str, translator) -> str:
    """Translate prose while validating exact restoration of math segments."""
    slots: list[str] = []
    def hold(match):
        slots.append(match.group(0))
        return f" NABILPROTECTEDTOKEN{len(slots)-1}END "
    masked = MATH.sub(hold, text)
    translated = translator.translate(masked)
    if not isinstance(translated, str):
        raise OfflineTranslationUnavailable("INVALID_TRANSLATION_OUTPUT")
    for i, exact in enumerate(slots):
        marker = f"NABILPROTECTEDTOKEN{i}END"
        if translated.count(marker) != 1:
            raise OfflineTranslationUnavailable("MATHEMATICAL_TOKEN_CHANGED")
        translated = translated.replace(marker, exact)
    if slots and any("NABILPROTECTEDTOKEN" in part for part in translated.split()):
        raise OfflineTranslationUnavailable("UNRESOLVED_MATH_PROTECTION")
    return translated

def translate_html_offline(html: str, source: str, target: str, translator=None) -> tuple[str, dict]:
    """Translate student-visible HTML text. JS-driven boards require separate QA.

    Does not rewrite scripts, JSON, element attributes or math; such fields
    must not be claimed translated by a full-page translation gate.
    """
    if source == target:
        return html, {"mode":"original", "complete":True, "languages":[source], "translated_nodes":0}
    tr = translator if translator is not None else _installed_translator(source, target)
    soup = BeautifulSoup(html, "html.parser")
    count = 0
    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or not node.strip():
            continue
        if any(tag.name in SKIP_TAGS or tag.has_attr("data-no-translate")
               for tag in node.parents if getattr(tag, "name", None)):
            continue
        translated = translate_scientific_text(str(node), tr)
        node.replace_with(translated)
        count += 1
    return str(soup), {"mode":"offline_argos", "complete":False,
                       "languages":[source, target], "translated_nodes":count,
                       "reason":"JS_BOARD_AND_ATTRIBUTES_UNTRANSLATED_REQUIRES_QA"}
