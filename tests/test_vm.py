from pathlib import Path

import pytest

from jvmrp.reader import read_class
from jvmrp.vm import VM


def execute_class_file(class_file):
    java_class = read_class(class_file)
    vm = VM()
    vm.execute(java_class)


def test_execute_hello(capsys):
    class_file = Path(__file__).parent / "data" / "Hello.class"
    execute_class_file(class_file)

    captured = capsys.readouterr()
    assert captured.out == "Hello, world.\n"
