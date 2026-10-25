# Sloperator

A tree-walking interpreter for [SlopLang](docs/spec.md), written in Python.

## Usage

```bash
uv run sloperator.py examples/fib.slop            # run a program
uv run sloperator.py --check path/to/program.slop # check syntax only
uv run playground/server.py                       # playground at http://localhost:8080
```

## Validation

```bash
uv run pytest              # tests
uv run ruff format --check # formatting
uv run ruff check          # linting
uv run ty check            # type checking
```

## Example

```slop
— Comments start with an em dash. Statements end with sparkles.
clanker describe(count) {
    vibe count > 1 {
        ship “big slop”✨
    } nah {
        ship “small slop”✨
    }
}

slop count = 0✨
ralph count < 3 {
    hallucinate(describe(count))✨
    count = count + 1✨
}
```

The full language reference is in [docs/spec.md](docs/spec.md).

## Layout

- `sloperator.py`: command-line entrypoint
- `sloperator/lexer/`, `parser/`, `evaluator/`: source to tokens, AST, then execution
- `sloperator/runner.py`: runs source through all three stages
- `docs/spec.md`: the language specification
- `examples/`, `tests/`, `playground/`: example programs, pytest suite, web editor
