
import random

class LeaksGenerator:
    def __init__(self, leak_scenarios):
        self.leak_scenarios = leak_scenarios
        self.delete_free_scenarios = []
        self.pointless_condition_scenarios = []
        self.wrong_pointer_scenarios = []
        self.wrong_counter_scenarios = []
        if 1 in self.leak_scenarios:
            # выбор для того, где будет удалена строка free()
            self.delete_free_scenarios = random.sample([1, 2, 3, 4], int(input
                                                                         ('Сколько удалений функции free() добавить в код?: ')))
            print("Free delete scenarios:", self.delete_free_scenarios)
        if 2 in self.leak_scenarios:
            # выбор того, где будет добавлено неверное условие
            self.pointless_condition_scenarios = random.sample([1, 2, 3, 4], int(input
                                                                         ('Сколько неверных условий добавить в код?: ')))
            print("pointless condition scenarios:", self.pointless_condition_scenarios)
        if 3 in self.leak_scenarios:
            # выбор того, где будет добавлена ошибка указателя на область
            self.wrong_pointer_scenarios = random.sample([1, 2, 3, 4], int(input
                                                                         ('Сколько ошибок указателей добавить в код?: ')))
            print("Wrong pointer scenarios:", self.wrong_pointer_scenarios)
        if 4 in self.leak_scenarios:
            # выбор того, где будет добавлена ошибка счетчика
            self.wrong_counter_scenarios = random.sample([1,2,3],int(input
                                                                         ('Сколько ошибок счетчика добавить в код?: ')))
            print("Wrong counter scenarios:", self.wrong_counter_scenarios)


    def libraries_and_signatures(self):
        return """#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* get_word(FILE* file);
void free_text(char** text, int count); 
char** get_text(FILE* file, int* count);
void print_text(char** text, int count);
"""

    def get_word_function(self):
        code = """
char* get_word(FILE* file){
    int size = 16;
    char* word = (char*)malloc(size * sizeof(char));
    if (!word) {
        fprintf(stderr, "Memory allocation error for word\\n");
        exit(EXIT_FAILURE);
    }
    int index = 0;
    char c;
    while ((c = fgetc(file)) != EOF && c != ' ' && c != '\\n'){
        if (index >= size - 1){
            size *= 2;
            word = (char*)realloc(word, size * sizeof(char));
            if (!word) {
                fprintf(stderr, "Memory reallocation error for word\\n");
                exit(EXIT_FAILURE);
            }
        }
        word[index++] = c;
    }
    word[index] = '\\0';
    if (index==0 && c!=' '){"""
        # если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 in self.leak_scenarios and 4 in self.pointless_condition_scenarios:
            code += """
        if (word[index]!='\\0'){"""
        # если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 not in self.leak_scenarios or 4 not in self.delete_free_scenarios:
            code += """
        free(word);"""
        # закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем к коду
        code += """
        }""" if 2 in self.leak_scenarios and 4 in self.pointless_condition_scenarios else ""
        code += """
        return NULL;
    }"""
        #если юзер выбрал сценарий с ошибкой указателя и рандом выбрал это место кода - добавим ошибочное выражение
        code+="""
    return word+1;""" if 3 in self.leak_scenarios and 2 in self.wrong_pointer_scenarios else """
    return word;"""
        code+="""
}
"""
        return code


    def get_text_function(self):
        code = """
char** get_text(FILE* file, int* count){
    int size = 8;
    char** text = (char**)malloc(size * sizeof(char*));
    if (!text){
        fprintf(stderr, "Memory allocation error for text\\n");
        exit(EXIT_FAILURE);
    }"""
        code+="""
    *count = 5;""" if 4 in self.leak_scenarios and 3 in self.wrong_counter_scenarios else """
    *count = 0;"""
        code +="""
    char* word;
    while ((word = get_word(file)) != NULL){
        if (*count >= size) {
            size *= 2;
            text = (char**)realloc(text, size * sizeof(char*));
            if (!text){
                fprintf(stderr, "Memory reallocation error for text\\n");
                exit(EXIT_FAILURE);
            }
        }
        text[(*count)++] = word;"""
        if 3 in self.leak_scenarios and 4 in self.wrong_pointer_scenarios:
            code += """
        text--;"""
        if 4 in self.leak_scenarios and 2 in self.wrong_counter_scenarios:
            code += """
        count--;"""
        code += """
    }
    return text;
}
"""
        return code


    def print_text_function(self):
        code = """
void print_text(char** text, int count){
    for (int i = 0; i < count; i++){
        printf("%s ", text[i]);
    }
    printf("\\n");"""
        #если юзер выбрал сценарий с ошибкой указателя и рандом выбрал это место кода - добавим ошибочное выражение
        if 3 in self.leak_scenarios and 3 in self.wrong_pointer_scenarios:
            code += """
    text+=1;"""
        code+="""   
}
"""
        return code


    def free_text_function(self):
        code = """
void free_text(char** text, int count){
    for (int i = 0; i < count; i++){"""
        #если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 in self.leak_scenarios and 1 in self.pointless_condition_scenarios:
            code += """
        if (i!=0){"""
        #если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 not in self.leak_scenarios or 1 not in self.delete_free_scenarios:
            code += """
        free(text[i]);"""
        #закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем к коду
        code += """
        }""" if 2 in self.leak_scenarios and 1 in self.pointless_condition_scenarios else ""
        code += """
    }"""

        # если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 in self.leak_scenarios and 2 in self.pointless_condition_scenarios:
            code += """        
    if (!text){"""
        # если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 not in self.leak_scenarios or 2 not in self.delete_free_scenarios:
            code += """
    free(text);"""
        # закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем
        code += """
    }""" if 2 in self.leak_scenarios and 2 in self.pointless_condition_scenarios else ""

        code += '\n}\n'
        return code


    def main_function(self):
        #первая строка мейна- перенаправление ошибок, чтобы не было видно тип ошибки при выводе результата по типу
        # free() - invalid pointer
        code = """
int main(){
    freopen("/dev/null", "w", stderr);    
    FILE* file = fopen("text1.txt", "r");
    if (!file){
        fprintf(stderr, "Failed to open file\\n");
        return EXIT_FAILURE;
    }
    int count;
    char** text = get_text(file, &count);"""
        #если юзер выбрал сценарий с ошибкой указателя и рандом выбрал это место кода - добавим ошибочное выражение
        if 3 in self.leak_scenarios and 1 in self.wrong_pointer_scenarios:
            code += """
    text[10] = text[count];"""

        #если юзер выбрал сценарий с ошибкой счетчика и рандом выбрал это место кода - добавим ошибочное выражение
        if 4 in self.leak_scenarios and 1 in self.wrong_counter_scenarios:
            code += """
    count++;"""

        code += """       
    print_text(text,count);
    fclose(file);"""
        # если юзер выбрал сценарий с неверным условием и рандом выбрал это место кода - добавим условие
        if 2 in self.leak_scenarios and 3 in self.pointless_condition_scenarios:
            code += """
    if (!text){"""
        # если юзер не выбрал сценарий с отсутствием вызова free или рандом не выбрал это место кода - free добавляется
        if 1 not in self.leak_scenarios or 3 not in self.delete_free_scenarios:
            code += """
    free_text(text, count);"""
        # закрываем сегмент условного оператора, если он был открыт, иначе ничего не добавляем
        code += """
    }""" if 2 in self.leak_scenarios and 3 in self.pointless_condition_scenarios else ""

        code += """
    return 0;\n}\n"""
        return code

    def generated_leaky_code(self):
        code = self.libraries_and_signatures()
        code += self.get_word_function()
        code += self.get_text_function()
        code += self.print_text_function()
        code += self.free_text_function()
        code += self.main_function()
        return code

if __name__ == "__main__":
    leak_scenarios = list(map(int, input("Какие сценарии утечек добавить в код?: ").split()))
    print("\nLeak scenarios that will be added:", leak_scenarios)
    generator = LeaksGenerator(leak_scenarios)
    generated_code = generator.generated_leaky_code()
    with open("leaks_generated.c", "w") as file:
        file.write(generated_code)
    print("\nC code with memory leak has been written to leaks_generated.c")



    """
    Код на python3 генерирует программу на C, которая считывает слова в динамический массив символов,
а потом присоединяет этот элемент в двоичный массив символов, таким образом образуя текст.
 Программа выводит текст, не производя с ним никаких действий, в конце очищает память.
  При запуске программа предлагает внедрить в код на С некоторое количество ошибок, 
которые приводят к утечке памяти (дополнительно может быть некорректный вывод в консоль),
  у ошибок есть 4 сценария возникновения, каждый сценарий имеет несколько мест, 
в которые генератор может эту ошибку внедрить. 
  При запуске предлагается выбрать номера внедряемых сценариев, вводом через пробелм 
  (ввод отличного числа сгенерирует верный код без утечек)
  Далее к каждому сценарию предлагается выбрать кол-во ошибок подобного рода, но без конкретного
указания места - это программа генерирует сама. На данный момент программа аварийно завершается
при вводе числа отрицательного, либо большего, чем доступное кол-во мест для внедрения ошибок 
в код.

Добавленные в код Си сценарии достижения утечек:
№1) Удаление функции free() 
Отсутсвие строк вызова функции free() в методе освобождения двумерного массива free_text(), 
либо отсутствие вызова самой функции free_text, там где это должно быть.
 Возможность возникновения такой ошибки есть в 4х местах кода (2 раза в функции free_text,
по 1 разу в функциях get_word и main)

№2) Неверные условия
Рядом с вызовом функции free, добавляет заведомо неверное условие, или верное, но
 которое помешает корректному освобождению памяти.
 Возможность возникновения такой ошибки есть в 4х местах кода (2 раза в функции free_text,
по 1 разу в функциях get_word и main). 
Может работать вместе с первым сценарием - будет добавлено условие, но free будет удалено
т.к. неверное условие без вызова free() или free_text() помешает компиляции кода

№3) Ошибка указателя
Указателю на динамический массив присваивается другой адрес, на который он указывает, 
таким образом на некоторую облать памяти потеряется доступ, она не сможет быть освобождена,
либо выведена в консоль. Возможность возникновения такой ошибки есть в 4х местах кода
(в get_word, get_text, main и print_text)

№4) Ошибка счетчика
По мере считывания текста из файла ведется счетчик слов, неверное изменение которого повлияет
на очищение памяти, а так же на неверный вывод в консоль. Подобная ошибка может появиться в 3х
фукнциях - get_text(дважды) и main().


  Планируется добавить :
  запуск программы со всеми аргументами через cli,
  обработку аварийных остановок,
  новые сценарии возникновения ошибок, ведущих к утечке
(двойное освобождение памяти одной области памяти,
повторный вызов malloc для одного указателя без предварительного его освобождения)
    """
