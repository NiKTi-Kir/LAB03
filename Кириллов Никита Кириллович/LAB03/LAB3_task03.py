#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


def generate_numbers(count: int = 20, low: int = -100, high: int = 100) -> list[int]:
    """Сгенерировать список случайных целых чисел.
    Args:
        count (int): Количество чисел для генерации.
        low (int): Нижняя граница диапазона (включительно).
        high (int): Верхняя граница диапазона (включительно).
    Returns:
        list[int]: Список случайных целых чисел.
    """
    return [random.randint(low, high) for _ in range(count)]


def filter_divisible_by_3_not_9(numbers: list[int]) -> list[int]:
    """Отфильтровать числа, делящиеся на 3, но не делящиеся на 9.
    Args:
        numbers (list[int]): Исходный список целых чисел.
    Returns:
        list[int]: Отфильтрованный список чисел.
    """
    return list(filter(lambda x: x % 3 == 0 and x % 9 != 0, numbers))


def filter_abs_greater_than_20(numbers: list[int]) -> list[int]:
    """Отфильтровать числа с абсолютным значением больше 20.
    Args:
        numbers (list[int]): Исходный список целых чисел.
    Returns:
        list[int]: Отфильтрованный список чисел.
    """
    return list(filter(lambda x: abs(x) > 20, numbers))


def filter_both_conditions(numbers: list[int]) -> list[int]:
    """Отфильтровать числа, удовлетворяющие обоим условиям одновременно.
    Условия: делится на 3, но не на 9, и |x| > 20.
    Args:
        numbers (list[int]): Исходный список целых чисел.
    Returns:
        list[int]: Отфильтрованный список чисел.
    """
    return list(
        filter(lambda x: x % 3 == 0 and x % 9 != 0 and abs(x) > 20, numbers)
    )


def print_result(title: str, items: list[int]) -> None:
    """Вывести заголовок, список и его длину.
    Args:
        title (str): Заголовок для вывода.
        items (list[int]): Список для вывода.
    Returns:
        None: Функция ничего не возвращает, только печатает.
    """

    print(f"{title}: {items}")
    print(f"  длина: {len(items)}")


def main() -> None:
    """Точка входа программы.
    Returns:
        None: Функция ничего не возвращает.
    """

    numbers = generate_numbers()
    print(f"Исходный список (20 чисел, [-100; 100]):\n  {numbers}\n")

    by_3_not_9 = filter_divisible_by_3_not_9(numbers)
    abs_gt_20 = filter_abs_greater_than_20(numbers)
    both = filter_both_conditions(numbers)

    print_result("Делятся на 3, но не на 9", by_3_not_9)
    print_result("|x| > 20", abs_gt_20)
    print_result("Оба условия одновременно", both)


if __name__ == "__main__":
    main()