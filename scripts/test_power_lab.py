"""POWER_EXPLORER must really compute (not just reveal text) and pass the factory's lab contracts."""
from pathlib import Path
from tempfile import TemporaryDirectory
from playwright.sync_api import sync_playwright
from scripts.nabil_interactive_lab import render_verified_lab, validate_lab_spec
from scripts.nabil_requirement5_gate import validate_requirement5_lab
from scripts.nabil_power_lab import build_power_spec, LAWS

SOURCES = {
    "definition": ("Positive number power definitions", "Let a be a number and n a natural number: a^n = a × a × … × a (n factors)."),
    "product_same_base": ("Rules for calculating powers", "For the same base: a^m × a^n = a^(m+n)."),
    "quotient_same_base": ("Rules for calculating powers", "For the same base: a^m ÷ a^n = a^(m-n) when m ≥ n."),
    "power_of_power": ("Rules for calculating powers", "A power of a power: (a^m)^n = a^(m×n)."),
    "product_same_exponent": ("Property 4", "If a and b are numbers then (a × b)^m = a^m × b^m."),
    "quotient_same_exponent": ("Property 5", "If b ≠ 0 then (a / b)^m = a^m / b^m."),
    "scientific_notation": ("Scientific notation", "A number written as a × 10^n with 1 ≤ a < 10 is in scientific notation."),
}


def main():
    assert set(SOURCES) == set(LAWS)
    with TemporaryDirectory() as tmp, sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        try:
            for law, (title, raw) in SOURCES.items():
                spec = build_power_spec(title, raw, "en", "C1")
                assert spec and spec["law"] == law, (law, spec and spec["law"])
                validate_lab_spec(spec)
                validate_requirement5_lab(spec, source_text=raw)
                html_lab, active = render_verified_lab(spec, "en", "C1")
                assert active and 'data-lab-kind="POWER_EXPLORER"' in html_lab
                assert ' min=' not in html_lab and ' max=' not in html_lab and 'type="range"' not in html_lab
                f = Path(tmp) / f"{law}.html"
                f.write_text("<html><head><meta charset='utf-8'></head><body>" + html_lab + "</body></html>", encoding="utf-8")
                page = b.new_page(viewport={"width": 390, "height": 900})
                errs = []
                page.on("pageerror", lambda e: errs.append(str(e)))
                page.goto(f.as_uri())
                # nothing is pre-filled
                assert page.evaluate("[...document.querySelectorAll('#lab_C1 input')].every(i=>i.value==='')")
                page.evaluate("document.getElementById('lab_C1').dispatchEvent(new CustomEvent('nabil:demo'))")
                out = page.evaluate("document.getElementById('C1_out').innerText")
                eq = page.evaluate("!!document.querySelector('#C1_out .pw-eq')&&document.querySelector('#C1_out .pw-eq').textContent.startsWith('✓')")
                sups = page.evaluate("document.querySelectorAll('#C1_out sup').length")
                if law != "definition":
                    assert eq, (law, out)
                assert sups >= 1 and "^" not in out, (law, out)
                # a different student value must also compute, and bad input must be refused
                page.fill("#C1_a", "5")
                assert page.evaluate("document.getElementById('C1_out').innerText.length")>0
                if law != "scientific_notation":
                    page.fill("#C1_a", "500")  # outside the safe range: refused, never a wrong number
                    assert "valid" in page.evaluate("document.getElementById('C1_out').innerText").lower()
                assert not errs, (law, errs)
                print("PASS", law, "|", out.replace("\n", " ")[:110])
                page.close()
            # exact values
            spec = build_power_spec("Rules", "For the same base: a^m × a^n = a^(m+n).", "en", "C1")
            html_lab, _ = render_verified_lab(spec, "en", "C1")
            f = Path(tmp) / "exact.html"
            f.write_text("<html><body>" + html_lab + "</body></html>", encoding="utf-8")
            page = b.new_page()
            page.goto(f.as_uri())
            page.fill("#C1_a", "2"); page.fill("#C1_m", "3"); page.fill("#C1_n", "4")
            vals = page.evaluate("[...document.querySelectorAll('#C1_out .pw-val')].map(x=>x.textContent)")
            assert vals == ["= 128", "= 128"], vals
            page.close()
            print("PASS exact arithmetic 2^3 × 2^4 = 2^7 = 128")
        finally:
            b.close()


if __name__ == "__main__":
    main()
