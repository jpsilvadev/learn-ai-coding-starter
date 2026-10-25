# AGENTS.md

Sloperator: tree-walking interpreter for SlopLang in Python 3.13, managed with `uv`, no runtime dependencies.

## Project layout

- `sloperator.py`: CLI entry point (`uv run sloperator.py examples/fib.slop`, `--check` for syntax only)
- `sloperator/lexer/`, `parser/`, `evaluator/`: source to tokens, AST, then execution; wired together by `sloperator/runner.py`
- `examples/`: `.slop` programs, each auto-run by `tests/test_examples.py` (must exit 0 with empty stderr and non-empty stdout)
- `tests/`: pytest suite
- `docs/spec.md`: language specification
- `playground/`: web playground

## Validation

After any code change, run `uv run ruff format` to format the code.

Run all four before finishing:

```bash
uv run pytest
uv run ruff format --check
uv run ruff check
uv run ty check
```

Run a single test with `uv run pytest tests/test_evaluator.py::test_name`.

Run the comparison precedence tests with `uv run pytest tests/test_comparisons.py`.

## Regression tests

Add a regression test whenever you fix a bug or change language behavior, in the test file for the affected stage (`test_lexer.py`, `test_parser.py`, `test_evaluator.py`, `test_errors.py`). The test should fail without the fix. Error messages are asserted verbatim, so update the tests when wording changes.

## Language behavior

`docs/spec.md` is the source of truth for SlopLang behavior; read it before changing semantics and update it in the same change. See [docs/spec.md](docs/spec.md).
