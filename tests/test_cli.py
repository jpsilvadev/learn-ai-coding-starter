import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INTERPRETER = ROOT / "sloperator.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INTERPRETER), *args], capture_output=True, encoding="utf-8"
    )


def test_runs_a_file():
    completed = run_cli(str(ROOT / "examples/hello.slop"))
    assert completed.returncode == 0
    assert completed.stdout == "hello, slop\n"
    assert completed.stderr == ""


def test_error_goes_to_stderr_after_earlier_output(tmp_path: Path):
    program = tmp_path / "boom.slop"
    program.write_text("hallucinate(“before”)✨\nhallucinate(missing)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == "before\n"
    assert completed.stderr == "SlopLang runtime error at line 2: undefined variable 'missing'\n"
    assert "Traceback" not in completed.stderr


def test_division_by_zero_reports_runtime_error_without_traceback(tmp_path: Path):
    program = tmp_path / "division.slop"
    program.write_text("hallucinate(1 / 0)✨\n", encoding="utf-8")
    completed = run_cli(str(program))
    assert completed.returncode == 1
    assert completed.stdout == ""
    assert completed.stderr == "SlopLang runtime error at line 1: division by zero\n"


def test_check_parses_without_executing(tmp_path: Path):
    program = tmp_path / "runtime-error.slop"
    program.write_text("hallucinate(“before”)✨\nhallucinate(missing)✨\n", encoding="utf-8")
    for args in (("--check", str(program)), (str(program), "--check")):
        completed = run_cli(*args)
        assert (completed.returncode, completed.stdout, completed.stderr) == (0, "", "")


def test_check_reports_lexical_and_syntax_errors(tmp_path: Path):
    program = tmp_path / "invalid.slop"
    for source, diagnostic in (
        ("@", "SlopLang lexical error at line 1: unexpected character '@'\n"),
        (
            "slop x✨",
            "SlopLang syntax error at line 1: "
            "expected '=' after variable name, an initializer is required, found '✨'\n",
        ),
    ):
        program.write_text(source, encoding="utf-8")
        completed = run_cli("--check", str(program))
        assert (completed.returncode, completed.stdout, completed.stderr) == (1, "", diagnostic)


def test_missing_file_and_usage():
    assert run_cli().returncode == 2
    missing = run_cli(str(ROOT / "nope.slop"))
    assert missing.returncode == 2
    assert "could not read" in missing.stderr
    assert run_cli("--check", str(ROOT / "nope.slop")).returncode == 2
    for args in (("--check",), ("--check", "--check", "file.slop"), ("--validate", "file.slop")):
        completed = run_cli(*args)
        assert completed.returncode == 2
        assert "usage:" in completed.stderr
