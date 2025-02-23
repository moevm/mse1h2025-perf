import cfile
from random import randint, choice
from cfile.core import Variable, Statement, Declaration, Block, Sequence, Type, Assignment, StringLiteral, FunctionCall, Blank, IncludeDirective, Function, FunctionReturn
from variables import StaticArray, Pointer
from random_expressions import get_expression

int_type = Type("int")


class CodeCGenerator:
    def __init__(self, blocks_recursion_depth=2,
                 max_n_blocks_in_block=5,
                 min_n_new_vars_in_block=1,
                 max_n_new_vars_in_block=5,
                 max_length_math_expression=5,
                 max_assignments_in_block=5):

        self.blocks_recursion_depth = blocks_recursion_depth
        self.max_n_blocks_in_block = max_n_blocks_in_block
        self.min_n_new_vars_in_block = min_n_new_vars_in_block
        self.max_n_new_vars_in_block = max_n_new_vars_in_block
        self.arithmetic_operators = ["+", "-", "*"]
        self.cmp_operations = [">", "<", ">=", "<=", "==", "!="]
        self.minuses_threshold = 0.5
        self.brackets_treshold = 0.5
        self.max_length_math_expression = max_length_math_expression
        self.max_assignments_in_block = max_assignments_in_block
        self.max_arr_size = 20
        self.max_int_value = 1000
        self.writer = cfile.Writer(cfile.StyleOptions())

    def generate_math_expression(self, vars):
        int_type_vars = []
        for var in vars:
            if isinstance(var, Pointer):
                if var.mem_size:
                    int_type_vars.append(var[randint(0, var.mem_size - 1)])
            elif isinstance(var, StaticArray):
                int_type_vars.append(var[randint(0, var.array - 1)])
            else:
                int_type_vars.append(var)
        var_names = [int_type_var.name for int_type_var in int_type_vars]
        return get_expression(var_names,
                              self.arithmetic_operators,
                              randint(1, self.max_length_math_expression),
                              randint(1, 100000),
                              minuses_threshold=self.minuses_threshold,
                              brackets_treshold=self.brackets_treshold
                              )

    def generate_condition_operator(self, vars):
        operator = choice(self.cmp_operations)
        condition = self.generate_math_expression(vars) + \
            f" {operator} " + self.generate_math_expression(vars)
        return FunctionCall("if", [condition])

    def generate_assignment(self, vars):
        var = choice(vars)
        if isinstance(var, Pointer):
            if var.mem_size:
                element = var[randint(0, var.mem_size - 1)]
                return Assignment(element, self.generate_math_expression(vars))
            else:
                var.mem_size = randint(1, self.max_arr_size - 1)
                var.need_to_free_mem = True
                return Assignment(var.name, FunctionCall("malloc", [f"sizeof(int) * {var.mem_size}"]))
        elif isinstance(var, StaticArray):
            element = var[randint(0, var.array)]
            return Assignment(element, self.generate_math_expression(vars))
        else:
            return Assignment(var, self.generate_math_expression(vars))

    def get_all_free_calls(self, vars):
        free_calls = []
        for var in vars:
            if isinstance(var, Pointer) and var.need_to_free_mem:
                free_calls.append(FunctionCall("free", [f"{var}"]))
                var.need_to_free_mem = False
                var.mem_size = 0

        return free_calls

    def generate_vars(self, existing_vars: list[Variable] = []):
        if existing_vars:
            seq_number = int(existing_vars[-1].name[1:]) + 1
        else:
            seq_number = 0
        vars_num = randint(
            self.min_n_new_vars_in_block, self.max_n_new_vars_in_block)

        vars = [None for _ in range(vars_num)]
        for i in range(vars_num):
            var_type = choice([Variable, StaticArray, Pointer])
            if var_type is Pointer:
                var = Pointer(f"x{seq_number + i}", int_type)
            elif var_type is StaticArray:
                var = StaticArray(f"x{seq_number + i}",
                                  int_type, randint(1, self.max_arr_size))
            else:
                var = Variable(f"x{seq_number + i}", int_type)
            vars[i] = var

        return vars

    def generate_var_declarations(self, var):
        if isinstance(var, Pointer):
            return Declaration(var)
            # var.mem_size = randint(1, self.max_arr_size)
            # var.need_to_free_mem = True
            # return Declaration(var, FunctionCall("malloc", f"sizeof(int) * {var.mem_size}"))
        elif isinstance(var, StaticArray):
            return Declaration(var, [randint(1, self.max_int_value) for _ in range(var.array)])
        else:
            return Declaration(var, randint(1, self.max_int_value))

    def generate_block(self, max_depth=None, existing_vars: list[Variable] = [], block_is_last=False):
        block = Block()

        new_vars = self.generate_vars(existing_vars)
        for var in new_vars:
            block.append(Statement(self.generate_var_declarations(var)))
        vars = existing_vars + new_vars
        number_assignments = randint(1, self.max_assignments_in_block)
        for i in range(number_assignments):
            block.append(Statement(self.generate_assignment(vars)))

        if max_depth is None:
            max_depth = self.blocks_recursion_depth

        elif max_depth == 0:
            if block_is_last:
                for function_call in self.get_all_free_calls(vars):
                    block.append(Statement(function_call))
            return block

        number_blocks = randint(0, self.max_n_blocks_in_block)
        for i in range(number_blocks):
            block_is_last = False
            if i == number_blocks - 1:
                block_is_last = True
            block.append(self.generate_condition_operator(vars))
            block.append(self.generate_block(
                randint(0, max_depth - 1), vars, block_is_last=block_is_last)
            )

        return block

    def generate_function(self, name, args: list[Variable] = []):
        code = Sequence()
        code.append(Declaration(Function(name, int_type, params=args)))
        body = self.generate_block()
        body.append(Statement(FunctionReturn(0)))
        code.append(body)
        return code

    def add_includes(self, code: Sequence):
        code_with_includes = Sequence()
        code_with_includes.append(IncludeDirective("stdlib.h", True))
        code_with_includes.append(Blank())
        code_with_includes.extend(code)
        return code_with_includes

    def write_code(self, code, file):
        self.writer.write_file(code, file)
