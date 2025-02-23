from codeCGenerator import CodeCGenerator

g = CodeCGenerator()
code = g.generate_function("main")
code = g.add_includes(code)
g.write_code(code, "test.c")