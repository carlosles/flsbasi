from importlib.resources import files

from hypothesis import given
from hypothesis import strategies as st

import tests.data
from spi.interpreter import interpret


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
    try:
        assert interpret(text) == xs[0] + xs[1] * xs[2] - xs[3] // xs[4]
    except ZeroDivisionError:
        pass


@given(st.lists(st.integers(1), min_size=7, max_size=7))
def test_interpret_parenthesis_expression(xs: list[int]) -> None:
    text = f'{xs[0]} + {xs[1]} * ({xs[2]} / ({xs[3]} / ({xs[4]} + {xs[5]}) - {xs[6]}))'
    expected = xs[0] + xs[1] * (xs[2] // (xs[3] // (xs[4] + xs[5]) - xs[6]))
    try:
        assert interpret(text) == expected
    except ZeroDivisionError:
        pass


@given(st.lists(st.integers(4), min_size=4, max_size=4))
def test_interpret_unary_operators(xs: list[int]) -> None:
    text = f'{xs[0]} - - - + - ({xs[1]} + {xs[2]}) - +{xs[3]}'
    expected = xs[0] + (xs[1] + xs[2]) - xs[3]
    try:
        assert interpret(text) == expected
    except ZeroDivisionError:
        pass


def test_interpret_program() -> None:
    text = files(tests.data).joinpath('program.txt').read_text()
    result = interpret(text)
    assert result['number'] == 2
    assert result['a'] == 2
    assert result['b'] == 20
    assert result['c'] == 22
