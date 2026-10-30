from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Assign, Binary, Block, Literal, Variable


def test_plus_equal_is_a_single_token():
    tokens = tokenize("x += 1✨")
    assert [t.type for t in tokens][:3] == [
        TokenType.IDENTIFIER,
        TokenType.PLUS_EQUAL,
        TokenType.NUMBER,
    ]
    assert tokens[1].lexeme == "+="


def test_plus_and_equal_separated_by_space_are_not_plus_equal():
    types = [t.type for t in tokenize("+ =")]
    assert types[:2] == [TokenType.PLUS, TokenType.EQUAL]


def test_plus_equal_statement_parses_to_assign():
    (statement,) = parse(tokenize("x += 1 + 2✨"))
    assert isinstance(statement, Assign)
    assert statement.name.lexeme == "x"
    assert statement.operator.type is TokenType.PLUS_EQUAL
    assert isinstance(statement.value, Binary)


def test_plain_assignment_still_uses_equal_operator():
    (statement,) = parse(tokenize("x = 1✨"))
    assert isinstance(statement, Assign)
    assert statement.operator.type is TokenType.EQUAL
    assert isinstance(statement.value, Literal)
    assert statement.value.value == 1


def test_plus_equal_parses_inside_blocks():
    (block,) = parse(tokenize("{ x += y✨ }"))
    assert isinstance(block, Block)
    (statement,) = block.statements
    assert isinstance(statement, Assign)
    assert isinstance(statement.value, Variable)
    assert statement.value.name.lexeme == "y"
