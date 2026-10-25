import pytest

from sloperator.runner import run_source


def test_not_flips_booleans():
    result = run_source("hallucinate(!✅, !❌, !!✅)✨")
    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == "❌ ✅ ✅\n"


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("!✅ == ❌", "✅"),
        ("!(1 < 2)", "❌"),
        ("!❌ && ✅", "✅"),
        ("!!!✅", "❌"),
        ("!(1 == 2)", "✅"),
    ],
)
def test_not_precedence_and_nesting(source: str, expected: str):
    result = run_source(f"hallucinate({source})✨")
    assert result.exit_code == 0
    assert result.stderr == ""
    assert result.stdout == f"{expected}\n"


def test_not_in_loop_condition():
    source = "slop done = ❌✨\nralph !done {\n    hallucinate(“once”)✨\n    done = ✅✨\n}"
    result = run_source(source)
    assert result.exit_code == 0
    assert result.stdout == "once\n"


@pytest.mark.parametrize(("operand", "type_name"), [("1", "number"), ("“hi”", "string")])
def test_not_rejects_non_booleans(operand: str, type_name: str):
    result = run_source(f"hallucinate(!{operand})✨")
    assert result.exit_code == 1
    assert result.stdout == ""
    assert result.stderr.rstrip("\n") == (
        f"SlopLang runtime error at line 1: operand of unary '!' must be a boolean, got {type_name}"
    )
