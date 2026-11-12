#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def add_final_price(products: list[dict]) -> list[dict]:
    """Вернуть новый список товаров с добавленным полем "final_price".

    Args:
        products (list[dict]): Список словарей с ключами
            "name", "price", "discount".
    Returns:
        list[dict]: Новый список словарей с добавленным ключом "final_price".
    """

    return list(
        map(
            lambda p: {
                **p,
                "final_price": round(p["price"] * (1 - p["discount"] / 100), 2),
            },
            products,
        )
    )


def sort_by_final_price(products: list[dict]) -> list[dict]:
    """Отсортировать товары по возрастанию final_price.
    Args:
        products (list[dict]): Список словарей, содержащих ключ
            "final_price".
    Returns:
        list[dict]: Новый отсортированный список словарей.
    """

    return sorted(products, key=lambda p: p["final_price"])


def print_products(products: list[dict]) -> None:
    """Вывести список товаров в удобном табличном формате.
    Args:
        products (list[dict]): Список словарей с ключами "name",
            "price", "discount", "final_price".
    Returns:
        None: Функция ничего не возвращает, только печатает.
    """

    for p in products:
        print(
            f'{p["name"]:<10} price={p["price"]:>7}  '
            f'discount={p["discount"]:>3}%  '
            f'final_price={p["final_price"]:>9.2f}'
        )


def main() -> None:
    """Точка входа программы.

    Returns:
        None: Функция ничего не возвращает.
    """
    products = [
        {"name": "Laptop", "price": 89990, "discount": 10},
        {"name": "Mouse", "price": 2490, "discount": 15},
        {"name": "Keyboard", "price": 5490, "discount": 0},
        {"name": "Monitor", "price": 27990, "discount": 25},
    ]
    with_final = add_final_price(products)
    sorted_products = sort_by_final_price(with_final)

    print("Итоговый список (отсортирован по final_price):")
    print_products(sorted_products)

    print("\nИсходные products не изменены:")
    for p in products:
        print(p)


if __name__ == "__main__":
    main()
