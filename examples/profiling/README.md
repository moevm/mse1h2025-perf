Пример запуска
```bash
python3 generators/profiling -m "init" -t 1 -f 10 -s 1 -d 1,2 -D 2,3 -n 1,2 -N 1,2
```
Опции:
```bash
options:
  -h, --help            show this help message and exit
  --task TASK, -t TASK  номер задания
  --mode MODE, -m MODE  "init" или "check"
  --number_funcrions NUMBER_FUNCRIONS, -f NUMBER_FUNCRIONS
                        число генерируемых функций
  --random_seed RANDOM_SEED, -s RANDOM_SEED
                        целое число, которое используется в качестве начального значения для генерации случайных чисел
  --norm_depth_for NORM_DEPTH_FOR, -d NORM_DEPTH_FOR
                        диапазон глубины вложенности циклов нормальной функции - "<min>,<max>"
  --deviant_depth_for DEVIANT_DEPTH_FOR, -D DEVIANT_DEPTH_FOR
                        диапазон глубины вложенности циклов отличающейся функции - "<min>,<max>"
  --norm_n_nested_for NORM_N_NESTED_FOR, -n NORM_N_NESTED_FOR
                        диапазон числа вложенных циклов нормальной функции - "<min>,<max>"
  --deviant_n_nested_for DEVIANT_N_NESTED_FOR, -N DEVIANT_N_NESTED_FOR
                        диапазон числа вложенных циклов отличающейся функции - "<min>,<max>"
  --output OUTPUT, -o OUTPUT
                        имя выходного файла
```