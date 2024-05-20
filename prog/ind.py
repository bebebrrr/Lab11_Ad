#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23 необходимо реализовать
# вычисление значений в двух функций в отдельных процессах.

import math
from multiprocessing import Process, Queue

E = 10e-7
results = [1]

# считаем целевой ряд y
def calc_sum(x):
    return math.exp(-(x**2))

# считаем числитель и помещаем данные в res
def calc_chis(x, res):
    res.put(-x)

# считаем знаменатель и помещаем данные в res
def calc_znam(n, res):
    res.put(n + 1)

def main():
    x = 1
    i = 0
    while math.fabs(results[-1]) > E:
        # создаём очереди для обмена данными между процессами 
        chisq = Queue()
        znamq = Queue()

        # Вычисляем числитель и знаменатель в отдельных потоках
        pr1 = Process(target=calc_chis, args = (x, chisq))
        pr2 = Process(target=calc_znam, args = (i, znamq))

        pr1.start()
        pr2.start()

        pr1.join()
        pr2.join()

        # извлекаем значения из очередей перед дальнейшей обработкой
        chis = chisq.get()
        znam = znamq.get()

        if chis and znam:
            cur = chis / znam
            results.append(cur * results[-1])

        i += 1

    y = calc_sum(x)
    calculated_sum = sum(results)
    print(f"x = {x}")
    print(f"Ожидаемое значение y = {y}")
    print(f"Подсчитанное значение суммы ряда = {calculated_sum}")

if __name__ == "__main__":
    main()
