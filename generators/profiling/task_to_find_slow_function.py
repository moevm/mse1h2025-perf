from random import choice, seed
from cfile.core import Sequence, Function, Declaration, Statement, IncludeDirective, Blank, Block, Type, FunctionCall
from function_generator import FunctionGenerator

int_type = Type("int")


def generate_task_to_find_slow_function(
        number_functions,
        # диапазон глубины вложенности циклов нормальной функции
        norm_range_nesting_depth_for: tuple[int, int],
        # диапазон числа вложенных циклов нормальной функции
        norm_range_n_nested_for: tuple[int, int],
        # диапазон глубины вложенности циклов отличающейся функции
        deviant_range_nesting_depth_for: tuple[int, int],
        # диапазон числа вложенных циклов отличающейся функции
        deviant_range_n_nested_for: tuple[int, int],
        random_seed
):
    """Генерация программы с вызовами функций, одна из которых выполняется
     дольше либо быстрее отстальных."""

    seed(random_seed)

    functions = [Function(f"f{i}", int_type) for i in range(number_functions)]
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
                deviant_range_nesting_depth_for[0],
                deviant_range_nesting_depth_for[1],
                deviant_range_n_nested_for[0],
                deviant_range_n_nested_for[1]
            )
        else:  # генерация тела нормальной функции
            function_body = generator.generate_function_body(
                norm_range_nesting_depth_for[0],
                norm_range_nesting_depth_for[1],
                norm_range_n_nested_for[0],
                norm_range_n_nested_for[1]
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
