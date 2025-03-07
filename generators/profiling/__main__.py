import argparse
from cfile import StyleOptions
from cfile.writer import Writer
from task_to_find_slow_function import generate_task_to_find_slow_function


def get_args():
    parser = argparse.ArgumentParser(
        description="""
        Генерация исходного кода программы для задачи на профилирование
        """)
    
    parser.add_argument("--task",  "-t",
                        type=int, required=True,
                        help="номер задания")
    
    parser.add_argument("--mode",  "-m",
                        type=str, required=True,
                        help='"init" или "check"')

    parser.add_argument("--number_funcrions",  "-f",
                        type=int, default=10,
                        help="число генерируемых функций")

    parser.add_argument("--random_seed",  "-s",
                        type=str, required=True,
                        help="целое число, которое используется в качестве начального значения для генерации случайных чисел")

    parser.add_argument("--norm_depth_for",  "-d",
                        type=str, required=True,
                        help='диапазон глубины вложенности циклов нормальной функции - "<min>,<max>"')

    parser.add_argument("--deviant_depth_for",  "-D",
                        type=str, required=True,
                        help='диапазон глубины вложенности циклов отличающейся функции - "<min>,<max>"')

    parser.add_argument("--norm_n_nested_for",  "-n",
                        type=str, required=True,
                        help='диапазон числа вложенных циклов нормальной функции - "<min>,<max>"')

    parser.add_argument("--deviant_n_nested_for",  "-N",
                        type=str, required=True,
                        help='диапазон числа вложенных циклов отличающейся функции - "<min>,<max>"')

    parser.add_argument("--output", "-o",
                        type=str, default="main.c",
                        help="имя выходного файла")

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    if args.task == 1:
        if args.mode == "init":
            task = generate_task_to_find_slow_function(
                args.number_funcrions,
                list(map(int, args.norm_depth_for.split(","))),
                list(map(int, args.norm_n_nested_for.split(","))),
                list(map(int, args.deviant_depth_for.split(","))),
                list(map(int, args.deviant_n_nested_for.split(","))),
                args.random_seed,
            )
            writer = Writer(StyleOptions())
            writer.write_file(task["code"], args.output)
