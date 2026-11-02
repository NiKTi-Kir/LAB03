#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime


class BankAccount:
    """Базовый класс банковского счёта."""

    def __init__(self, owner, balance=0.0):
        """Инициализирует банковский счёт.

        Args:
            owner (str): Имя владельца счёта.
            balance (float, optional): Начальный баланс. По умолчанию 0.0.

        Returns:
            None
        """
        self.__owner = owner
        self.__balance = balance
        self.__history = []

        # Стартовая запись в истории
        self.__log_transaction("OPEN", 0, f"Счёт открыт. Начальный баланс: {balance:.2f}")

    # --- Свойства ТОЛЬКО ДЛЯ ЧТЕНИЯ (нет setter'ов) ---
    @property
    def balance(self):
        """Возвращает текущий баланс счёта.

        Свойство доступно только для чтения: изменить баланс напрямую
        нельзя, только через методы deposit() и withdraw().

        Returns:
            float: Текущий баланс счёта.
        """
        return self.__balance

    @property
    def owner(self):
        """Возвращает имя владельца счёта.

        Свойство доступно только для чтения.

        Returns:
            str: Имя владельца счёта.
        """
        return self.__owner

    @property
    def history(self):
        """Возвращает копию истории операций по счёту.

        Возвращается глубокая копия (deepcopy), поэтому изменения
        в полученном списке не затрагивают внутреннюю историю счёта.

        Returns:
            list[dict]: Список словарей с записями об операциях.
        """
        # deepcopy гарантирует, что вложенные словари тоже скопируются
        return deepcopy(self.__history)

    # --- Внутренний метод логирования ---
    def __log_transaction(self, op_type, amount, comment=""):
        """Добавляет запись об операции во внутреннюю историю.

        Метод приватный и используется только внутри класса.

        Args:
            op_type (str): Тип операции (например, 'DEPOSIT', 'WITHDRAW',
                'OPEN', 'INTEREST').
            amount (int | float): Сумма операции.
            comment (str, optional): Текстовый комментарий к операции.
                По умолчанию пустая строка.

        Returns:
            None
        """
        record = {
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": op_type,
            "amount": amount,
            "balance_after": self.__balance,
            "comment": comment,
        }
        self.__history.append(record)

    # --- Публичные методы операций ---
    def deposit(self, amount):
        """Пополняет счёт на указанную сумму.

        Args:
            amount (int | float): Сумма пополнения. Должна быть
                положительным числом.

        Returns:
            float: Новый баланс после пополнения.

        Raises:
            TypeError: Если amount не является числом.
            ValueError: Если amount не положительно.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")

        self.__balance += amount
        self.__log_transaction("DEPOSIT", amount, f"Пополнение на {amount:.2f}")
        return self.__balance

    def withdraw(self, amount):
        """Снимает указанную сумму со счёта.

        Args:
            amount (int | float): Сумма снятия. Должна быть
                положительным числом и не превышать текущий баланс.

        Returns:
            float: Новый баланс после снятия.

        Raises:
            TypeError: Если amount не является числом.
            ValueError: Если amount не положительно или превышает баланс.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        if amount > self.__balance:
            raise ValueError(
                f"Недостаточно средств. Баланс: {self.__balance:.2f}, "
                f"требуется: {amount:.2f}"
            )

        self.__balance -= amount
        self.__log_transaction("WITHDRAW", amount, f"Снятие {amount:.2f}")
        return self.__balance

    # --- Фабричный (публичный) метод создания объекта ---
    @classmethod
    def create_account(cls, owner, initial_balance=0.0):
        """Создаёт новый счёт с проверкой входных данных.

        Фабричный метод, альтернативный вызову конструктора.

        Args:
            owner (str): Имя владельца счёта. Непустая строка.
            initial_balance (int | float, optional): Начальный баланс,
                не может быть отрицательным. По умолчанию 0.0.

        Returns:
            BankAccount: Новый экземпляр класса (или подкласса) cls.

        Raises:
            ValueError: Если owner не является непустой строкой
                или initial_balance отрицателен.
        """
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца должно быть непустой строкой")
        if initial_balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        return cls(owner, initial_balance)

    def __str__(self):
        """Возвращает строковое представление счёта.

        Returns:
            str: Строка вида "BankAccount(владелец='...', баланс=...)".
        """
        return (f"{self.__class__.__name__}(владелец='{self.__owner}', "
                f"баланс={self.__balance:.2f})")


# Класс SavingsAccount — сберегательный счёт

class SavingsAccount(BankAccount):
    """Сберегательный счёт с процентной ставкой и ограничением на снятие."""

    def __init__(self, owner, balance=0.0, interest_rate=0.0):
        """Инициализирует сберегательный счёт.

        Args:
            owner (str): Имя владельца счёта.
            balance (float, optional): Начальный баланс. По умолчанию 0.0.
            interest_rate (int | float, optional): Годовая процентная
                ставка в процентах. По умолчанию 0.0.

        Returns:
            None
        """
        super().__init__(owner, balance)
        self.interest_rate = interest_rate  # годовая ставка, %

    @property
    def interest_rate(self):
        """Возвращает годовую процентную ставку.

        Returns:
            int | float: Процентная ставка в процентах годовых.
        """
        return self.__interest_rate

    @interest_rate.setter
    def interest_rate(self, value):
        """Устанавливает процентную ставку с валидацией значения.

        Args:
            value (int | float): Новая процентная ставка в процентах.

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value отрицательно.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Процентная ставка должна быть числом")
        if value < 0:
            raise ValueError("Процентная ставка не может быть отрицательной")
        self.__interest_rate = value

    def apply_interest(self):
        """Начисляет проценты на текущий баланс.

        Рассчитывает сумму процентов по годовой ставке и зачисляет её
        на счёт через родительский deposit(). После этого корректирует
        последнюю запись в истории, чтобы она отражала тип 'INTEREST'.

        Returns:
            float: Сумма начисленных процентов.
        """
        interest = self.balance * (self.__interest_rate / 100)
        # Используем родительский deposit, чтобы операция попала в историю
        self.deposit(interest)
        # Переопределим комментарий последней записи
        self._BankAccount__history[-1]["type"] = "INTEREST"
        self._BankAccount__history[-1]["amount"] = interest
        self._BankAccount__history[-1]["comment"] = (
            f"Начисление процентов {self.__interest_rate}%: +{interest:.2f}"
        )
        return interest

    def withdraw(self, amount):
        """Снимает средства со сберегательного счёта.

        Переопределённое снятие: за одну операцию нельзя снять более
        50% текущего баланса.

        Args:
            amount (int | float): Сумма снятия. Должна быть положительной
                и не превышать 50% текущего баланса.

        Returns:
            float: Новый баланс после снятия.

        Raises:
            TypeError: Если amount не является числом.
            ValueError: Если amount не положительно или превышает
                допустимый лимит (50% баланса) либо текущий баланс.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")

        max_allowed = self.balance * 0.5
        if amount > max_allowed:
            raise ValueError(
                f"Сберегательный счёт: нельзя снять более 50% баланса. "
                f"Максимум: {max_allowed:.2f}, запрошено: {amount:.2f}"
            )
        # Остальная валидация (хватит ли денег) — через родительский метод
        return super().withdraw(amount)


# ДЕМОНСТРАЦИЯ

def separator(title):
    """Печатает заголовок-разделитель для секций демонстрации.

    Args:
        title (str): Текст заголовка, выводимый между линиями '='.

    Returns:
        None
    """
    print(f"\n{'=' * 25} {title} {'=' * 25}")


def main():
    """Демонстрирует работу классов BankAccount и SavingsAccount.

    Показывает:
        1. Создание объектов через фабричный метод и конструктор.
        2. Корректные пополнение и снятие.
        3. Обработку ошибок при некорректных операциях.
        4. Невозможность изменить баланс и владельца напрямую.
        5. Возврат копии истории операций.
        6. Начисление процентов и ограничение снятия на сберсчёте.
        7. Полиморфное поведение метода withdraw().
        8. Итоговые истории обоих счетов.

    Returns:
        None
    """
    # 1. Создание через фабричный метод и через конструктор
    separator("1. Создание объектов")
    acc1 = BankAccount.create_account("Иванов И.И.", 1000)
    acc2 = SavingsAccount("Петров П.П.", 5000, interest_rate=7.5)
    print(acc1)
    print(acc2)

    # 2. Корректные пополнение и снятие
    separator("2. Корректные операции")
    acc1.deposit(500)
    print(f"После пополнения на 500: баланс = {acc1.balance:.2f}")
    acc1.withdraw(200)
    print(f"После снятия 200: баланс = {acc1.balance:.2f}")

    # 3. Ошибки при некорректных операциях
    separator("3. Ошибки при операциях")

    # 3.1. Отрицательная сумма пополнения
    try:
        acc1.deposit(-100)
    except ValueError as e:
        print(f"Ошибка пополнения: {e}")

    # 3.2. Отрицательная сумма снятия
    try:
        acc1.withdraw(-50)
    except ValueError as e:
        print(f"Ошибка снятия: {e}")

    # 3.3. Превышение баланса
    try:
        acc1.withdraw(10000)
    except ValueError as e:
        print(f"Ошибка снятия (превышение): {e}")

    # 3.4. Сумма не число
    try:
        acc1.deposit("тысяча")
    except TypeError as e:
        print(f"Ошибка типа: {e}")

    # 4. Невозможность изменить баланс напрямую
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

    # 5. Вывод истории операций
    separator("5. История операций")
    print("История acc1:")
    for record in acc1.history:
        print(f"  [{record['datetime']}] {record['type']:>8} "
              f"{record['amount']:>8.2f} | баланс: {record['balance_after']:.2f} "
              f"| {record['comment']}")

    # Демонстрация, что возвращается именно копия
    hist_copy = acc1.history
    hist_copy.append({"fake": True})
    print(f"\nДобавили фейковую запись в копию. "
          f"Реальная длина истории: {len(acc1.history)} (не изменилась)")

    # 6. Сберегательный счёт: начисление процентов и ограничение снятия
    separator("6. Сберегательный счёт")
    print(f"Начальный баланс: {acc2.balance:.2f}")
    interest = acc2.apply_interest()
    print(f"Начислено процентов: {interest:.2f}")
    print(f"Баланс после начисления: {acc2.balance:.2f}")

    # Попытка снять больше 50%
    try:
        acc2.withdraw(3000)  # 50% от 5375 = 2687.5
    except ValueError as e:
        print(f"Ошибка снятия с сберсчёта: {e}")

    # Корректное снятие
    acc2.withdraw(2000)
    print(f"После снятия 2000: баланс = {acc2.balance:.2f}")

    # 7. Полиморфное поведение метода withdraw
    separator("7. Полиморфизм: снятие для разных типов счетов")
    accounts = [
        BankAccount.create_account("Обычный клиент", 1000),
        SavingsAccount("Сберегательный клиент", 1000, interest_rate=5),
    ]

    # Попытка снять 600 (60% баланса) — для обычного счёта это ОК,
    # для сберегательного — нет
    for acc in accounts:
        print(f"\n{acc}")
        try:
            acc.withdraw(600)
            print(f"  ✓ Снятие 600 прошло успешно. Баланс: {acc.balance:.2f}")
        except ValueError as e:
            print(f"  ✗ Ошибка: {e}")

    # Итоговая история обоих счетов
    separator("8. Итоговые истории")
    for acc in accounts:
        print(f"\n{acc.owner}:")
        for r in acc.history:
            print(f"  {r['type']:>8} {r['amount']:>8.2f} | {r['comment']}")


if __name__ == "__main__":
    main()
