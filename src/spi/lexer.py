from collections.abc import Iterator
from itertools import chain, repeat

from more_itertools import before_and_after, first

from spi.token import Token, TokenType


def tokenize(chars: str) -> Iterator[Token]:
    """Lexically analyze (also known as scan or tokenize) input source."""
    yield from itokenize(iter(chars))
    yield from repeat(Token(TokenType.EOF, None))


def itokenize(chars: Iterator[str]) -> Iterator[Token]:
    char = first(chars, default=None)
    match char:
        case None:
            return
        case ' ':
            pass  # do nothing
        case '.':
            yield Token(TokenType.DOT, char)
        case ';':
            yield Token(TokenType.SEMI, char)
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
        case ':':
            if (equal := next(chars)) != '=':
                raise ValueError(f'error parsing input "{char + equal}"')
            yield Token(TokenType.ASSIGN, ':=')
        case c if c.isalpha():
            letters, chars = before_and_after(str.isalpha, chars)
            word = ''.join(chain(char, letters))
            if word == 'BEGIN':
                yield Token(TokenType.BEGIN, word)
            elif word == 'END':
                yield Token(TokenType.END, word)
            else:
                yield Token(TokenType.ID, word)
        case c if c.isdigit():
            digits, chars = before_and_after(str.isdigit, chars)
            integer = int(''.join(chain(char, digits)))
            yield Token(TokenType.INTEGER, integer)
        case _:
            raise ValueError(f'error parsing input "{char}"')
    yield from itokenize(chars)
