import pytest

from jvmrp.instruction import instruction_of


def test_instruction_of():
    assert instruction_of(178).name == "getstatic"
