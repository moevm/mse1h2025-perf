import re

def find_potential_array_out_of_bounds(c_code):
    '''Функция ищет некорректный код с ошибкой в цикле for'''
    # Найти объявления массивов
    array_declarations = {}  # Словарь для хранения имен массивов и их размеров
    array_declarations_use = {}  # Словарь для хранения присвоений массивов
    issues = {}  # Словарь для хранения найденных проблем
    lines_and_issues = {} # Словарь для хранения найденных проблем и номеров строк
    boundaries = 1 # Число для определения пустого условия

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
    
    # Регулярное выражение для поиска условий цикла for
    pattern = r'for\s*\((.*?)\)\s*{'
    # Найти все совпадения
    matches = re.findall(pattern, c_code, re.DOTALL)
    # Список для хранения найденных условий с ошибкой
    conditions = []
    
    for match in matches:
        errors = []  # Список для хранения ошибок в текущей строке
        # Извлечение переменной цикла
        loop_index = match.split('=')[0].strip()
        # Находит числа после знака '='
        assignment_number = re.search(r'=\s*([-+]?\d+)', match)
        # Находит числа после знаков сравнения
        comparison_number = re.search(r'([<>]=?)\s*([-+]?\d+)', match)
        # Определение границ цикла (начальное и конечное значения)
        if assignment_number and comparison_number:
            start_index = int(assignment_number.group(1))
            end_index = int(comparison_number.group(2))
            boundaries = 2
        elif assignment_number:
            start_index = int(assignment_number.group(1))
            end_index = start_index
            boundaries = 1
        for array_name, array_size in array_declarations.items():
            # Проверка индексов на выход за границы
            if loop_index in array_declarations_use[array_name]:
                if boundaries == 1:
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
                if match not in conditions:
                    conditions.append(match)
                issues[match] = errors

    # Добавляем в словарь номера строк в коде и соответствующую ошибку
    for i, line in enumerate(lines):
        for error in conditions:
            if error in line:
                lines_and_issues[i + 1] = issues[error]

    return lines_and_issues


def find_potential_errors_array_out_of_bounds(filename):
    '''Функция считывает содержимое файла с кодом и запускает функцию поиска ошибки'''
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
                print("Строка с ошибкой:", line)
                for issue in description:
                    # Выводим описание каждой проблемы
                    print(f"Описание: {issue}")
        else:
            print("Потенциальных проблем с выходом за границы массива не обнаружено.")
            
    # Обработка ошибки, если файл не найден
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")


if __name__ == "__main__":
    filename = "generated_code_with_cycle.c"
    find_potential_errors_array_out_of_bounds(filename)
