from collections.abc import Iterator
from itertools import pairwise, repeat

from spi.token import Token, TokenType


def tokenize(text: str) -> Iterator[Token]:
    """Lexically analyze (also known as scan or tokenize) input source."""
    digits: list[str] = []
    for char, next_char in pairwise(text + ' '):
        if char.isspace():
            continue
        match char:
            case c if c.isdigit():
                digits += char
                if not next_char.isdigit():
                    yield Token(TokenType.INTEGER, int(''.join(digits)))
                    digits = []
            case '+':
                yield Token(TokenType.PLUS, char)
            case '-':
                yield Token(TokenType.MINUS, char)
            case '*':
                yield Token(TokenType.MUL, char)
            case '/':
                yield Token(TokenType.DIV, char)
            case '(':
                yield Token(TokenType.LPAREN, char)
            case ')':
                yield Token(TokenType.RPAREN, char)
            case _:
                raise ValueError(f'error parsing input "{char}"')
    yield from repeat(Token(TokenType.EOF, None))
