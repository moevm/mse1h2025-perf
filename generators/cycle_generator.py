import random
import os

class CCodeGenerator:
    def __init__(self, max_depth=1):
        self.max_depth = max_depth # Максимальная глубина вложенности циклов
        # Исходный код на C
        ''' c_code_part1:
            Первая часть исходного кода задачи, 
            Parameters:
            number (int): число - первый множитель
            multi (int): число - произведение переменных number и индексов
        '''
        self.c_code_part1 = r"""
#include <stdio.h>
#include <stdlib.h>

int main() 
{
    int number = 3;
    int multi = 0;
"""
        ''' c_code_part2:
            Вторая часть исходного кода задачи, 
            В данной части содержится код,
            который проверяет индекс i1 на выход за границы массива
        '''
        self.c_code_part2 = r"""
    if (i1 < 0 || i1 >= 10) { 
        fprintf(stderr, "Error: index out of range\n"); 
        exit(EXIT_FAILURE); 
    }
"""
        ''' c_code_part3:
            Третья часть исходного кода задачи, 
            В данной части возвращается 0
        '''
        self.c_code_part3 = r"""
    return 0;
}
"""

    def generate_random_number(self):
        '''Функция генерирует и возвращает случайное число от -100 до 100'''
        return random.randint(-100, 100)

    def random_comparison_operator(self):
        '''Функция случайно выбирает и возвращает оператор сравнения'''
        return random.choice(['<=', '>='])

    def random_comparison_operator_less(self):
        '''Функция случайно выбирает и возвращает оператор сравнения'''
        return random.choice(['<=', '<'])

    def random_comparison_operator_more(self):
        '''Функция случайно выбирает и возвращает оператор сравнения'''
        return random.choice(['>=', '>'])

    def random_sign_operator(self):
        '''Функция случайно выбирает и возвращает знак сложения или вычитания'''
        return random.choice(['-', '+'])

    def generate_counter_change(self, index_in_cycle):
        '''Функция генерирует и возвращает случайное условие изменения счетчика'''
        # Генерируем знаки изменения счетчика
        sign1 = self.random_sign_operator()
        # Соединяем знаки в одну строку условия изменения счетчика
        generated_counter_change = f"{index_in_cycle}{sign1}{sign1}" 
        return generated_counter_change

    def generate_incorrect_cycle(self, current_depth):
        '''Функция генерирует некорректную строку кода с ошибкой в цикле for'''
        # Получение индекса для текущей глубины вложенности из алфавита
        index_in_cycle = f"i{current_depth}"
        # for (index_in_cycle = number_one; index_in_cycle <= number_two ; index_in_cycle++) 
        # Генерация случайных чисел для  цикла
        number_one = self.generate_random_number()
        number_two = self.generate_random_number()
        # Формирование строки для инициализации индекса цикла
        final_index_i = f"{index_in_cycle} = {number_one}" 

        # Проверка, находится ли number_one вне допустимого диапазона
        if number_one < 0 or number_one >= 10:
            # Генерируем условие изменения счетчика
            final_counter_change = self.generate_counter_change(index_in_cycle)

            # Определение условия выхода из цикла в зависимости от значений number_one и number_two
            if number_two > number_one:
                final_condition = f"{index_in_cycle} < {number_two}" 
            elif number_two < number_one:
                final_condition = f"{index_in_cycle} > {number_two}" 
            else:
                # Если значения равны, выбираем случайный оператор сравнения
                operator_for_condition = self.random_comparison_operator()
                final_condition = f"{index_in_cycle} {operator_for_condition} {number_two}" 
        else:
            # Если number_one в допустимом диапазоне, обрабатываем number_two
            if number_two >= 11:
                # Генерация условия выхода из цикла с оператором сравнения "меньше" или "меньше или равно"
                operator_for_condition = self.random_comparison_operator_less()
                final_condition = f"{index_in_cycle} {operator_for_condition} {number_two}" 
                final_counter_change = f"{index_in_cycle}++" # Увеличение индекса
            elif number_two < 0:
                # Генерация условия выхода из цикла с оператором сравнения "больше" или "больше или равно"
                operator_for_condition = self.random_comparison_operator_more()
                final_condition = f"{index_in_cycle} {operator_for_condition} {number_two}" 
                final_counter_change = f"{index_in_cycle}--" # Уменьшение индекса
            else:
                final_condition = f" " # Пустое условие выхода из цикла
                # Генерация изменения счетчика
                final_counter_change = self.generate_counter_change(index_in_cycle)

        # Соединяем условия выхода из цикла и изменения счетчика в одну строку
        string_for = f"for ({final_index_i}; {final_condition}; {final_counter_change})"
        return string_for

    def tabulate_code(self, code, depth):
        '''Функция табулирует код в зависимости от глубины вложенности'''
        # Инициализация пустой строки для хранения табулированного кода
        tabulated_code = ""  
        # Определение отступа в зависимости от глубины вложенности
        indentation = "    " * depth 

        # Разделение входного кода на строки и добавление отступа к каждой строке
        for line in code.strip().splitlines():
            # Добавление отступа к текущей строке и добавление её в tabulated_code
            tabulated_code += f"{indentation}{line}\n" 
        return "    " + tabulated_code  

    def generate_incorrect_c_code(self):
        '''Функция генерирует некорректный код с ошибкой в цикле for'''
        loops_for = ""  # Инициализация пустой строки для хранения кода циклов for
        indices = "    int "  # Инициализация строки для объявления переменных индексов
        array_dimensions = ""  # Инициализация строки для хранения размеров массивов
        multiplication = ""  # Инициализация строки для хранения выражения умножения
        open_bracket = r"{"  # Открывающая фигурная скобка для блока кода
        close_bracket = r"}"  # Закрывающая фигурная скобка для блока кода
        close_brackets = ""  # Инициализация строки для хранения закрывающих скобок
        array_code = "" # Инициализация пустой строки для хранения кода массивов

        # Цикл для генерации кода в зависимости от глубины вложенности
        for current_depth in range(1, self.max_depth + 1):
            index = f"i{current_depth}"  # Получение текущего индекса из алфавита
            indices += f"{index}"  # Добавление индекса к строке объявлений переменных
            array_dimensions += f"[{index}]"  # Формирование размеров массива
            multiplication += f"{index} * "  # Формирование выражения для умножения
            tabs = "    " * current_depth  # Определение отступа в зависимости от глубины вложенности

            # Генерация вложенного цикла
            nested_code = self.generate_incorrect_cycle(current_depth)  # Генерация кода для вложенного цикла
            loops_for += f"{tabs}{nested_code} {open_bracket}\n"  # Добавление кода цикла в строку loops_for
            close_brackets = f"{tabs}{close_bracket}\n" + close_brackets  # Добавление закрывающей скобки

            # Определение переменной multi и массива numbers
            if current_depth < self.max_depth:
                indices += f", "  # Добавление запятой для следующего индекса
            else:
                # Если достигнута максимальная глубина, добавляем код для переменной multi
                multi = f"    {tabs}multi = {multiplication}number;\n"
                multi_array = f"    {tabs}numbers_{index}{array_dimensions} = multi;\n"
                print_statement = f"    {tabs}printf(\"multi = %d\\n\", multi);\n"  # Формирование строки для вывода
                tabuleted_code = self.tabulate_code(self.c_code_part2, current_depth)  # Табулирование кода
                loops_for += tabuleted_code + multi + multi_array + print_statement  # Добавление всех строк в loops_for

        # Формирование размера массива: current_depth определяет количество измерений
        array_dimensions_const = self.max_depth * "[10]"
        # Добавление строки объявления массива в код
        # Формат: int numbers_<буква>[10][10]... (в зависимости от глубины)
        array_code = f"    int numbers_{index}{array_dimensions_const};\n"
        indices += f";\n"  # Добавление последнего индекса с точкой с запятой
        # Формирование полного кода C, объединяя все части
        c_code = self.c_code_part1 + indices + array_code + loops_for + close_brackets + self.c_code_part3
        return c_code  # Возврат сгенерированного кода

    def write_c_code_to_file(self, file_path):
        '''Функция записывает код с ошибкой в файл'''
        # Генерируем некорректный код с ошибкой в цикле
        c_code = self.generate_incorrect_c_code()
        # Получаем директорию из пути к файлу
        directory = os.path.dirname(file_path)
        # Создаём директорию, если она не существует
        os.makedirs(directory, exist_ok=True)
        # Открываем и записываем полученный код в файл
        with open(file_path, 'w') as file:
            file.write(c_code)

# Использование класса
if __name__ == "__main__":  # Проверяем, что скрипт запущен как основная программа
    try:
        # Запрашиваем у пользователя ввод максимальной глубины вложенности циклов
        max_depth = int(input("Введите максимальную глубину вложенности циклов: "))  
        if max_depth < 1 or max_depth > 100:  # Проверяем, что введенное значение положительное
            raise ValueError("Глубина должна быть положительным целым числом, меньше или равным 100.")  # Если значение меньше 1, выбрасываем исключение
    except ValueError as e:  # Обрабатываем исключения, возникающие при некорректном вводе
        print(f"Ошибка ввода: {e}")  # Выводим сообщение об ошибке
    else:  # Если исключений не возникло
        generator = CCodeGenerator(max_depth=max_depth)  # Создаем экземпляр класса CCodeGenerator с заданной глубиной
        output_file_path = "generators/data/generators_files/generated_code_with_cycle.c"  # Указываем путь к файлу для сохранения сгенерированного кода
        generator.write_c_code_to_file(output_file_path)  # Вызываем метод для записи сгенерированного кода в файл
        print(f"Код успешно сгенерирован и записан в файл: {output_file_path}")  # Сообщаем пользователю об успешном завершении операции

