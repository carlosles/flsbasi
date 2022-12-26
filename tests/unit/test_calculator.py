from hypothesis import given
from hypothesis import strategies as st

from spi.calculator import interpret


@given(st.integers(0))
def test_interpret_single_integer(x: int) -> None:
    text = str(x)
    assert interpret(text) == x


@given(st.integers(0), st.integers(1), st.sampled_from(['+', '-', '*', '/']))
def test_interpret_integer_pair(x: int, y: int, op: str) -> None:
    text = f'{x} {op} {y}'
    if op == '+':
        assert interpret(text) == x + y
    elif op == '-':
        assert interpret(text) == x - y
    elif op == '*':
        assert interpret(text) == x * y
    elif op == '/':
        assert interpret(text) == x // y
    else:
        raise ValueError(f'unexpected operator "{op}"')


@given(st.lists(st.integers(1), min_size=5, max_size=5))
def test_interpret_full_expression(xs: list[int]) -> None:
    text = f'{xs[0]} + {xs[1]} * {xs[2]} - {xs[3]} / {xs[4]}'
    assert interpret(text) == xs[0] + xs[1] * xs[2] - xs[3] // xs[4]
