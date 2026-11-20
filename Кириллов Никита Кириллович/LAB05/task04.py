#!/usr/bin/env python3
import argparse
import os
import sys

def parse_replace(value):
    """
    Args:
        value (str): Строка вида "OLD=NEW". Символ '=' может встречаться
            в NEW — используется только первое вхождение.

    Returns:
        tuple[str, str]: Кортеж (old, new), где old — заменяемая подстрока,
            new — строка-замена.
    """

    if "=" not in value:
        raise argparse.ArgumentTypeError(
            f"Ожидается формат OLD=NEW, получено: '{value}'"
        )
    old, new = value.split("=", 1)
    return old, new


parser = argparse.ArgumentParser(description="Копирование файла с заменами")
parser.add_argument("--input", required=True, help="Путь к входному файлу")
parser.add_argument("--output", required=True, help="Путь к выходному файлу")
parser.add_argument("--replace", type=parse_replace, action="append",
                    default=[], help="Замена OLD=NEW (можно указывать несколько раз)")
parser.add_argument("--append-footer", default=None,
                    help="Строка, добавляемая в конец выходного файла")
parser.add_argument("--overwrite", action="store_true",
                    help="Разрешить перезапись существующего выходного файла")

args = parser.parse_args()

if not os.path.isfile(args.input):
    print(f"Ошибка: входной файл '{args.input}' не найден", file=sys.stderr)
    sys.exit(1)

if os.path.exists(args.output) and not args.overwrite:
    print(f"Ошибка: выходной файл '{args.output}' уже существует. "
          f"Используйте --overwrite для перезаписи.", file=sys.stderr)
    sys.exit(1)

with open(args.input, "r", encoding="utf-8") as f:
    content = f.read()

total_replacements = 0
for old, new in args.replace:
    if old:
        count = content.count(old)
        content = content.replace(old, new)
        total_replacements += count

if args.append_footer is not None:
    if content and not content.endswith("\n"):
        content += "\n"
    content += args.append_footer + "\n"

with open(args.output, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Выполнено замен: {total_replacements}")

if __name__ == "__main__":
    print("Примеры запуска:")
    print("  python task4.py --input in.txt --output out.txt --replace foo=bar")
    print("  python task4.py --input in.txt --output out.txt --append-footer '---'")
    print("  python task4.py --input in.txt --output out.txt --overwrite")
