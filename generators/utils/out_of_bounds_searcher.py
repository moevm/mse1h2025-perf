import re

def find_potential_array_out_of_bounds(c_code):
    # Найти объявления массивов
    array_declarations = {}  # Словарь для хранения имен массивов и их размеров
    array_declarations_use = {}  # Словарь для хранения присвоений массивов
    issues = {}  # Словарь для хранения найденных проблем

    # Разбиваем код на строки
    lines = c_code.splitlines()

    # Проходим по каждой строке
    for line in lines:
        # Паттерн для поиска объявлений массивов
        array_decl = re.match(r'\s*int\s+(\w+)\[(\d+)\]', line)
        # Паттерн для поиска присвоений с использованием массивов
        assignment_pattern = re.match(r'\s*(\w+)\[(.*?)\]\s*=\s*(.*?);', line)

        if array_decl:
            # Если найдено объявление массива, сохраняем имя и размер
            array_name = array_decl.group(1)
            array_size = int(array_decl.group(2))
            array_declarations[array_name] = array_size

        if assignment_pattern:
            # Если найдено присвоение, сохраняем имя массива и индекс
            array_name_use = assignment_pattern.group(1)
            index_expr = assignment_pattern.group(2).strip()
            if "][" in index_expr:
                # Если индекс состоит из нескольких частей, разбиваем его
                parts = index_expr.split("][")
                if array_name_use in array_declarations_use:
                    array_declarations_use[array_name_use].extend(parts)
                else:
                    array_declarations_use[array_name_use] = parts
            else:
                array_declarations_use[array_name_use] = index_expr
            

    # Проверка диапазонов индексов в циклах
    for line_num, line in enumerate(lines):
        errors = []  # Список для хранения ошибок в текущей строке
        # Паттерн для поиска циклов for
        for_loop = re.search(r'for\s*\(([^)]+)\)', line)
            
        if for_loop:
            # Извлечение и анализ переменной цикла
            loop_var = re.search(r'(\w+)\s*=\s*([^;]+)', for_loop.group(1))
            if loop_var:
                loop_index = loop_var.group(1).strip()
                # Определение границ цикла (начальное и конечное значения)
                boundaries = re.findall(r'-?\d+', for_loop.group(1))
                if boundaries:
                    start_index = int(boundaries[0])
                    end_index = int(boundaries[-1])

                    for array_name, array_size in array_declarations.items():
                        # Проверка индексов на выход за границы
                        if loop_index in array_declarations_use[array_name]:
                            if len(boundaries) == 1:
                                if start_index < 0 or start_index >= array_size:
                                    probl = f"начальный индекс {start_index} за пределами массива {array_name}, пустое условие выхода из цикла"
                                    errors.append(probl)
                                else:
                                    errors.append("пустое условие выхода из цикла")
                            else:
                                if (start_index < 0 or start_index >= array_size) and (end_index < 0 or end_index >= array_size):
                                    probl = f"начальный {start_index} и конечный {end_index} индексы за пределами массива {array_name}"
                                    errors.append(probl)
                                elif start_index < 0 or start_index >= array_size:
                                    probl = f"начальный индекс {start_index} за пределами массива {array_name}"
                                    errors.append(probl)
                                elif end_index < 0 or end_index >= array_size:
                                    probl = f"конечный индекс {end_index} за пределами массива {array_name}"
                                    errors.append(probl)
                        # Если есть ошибки, добавляем их в словарь
                        if errors:
                            issues[line_num] = errors
    return issues


if __name__ == "__main__":
    # Статически заданное имя файла
    filename = "generated_code_with_cycle.c"  # Имя C-файла

    try:
        # Читаем содержимое файла
        with open(filename, "r") as f:
            c_code = f.read()

        # Ищем потенциальные проблемы
        issues_in_code = find_potential_array_out_of_bounds(c_code)

        if issues_in_code:
            print("Обнаружены потенциальные проблемы:")
            for line, description in issues_in_code.items():
                # Выводим номер строки с ошибкой
                print("Строка с ошибкой:", line + 1)
                for issue in description:
                    # Выводим описание каждой проблемы
                    print(f"Описание: {issue}")
        else:
            print("Потенциальных проблем с выходом за границы массива не обнаружено.")
            
    # Обработка ошибки, если файл не найден
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")

