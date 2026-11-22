#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime

SEPARATOR_WIDTH = 25
DEFAULT_BALANCE = 0.0
DEFAULT_INTEREST_RATE = 0.0
MAX_WITHDRAW_PERCENT = 0.5


class BankAccount:
    """Базовый класс банковского счёта."""

    def __init__(self, owner, balance=DEFAULT_BALANCE):
        """Инициализирует банковский счёт.

        Args:
            owner (str): Имя владельца счёта.
            balance (float, optional): Начальный баланс. По умолчанию 0.0.

        Returns:
            None
        """
        self._owner = owner
        self._balance = balance
        self._history = []
        self._log_transaction("OPEN", 0, f"Счёт открыт. Начальный баланс: {balance:.2f}")

    @property
    def balance(self):
        """Возвращает текущий баланс.

        Returns:
            float: Текущий баланс счёта.
        """
        return self._balance

    @property
    def owner(self):
        """Возвращает имя владельца.

        Returns:
            str: Имя владельца счёта.
        """
        return self._owner

    @property
    def history(self):
        """Возвращает копию истории операций.

        Returns:
            list[dict]: Глубокая копия списка записей об операциях.
        """
        return deepcopy(self._history)

    def _log_transaction(self, op_type, amount, comment=""):
        """Добавляет запись об операции в историю.

        Args:
            op_type (str): Тип операции ('DEPOSIT', 'WITHDRAW', 'OPEN', 'INTEREST').
            amount (int | float): Сумма операции.
            comment (str, optional): Комментарий к операции. По умолчанию ''.

        Returns:
            None
        """
        record = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": op_type,
            "amount": amount,
            "balance_after": self._balance,
            "comment": comment,
        }
        self._history.append(record)

    def deposit(self, amount):
        """Пополняет счёт на указанную сумму.

        Args:
            amount (int | float): Сумма пополнения (положительное число).

        Returns:
            float: Новый баланс после пополнения.
        """
        if type(amount) not in (int, float):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")

        self._balance += amount
        self._log_transaction("DEPOSIT", amount, f"Пополнение на {amount:.2f}")
        return self._balance

    def withdraw(self, amount):
        """Снимает указанную сумму со счёта.

        Args:
            amount (int | float): Сумма снятия (положительное число, не больше баланса).

        Returns:
            float: Новый баланс после снятия.
        """
        if type(amount) not in (int, float):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self._balance:
            raise ValueError(
                f"Недостаточно средств. Баланс: {self._balance:.2f}, "
                f"требуется: {amount:.2f}"
            )

        self._balance -= amount
        self._log_transaction("WITHDRAW", amount, f"Снятие {amount:.2f}")
        return self._balance

    @classmethod
    def create_account(cls, owner, initial_balance=DEFAULT_BALANCE):
        """Создаёт новый счёт с проверкой входных данных.

        Args:
            owner (str): Имя владельца (непустая строка).
            initial_balance (int | float, optional): Начальный баланс. По умолчанию 0.0.

        Returns:
            BankAccount: Новый экземпляр класса.
        """
        if type(owner) != str or not owner.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        return cls(owner, initial_balance)

    def __str__(self):
        """Строковое представление счёта.

        Returns:
            str: Строка вида "BankAccount(владелец='...', баланс=...)".
        """
        return (f"{self.__class__.__name__}(владелец='{self._owner}', "
                f"баланс={self._balance:.2f})")


class SavingsAccount(BankAccount):
    """Сберегательный счёт с процентной ставкой и ограничением на снятие."""

    def __init__(self, owner, balance=DEFAULT_BALANCE, interest_rate=DEFAULT_INTEREST_RATE):
        """Инициализирует сберегательный счёт.

        Args:
            owner (str): Имя владельца счёта.
            balance (float, optional): Начальный баланс. По умолчанию 0.0.
            interest_rate (int | float, optional): Годовая ставка в %. По умолчанию 0.0.

        Returns:
            None
        """
        super().__init__(owner, balance)
        self.interest_rate = interest_rate

    @property
    def interest_rate(self):
        """Возвращает годовую процентную ставку.

        Returns:
            int | float: Процентная ставка в процентах годовых.
        """
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, value):
        """Устанавливает процентную ставку с валидацией.

        Args:
            value (int | float): Новая процентная ставка в процентах.

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Процентная ставка должна быть числом")
        if value < 0:
            raise ValueError("Процентная ставка не может быть отрицательной")
        self._interest_rate = value

    def apply_interest(self):
        """Начисляет проценты на текущий баланс.

        Returns:
            float: Сумма начисленных процентов.
        """
        interest = self.balance * (self._interest_rate / 100)
        self.deposit(interest)
        if len(self._history) > 0:
            self._history[-1]["type"] = "INTEREST"
            self._history[-1]["amount"] = interest
            self._history[-1]["comment"] = (
                f"Начисление процентов {self._interest_rate}%: +{interest:.2f}"
            )
        return interest

    def withdraw(self, amount):
        """Снимает средства со сберегательного счёта (не более 50% баланса).

        Args:
            amount (int | float): Сумма снятия (положительное число, не более 50% баланса).

        Returns:
            float: Новый баланс после снятия.
        """
        if type(amount) not in (int, float):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        max_allowed = self.balance * MAX_WITHDRAW_PERCENT
        if amount > max_allowed:
            raise ValueError(
                f"Сберегательный счёт: нельзя снять более "
                f"{int(MAX_WITHDRAW_PERCENT * 100)}% баланса. "
                f"Максимум: {max_allowed:.2f}, запрошено: {amount:.2f}"
            )
        return super().withdraw(amount)


def separator(title):
    """Печатает заголовок-разделитель.

    Args:
        title (str): Текст заголовка.

    Returns:
        None
    """
    print(f"\n{'=' * SEPARATOR_WIDTH} {title} {'=' * SEPARATOR_WIDTH}")


if __name__ == "__main__":

    separator("1. Создание объектов")
    acc1 = BankAccount.create_account("Иванов И.И.", 1000)
    acc2 = SavingsAccount("Петров П.П.", 5000, interest_rate=7.5)
    print(acc1)
    print(acc2)

    separator("2. Корректные операции")
    acc1.deposit(500)
    print(f"После пополнения на 500: баланс = {acc1.balance:.2f}")
    acc1.withdraw(200)
    print(f"После снятия 200: баланс = {acc1.balance:.2f}")

    separator("3. Ошибки при операциях")
    try:
        acc1.deposit(-100)
    except ValueError as e:
        print(f"Ошибка пополнения: {e}")

    try:
        acc1.withdraw(-50)
    except ValueError as e:
        print(f"Ошибка снятия: {e}")

    try:
        acc1.withdraw(10000)
    except ValueError as e:
        print(f"Ошибка снятия (превышение): {e}")

    try:
        acc1.deposit("тысяча")
    except TypeError as e:
        print(f"Ошибка типа: {e}")

    separator("4. Попытка изменить баланс напрямую")
    try:
        acc1.balance = 999999
    except AttributeError as e:
        print(f"Ошибка: {e}")
    print(f"Баланс после попытки изменения: {acc1.balance:.2f} (не изменился)")

    try:
        acc1.owner = "Хакер"
    except AttributeError as e:
        print(f"Ошибка: {e}")
    print(f"Владелец: {acc1.owner} (не изменился)")

    separator("5. История операций")
    print("История acc1:")
    for record in acc1.history:
        print(f"  [{record['datetime']}] {record['type']:>8} "
              f"{record['amount']:>8.2f} | баланс: {record['balance_after']:.2f} "
              f"| {record['comment']}")

    hist_copy = acc1.history
    hist_copy.append({"fake": True})
    print(f"\nДобавили фейковую запись в копию. "
          f"Реальная длина истории: {len(acc1.history)} (не изменилась)")

    separator("6. Сберегательный счёт")
    print(f"Начальный баланс: {acc2.balance:.2f}")
    interest = acc2.apply_interest()
    print(f"Начислено процентов: {interest:.2f}")
    print(f"Баланс после начисления: {acc2.balance:.2f}")

    try:
        acc2.withdraw(3000)
    except ValueError as e:
        print(f"Ошибка снятия с сберсчёта: {e}")

    acc2.withdraw(2000)
    print(f"После снятия 2000: баланс = {acc2.balance:.2f}")

    separator("7. Полиморфизм: снятие для разных типов счетов")
    accounts = [
        BankAccount.create_account("Обычный клиент", 1000),
        SavingsAccount("Сберегательный клиент", 1000, interest_rate=5),
    ]

    for acc in accounts:
        print(f"\n{acc}")
        try:
            acc.withdraw(600)
            print(f"  ✓ Снятие 600 прошло успешно. Баланс: {acc.balance:.2f}")
        except ValueError as e:
            print(f"  ✗ Ошибка: {e}")

    separator("8. Итоговые истории")
    for acc in accounts:
        print(f"\n{acc.owner}:")
        for r in acc.history:
            print(f"  {r['type']:>8} {r['amount']:>8.2f} | {r['comment']}")
            
