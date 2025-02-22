# Установка и настройка средств профилирования для C

* [gprof](#GNU-Profiler-gprof)
* [perf](#Perf)
* [valgrind](#Valgrind)

## GNU Profiler (gprof)

gprof используется для отслеживания времени выполнения и количества вызовов каждого метода в программе, 
чтобы найти наиболее трудоемкую функцию в программе.

### Установка в Linux

```bash
sudo apt-get install binutils
```

### Использование gprof

Ниже приведён исходный код программы.

```c
// test.c
#include
<math.h>
#include
<stdlib.h>
void fastFunction() {
    double* result = malloc(sizeof(double) * 1000000);
    for (int i = 0; i < 1000000; ++i) {
        result[i] = sin(i) * cos(i);
    }
    free(result);
}
void slowFunction() {
    double* result = malloc(sizeof(double) * 5000000);
    for (int i = 0; i < 5000000; ++i) {
        result[i] = sqrt(i) * log(i);
    }
    free(result);
}
int main() {
    for (int i = 0; i < 5; ++i) {
        fastFunction();
        slowFunction();
    }
    return 0;
}
```

1. Компиляция исходного кода с флагом -pg.\

* Флаг -pg в GCC помещает в исполняемый файл инструкции профилирования для генерации информации, используемой утилитой
  gprof.
   ```bash
   gcc -pg test.c -o test.out -lm
   ```

2. Запуск программы для сбора данных профилирования.
   ```bash
   ./test.out
   ```
3. Создание файла данных профилирования (`analysis.txt`)
   ```bash
   gprof test.out gmon.out > analysis.txt
   ```
4. Просмотр информации о профилировании\

* В первой таблице приведён плоский профиль, который предоставляет информацию о каждой функции по отдельности.\
  В ней для каждой функции указаны:
    + процент от общего времени работы программы (`time`),
    + время, потраченное на данную функцию и на функции выше её в таблице (`% cumulative seconds`),
    + время, потраченное только на данную функцию (`% cumulative seconds`),
    + число вызовов (`calls`),
    + среднее время выполнения только данной функции (`self ms/call`),
    + среднее время выполнения функции и её потомков (`total ms/call`).

   ```
   Flat profile:

    Each sample counts as 0.01 seconds.
    %   cumulative   self              self     total           
    time   seconds   seconds    calls  ms/call  ms/call  name    
    87.50      0.28     0.28        5    56.00    56.00  slowFunction
    12.50      0.32     0.04        5     8.00     8.00  fastFunction
   ```
* Во второй таблице приведён граф вызовов, который показывает иерархическую структуру вызовов функций.\
  В ней для каждой функции (`self`) и для каждой вызванной ею функции (`children`) указаны:
    + процент от общего времени исполнения программы (`time`),
    + время выполнения данной функции (`self`),
    + время выполнения всех вызванных функций (`children`),
    + число вызовов данной функции (`called`).

   ```
		     Call graph (explanation follows)


    granularity: each sample hit covers 4 byte(s) for 3.12% of 0.32 seconds
    
    index % time    self  children    called     name
    <spontaneous>
    [1]    100.0    0.00    0.32                 main [1]
    0.28    0.00       5/5           slowFunction [2]
    0.04    0.00       5/5           fastFunction [3]
    -----------------------------------------------
                    0.28    0.00       5/5           main [1]
    [2]     87.5    0.28    0.00       5         slowFunction [2]
    -----------------------------------------------
                    0.04    0.00       5/5           main [1]
    [3]     12.5    0.04    0.00       5         fastFunction [3]
    -----------------------------------------------
   ```

## Perf

Он основан на принципе выборки событий и событиях производительности и 
часто используется для поиска узких мест в производительности и локализации горячего кода.

### Установка в Linux

   ```bash
   sudo apt-get install linux-tools-common
   ```

### Использование perf

1. Компиляция исходного кода с флагом -g
   ```bash
   gcc -g test.c -o test.out -lm
   ```
2. Сбор данных производительности
   ```bash
   sudo perf record ./test.out
   ```
3. Анализ данных
   ```bash
   sudo perf report
   ```

+ В таблице для каждой функции (`Symbol`) выводятся:
    * процент общих выборок функции (`Overhead`),
    * процесс, из которого собраны выборки (`Command`),
    * вызванная программа, библиотека или ядро (`Shared Object`),
    * символ, к которой относится адрес функции (`Symbol`).

![](/images/perf_table.jpg)

+ Если сбор данных выполнен с ключом -g
   ```bash
   sudo perf record -g ./test.out
   ```
  то будет выведен граф вызовов. При нажатии на '+' появляются строки с вызванными внутри функциями.\
  К таблице добавляются:
    * процент выборок вызванных внутри фунций (`Children`),
    * процент выборок самой функии (`Self`).

![](/images/perf_table_g.jpg)

## Valgrind

Инструмент для обнаружения утечек памяти и других ошибок, связанных с памятью.
Предоставляет подробные отчёты о потреблении памяти, что позволяет легко находить и устранять утечки.

### Установка в Linux

   ```bash
   sudo apt-get install valgrind
   ```

### Использование Valgrind

В исходный код добавлены ошибки.

```c
// test.c
#include <math.h>
#include <stdlib.h>
void fastFunction() {
    double* result = malloc(sizeof(double) * 1000000);
    for (int i = 0; i < 1000000; ++i) {
        result[i] = sin(i) * cos(i);
    }
    result[1000000] = 1;
    //free(result);
}
void slowFunction() {
    double* result = malloc(sizeof(double) * 5000000);
    for (int i = 0; i < 5000000; ++i) {
        result[i] = sqrt(i) * log(i);
    }
    free(result);
}
int main() {
    for (int i = 0; i < 5; ++i) {
        fastFunction();
        slowFunction();
    }
    return 0;
}
```

1. Компиляция исходного кода с флагом -g
    ```bash
    gcc -g test.c -o test.out -lm
    ```
2. Запуск valgrind
    ```bash
    valgrind --tool=memcheck --leak-check=yes ./test.out
    ```

+ Выведена информация о ошибках работы с памятью с указанием участка кода
  ```
  ==22449== Invalid write of size 8
  ==22449==    at 0x10927D: fastFunction (test.c:8)
  ==22449==    by 0x109333: main (test.c:20)
  ==22449==  Address 0x5323240 is 0 bytes after a block of size 8,000,000 alloc'd
  ==22449==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
  ==22449==    by 0x1091FE: fastFunction (test.c:4)
  ==22449==    by 0x109333: main (test.c:20)
  ```
+ `HEAP SUMMARY` сообщает, сколько произошло выделений памяти и сколько байт памяти потеряно
    ```
    ==22449== HEAP SUMMARY:
    ==22449== in use at exit: 40,000,000 bytes in 5 blocks
    ==22449== total heap usage: 10 allocs, 5 frees, 240,000,000 bytes allocated
    ==22449==
    ==22449== 16,000,000 bytes in 2 blocks are possibly lost in loss record 1 of 2
    ==22449== at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==22449== by 0x1091FE: fastFunction (test.c:4)
    ==22449== by 0x109333: main (test.c:20)
    ==22449==
    ==22449== 24,000,000 bytes in 3 blocks are definitely lost in loss record 2 of 2
    ==22449== at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
    ==22449== by 0x1091FE: fastFunction (test.c:4)
    ==22449== by 0x109333: main (test.c:20)
    ```
+ `LEAK SUMMARY` даёт сводку обнаруженных утечек памяти
    ```
    ==22449==    definitely lost: 24,000,000 bytes in 3 blocks
    ==22449==    indirectly lost: 0 bytes in 0 blocks
    ==22449==      possibly lost: 16,000,000 bytes in 2 blocks
    ==22449==    still reachable: 0 bytes in 0 blocks
    ==22449==         suppressed: 0 bytes in 0 blocks

    ```