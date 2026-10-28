"""Exact stdout for selected programs in examples/."""

from pathlib import Path

from sloperator.runner import run_source

EXAMPLES = Path(__file__).resolve().parent.parent / "examples"


def run_example(name: str):
    return run_source((EXAMPLES / f"{name}.slop").read_text(encoding="utf-8"))


def test_equality_output():
    result = run_example("equality")
    assert result.stderr == ""
    assert result.exit_code == 0
    assert result.stdout == "✅\n❌\n❌\n"
