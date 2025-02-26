import sys

from generators import generate_profiling_task
from cfile import StyleOptions
from cfile.writer import Writer
import time


task = generate_profiling_task(10, 2, 2, 2, 3, time.time())
writer = Writer(StyleOptions())
writer.write_file(task["code"], "task/code.c")

with open('task/description.txt', 'w') as file:
    file.write(task["description"])

with open('task/answer.txt', 'w', encoding='utf-8') as file:
    file.write(task["answer"])