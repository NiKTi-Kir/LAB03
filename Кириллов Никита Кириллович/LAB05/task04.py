#!/usr/bin/env python3

import argparse
from pathlib import Path

EXIT_INPUT_NOT_FOUND = 1
EXIT_OUTPUT_EXISTS = 2
REPLACE_SEPARATOR = "="


def parse_replace(value):
    """
    Разбирает строку вида OLD=NEW в кортеж (old, new).

    Args:
        value (str): Строка с разделителем REPLACE_SEPARATOR.

    Returns:
        tuple[str, str]: (old, new). Разделитель ищется только в первом вхождении.

    Raises:
        argparse.ArgumentTypeError: Если разделитель отсутствует.
    """
    if REPLACE_SEPARATOR not in value:
        raise argparse.ArgumentTypeError(
            f"Ожидается формат OLD{REPLACE_SEPARATOR}NEW, получено: '{value}'"
        )
    old, new = value.split(REPLACE_SEPARATOR, 1)
    return old, new


def build_parser():
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(description="Копирование файла с заменами")
    parser.add_argument("--input", required=True, help="Путь к входному файлу")
    parser.add_argument("--output", required=True, help="Путь к выходному файлу")
    parser.add_argument(
        "--replace", type=parse_replace, action="append", default=[],
        help="Замена OLD=NEW (можно указывать несколько раз)",
    )
    parser.add_argument(
        "--append-footer", default=None,
        help="Строка, добавляемая в конец выходного файла",
    )
    parser.add_argument(
        "--overwrite", action="store_true",
        help="Разрешить перезапись существующего выходного файла",
    )
    return parser


def apply_replacements(content, replacements):
    """
    Применяет последовательность замен и считает общее число вхождений.

    Args:
        content (str): Исходный текст.
        replacements (list[tuple[str, str]]): Пары (old, new).

    Returns:
        tuple[str, int]: Изменённый текст и суммарное число замен.
    """
    total = 0
    for old, new in replacements:
        if not old:
            continue
        total += content.count(old)
        content = content.replace(old, new)
    return content, total


def add_footer(content, footer):
    """
    Добавляет футер в конец текста, гарантируя перевод строки перед ним.

    Args:
        content (str): Исходный текст.
        footer (str | None): Строка футера или None.

    Returns:
        str: Текст с футером (или без изменений при footer is None).
    """
    if footer is None:
        return content
    if content and not content.endswith("\n"):
        content += "\n"
    return content + footer + "\n"


if __name__ == "__main__":
    args = build_parser().parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    if not input_path.is_file():
        print(f"Ошибка: входной файл '{args.input}' не найден")
        exit(EXIT_INPUT_NOT_FOUND)

    if output_path.exists() and not args.overwrite:
        print(
            f"Ошибка: выходной файл '{args.output}' уже существует. "
            f"Используйте --overwrite для перезаписи."
        )
        exit(EXIT_OUTPUT_EXISTS)

    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    content, total = apply_replacements(content, args.replace)
    content = add_footer(content, args.append_footer)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Выполнено замен: {total}")
    
