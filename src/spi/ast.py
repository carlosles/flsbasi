from __future__ import annotations

from dataclasses import dataclass

from spi.token import Token


@dataclass
class BinOp:
    left: AST
    token: Token
    right: AST


@dataclass
class Num:
    token: Token


AST = BinOp | Num
