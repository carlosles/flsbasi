from collections.abc import Iterator
from itertools import pairwise, repeat

from spi.token import Token, TokenType


def tokenize(text: str) -> Iterator[Token]:
    """Lexically analyze (also known as scan or tokenize) input source."""
    digits: list[str] = []
    for char, next_char in pairwise(text + ' '):
        if char.isspace():
            continue
        elif char.isdigit():
            digits += char
            if not next_char.isdigit():
                yield Token(TokenType.INTEGER, int(''.join(digits)))
                digits = []
        elif char == '+':
            yield Token(TokenType.PLUS, char)
        elif char == '-':
            yield Token(TokenType.MINUS, char)
        elif char == '*':
            yield Token(TokenType.MUL, char)
        elif char == '/':
            yield Token(TokenType.DIV, char)
        elif char == '(':
            yield Token(TokenType.LPAREN, char)
        elif char == ')':
            yield Token(TokenType.RPAREN, char)
        else:
            raise ValueError(f'error parsing input "{char}"')
    yield from repeat(Token(TokenType.EOF, None))
