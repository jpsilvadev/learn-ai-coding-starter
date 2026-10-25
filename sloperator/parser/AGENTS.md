# Parser

Recursive descent parser in `parser.py`.

- Use one method per grammar rule (e.g. `if_stmt`, `while_stmt`, and one per precedence level: `logic_or`, `logic_and`, `equality`, `comparison`, `term`, `factor`, `unary`, `call`, `primary`). Add a new method for a new rule instead of extending an existing one.
- Syntax errors must describe the token that was found. Build them with `self.error(token, message)` or `self.expect(type, message)`, which append `, found '<lexeme>'` (or `, but reached end of file`). Don't raise a bare `SlopSyntaxError` for an unexpected token.
- Tests assert error messages verbatim, so update `tests/test_parser.py` and `docs/spec.md` when wording changes.
