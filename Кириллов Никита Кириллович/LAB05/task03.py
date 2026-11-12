#!/usr/bin/env python3
import argparse
import sys

"""
Утилита для обработки списка строк.

Поддерживает фильтрацию уникальных строк, фильтрацию по минимальной длине,
сортировку (по возрастанию/убыванию/без сортировки) и подсчёт количества
строк после применения всех фильтров.
"""


parser = argparse.ArgumentParser(description="Обработчик строк")
parser.add_argument("strings", nargs="+", help="Одна или несколько строк")
parser.add_argument("-c", "--count", action="store_true",
                    help="Вывести только количество строк после фильтров")
parser.add_argument("-u", "--unique", action="store_true",
                    help="Оставить только уникальные строки")
parser.add_argument("-m", "--min-length", type=int, default=None,
                    help="Минимальная длина строки")
parser.add_argument("--sort", choices=["asc", "desc", "none"],
                    default="none", help="Порядок сортировки")

args = parser.parse_args()


if not args.strings:
    print("Ошибка: не передано ни одной строки", file=sys.stderr)
    sys.exit(1)

data = list(args.strings)


if args.unique:
    seen = set()
    unique = []
    for s in data:
        if s not in seen:
            seen.add(s)
            unique.append(s)
    data = unique

if args.min_length is not None:
    data = [s for s in data if len(s) >= args.min_length]

if args.sort == "asc":
    data.sort()
elif args.sort == "desc":
    data.sort(reverse=True)

if args.count:
    print(len(data))
else:
    for s in data:
        print(s)

if __name__ == "__main__":
    print("Примеры запуска:")
    print("  python task3.py apple banana apple cherry -u")
    print("  python task3.py a bb ccc dddd -m 3 --sort desc")
    print("  python task3.py a b c -c")