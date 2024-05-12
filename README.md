# jvmrp

jvmrp is a toy Java VM written in Python.

## How to play

```py
from jvmrp.reader import read_class
from jvmrp.vm import VM

with open("tests/data/Hello.class", "rb") as f:
    java_class = read_class(f)

vm = VM()
vm.execute(java_class)
```
