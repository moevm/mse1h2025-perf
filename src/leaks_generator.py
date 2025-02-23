import random

#Начало кода - библиотеки языка и сигнатуры для возможных функций обработки динамических массивов в задаче
def libraries_and_signatures():
    return """#include <stdio.h>
#include <stdlib.h>

//void process_array(int *arr, int size);
    """

#инициализация функции мейн и переменных
def main_var_init_code(sizeof_arr):
    return f"""
int main() {{
    int *array1, *array2, *array3;
    int sizeof_arr = {sizeof_arr};
    """

#Обработка случайного выбора(см. ф-ю generate_leaky_code)
def process_first_choice(free_flag):
    code = """
    array1 = (int *)malloc(sizeof(int)*sizeof_arr); 
    """
    if free_flag:
        return code
    return code+"""free(array1);
    """

#Обработка случайного выбора(см. ф-ю generate_leaky_code)
def process_second_choice(free_flag):
    code = """
    array2 = (int *)malloc(sizeof(int)*sizeof_arr); 
    """
    if free_flag:
        return code
    return code+"""free(array2);
    """

#Обработка случайного выбора (см. ф-ю generate_leaky_code)
def process_third_choice(free_flag):
    code = """
    array3 = (int *)malloc(sizeof(int)*sizeof_arr); 
    """
    if free_flag:
        return code
    return code+"""free(array3);
    """

#конец кода
def end_the_code():
    return """
    return 0;
}
    """

#Включение всех частей кода
def generate_leaky_code(sizeof_arr):
    # Статическая часть кода
    code = libraries_and_signatures();
    code += main_var_init_code(sizeof_arr)

    # Выбор случайного места для утечки памяти (malloc)
    leak_location = random.choice([1, 2, 3])

    # Добавление выделений памяти с возможной утечкой
    code += process_first_choice(leak_location==1)
    code += process_second_choice(leak_location==2)
    code += process_third_choice(leak_location==3)

    code += end_the_code()
    return code


# Генерация кода
generated_code = generate_leaky_code(5)

# Запись сгенерированного кода в файл
with open("generated.c", "w") as file:
    file.write(generated_code)

print("C code with memory leak has been written to generated.с")
