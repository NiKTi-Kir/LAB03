#!/usr/bin/env python3

import argparse

SORT_CHOICES = ("asc", "desc", "none")


def deduplicate(data):
    """
    Удаляет дубликаты, сохраняя исходный порядок.

    Args:
        data (list[str]): Исходный список строк.

    Returns:
        list[str]: Список без повторов.
    """
    seen = set()
    result = []
    for s in data:
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result


def filter_by_length(data, min_length):
    """
    Оставляет строки длиной не меньше min_length.

    Args:
        data (list[str]): Исходный список.
        min_length (int | None): Минимальная длина или None (без фильтра).

    Returns:
        list[str]: Отфильтрованный список.
    """
    if min_length is None:
        return data
    return [s for s in data if len(s) >= min_length]


def apply_sort(data, order):
    """
    Сортирует список согласно выбранному порядку.

    Args:
        data (list[str]): Список строк.
        order (str): Одно из SORT_CHOICES.

    Returns:
        list[str]: Отсортированный список (или тот же при order == "none").
    """
    if order == "asc":
        return sorted(data)
    if order == "desc":
        return sorted(data, reverse=True)
    return data


def build_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Обработчик строк")
    parser.add_argument("strings", nargs="+", help="Одна или несколько строк")
    parser.add_argument(
        "-c", "--count", action="store_true",
        help="Вывести только количество строк после фильтров",
    )
    parser.add_argument(
        "-u", "--unique", action="store_true",
        help="Оставить только уникальные строки",
    )
    parser.add_argument(
        "-m", "--min-length", type=int, default=None,
        help="Минимальная длина строки",
    )
    parser.add_argument(
        "--sort", choices=SORT_CHOICES, default="none",
        help="Порядок сортировки",
    )
    return parser


def process(strings, unique, min_length, order):
    """
    Применяет все фильтры и сортировку последовательно.

    Args:
        strings (list[str]): Исходные строки.
        unique (bool): Удалять ли дубликаты.
        min_length (int | None): Минимальная длина.
        order (str): Порядок сортировки.

    Returns:
        list[str]: Обработанный список.
    """
    data = list(strings)
    if unique:
        data = deduplicate(data)
    data = filter_by_length(data, min_length)
    return apply_sort(data, order)


if __name__ == "__main__":
    args = build_parser().parse_args()
    data = process(args.strings, args.unique, args.min_length, args.sort)
    if args.count:
        print(len(data))
    else:
        for s in data:
            print(s)
          
