from hypothesis import given
from hypothesis import strategies as st

from spi.calculator import interpret


@given(st.integers(0))
def test_interpret_single_integer(x: int) -> None:
    text = str(x)
    assert interpret(text) == x


@given(st.integers(0), st.integers(0), st.sampled_from(['+', '-']))
def test_interpret_integer_pair(x: int, y: int, op: str) -> None:
    text = f'{x} {op} {y}'
    if op == '+':
        assert interpret(text) == x + y
    elif op == '-':
        assert interpret(text) == x - y
    else:
        raise ValueError(f'unexpected operator "{op}"')


@given(st.lists(st.integers(0), min_size=4, max_size=4))
def test_interpret_four_integers(xs: list[int]) -> None:
    text = f'{xs[0]} + {xs[1]} - {xs[2]} - {xs[3]}'
    assert interpret(text) == xs[0] + xs[1] - xs[2] - xs[3]
