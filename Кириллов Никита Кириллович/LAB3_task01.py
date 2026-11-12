#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def classify_number(n: int) -> str:
    """Классифицировать целое число.

    Args:
        n (int): Целое число для классификации.

    Returns:
        str: "positive even", "positive odd", "negative" или "zero".
    """
    if n == 0:
        return "zero"
    if n < 0:
        return "negative"
    if n % 2 == 0:
        return "positive even"
    return "positive odd"


def read_numbers() -> list[int]:
    """Запросить у пользователя числа и вернуть список целых чисел.

    Нечисловые значения пропускаются с предупреждением.

    Returns:
        list[int]: Список целых чисел, введённых пользователем.
    """
    raw = input("Введите числа через пробел: ").split()
    numbers: list[int] = []
    for item in raw:
        try:
            numbers.append(int(item))
        except ValueError:
            print(f"Пропущено (не целое число): {item!r}")
    return numbers


def main() -> None:
    """Точка входа программы.

    Returns:
        None: Функция ничего не возвращает.
    """
    classify = lambda n: classify_number(n)  # noqa: E731
    numbers = read_numbers()
    for n in numbers:
        print(f"{n:>6} — {classify(n)}")


if __name__ == "__main__":
    main()
