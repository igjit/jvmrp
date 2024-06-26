from dataclasses import dataclass


@dataclass
class Instruction:
    name: str
    opcode: int
    arity: int


instruction_set = [
    Instruction("iconst_m1", 2, 0),
    Instruction("iconst_0", 3, 0),
    Instruction("iconst_1", 4, 0),
    Instruction("iconst_2", 5, 0),
    Instruction("iconst_3", 6, 0),
    Instruction("iconst_4", 7, 0),
    Instruction("iconst_5", 8, 0),
    Instruction("bipush", 16, 1),
    Instruction("ldc", 18, 1),
    Instruction("iload_0", 26, 0),
    Instruction("iload_1", 27, 0),
    Instruction("iload_2", 28, 0),
    Instruction("iload_3", 29, 0),
    Instruction("istore_0", 59, 0),
    Instruction("istore_1", 60, 0),
    Instruction("istore_2", 61, 0),
    Instruction("istore_3", 62, 0),
    Instruction("iadd", 96, 0),
    Instruction("isub", 100, 0),
    Instruction("imul", 104, 0),
    Instruction("idiv", 108, 0),
    Instruction("irem", 112, 0),
    Instruction("iinc", 132, 2),
    Instruction("ifeq", 153, 2),
    Instruction("ifne", 154, 2),
    Instruction("iflt", 155, 2),
    Instruction("ifge", 156, 2),
    Instruction("ifgt", 157, 2),
    Instruction("ifle", 158, 2),
    Instruction("if_icmpeq", 159, 2),
    Instruction("if_icmpne", 160, 2),
    Instruction("if_icmplt", 161, 2),
    Instruction("if_icmpge", 162, 2),
    Instruction("if_icmpgt", 163, 2),
    Instruction("if_icmple", 164, 2),
    Instruction("goto", 167, 2),
    Instruction("getstatic", 178, 2),
    Instruction("return", 177, 0),
    Instruction("invokevirtual", 182, 2),
]

opcode_to_instruction = dict(zip([i.opcode for i in instruction_set], instruction_set))


def instruction_of(opcode):
    return opcode_to_instruction[opcode]
