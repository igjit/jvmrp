class Instruction:
    def __init__(self, name, opcode, arity):
        self.name = name
        self.opcode = opcode
        self.arity = arity

    def __repr__(self):
        return (
            f"Instruction(name='{self.name}', opcode={self.opcode}, arity={self.arity})"
        )


instruction_set = [
    Instruction("ldc", 18, 1),
    Instruction("getstatic", 178, 2),
    Instruction("return", 177, 0),
    Instruction("invokevirtual", 182, 2),
]
