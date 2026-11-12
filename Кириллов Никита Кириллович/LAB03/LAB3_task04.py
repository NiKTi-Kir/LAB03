#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce


def read_words() -> list[str]:

    """ Запросить у пользователя список слов.
    Returns:
        list[str]: Список введённых слов.
    """

    return input("Введите слова через пробел: ").split()


def filter_long(words: list[str], n: int = 7) -> list[str]:
    """ Оставить слова длиной не менее n символов.
    Args:
        words (list[str]): Исходный список слов.
        n (int): Минимальная длина слова.
    Returns:
        list[str]: Отфильтрованный список слов.
    """

    return list(filter(lambda w: len(w) >= n, words))


def to_pairs(words: list[str]) -> list[tuple[str, int]]:
    """ Преобразовать слова в пары (слово, длина).
    Args:
        words (list[str]): Список слов.
    Returns:
        list[tuple[str, int]]: Список пар (слово, длина).
    """

    return list(map(lambda w: (w, len(w)), words))


def longest(pairs: list[tuple[str, int]]) -> tuple[str, int] | None:
    """ Найти пару с максимальной длиной через reduce.
    Args:
        pairs (list[tuple[str, int]]): Список пар (слово, длина).
    Returns:
        tuple[str, int] | None: Пара с максимальной длиной или None.
    """

    return reduce(lambda a, b: a if a[1] >= b[1] else b, pairs) if pairs else None


def total_letters(words: list[str]) -> int:
    """ Посчитать суммарное количество букв.
    Args:
        words (list[str]): Список слов.
    Returns:
        int: Суммарное количество букв.
    """

    return reduce(lambda acc, w: acc + len(w), words, 0)


def main() -> None:

    """ Точка входа программы.
    Returns:
        None: Функция ничего не возвращает.
    """

    words = read_words()
    long_words = filter_long(words)
    pairs = to_pairs(long_words)
    best = longest(pairs)

    print(f"Исходный список: {words}")
    print(f"После filter: {long_words}")
    print(f"После map: {pairs}")
    print(f"Самое длинное: {best[0]!r} ({best[1]})" if best else "Самое длинное: нет")
    print(f"Суммарно букв: {total_letters(long_words)}")


if __name__ == "__main__":
    main()
