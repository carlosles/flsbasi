from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from itertools import pairwise, repeat

from more_itertools import peekable


class TokenType(Enum):
    INTEGER = 'INTEGER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    EOF = 'EOF'  # end-of-file


@dataclass
class Token:
    """Token container.

    :param type: Type of token.
    :param value: Value of token, must be in
        {0, 1, 2, ..., '+', '-', '*', '/', '(', ')' None}.
    """

    type: TokenType
    value: int | str | None

    def __str__(self) -> str:
        return f'Token({self.type.value}, {self.value})'

    __repr__ = __str__


def interpret(text: str) -> int:
    """Analyse, parse and evaluate input arithmetic sentence."""
    tokens = tokenize(text)
    return expr(peekable(tokens))


def expr(tokens: peekable) -> int:
    """Evaluate expression from stream of tokens.

    Expression can be of the following grammar:
        expr: term ((PLUS | MINUS) term)*
        term: factor ((MUL | DIV) factor)*
        factor: INTEGER | LPAREN expr RPAREN
    where INTEGER represents any non-negative integer.
    """
    ops = (TokenType.PLUS, TokenType.MINUS)
    result = term(tokens)
    while (operator_type := tokens.peek().type) in ops:
        _ = eat(tokens, *ops)
        if operator_type is TokenType.PLUS:
            result += term(tokens)
        elif operator_type is TokenType.MINUS:
            result -= term(tokens)
        else:
            raise TypeError(f'invalid operator token type {operator_type}')
    return result


def term(tokens: peekable) -> int:
    """Evaluate term from stream of tokens.

    Term can be of the following grammar:
        term: factor ((MUL | DIV) factor)*
        factor: INTEGER | LPAREN expr RPAREN
    where INTEGER represents any non-negative integer.
    """
    ops = (TokenType.MUL, TokenType.DIV)
    result = factor(tokens)
    while (operator_type := tokens.peek().type) in ops:
        _ = eat(tokens, *ops)
        if operator_type is TokenType.MUL:
            result *= factor(tokens)
        elif operator_type is TokenType.DIV:
            result //= factor(tokens)
        else:
            raise TypeError(f'invalid operator token type {operator_type}')
    return result


def factor(tokens: Iterator[Token]) -> int:
    """Evaluate factor from stream of tokens.

    Factor can be of the following grammar:
        factor: INTEGER | LPAREN expr RPAREN
    where INTEGER represents any non-negative integer.
    """
    token = eat(tokens, TokenType.INTEGER, TokenType.LPAREN)
    if token.type is TokenType.INTEGER:
        result = token.value
        assert isinstance(result, int)
        return result
    elif token.type is TokenType.LPAREN:
        result = expr(tokens)
        _ = eat(tokens, TokenType.RPAREN)
        return result
    raise TypeError(f'invalid token type {token.type}')


def eat(tokens: Iterator[Token], *token_types: TokenType) -> Token:
    """Consume and return next token if it matches the passed token."""
    token = next(tokens)
    if token.type not in set(token_types):
        valid_types = [t.value for t in token_types]
        raise ValueError(f'expected one of {valid_types} but got {token.value}')
    return token


def tokenize(text: str) -> Iterator[Token]:
    """Lexically analyze (also known as scan or tokenize) input sentence."""
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
