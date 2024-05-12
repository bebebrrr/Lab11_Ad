#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23 необходимо реализовать
# вычисление значений в двух функций в отдельных процессах.

import math
from multiprocessing import Process, Queue

E = 10e-7


def calc_sum(x):
    return math.exp(-(x**2))


def calc_chis(x, n, result_queue):
    result_queue.put(calc_chis_helper(x, n))


def calc_chis_helper(x, n):
    return ((-1) ** n) * (x ** (2 * n))


def calc_znam(n, result_queue):
    result_queue.put(math.factorial(n))


def main():
    x = -0.7
    results = [1]  # Начальное значение ряда
    result_queue = Queue()

    processes = []

    i = 1
    while True:
        # Создаем процессы для вычисления числителя и знаменателя
        chis_process = Process(target=calc_chis, args=(x, i, result_queue))
        znam_process = Process(target=calc_znam, args=(i, result_queue))

        # Запускаем процессы
        chis_process.start()
        znam_process.start()

        # Добавляем процессы в список для последующего ожидания их завершения
        processes.append(chis_process)
        processes.append(znam_process)

        # Получаем результаты из очереди
        chis = result_queue.get()
        znam = result_queue.get()

        # Проверяем условие остановки
        if abs(chis / znam) < E:
            break

        # Добавляем результаты в список
        results.append(chis)
        results.append(znam)

        i += 1

    # Ожидаем завершения всех процессов
    for process in processes:
        process.join()

    y = calc_sum(x)
    calculated_sum = sum(results)
    print(f"x = {x}")
    print(f"Ожидаемое значение y = {y}")
    print(f"Подсчитанное значение суммы ряда = {calculated_sum}")


if __name__ == "__main__":
    main()
