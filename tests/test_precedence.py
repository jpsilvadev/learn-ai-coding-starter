from sloperator.lexer import TokenType, tokenize
from sloperator.parser import parse
from sloperator.parser.ast import Binary, ExprStmt, Literal


def test_multiplication_takes_precedence_over_addition():
    (statement,) = parse(tokenize("1 + 2 * 3✨"))

    assert isinstance(statement, ExprStmt)
    expression = statement.expression
    assert isinstance(expression, Binary)
    assert expression.operator.type is TokenType.PLUS
    assert isinstance(expression.left, Literal) and expression.left.value == 1
    assert isinstance(expression.right, Binary)
    assert expression.right.operator.type is TokenType.STAR
    assert isinstance(expression.right.left, Literal) and expression.right.left.value == 2
    assert isinstance(expression.right.right, Literal) and expression.right.right.value == 3
