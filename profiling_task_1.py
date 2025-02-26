import subprocess

def create_c_file1(filename, code):
    """
    Создает файл с расширением .c и заполняет его кодом
    """
    try:
        # Добавляем расширение .c если его нет
        if not filename.endswith('.c'):
            filename += '.c'
            
        # Создаем файл и записываем код
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(code)
            
        print(f"Файл {filename} успешно создан")
        return True
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return False

code1 = """#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

// Функция для сравнения символов при сортировке
int compare_chars(const void *a, const void *b) {
    return (*(char*)a - *(char*)b);
}

// Функция для проверки являются ли строки анаграммами
int are_anagrams(char *str1, char *str2) {
    // Если длины строк разные, они не могут быть анаграммами
    if (strlen(str1) != strlen(str2)) {
        return 0;
    }

    // Создаем копии строк для сортировки
    char *str1_copy = (char*)malloc(strlen(str1) + 1);
    char *str2_copy = (char*)malloc(strlen(str2) + 1);

    // Проверяем успешность выделения памяти
    if (!str1_copy || !str2_copy) {
        free(str1_copy);
        free(str2_copy);
        return 0;
    }

    // Копируем строки
    strcpy(str1_copy, str1);
    strcpy(str2_copy, str2);

    // Сортируем обе копии строк
    qsort(str1_copy, strlen(str1_copy), sizeof(char), compare_chars);
    qsort(str2_copy, strlen(str2_copy), sizeof(char), compare_chars);

    // Сравниваем отсортированные строки
    int result = strcmp(str1_copy, str2_copy) == 0;

    // Освобождаем память
    free(str1_copy);
    free(str2_copy);

    return result;
}

int main() {
    // Генерируем случайную длину строки
    srand(time(NULL));
    size_t len = rand() % 10000 + 1; // длина от 1 до 10000

    // Создаем две строки с динамической длиной
    char *str1 = (char*)malloc(len + 1);
    char *str2 = (char*)malloc(len + 1);

    // Проверяем успешность выделения памяти
    if (!str1 || !str2) {
        free(str1);
        free(str2);
        return 1;
    }

    // Заполняем первую строку случайными символами
    for(size_t i = 0; i < len; i++) {
        str1[i] = 'a' + rand() % 26;
    }
    str1[len] = '\\0';

    // Создаем вторую строку как перестановку первой
    for(size_t i = 0; i < len; i++) {
        size_t pos = rand() % (len - i);
        str2[i] = str1[pos];
        str1[pos] = str1[len - i - 1];
    }
    str2[len] = '\\0';

    // Измеряем время выполнения
    clock_t start_time = clock();

    // Проверяем являются ли строки анаграммами
    int result = are_anagrams(str1, str2);

    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    // Выводим результаты с размерами строк
    printf("Длина первой строки: %zu", len);
    printf("\\n");
    printf("Первая строка: %.20s...", str1);
    printf("\\n");
    printf("Длина второй строки: %zu", len);
    printf("\\n");
    printf("Вторая строка: %.20s...", str2);
    printf("\\n");
    printf("Являются ли строки анаграммами: %s", result ? "Да" : "Нет");
    printf("\\n");
    printf("Время выполнения: %.6f секунд", elapsed_time);
    printf("\\n");

    // Освобождаем память
    free(str1);
    free(str2);

    return 0;
}
"""

# Создаем файл
create_c_file1("test1", code1)


def create_c_file2(filename, code):
    """
    Создает файл с расширением .c и заполняет его кодом
    """
    try:
        # Добавляем расширение .c если его нет
        if not filename.endswith('.c'):
            filename += '.c'
            
        # Создаем файл и записываем код
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(code)
            
        print(f"Файл {filename} успешно создан")
        return True
    except Exception as e:
        print(f"Ошибка при создании файла: {e}")
        return False

# Пример использования
code2 = """#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

// Функция для проверки являются ли строки анаграммами
int are_anagrams(char *str1, char *str2) {
    // Если длины строк разные, они не могут быть анаграммами
    if (strlen(str1) != strlen(str2)) {
        return 0;
    }

    // Создаем массив для подсчета символов
    int count[256] = {0}; // 256 для всех возможных ASCII символов

    // Подсчитываем символы в первой строке
    for (size_t i = 0; str1[i]; i++) {
        count[(unsigned char)str1[i]]++;
    }

    // Вычитаем символы второй строки
    for (size_t i = 0; str2[i]; i++) {
        count[(unsigned char)str2[i]]--;
    }

    // Проверяем, все ли счетчики равны нулю
    for (int i = 0; i < 256; i++) {
        if (count[i] != 0) {
            return 0;
        }
    }

    return 1;
}

int main() {
    // Генерируем случайную длину строки
    srand(time(NULL));
    size_t len = rand() % 10000 + 1;

    // Создаем две строки с динамической длиной
    char *str1 = (char*)malloc(len + 1);
    char *str2 = (char*)malloc(len + 1);

    // Проверяем успешность выделения памяти
    if (!str1 || !str2) {
        free(str1);
        free(str2);
        return 1;
    }

    // Заполняем первую строку случайными символами
    for(size_t i = 0; i < len; i++) {
        str1[i] = 'a' + rand() % 26;
    }
    str1[len] = '\\0';

    // Создаем вторую строку как перестановку первой
    for(size_t i = 0; i < len; i++) {
        size_t pos = rand() % (len - i);
        str2[i] = str1[pos];
        str1[pos] = str1[len - i - 1];
    }
    str2[len] = '\\0';

    // Измеряем время выполнения
    clock_t start_time = clock();

    // Проверяем являются ли строки анаграммами
    int result = are_anagrams(str1, str2);

    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    // Выводим результаты с размерами строк
    printf("Длина первой строки: %zu", len);
    printf("\\n");
    printf("Первая строка: %.20s...", str1);
    printf("\\n");
    printf("Длина второй строки: %zu", len);
    printf("\\n");
    printf("Вторая строка: %.20s...", str2);
    printf("\\n");
    printf("Являются ли строки анаграммами: %s", result ? "Да" : "Нет");
    printf("\\n");
    printf("Время выполнения: %.6f секунд", elapsed_time);
    printf("\\n");

    // Освобождаем память
    free(str1);
    free(str2);

    return 0;
}
"""

# Создаем файл
create_c_file2("test2", code2)

def compile_and_run_c_files(output_filename="results.txt"):
    try:
        # Создаем файл для вывода результатов
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            # Компилируем первый файл
            print(f"Компилируем test1.c...\n")
            compile_result1 = subprocess.run(
                ['gcc', '-o', 'test1.exe', 'test1.c'],
                capture_output=True,
                text=True
            )
            
            if compile_result1.returncode != 0:
                print("Ошибка компиляции test1.c:")
                print(compile_result1.stderr)
                return False
            
            # Запускаем первый файл
            print(f"Запускаем test1.exe...\n")
            run_result1 = subprocess.run(
                './test1.exe',
                capture_output=True,
                text=True
            )
            
            # Записываем результаты первого файла
            output_file.write("=== Результаты тест1.c ===\n")
            output_file.write(run_result1.stdout + "\n\n")
            
            # Компилируем второй файл
            print(f"Компилируем test2.c...\n")
            compile_result2 = subprocess.run(
                ['gcc', '-o', 'test2.exe', 'test2.c'],
                capture_output=True,
                text=True
            )
            
            if compile_result2.returncode != 0:
                print("Ошибка компиляции test2.c:")
                print(compile_result2.stderr)
                return False
            
            # Запускаем второй файл
            print(f"Запускаем test2.exe...\n")
            run_result2 = subprocess.run(
                './test2.exe',
                capture_output=True,
                text=True
            )
            
            # Записываем результаты второго файла
            output_file.write("=== Результаты тест2.c ===\n")
            output_file.write(run_result2.stdout + "\n")
            
            print(f"Все результаты сохранены в {output_filename}")
            return True
            
    except Exception as e:
        print(f"Произошла ошибка при выполнении программы: {str(e)}")
        return False

# Запуск новой функции
compile_and_run_c_files()
