from hypothesis import given
from hypothesis import strategies as st

from spi.calculator import interpret


@given(st.integers(0, 9), st.integers(0, 9), st.sampled_from(['+', '-']))
def test_interpret_operators(x: int, y: int, op: str) -> None:
    text = f'{x}{op}{y}'
    if op == '+':
        assert interpret(text) == x + y
    elif op == '-':
        assert interpret(text) == y - y
    else:
        raise ValueError(f'unexpected operator "{op}"')


@given(st.integers(0, 9), st.integers(0, 9), st.sampled_from(['+', '-']))
def test_interpret_with_whitespaces(x: int, y: int, op: str) -> None:
    text = f'{x} {op}  {y}'
    if op == '+':
        assert interpret(text) == x + y
    elif op == '-':
        assert interpret(text) == y - y
    else:
        raise ValueError(f'unexpected operator "{op}"')


@given(st.integers(min_value=10), st.integers(min_value=0), st.sampled_from(['+', '-']))
def test_interpret_with_multidigit_ints(x: int, y: int, op: str) -> None:
    text = f'{x}{op}{y}'
    if op == '+':
        assert interpret(text) == x + y
    elif op == '-':
        assert interpret(text) == y - y
    else:
        raise ValueError(f'unexpected operator "{op}"')
