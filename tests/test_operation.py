import pytest

from jvmrp.operation import Operation, State, dispatch_table, read_operation


def test_read_operation():
    state = State()
    code = [178, 0, 2, 18, 3, 182, 0, 4, 177]

    op = read_operation(code, state)
    assert op == Operation(178, [0, 2])
    assert state.pc == 4

    op = read_operation(code, state)
    assert op == Operation(18, [3])
    assert state.pc == 6


def test_iconst_i():
    iconst_2 = dispatch_table[5]
    state = State()

    iconst_2(None, {}, state)
    assert state.stack == [2]


def test_istore_n():
    istore_2 = dispatch_table[61]
    state = State(stack=[34])

    istore_2(None, {}, state)
    assert state.stack == []
    assert state.frame == {2: 34}


def test_iload_n():
    iload_2 = dispatch_table[28]
    state = State(frame={2: 34})

    iload_2(None, {}, state)
    assert state.stack == [34]
