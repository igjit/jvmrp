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
