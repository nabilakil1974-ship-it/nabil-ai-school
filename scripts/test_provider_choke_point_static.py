from __future__ import annotations

import ast
from pathlib import Path

FACTORY = Path("scripts/nabil_lesson_factory.py")


def _enclosing_function(node, parents):
    cur = node
    while cur in parents:
        cur = parents[cur]
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return cur.name
    return None


def main():
    source = FACTORY.read_text(encoding="utf-8")
    tree = ast.parse(source)
    parents = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent

    raw_calls = []
    strict_calls = []
    provider_http_calls = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = None
        if isinstance(node.func, ast.Name):
            fn = node.func.id
        elif isinstance(node.func, ast.Attribute):
            fn = node.func.attr

        if fn == "execute_llm_completion":
            raw_calls.append(node)
            names = {kw.arg for kw in node.keywords if kw.arg}
            assert "operation" in names, (
                "Every execute_llm_completion call must declare operation at "
                f"line {node.lineno}"
            )
            assert "unit_id" in names, (
                "Every execute_llm_completion call must declare unit_id at "
                f"line {node.lineno}"
            )

        if fn == "_execute_llm_json_strict":
            strict_calls.append(node)
            names = {kw.arg for kw in node.keywords if kw.arg}
            assert "purpose" in names, (
                "Every _execute_llm_json_strict call must declare purpose at "
                f"line {node.lineno}"
            )

        if isinstance(node.func, ast.Attribute):
            chain = []
            obj = node.func
            while isinstance(obj, ast.Attribute):
                chain.append(obj.attr)
                obj = obj.value
            if isinstance(obj, ast.Name):
                chain.append(obj.id)
            dotted = ".".join(reversed(chain))
            if dotted == "urllib.request.urlopen":
                provider_http_calls.append(node)
                assert _enclosing_function(node, parents) == "execute_llm_completion", (
                    "Provider HTTP call escaped execute_llm_completion choke point "
                    f"at line {node.lineno}"
                )

    assert raw_calls, "No execute_llm_completion calls found"
    assert strict_calls, "No _execute_llm_json_strict calls found"
    assert provider_http_calls, "No provider HTTP call found"

    # The strict JSON helper must itself route through the same typed choke.
    strict_def = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef)
        and n.name == "_execute_llm_json_strict"
    )
    assert any(
        isinstance(n, ast.Call)
        and isinstance(n.func, ast.Name)
        and n.func.id == "execute_llm_completion"
        for n in ast.walk(strict_def)
    ), "_execute_llm_json_strict bypasses execute_llm_completion"

    # Production boundary must be the only persistence point for typed pauses.
    wrapper = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef)
        and n.name == "produce_lesson_for_entry"
    )
    wrapper_text = ast.get_source_segment(source, wrapper) or ""
    assert "_persist_factory_recovery_state" in wrapper_text
    assert "_produce_lesson_for_entry_impl" in wrapper_text

    print(
        "NABIL_PROVIDER_CHOKE_POINT_STATIC_PASS "
        f"raw_calls={len(raw_calls)} strict_calls={len(strict_calls)} "
        f"http_calls={len(provider_http_calls)}"
    )


if __name__ == "__main__":
    main()
