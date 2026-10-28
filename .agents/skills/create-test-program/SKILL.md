---
name: create-test-program
description: Given a SlopLang language feature, read docs/spec.md, write an example program in examples/, and add an exact-output test in tests/test_example_outputs.py
---

# Create test program

Input: a language feature (e.g. "while loops", "string concatenation").

From the project root:

1. Read `docs/spec.md` for the feature. The spec is the source of truth; never infer syntax from other examples alone. Existing files in `examples/` show style (comment line starts with `—`, statements end with `✨`).
2. Write `examples/<feature>.slop`:
   - Exercise the feature, including an edge case or two the spec describes.
   - Print results with `hallucinate(...)`; stdout must be non-empty, stderr empty, exit code 0 (`tests/test_examples.py` auto-runs every example).
   - Keep it deterministic and small.
3. Run it: `uv run sloperator.py examples/<feature>.slop`. Check the output against what the spec says it should be, not just what the interpreter prints. If they differ, report the discrepancy as a possible bug instead of recording it.
4. Add a test to `tests/test_example_outputs.py` (create the file if missing) that runs the example via `sloperator.runner.run_source` and asserts `result.stdout` equals the exact expected string, plus `stderr == ""` and `exit_code == 0`. Check how `run_source` formats stdout (e.g. newlines) before writing the expected string.
5. Run `uv run ruff format`, then the validate skill checks (`uv run pytest`, `uv run ruff format --check`, `uv run ruff check`, `uv run ty check`).

Report the files created and the check results.
