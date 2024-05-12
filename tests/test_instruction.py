import pytest

from jvmrp.instruction import Instruction, instruction_of


def test_instruction_of():
    assert instruction_of(178) == Instruction(name="getstatic", opcode=178, arity=2)
