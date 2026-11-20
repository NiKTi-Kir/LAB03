#!/usr/bin/env python3
import argparse

DEFAULT_PRECISION = 2
EXIT_DIVISION_BY_ZERO = 1
OPERATIONS = ("add", "sub", "mul", "div")


def compute(x, y, op, precision):
    """
    Выполняет арифметическую операцию и округляет результат.

    Args:
        x (float): Первый операнд.
        y (float): Второй операнд.
        op (str | None): Одна из OPERATIONS или None.
        precision (int): Количество знаков после запятой.

    Returns:
        float | None: Результат или None, если op is None.

    Raises:
        SystemExit: При делении на ноль.
    """
    if op is None:
        return None
    if op == "add":
        res = x + y
    elif op == "sub":
        res = x - y
    elif op == "mul":
        res = x * y
    else:  # op == "div"
        if y == 0:
            print("Ошибка: деление на ноль")
            exit(EXIT_DIVISION_BY_ZERO)
        res = x / y
    return round(res, precision)


def build_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Калькулятор с историей")
    parser.add_argument("x", type=float, help="Первое число")
    parser.add_argument("y", type=float, help="Второе число")
    parser.add_argument(
        "operation", nargs="?", choices=OPERATIONS, default=None,
        help="Операция (по умолчанию — просто вывод чисел)",
    )
    parser.add_argument(
        "-p", "--precision", type=int, default=DEFAULT_PRECISION,
        help=f"Точность (знаков после запятой), по умолчанию {DEFAULT_PRECISION}",
    )
    parser.add_argument(
        "-n", "--name", default=None,
        help="Имя файла для сохранения результата",
    )
    return parser


def format_line(x, y, op, precision):
    """
    Формирует строку результата для вывода и сохранения.

    Args:
        x (float): Первый операнд.
        y (float): Второй операнд.
        op (str | None): Операция или None.
        precision (int): Точность округления.

    Returns:
        str: Строка вида "x op y = result" или "x y".
    """
    if op is None:
        return f"{x} {y}"
    result = compute(x, y, op, precision)
    return f"{x} {op} {y} = {result}"


def save_line(path, line):
    """Дописывает строку в файл.

    Args:
        path (str): Путь к файлу.
        line (str): Строка для записи.
    """
    with open(path, "a", encoding="utf-8") as f:
        f.write(line + "\n")


if __name__ == "__main__":
    args = build_parser().parse_args()
    line = format_line(args.x, args.y, args.operation, args.precision)
    print(line)
    if args.name is not None:
        save_line(args.name, line)
        
