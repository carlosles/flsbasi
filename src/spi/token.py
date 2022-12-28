from dataclasses import dataclass
from enum import Enum


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
