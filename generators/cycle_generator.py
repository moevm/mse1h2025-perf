import random

# Исходный код на C

''' c_code_part1:
    Первая часть исходного кода задачи, 
    которая в дальнейшем будет соединена с созданными условиями для цикла for
    В данной части создаются переменные, второй множитель будет задаваться в цикле for
    Parameters:
    k (int): число - первый множитель
    multi (int): число - произведение переменных k и i
    numbers[10] - массив для хранения результатов перемножения
 '''
c_code_part1 = r"""
#include <stdio.h>
#include <stdlib.h>

int main() 
{
  int k = 3;
  int multi = 0;
  int numbers[10];
"""
''' c_code_part2:
    Вторая часть исходного кода задачи, 
    которая в дальнейшем будет соединена с созданными условиями для цикла for
    В данной части содержится код,
    который будет выполняться в цикле for,
    а именно произведение переменных k и i, 
    проверка индекса i на выход за границы массива,
    сохранение результата перемножения в массив
    вывод результата. А также возвращается 0
 '''
c_code_part2 = r"""
  {
    multi = k * i;
    if (i < 0 || i >= 10) { 
      fprintf(stderr, "Error: index out of range\n"); 
      exit(EXIT_FAILURE); 
    }
    numbers[i] = multi;
    printf("multi = %d\n", numbers[i]);
  }
  
  return 0;
}
"""

def generate_random_number():
    '''Функция генерирует и возвращает случайное число от -100 до 100'''
    return random.randint(-100, 100)

def random_comparison_operator():
    '''Функция случайно выбирает и возвращает оператор сравнения'''
    return random.choice(['<=', '>='])

def random_comparison_operator_less():
    '''Функция случайно выбирает и возвращает оператор сравнения'''
    return random.choice(['<=', '<'])

def random_comparison_operator_more():
    '''Функция случайно выбирает и возвращает оператор сравнения'''
    return random.choice(['>=', '>'])

def random_sign_operator():
    '''Функция случайно выбирает и возвращает знак сложения или вычитания'''
    return random.choice(['-', '+'])

def generate_condition(num):
    '''Функция генерирует и возвращает случайное условие выхода из цикла'''
    # Выставляем число для условия выхода из цикла
    num_for_condition = num
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

def generate_incorrect_c_code():
    '''Функция генерирует некорректный код с ошибкой в цикле for'''
    # for (int i = a; i <= b ; i++) 
    # Генерируем индекс a
    index_a = generate_random_number()
    # Генерируем индекс b, число для условия выхода из цикла
    index_b = generate_random_number()
    # Генерируем начальную строку с индексом i
    final_index_i = f"int i = {index_a}" 
    if index_a < 0 or index_a >= 10:
        # Генерируем условие изменения счетчика
        final_counter_change = generate_counter_change()
        if index_b > index_a:
            # Генерируем условие выхода из цикла
            final_condition = f"i < {index_b}" 
        elif index_b < index_a:
            # Генерируем условие выхода из цикла
            final_condition = f"i > {index_b}" 
        else:
            # Генерируем оператор для условия выхода из цикла
            operator_for_condition = random_comparison_operator()
            # Генерируем условие выхода из цикла
            final_condition = f"i {operator_for_condition} {index_b}" 
    else:
        if index_b >= 11:
            # Генерируем оператор для условия выхода из цикла
            operator_for_condition = random_comparison_operator_less()
            # Генерируем условие выхода из цикла
            final_condition = f"i {operator_for_condition} {index_b}" 
            # Генерируем условие изменения счетчика
            final_counter_change = f"i++"
        elif index_b < 0:
            # Генерируем оператор для условия выхода из цикла
            operator_for_condition = random_comparison_operator_more()
            # Генерируем условие выхода из цикла
            final_condition = f"i {operator_for_condition} {index_b}" 
            # Генерируем условие изменения счетчика
            final_counter_change = f"i--"
        else:
            # Генерируем условие выхода из цикла
            final_condition = f" "
            # Генерируем условие изменения счетчика
            final_counter_change = generate_counter_change()
    # Соединяем условия выхода из цикла и изменения счетчика в одну строку
    string_for = f"  for ({final_index_i};{final_condition}; {final_counter_change})"
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
output_filename = "generated_code_with_cycle.c"
write_c_code_to_file(output_filename)
