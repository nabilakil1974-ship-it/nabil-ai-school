from __future__ import annotations

# ==============================================================================
# 1. STRICT ANTI-HARDCODE & MARKDOWN CONTAMINATION SCANNER
# ==============================================================================
FORBIDDEN_EDUCATIONAL_HARDCODE = [
    "a solid has a definite shape",
    "a liquid has a definite volume",
    "free surface of a liquid",
    "standard macroscopic rule applied",
    "solid wooden block",
    "cylinder vessel",
    "communicating vessels",
    "standard pedagogical investigation",
    "documented curriculum phenomenon",
    "y = 2 * x",
    "y = 2*x",
    "conclusive solution for",
    "evaluation conforming to level",
    "directly observed curriculum setup",
    "procedure structured under official curriculum guidelines",
    "core principle p.",
]


def assert_no_lesson_specific_hardcode(source_code: str):
    # Scan executable/source content while excluding the detector's own
    # forbidden-pattern declaration; otherwise the scanner detects itself.
    import ast
    tree = ast.parse(source_code)
    lines = source_code.splitlines(keepends=True)
    scan_lines = list(lines)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == "FORBIDDEN_EDUCATIONAL_HARDCODE" for t in targets):
                for idx in range(node.lineno - 1, node.end_lineno):
                    scan_lines[idx] = "\n"
    scan_source = "".join(scan_lines)
    found = [p for p in FORBIDDEN_EDUCATIONAL_HARDCODE if p.lower() in scan_source.lower()]
    if found:
        raise RuntimeError(f"LESSON_SPECIFIC_HARDCODE_DETECTED: Found {found}")


def assert_no_markdown_urls_in_runtime_code(source_code: str):
    bad_patterns = [
        'src="[http',
        'scopes = ["[http',
        '](http',
    ]
    # Exclude this scanner's own bad-pattern declaration from the scan.
    import ast
    tree = ast.parse(source_code)
    lines = source_code.splitlines(keepends=True)
    scan_lines = list(lines)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(t, ast.Name) and t.id == "bad_patterns" for t in targets):
                for idx in range(node.lineno - 1, node.end_lineno):
                    scan_lines[idx] = "\n"
    scan_source = "".join(scan_lines)
    found = [p for p in bad_patterns if p in scan_source]
    if found:
        raise RuntimeError(f"MARKDOWN_URL_CONTAMINATION_DETECTED: Found banned markdown patterns -> {found}")



def assert_renderer_family_contract() -> None:
    """Fail closed when deployed lab renderers do not support teacher-led labs."""
    import importlib
    interactive = importlib.import_module("scripts.nabil_interactive_lab")
    if not callable(getattr(interactive, "render_verified_lab", None)):
        raise RuntimeError("RENDERER_CONTRACT_MISSING:render_verified_lab")
    if not callable(getattr(interactive, "validate_lab_spec", None)):
        raise RuntimeError("RENDERER_CONTRACT_MISSING:validate_lab_spec")
    source = Path(interactive.__file__).read_text(encoding="utf-8")
    for token in ("teacher_script", "data-teacher-pointer", "nabil:teacher"):
        if token not in source:
            raise RuntimeError(f"RENDERER_TEACHER_CONTRACT_MISSING:{token}")
    optional = (
        ("scripts.nabil_geometry_lab", "render_geometry_proof_lab"),
        ("scripts.nabil_advanced_lab", "render_advanced_verified_lab"),
    )
    for module_name, callable_name in optional:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        if not callable(getattr(module, callable_name, None)):
            raise RuntimeError(
                f"RENDERER_FAMILY_CONTRACT_MISSING:{module_name}:{callable_name}")


from scripts.nabil_factory.p1.source_completeness import (
    attach_and_verify_source_completeness,
    build_independent_source_inventory,
)
