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


def test_isub():
    isub = dispatch_table[100]
    state = State(stack=[5, 2])

    isub(None, {}, state)
    assert state.stack == [3]


def test_iinc():
    iinc = dispatch_table[132]
    state = State(frame={1: 10, 2: 20})

    iinc(Operation(132, [2, 4]), {}, state)
    assert state.frame == {1: 10, 2: 24}


def test_if_icmpcond():
    if_icmplt = dispatch_table[161]

    state = State(pc=4, stack=[2, 3])
    if_icmplt(Operation(161, [0, 10]), {}, state)
    assert state.pc == 11

    state = State(pc=4, stack=[3, 2])
    if_icmplt(Operation(161, [0, 10]), {}, state)
    assert state.pc == 4


def test_ifcond():
    ifeq = dispatch_table[153]

    state = State(pc=4, stack=[0])
    ifeq(Operation(161, [0, 10]), {}, state)
    assert state.pc == 11

    state = State(pc=4, stack=[1])
    ifeq(Operation(161, [0, 10]), {}, state)
    assert state.pc == 4


def test_goto():
    goto = dispatch_table[167]

    state = State(pc=4)
    goto(Operation(167, [0, 10]), {}, state)
    assert state.pc == 11
