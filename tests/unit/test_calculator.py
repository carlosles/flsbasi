import pytest
from hypothesis import given
from hypothesis import strategies as st

from spi.calculator import interpret


@given(st.integers(0, 9), st.integers(0, 9))
def test_interpret(x: int, y: int) -> None:
    text = f'{x}+{y}'
    assert interpret(text) == x + y


@given(st.integers(min_value=10), st.integers(0, 9))
def test_interpret_raises_error_tokenizing_digit(x: int, y: int):
    text = f'{x}+{y}'
    with pytest.raises(ValueError):
        interpret(text)


@given(st.integers(0, 9), st.integers(0, 9))
def test_interpret_raises_error_tokenizing_operator(x: int, y: int):
    text = f'{x}-{y}'
    with pytest.raises(ValueError):
        interpret(text)
