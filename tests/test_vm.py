from pathlib import Path

import pytest

from jvmrp.reader import read_class
from jvmrp.vm import VM


def test_execute_hello(capsys):
    class_file = Path(__file__).parent / "data" / "Hello.class"

    with open(class_file, "rb") as f:
        java_class = read_class(f)

    vm = VM()
    vm.execute(java_class)

    captured = capsys.readouterr()
    assert captured.out == "Hello, world.\n"
