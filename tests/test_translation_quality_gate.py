import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.nabil_factory.factory import orchestrator as o  # noqa: E402

C = ["Compute the value of the power", "Solve the equation for x", "x = 2"]


def test_untranslated_prose_is_rejected():
    b = {"en": {c: c for c in C}, "fr": {c: c for c in C},
         "ar": {C[0]: "احسب قيمة القوة", C[1]: "حل المعادلة", "x = 2": "x = 2"}}
    r = o.translation_quality_report(C, b, "en")
    assert not r["ok"] and r["languages"]["fr"]["untranslated"] == 2


def test_wrong_script_is_rejected():
    b = {"en": {c: c for c in C},
         "fr": {C[0]: "Calculez la valeur", C[1]: "Résolvez l'équation", "x = 2": "x = 2"},
         "ar": {C[0]: "Compute la valeur", C[1]: "Solve it now ok", "x = 2": "x = 2"}}
    r = o.translation_quality_report(C, b, "en")
    assert not r["ok"] and r["languages"]["ar"]["wrong_script"] == 2


def test_good_bundles_pass_and_formulas_ignored():
    b = {"en": {c: c for c in C},
         "fr": {C[0]: "Calculez la valeur de la puissance", C[1]: "Résolvez l'équation en x", "x = 2": "x = 2"},
         "ar": {C[0]: "احسب قيمة القوة", C[1]: "حل المعادلة بالنسبة إلى س", "x = 2": "x = 2"}}
    assert o.translation_quality_report(C, b, "en")["ok"]
