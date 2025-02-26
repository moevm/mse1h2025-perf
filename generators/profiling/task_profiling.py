from random import choice, seed
from cfile.core import Sequence, Function, Declaration, Statement, IncludeDirective, Blank, Block, Type, FunctionCall
from .code_c_generator import CodeCGenerator


int_type = Type("int")

description = """
Определить название самой долго выполняющейся функции, запускающейся из функции main.
"""

def generate_profiling_task(number_functions,
                  norm_n_nested_for,
                  norm_n_for_in_block,
                  deviant_n_nested_for,
                  deviant_n_for_in_block,
                  random_seed):
    seed(random_seed)
    
    functions = [Function(f"f{i}", int_type) for i in range(number_functions)]
    slow_function = choice(functions)
    answer = slow_function.name
    code = Sequence()
    code.append(IncludeDirective("stdlib.h", True))
    code.append(Blank())

    generator = CodeCGenerator()
    for function in functions:
        code.append(Declaration(function))
        if function == slow_function:
            function_body = generator.generate_function_body(deviant_n_nested_for, deviant_n_for_in_block)
        else:
            function_body = generator.generate_function_body(norm_n_nested_for, norm_n_for_in_block)
        code.append(function_body)

    main_function = Function("main", "int")
    code.append(Declaration(main_function))
    function_body = Block()
    for function in functions:
        function_body.append(Statement(FunctionCall(function.name)))
    code.append(function_body)

    return {
        "code": code,
        "description": description,
        "answer": answer
    }