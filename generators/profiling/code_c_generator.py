import cfile
from random import randint, choice, random
from cfile.core import Variable, Statement, Declaration, Block, Sequence, Type, Assignment, Function, FunctionCall, Blank, IncludeDirective, Function, FunctionReturn, StringLiteral
from .variables import StaticArray, Pointer, Counter
from .random_expressions import get_expression

int_type = Type("int")


class CodeCGenerator:
    def __init__(self,
                 max_if_nested=2,
                 max_for_nested=2,
                 max_n_if_in_block=2,
                 max_n_for_in_block=2,
                 ):

        self.max_if_nested = max_if_nested
        self.max_for_nested = max_for_nested
        self.max_n_if_in_block = max_n_if_in_block
        self.max_n_for_in_block = max_n_for_in_block
        self.min_n_new_vars_in_block = 1
        self.max_n_new_vars_in_block = 5
        self.arithmetic_operators = ["+", "-", "*"]
        self.cmp_operations = [">", "<", ">=", "<=", "==", "!="]
        self.minuses_threshold = 0.5
        self.brackets_threshold = 0.5
        self.function_calls_threshold = 0.5
        self.max_length_math_expression = 4
        self.max_assignments_in_block = 5
        self.max_arr_size = 20
        self.max_int_value = 1000
        self.max_count_function_args = 3
        self.writer = cfile.Writer(cfile.StyleOptions())

    def generate_int_vars_from_any_vars(self, vars):
        int_type_vars = []
        for var in vars:
            # if isinstance(var, Pointer):
            #     if var.mem_size:
            #         int_type_vars.append(var[randint(0, var.mem_size - 1)])
            if isinstance(var, StaticArray):
                int_type_vars.append(var[randint(0, var.array - 1)])
            elif not isinstance(var, Counter):
                int_type_vars.append(var)
        return int_type_vars

    def generate_math_expression(self, vars):
        int_type_vars = self.generate_int_vars_from_any_vars(vars)
        var_names = [int_type_var.name for int_type_var in int_type_vars]
        return get_expression(var_names,
                              self.arithmetic_operators,
                              randint(1, self.max_length_math_expression),
                              randint(1, 100000),
                              minuses_threshold=self.minuses_threshold,
                              brackets_treshold=self.brackets_threshold
                              )

    def generate_operator_if(self, vars):
        operator = choice(self.cmp_operations)
        condition = self.generate_math_expression(vars) + \
            f" {operator} " + self.generate_math_expression(vars)
        return FunctionCall("if", [condition])

    def generate_operator_for(self, existing_vars, min_n_iterations, max_n_iterations):
        seq_number = len(existing_vars)
        counter = Counter(f"i{seq_number + 1}", int_type)
        counter_declaration = self.writer.write_str_elem(
            Declaration(counter, 0))
        n_iterations = randint(min_n_iterations, max_n_iterations)
        stop_condition = f"{counter.name} < {n_iterations}"
        step = f"{counter.name}++"
        return FunctionCall("for", [f"{counter_declaration}; {stop_condition}; {step}"])

    def generate_right_value(self, vars: list[Variable], function_calls: dict = {}):
        if function_calls and random() > self.function_calls_threshold:
            function = choice(list(function_calls.keys()))
            function_calls[function] = True
            int_type_vars = self.generate_int_vars_from_any_vars(vars)
            args = [choice(int_type_vars) for _ in range(len(function.params))]
            return FunctionCall(function.name, args)
        else:
            return self.generate_math_expression(vars)

    def generate_assignment(self, vars: list[Variable], function_calls: dict = {}):
        var = choice(vars)
        # if isinstance(var, Pointer):
        #     if var.mem_size:
        #         element = var[randint(0, var.mem_size - 1)]
        #         return Assignment(element, self.generate_right_value(vars, function_calls))
        #     else:
        #         var.mem_size = randint(1, self.max_arr_size - 1)
        #         var.need_to_free_mem = True
        #         return Assignment(var.name, FunctionCall("malloc", [f"sizeof(int) * {var.mem_size}"]))
        if isinstance(var, StaticArray):
            element = var[randint(0, var.array)]
            return Assignment(element, self.generate_right_value(vars, function_calls))
        elif not isinstance(var, Counter):
            return Assignment(var, self.generate_right_value(vars, function_calls))

    def get_all_free_calls(self, vars):
        free_calls = []
        for var in vars:
            if isinstance(var, Pointer) and var.need_to_free_mem:
                free_calls.append(FunctionCall("free", [f"{var}"]))
                var.need_to_free_mem = False
                var.mem_size = 0

        return free_calls

    def generate_vars(self, vars_num, existing_vars: list[Variable] = []):
        seq_number = len(existing_vars)

        vars = [None for _ in range(vars_num)]
        for i in range(vars_num):
            var_type = choice([Variable, StaticArray])
            # if var_type is Pointer:
            #     var = Pointer(f"x{seq_number + i}", int_type)
            if var_type is StaticArray:
                var = StaticArray(f"x{seq_number + i}",
                                  int_type, randint(1, self.max_arr_size))
            else:
                var = Variable(f"x{seq_number + i}", int_type)
            vars[i] = var

        return vars

    def generate_var_declarations(self, var):
        # if isinstance(var, Pointer):
        #     return Declaration(var)
            # var.mem_size = randint(1, self.max_arr_size)
            # var.need_to_free_mem = True
            # return Declaration(var, FunctionCall("malloc", f"sizeof(int) * {var.mem_size}"))
        if isinstance(var, StaticArray):
            return Declaration(var, [randint(1, self.max_int_value) for _ in range(var.array)])
        else:
            return Declaration(var, randint(1, self.max_int_value))

    def generate_assignments_with_not_called_functions(self,
                                                       existing_vars: list[Variable] = [],
                                                       function_calls: dict = {}
                                                       ):
        not_called_functions = []
        for function, has_called in function_calls.items():
            if not has_called:
                not_called_functions.append(function)

        int_type_vars = self.generate_int_vars_from_any_vars(existing_vars)

        assignments = []
        for function in not_called_functions:
            args = [choice(int_type_vars) for _ in range(len(function.params))]
            assignments.append(Assignment(choice(int_type_vars),
                                          FunctionCall(function.name, args)))

        return assignments

    def generate_block(self,
                       n_nested_for,
                       n_for_in_block,
                       existing_vars: list[Variable] = [],
                        ):
        block = Block()

        number_new_vars = randint(
            self.min_n_new_vars_in_block, self.max_n_new_vars_in_block)
        new_vars = self.generate_vars(number_new_vars, existing_vars)
        for var in new_vars:
            block.append(Statement(self.generate_var_declarations(var)))
        vars = existing_vars + new_vars

        number_assignments = randint(1, self.max_assignments_in_block)
        for i in range(number_assignments):
            block.append(
                Statement(self.generate_assignment(vars)))

        if n_nested_for:
            for i in range(n_for_in_block):
                block.append(self.generate_operator_for(vars, 50, 100))
                block.append(self.generate_block(
                    n_nested_for - 1,
                    n_for_in_block,
                    vars,)
                )

        return block

    def generate_function(self, name, max_count_function_args):
        count_args = randint(1, max_count_function_args)
        args = [Variable(f"x{i}", int_type) for i in range(count_args)]
        return Function(name, int_type, params=args)

    def generate_function_body(self, n_nested_for, n_for_in_block) -> Block:
        body = self.generate_block(n_nested_for, n_for_in_block)
        body.append(Statement(FunctionReturn(0)))
        return body
