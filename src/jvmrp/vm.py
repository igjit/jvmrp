from jvmrp.operation import State, dispatch_table, read_operation


def find(l, cond):
    return next(x for x in l if cond(x))


class VM:
    def execute(self, java_class):
        constant_pool = java_class["constant_pool"]
        main_method = find(java_class["methods"], lambda x: x["name"] == b"main")
        code = find(
            main_method["attributes"], lambda x: x["attribute_name"] == b"Code"
        )["code"]

        self.execute_code(code, constant_pool)

    def execute_code(self, code, constant_pool):
        self.state = State()
        self.constant_pool = constant_pool

        while self.state.pc <= len(code):
            op = read_operation(code, self.state)
            self.execute_operation(op)

    def execute_operation(self, op):
        func = dispatch_table[op.opcode]
        func(op, self.constant_pool, self.state)
