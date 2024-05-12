from dataclasses import dataclass


@dataclass
class Instruction:
    name: str
    opcode: int
    arity: int


instruction_set = [
    Instruction("ldc", 18, 1),
    Instruction("getstatic", 178, 2),
    Instruction("return", 177, 0),
    Instruction("invokevirtual", 182, 2),
]

opcode_to_instruction = dict(zip([i.opcode for i in instruction_set], instruction_set))


def instruction_of(opcode):
    return opcode_to_instruction[opcode]
