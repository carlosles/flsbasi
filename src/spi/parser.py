from collections.abc import Iterator

from more_itertools import peekable

from spi.ast import AST, BinOp, Num
from spi.token import Token, TokenType


def parse(tokens: Iterator[Token]) -> AST:
    """Return abstract syntax tree parsed from stream of tokens."""
    return expr(peekable(tokens))


def expr(tokens: peekable) -> AST:
    """Evaluate expression from stream of tokens.

    Expression can be of the following grammar:
        expr: term ((PLUS | MINUS) term)*
    where PLUS, MINUS represent the tokens for '+', '-'.
    """
    node = term(tokens)
    while (token_type := tokens.peek().type) in {TokenType.PLUS, TokenType.MINUS}:
        token = eat(tokens, token_type)
        node = BinOp(left=node, token=token, right=term(tokens))
    return node


def term(tokens: peekable) -> AST:
    """Evaluate term from stream of tokens.

    Term can be of the following grammar:
        term: factor ((MUL | DIV) factor)*
    where MUL, DIV represent the tokens for '*', '/'.
    """
    node = factor(tokens)
    while (token_type := tokens.peek().type) in {TokenType.MUL, TokenType.DIV}:
        token = eat(tokens, token_type)
        node = BinOp(left=node, token=token, right=factor(tokens))
    return node


def factor(tokens: Iterator[Token]) -> AST:
    """Evaluate factor from stream of tokens.

    Factor can be of the following grammar:
        factor: INTEGER | LPAREN expr RPAREN
    where INTEGER represents any non-negative integer.
    """
    token = eat(tokens, TokenType.INTEGER, TokenType.LPAREN)
    if token.type is TokenType.INTEGER:
        return Num(token=token)
    elif token.type is TokenType.LPAREN:
        node = expr(tokens)
        _ = eat(tokens, TokenType.RPAREN)
        return node
    raise TypeError(f'invalid token type {token.type}')


def eat(tokens: Iterator[Token], *token_types: TokenType) -> Token:
    """Consume and return next token if it matches the passed token."""
    token = next(tokens)
    if token.type not in set(token_types):
        valid_types = [t.value for t in token_types]
        raise ValueError(f'expected one of {valid_types} but got {token.value}')
    return token
