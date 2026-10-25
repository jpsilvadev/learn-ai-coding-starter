import pytest

from sloperator.errors import LexicalError
from sloperator.lexer import tokenize


@pytest.mark.parametrize(
    ("source", "line"),
    [
        ("— c\n@", 2),
        ("— a\n— b\n@", 3),
        ("x\n— c\n\n@", 4),
        ("— c\r\n@", 2),
    ],
)
def test_lexical_error_line_is_correct_after_comment(source: str, line: int):
    with pytest.raises(LexicalError) as info:
        tokenize(source)
    assert info.value.line == line


def test_token_line_is_correct_after_comment():
    tokens = tokenize("— c\nx")
    assert tokens[0].line == 2
