import textwrap
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


def test_execute_arith(capsys):
    class_file = Path(__file__).parent / "data" / "Arith.class"
    execute_class_file(class_file)

    captured = capsys.readouterr()
    assert captured.out == "42\n"


def test_execute_fizz_buzz(capsys):
    class_file = Path(__file__).parent / "data" / "FizzBuzz.class"
    execute_class_file(class_file)

    captured = capsys.readouterr()
    expected = textwrap.dedent(
        """\
        1
        2
        Fizz
        4
        Buzz
        Fizz
        7
        8
        Fizz
        Buzz
        11
        Fizz
        13
        14
        FizzBuzz
        16
        17
        Fizz
        19
        Buzz
        """
    )

    assert captured.out == expected
