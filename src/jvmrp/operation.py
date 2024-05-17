from dataclasses import dataclass, field

from jvmrp.instruction import instruction_of


@dataclass
class State:
    pc: int = 1
    stack: list = field(default_factory=list)
    frame: dict = field(default_factory=dict)


@dataclass
class Operation:
    opcode: int
    operands: list[int]


def read_operation(code, state):
    pc = state.pc
    opcode = code[pc - 1]
    inst = instruction_of(opcode)

    operands = []
    if inst.arity > 0:
        operands = code[pc : (pc + inst.arity)]
    state.pc += 1 + inst.arity

    return Operation(inst.opcode, operands)


def ldc(op, constant_pool, state):
    index = op.operands[0]
    bytes = constant_pool[constant_pool[index - 1]["string_index"] - 1]["bytes"]
    state.stack.append(bytes.decode())


def getstatic(op, constant_pool, state):
    cp_index = as_u2(*op.operands)
    symbol_name_index = constant_pool[cp_index - 1]
    cls = constant_pool[
        constant_pool[symbol_name_index["class_index"] - 1]["name_index"] - 1
    ]["bytes"]
    field = constant_pool[
        constant_pool[symbol_name_index["name_and_type_index"] - 1]["name_index"] - 1
    ]["bytes"]
    name = f"{cls.decode()}.{field.decode()}"
    state.stack.append(name)


def invokevirtual(op, constant_pool, state):
    index = as_u2(*op.operands)
    callee = constant_pool[constant_pool[index - 1]["name_and_type_index"] - 1]
    method_name = constant_pool[callee["name_index"] - 1]["bytes"]
    # TODO
    if method_name != b"println":
        raise Exception(f"Not implemented: {method_name}")
    args = state.stack.pop()
    object_name = state.stack.pop()
    print(args)


def return_(op, constant_pool, state):
    pass


def bipush(op, constant_pool, state):
    state.stack.append(op.operands[0])


def iconst_i(i):
    return lambda op, constant_pool, state: state.stack.append(i)


def istore_n(n):
    def f(op, constant_pool, state):
        state.frame[n] = state.stack.pop()

    return f


def iload_n(n):
    return lambda op, constant_pool, state: state.stack.append(state.frame[n])


def int_arith(a):
    def f(op, constant_pool, state):
        value2 = state.stack.pop()
        value1 = state.stack.pop()
        result = a(value1, value2)
        state.stack.append(result)

    return f


dispatch_table = {
    2: iconst_i(-1),
    3: iconst_i(0),
    4: iconst_i(1),
    5: iconst_i(2),
    6: iconst_i(3),
    7: iconst_i(4),
    8: iconst_i(5),
    16: bipush,
    18: ldc,
    26: iload_n(0),
    27: iload_n(1),
    28: iload_n(2),
    29: iload_n(3),
    59: istore_n(0),
    60: istore_n(1),
    61: istore_n(2),
    62: istore_n(3),
    96: int_arith(int.__add__),
    100: int_arith(int.__sub__),
    104: int_arith(int.__mul__),
    108: int_arith(int.__floordiv__),
    112: int_arith(int.__mod__),
    177: return_,
    178: getstatic,
    182: invokevirtual,
}


def as_u2(byte1, byte2):
    return (byte1 << 8) + byte2
