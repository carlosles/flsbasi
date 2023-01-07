from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    DOT = 'DOT'
    BEGIN = 'BEGIN'
    END = 'END'
    SEMI = 'SEMI'
    ASSIGN = 'ASSIGN'
    ID = 'ID'
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
    :param value: Value of token.
    """

    type: TokenType
    value: int | str | None

    def __str__(self) -> str:
        return f'Token({self.type.value}, {self.value})'

    __repr__ = __str__
