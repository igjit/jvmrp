from pathlib import Path

import pytest

from jvmrp.reader import read_class


def test_read_class():
    class_file = Path(__file__).parent / "data" / "Hello.class"
    cls = read_class(class_file)

    assert cls["magic"] == b"\xca\xfe\xba\xbe"
    assert cls["this_class_name"] == b"Hello"
