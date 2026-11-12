#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps


def repeat(n):
    """Декоратор: вызвать функцию n раз и вернуть список результатов.
    Args:
        n (int): Сколько раз вызывать функцию.
    Returns:
        function: Декоратор.
    """
    def decorator(func):
        """Обернуть функцию.
        Args:
            func (function): Декорируемая функция.
        Returns:
            function: Обёрнутая функция.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Вызвать func n раз.
            Args:
                *args: Позиционные аргументы.
                **kwargs: Именованные аргументы.
            Returns:
                list: Список результатов всех вызовов.
            """
            results = []
            for i in range(1, n + 1):
                print(f"Запуск {i} из {n}")
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator


@repeat(3)
def square(x):
    """Возвести число в квадрат.
    Args:
        x (int): Число.
    Returns:
        int: Квадрат числа.
    """
    return x * x


def main():
    """Точка входа программы.
    Returns:
        None: Ничего не возвращает.
    """
    result = square(5)
    print(f"Результаты: {result}")


if __name__ == "__main__":
    main()
