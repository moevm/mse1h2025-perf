import random
'''Задача 1, цикл for: 
 Вывести значения произведения числа k на i, значение которого изменяется от 1 до 10 включительно'''

# Корректное условие для задачи (i; i <= 10; i++)
correct_condition = "i <= 10"
correct_counter_change = "i++"

# Исходный код на C

''' c_code_part1:
    Первая часть исходного кода задачи, 
    которая в дальнейшем будет соединена с созданными условиями для цикла for
    В данной части создаются переменные
    Parameters:
    k (int): число - первый множитель
    i (int): число - второй множитель, значение которого изменяется от 1 до 10
    multi (int): число - произведение переменных k и i
 '''
c_code_part1 = r"""
#include <stdio.h>

int main() 
{
  int k = 3;
  int i = 1;
  int multi = 0;
"""
''' c_code_part2:
    Вторая часть исходного кода задачи, 
    которая в дальнейшем будет соединена с созданными условиями для цикла for
    В данной части содержится код,
    который будет выполняться в цикле for,
    а именно произведение переменных k и i,
    вывод результата. А также возвращается 0
 '''
c_code_part2 = r"""
  {
    multi = k * i;
    printf("multi = %d\n", multi);
  }
  
  return 0;
}
"""

def generate_random_number():
    '''Функция генерирует и возвращает случайное число от 1 до 100'''
    return random.randint(1, 100)

def random_comparison_operator():
    '''Функция случайно выбирает и возвращает оператор сравнения'''
    return random.choice(['<', '<=', '>', '>='])

def random_sign_operator():
    '''Функция случайно выбирает и возвращает знак сложения или вычитания'''
    return random.choice(['-', '+'])

def generate_condition():
    '''Функция генерирует и возвращает случайное условие выхода из цикла'''
    # Генерируем число для условия выхода из цикла
    num_for_condition = generate_random_number()
    # Генерируем оператор для условия выхода из цикла
    operator_for_condition = random_comparison_operator()
    # Соединяем число и оператор в одну строку условия выхода из цикла
    generated_condition = f"i {operator_for_condition} {num_for_condition}" 
    return generated_condition

def generate_counter_change():
    '''Функция генерирует и возвращает случайное условие изменения счетчика'''
    # Генерируем знаки изменения счетчика
    sign1 = random_sign_operator()
    # Соединяем знаки в одну строку условия изменения счетчика
    generated_counter_change = f"i{sign1}{sign1}" 
    return generated_counter_change

def is_equal_to_correct_string(condition, counter_change):
    '''Функция проверяет, что хотя бы одно из условий было некорректно,
       Иначе случайным образом изменяет одно из условий
    '''
    # Пока сгенерированные условия выхода из цикла и изменения счетчика равны корректным условиям для задачи
    while (condition == correct_condition and counter_change == correct_counter_change):
        # Генерируем случайное число для выбора условия, которое необходимо изменить
        random_num = random.randint(1, 2)
        # Если число равно 1, то изменяем условие выхода из цикла
        if random_num == 1:
            condition = generate_condition()
        # Если число равно 2, то изменяем условие изменения счетчика
        if random_num == 2:
            counter_change = generate_counter_change()
    # Возвращаем итоговые условия выхода из цикла и изменения счетчика
    return condition, counter_change

def generate_incorrect_c_code():
    '''Функция генерирует некорректный код с ошибкой в цикле for'''
    # Генерируем условие выхода из цикла
    final_condition = generate_condition()
    # Генерируем условие изменения счетчика
    final_counter_change = generate_counter_change()
    # Проверяем условия на некорректность 
    final_condition, final_counter_change = is_equal_to_correct_string(final_condition, final_counter_change)
    # Соединяем условия выхода из цикла и изменения счетчика в одну строку
    string_for = f"  for (i; {final_condition}; {final_counter_change})"
    # Соединяем все части кода 
    c_code = c_code_part1 + string_for + c_code_part2
    return c_code

def write_c_code_to_file(filename):
    '''Функция записывает код с ошибкой в файл'''
    # Генерируем некорректный код с ошибкой в цикле
    c_code = generate_incorrect_c_code()
    # Открываем и записываем полученный код в файл
    with open(filename, 'w') as file:
        file.write(c_code)

# Указываем имя файла для записи
output_filename = "task.c"
write_c_code_to_file(output_filename)
