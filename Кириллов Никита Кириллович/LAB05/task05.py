#!/usr/bin/env python3

import argparse
import random
import string

MIN_LENGTH = 8
MAX_LENGTH = 64
MIN_COUNT = 1
EXIT_INVALID_LENGTH = 1
EXIT_INVALID_COUNT = 2
EXIT_EMPTY_CHARSET = 3

SPECIAL_CHARS = "!@#$%^&*()-_=+[]{};:,.<>?/"
LETTERS = string.ascii_letters
DIGITS = string.digits


def build_charset(no_digits, no_special):
    """
    Формирует набор допустимых символов для пароля.

    Args:
        no_digits (bool): Исключить цифры.
        no_special (bool): Исключить специальные символы.

    Returns:
        str: Строка допустимых символов.
    """
    charset = LETTERS
    if not no_digits:
        charset += DIGITS
    if not no_special:
        charset += SPECIAL_CHARS
    return charset


def generate_password(length, charset):
    """
    Генерирует пароль заданной длины с гарантией категорий из charset.

    Args:
        length (int): Длина пароля (>= 1).
        charset (str): Непустой набор допустимых символов.

    Returns:
        str: Пароль длиной ровно length.
    """
    pool = [random.choice(LETTERS)]
    if any(c in DIGITS for c in charset):
        pool.append(random.choice(DIGITS))
    if any(c in SPECIAL_CHARS for c in charset):
        pool.append(random.choice(SPECIAL_CHARS))

    remaining = length - len(pool)
    if remaining < 0:
        pool = []
        remaining = length

    pool += [random.choice(charset) for _ in range(remaining)]
    random.shuffle(pool)
    return "".join(pool)


def build_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Генератор паролей")
    parser.add_argument(
        "length", type=int,
        help=f"Длина пароля ({MIN_LENGTH}..{MAX_LENGTH})",
    )
    parser.add_argument("count", type=int, help="Количество паролей")
    parser.add_argument("--no-digits", action="store_true", help="Исключить цифры")
    parser.add_argument("--no-special", action="store_true", help="Исключить специальные символы")
    parser.add_argument("--output", default=None, help="Файл для сохранения паролей")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()

    if not MIN_LENGTH <= args.length <= MAX_LENGTH:
        print(f"Ошибка: длина пароля должна быть в диапазоне от {MIN_LENGTH} до {MAX_LENGTH}")
        exit(EXIT_INVALID_LENGTH)

    if args.count < MIN_COUNT:
        print(f"Ошибка: количество паролей должно быть >= {MIN_COUNT}")
        exit(EXIT_INVALID_COUNT)

    charset = build_charset(args.no_digits, args.no_special)
    if not charset:
        print("Ошибка: после применения фильтров не осталось символов для генерации пароля")
        exit(EXIT_EMPTY_CHARSET)

    passwords = [generate_password(args.length, charset) for _ in range(args.count)]
    for p in passwords:
        print(p)

    if args.output is not None:
        with open(args.output, "w", encoding="utf-8") as f:
            for p in passwords:
                f.write(p + "\n")
                
