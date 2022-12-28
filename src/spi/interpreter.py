from functools import singledispatch

from spi import lexer, parser
from spi.ast import AST, BinOp, Num
from spi.token import TokenType


def interpret(text: str) -> int:
    """Analyse, parse and evaluate input arithmetic expression."""
    tokens = lexer.tokenize(text)
    ast = parser.parse(tokens)
    return evaluate(ast)


@singledispatch
def evaluate(node: AST) -> int:
    """Evalute abstract syntax tree and return result."""
    raise NotImplementedError(f'invalid node type {type(node)}')


@evaluate.register
def _(node: Num) -> int:
    value = node.token.value
    assert isinstance(value, int)
    return value


@evaluate.register
def _(node: BinOp) -> int:
    match node.token.type:
        case TokenType.PLUS:
            return evaluate(node.left) + evaluate(node.right)
        case TokenType.MINUS:
            return evaluate(node.left) - evaluate(node.right)
        case TokenType.MUL:
            return evaluate(node.left) * evaluate(node.right)
        case TokenType.DIV:
            return evaluate(node.left) // evaluate(node.right)
        case _:
            raise ValueError(f'invalid token type {node.token.type}')


def main() -> None:
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        result = interpret(text)
        print(result)


if __name__ == '__main__':
    main()
