#!/usr/bin/env python3
import argparse


def valid_age(value):
    """
    Проверяет, что переданное значение является целым числом
    в диапазоне от 0 до 120 включительно.

    Args:
        value: Строковое значение, которое должно быть преобразовано в возраст.

    Returns:
        int: Целое число возраста, если валидация прошла успешно.
    """
    try:
        age = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Возраст должен быть целым числом, получено: '{value}'"
        )
    if age < 0 or age > 120:
        raise argparse.ArgumentTypeError(
            f"Возраст должен быть в диапазоне от 0 до 120, получено: {age}"
        )
    return age


# === Главный код ===
parser = argparse.ArgumentParser(description="Приветствие пользователя")
parser.add_argument("name", help="Имя пользователя")
parser.add_argument("age", nargs="?", type=valid_age, default=None,
                    help="Возраст (0..120)")
parser.add_argument("-g", "--greet", action="store_true",
                    help="Использовать официальное приветствие")

args = parser.parse_args()

prefix = "Уважаемый(ая) " if args.greet else ""
if args.age is None:
    print(f"{prefix}{args.name}")
else:
    print(f"{prefix}{args.name}, возраст: {args.age}")

if __name__ == "__main__":
    print("Примеры запуска:")
    print("  python task1.py Иван")
    print("  python task1.py Мария 25 -g")
    print("  python task1.py Пётр 200   # -> ошибка, код 2")
