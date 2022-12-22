from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from itertools import repeat


class TokenType(Enum):
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    EOF = 'EOF'  # end-of-file


@dataclass
class Token:
    """Token container.

    :param type: Type of token.
    :param value: Value of token, must be in {0, 1, 2, ..., 9, '+', '-', None}.
    """

    type: TokenType
    value: int | str | None

    def __str__(self) -> str:
        return f'Token({self.type.value}, {self.value})'

    __repr__ = __str__


def interpret(text: str) -> int:
    """Evaluate expression from input sentence.

    Expression can only be of the forms:
    <int>+<int>
    <int>-<int>
    """
    tokens = tokenize(text)

    left = eat(tokens, TokenType.INTEGER).value
    operator = eat(tokens, TokenType.PLUS, TokenType.MINUS)
    right = eat(tokens, TokenType.INTEGER).value

    assert isinstance(left, int)
    assert isinstance(right, int)
    if operator.type is TokenType.PLUS:
        return left + right
    elif operator.type is TokenType.MINUS:
        return left - right
    raise TypeError(f'invalid operator token type {operator.type}')


def eat(tokens: Iterator[Token], *token_types: TokenType) -> Token:
    """Consume and return next token if it matches the passed token."""
    token = next(tokens)
    if token.type not in set(token_types):
        valid_types = [t.value for t in token_types]
        raise ValueError(f'expected one of {valid_types} but got {token.value}')
    return token


def tokenize(text: str) -> Iterator[Token]:
    """Lexically analyze (also known as scan or tokenize) input sentence."""
    for char in text:
        if char == ' ':
            continue
        elif char.isdigit():
            yield Token(TokenType.INTEGER, int(char))
        elif char == '+':
            yield Token(TokenType.PLUS, char)
        elif char == '-':
            yield Token(TokenType.MINUS, char)
        else:
            raise ValueError('error parsing input')
    yield from repeat(Token(TokenType.EOF, None))


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
