from pathlib import Path

import pytest

from jvmrp.reader import read_class
from jvmrp.vm import VM


def test_execute_hello(capsys):
    class_file = Path(__file__).parent / "data" / "Hello.class"
    java_class = read_class(class_file)

    vm = VM()
    vm.execute(java_class)

    captured = capsys.readouterr()
    assert captured.out == "Hello, world.\n"
