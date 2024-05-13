from dataclasses import dataclass, field

from jvmrp.instruction import instruction_of


@dataclass
class State:
    pc: int = 1
    stack: list = field(default_factory=list)
    frame: list = field(default_factory=list)


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


dispatch_table = {
    16: bipush,
    18: ldc,
    177: return_,
    178: getstatic,
    182: invokevirtual,
}


def as_u2(byte1, byte2):
    return (byte1 << 8) + byte2
