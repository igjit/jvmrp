# jvmrp

jvmrp is a toy Java VM written in Python.

## How to play

```py
from jvmrp.reader import read_class
from jvmrp.vm import VM

java_class = read_class("tests/data/Hello.class")

vm = VM()
vm.execute(java_class)
```
