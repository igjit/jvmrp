import pytest

from jvmrp.operation import Operation, State, read_operation


def test_read_operation():
    state = State()
    code = [178, 0, 2, 18, 3, 182, 0, 4, 177]

    op = read_operation(code, state)
    assert op == Operation(178, [0, 2])
    assert state.pc == 4

    op = read_operation(code, state)
    assert op == Operation(18, [3])
    assert state.pc == 6
