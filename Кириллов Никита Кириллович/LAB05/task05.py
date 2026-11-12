#!/usr/bin/env python3
"""Генератор паролей с настраиваемым алфавитом.

Генерирует заданное количество паролей указанной длины. Поддерживает
исключение цифр и/или специальных символов, а также сохранение
результатов в файл. Проверяет корректность длины (8..64) и
возможность генерации после применения фильтров.
"""
import argparse
import random
import string
import sys


# Набор специальных символов, используемых в паролях
SPECIAL_CHARS = "!@#$%^&*()-_=+[]{};:,.<>?/"


def build_charset(no_digits, no_special):
    """Формирует набор символов для генерации пароля.

    Базовый набор всегда включает буквы латинского алфавита (верхнего
    и нижнего регистра). Цифры и специальные символы добавляются
    в зависимости от переданных флагов.

    Args:
        no_digits (bool): Если True, цифры исключаются из набора.
        no_special (bool): Если True, специальные символы исключаются.

    Returns:
        str: Строка, содержащая все допустимые символы для пароля.
            Может быть пустой, если все категории исключены.
"""

    letters = string.ascii_letters
    digits = string.digits

    charset = letters
    if not no_digits:
        charset += digits
    if not no_special:
        charset += SPECIAL_CHARS
    return charset


def generate_password(length, charset):
    """
    Генерирует один пароль заданной длины из указанного набора символов.

    Args:
        length (int): Длина генерируемого пароля (должна быть >= 1).
        charset (str): Набор допустимых символов. Не должен быть пустым.

    Returns:
        str: Сгенерированный пароль длиной ровно `length` символов.

    """
    pool = []

    pool.append(random.choice(string.ascii_letters))

    if any(c in string.digits for c in charset):
        pool.append(random.choice(string.digits))

    if any(c in SPECIAL_CHARS for c in charset):
        pool.append(random.choice(SPECIAL_CHARS))

    remaining = length - len(pool)
    if remaining < 0:

        pool = []
        remaining = length

    pool += [random.choice(charset) for _ in range(remaining)]
    random.shuffle(pool)
    return "".join(pool)



parser = argparse.ArgumentParser(description="Генератор паролей")
parser.add_argument("length", type=int, help="Длина пароля (8..64)")
parser.add_argument("count", type=int, help="Количество паролей")
parser.add_argument("--no-digits", action="store_true",
                    help="Исключить цифры")
parser.add_argument("--no-special", action="store_true",
                    help="Исключить специальные символы")
parser.add_argument("--output", default=None,
                    help="Файл для сохранения паролей")

args = parser.parse_args()

if args.length < 8 or args.length > 64:
    print("Ошибка: длина пароля должна быть в диапазоне от 8 до 64",
          file=sys.stderr)
    sys.exit(1)

if args.count < 1:
    print("Ошибка: количество паролей должно быть >= 1", file=sys.stderr)
    sys.exit(1)

charset = build_charset(args.no_digits, args.no_special)
if not charset:
    print("Ошибка: после применения фильтров не осталось символов "
          "для генерации пароля", file=sys.stderr)
    sys.exit(1)

passwords = [generate_password(args.length, charset) for _ in range(args.count)]

for p in passwords:
    print(p)

if args.output is not None:
    with open(args.output, "w", encoding="utf-8") as f:
        for p in passwords:
            f.write(p + "\n")

if __name__ == "__main__":
    print("Примеры запуска:")
    print("  python task5.py 12 3")
    print("  python task5.py 10 2 --no-digits --no-special --output pw.txt")
    print("  python task5.py 5 1   # -> ошибка: длина вне диапазона 8..64")
