#!/usr/bin/env python3
import argparse
import sys

def compute(x, y, op, precision):

    """Выполняет арифметическую операцию над двумя числами.
    Args:
        x (float): Первое число-операнд.
        y (float): Второе число-операнд.
        op (str или None): Название операции. Допустимые значения:
            'add' — сложение, 'sub' — вычитание,
            'mul' — умножение, 'div' — деление.
            Если None, операция не выполняется.
        precision (int): Количество знаков после запятой в результате.

    Returns:
        float или None: Результат операции, округлённый до указанной точности.
            Возвращает None, если op равен None.
    """

    if op is None:
        return None
    if op == "add":
        res = x + y
    elif op == "sub":
        res = x - y
    elif op == "mul":
        res = x * y
    elif op == "div":
        if y == 0:
            print("Ошибка: деление на ноль", file=sys.stderr)
            sys.exit(1)
        res = x / y
    else:
        res = 0
    return round(res, precision)


# === Главный код ===
parser = argparse.ArgumentParser(description="Калькулятор с историей")
parser.add_argument("x", type=float, help="Первое число")
parser.add_argument("y", type=float, help="Второе число")
parser.add_argument("operation", nargs="?",
                    choices=["add", "sub", "mul", "div"], default=None,
                    help="Операция (по умолчанию — просто вывод чисел)")
parser.add_argument("-p", "--precision", type=int, default=2,
                    help="Точность (знаков после запятой)")
parser.add_argument("-n", "--name", default=None,
                    help="Имя файла для сохранения результата")

args = parser.parse_args()

if args.operation is None:
    line = f"{args.x} {args.y}"
else:
    result = compute(args.x, args.y, args.operation, args.precision)
    line = f"{args.x} {args.operation} {args.y} = {result}"

print(line)

if args.name is not None:

    with open(args.name, "a", encoding="utf-8") as f:
        f.write(line + "\n")

if __name__ == "__main__":
    print("Примеры запуска:")
    print("  python task2.py 3 4")
    print("  python task2.py 10 3 add -p 4 -n log.txt")
    print("  python task2.py 5 0 div   # -> ошибка деления на ноль")
