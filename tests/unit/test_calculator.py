from hypothesis import given
from hypothesis import strategies as st

from spi.calculator import interpret


@given(st.integers(0), st.integers(1), st.sampled_from(['+', '-', '*', '/']))
def test_interpret(x: int, y: int, op: str) -> None:
    for text in (f'{x}{op}{y}', f'{x} {op}  {y}'):
        match op:
            case '+':
                assert interpret(text) == x + y
            case '-':
                assert interpret(text) == x - y
            case '*':
                assert interpret(text) == x * y
            case '/':
                assert interpret(text) == x // y
            case _:
                raise ValueError(f'unexpected operator "{op}"')
