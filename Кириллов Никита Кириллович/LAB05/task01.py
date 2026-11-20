#!/usr/bin/env python3
import argparse

MIN_AGE = 0
MAX_AGE = 120


def valid_age(value):
    """
    Преобразует строку в возраст и проверяет диапазон MIN_AGE..MAX_AGE.

    Args:
        value (str): Строковое значение возраста.

    Returns:
        int: Возраст в допустимом диапазоне.

    Raises:
        argparse.ArgumentTypeError: Если значение не число или вне диапазона.
    """
    
    try:
        age = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Возраст должен быть целым числом, получено: '{value}'"
        )
    if not MIN_AGE <= age <= MAX_AGE:
        raise argparse.ArgumentTypeError(
            f"Возраст должен быть в диапазоне от {MIN_AGE} до {MAX_AGE}, получено: {age}"
        )
    return age


def build_parser():
    """Создаёт и возвращает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Приветствие пользователя")
    parser.add_argument("name", help="Имя пользователя")
    parser.add_argument(
        "age", nargs="?", type=valid_age, default=None,
        help=f"Возраст ({MIN_AGE}..{MAX_AGE})",
    )
    parser.add_argument(
        "-g", "--greet", action="store_true",
        help="Использовать официальное приветствие",
    )
    return parser


def build_greeting(name, age, official):
    """
    Args:
        name (str): Имя пользователя.
        age (int | None): Возраст или None.
        official (bool): Использовать ли официальное обращение.

    Returns:
        str: Готовая строка приветствия.
    """
    
    prefix = "Уважаемый(ая) " if official else ""
    if age is None:
        return f"{prefix}{name}"
    return f"{prefix}{name}, возраст: {age}"


if __name__ == "__main__":
    args = build_parser().parse_args()
    print(build_greeting(args.name, args.age, args.greet))
    
