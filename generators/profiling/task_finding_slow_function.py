from random import choice, seed
from cfile.core import Sequence, Function, Declaration, Statement, IncludeDirective, Blank, Block, Type, FunctionCall
from function_generator import FunctionGenerator

int_type = Type("int")


class TaskFindingSlowFunctionGenerator:
    def __init__(self,
                 number_functions,
                 # диапазон глубины вложенности циклов нормальной функции
                 norm_range_nesting_depth_for: tuple[int, int],
                 # диапазон числа вложенных циклов нормальной функции
                 norm_range_n_nested_for: tuple[int, int],
                 # диапазон глубины вложенности циклов отличающейся функции
                 deviant_range_nesting_depth_for: tuple[int, int],
                 # диапазон числа вложенных циклов отличающейся функции
                 deviant_range_n_nested_for: tuple[int, int],
                 ):
        self.number_functions = number_functions
        self.norm_range_nesting_depth_for = norm_range_nesting_depth_for
        self.norm_range_n_nested_for = norm_range_n_nested_for
        self.deviant_range_nesting_depth_for = deviant_range_nesting_depth_for
        self.deviant_range_n_nested_for = deviant_range_n_nested_for

    def generate_task(self, random_seed) -> Sequence:
        """Генерация программы с вызовами функций, одна из которых выполняется
        дольше либо быстрее отстальных."""

        seed(random_seed)

        functions = [
            Function(f"f{i}", int_type)
            for i in range(self.number_functions)
        ]
        deviant_function = choice(functions)

        answer = deviant_function.name

        code = Sequence()
        code.append(IncludeDirective("stdlib.h", True))
        code.append(Blank())

        generator = FunctionGenerator()
        for function in functions:
            code.append(Declaration(function))
            if function == deviant_function:  # генерация тела отличающейся функции
                function_body = generator.generate_function_body(
                    self.deviant_range_nesting_depth_for[0],
                    self.deviant_range_nesting_depth_for[1],
                    self.deviant_range_n_nested_for[0],
                    self.deviant_range_n_nested_for[1]
                )
            else:  # генерация тела нормальной функции
                function_body = generator.generate_function_body(
                    self.norm_range_nesting_depth_for[0],
                    self.norm_range_nesting_depth_for[1],
                    self.norm_range_n_nested_for[0],
                    self.norm_range_n_nested_for[1]
                )
            code.append(function_body)

        main_function = Function("main", "int")
        code.append(Declaration(main_function))
        function_body = Block()
        for function in functions:  # вызов всех функций в функции main
            function_body.append(Statement(FunctionCall(function.name)))
        code.append(function_body)

        return {
            "code": code,
            "answer": answer
        }