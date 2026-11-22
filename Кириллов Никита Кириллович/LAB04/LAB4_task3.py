#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from abc import ABC, abstractmethod


SEPARATOR_WIDTH = 30
ADULT_AGE = 18
MAX_AGE = 120
MONTHS_IN_YEAR = 12
RETIREMENT_AGE = 65
VALID_GENDERS = ("мужской", "женский")


def _validate_collection(value, name):
    """Валидирует коллекцию непустых строк.

    Args:
        value: Проверяемый объект.
        name (str): Название поля для сообщения об ошибке.

    Returns:
        list[str]: Список нормализованных строк.
    """
    if type(value) not in (list, tuple, set):
        raise TypeError(f"{name} должны быть коллекцией")
    if len(value) == 0:
        raise ValueError(f"Список {name.lower()} не может быть пустым")
    for item in value:
        if type(item) != str or not item.strip():
            raise ValueError(f"Каждый элемент {name.lower()} должен быть непустой строкой")
    return [str(x).strip() for x in value]


class Person:
    """Базовый класс человека."""

    def __init__(self, name, gender, age):
        """Инициализирует объект человека.

        Args:
            name (str): Имя человека.
            gender (str): Пол ('мужской' или 'женский').
            age (int | float): Возраст в диапазоне [0; MAX_AGE].

        Returns:
            None
        """
        self.name = name
        self.gender = gender
        self.age = age
        self.is_alive = True

    @property
    def name(self):
        """Возвращает имя.

        Returns:
            str: Имя без ведущих и завершающих пробелов.
        """
        return self._name

    @name.setter
    def name(self, value):
        """Устанавливает имя с валидацией.

        Args:
            value (str): Новое имя (непустая строка).

        Returns:
            None
        """
        if type(value) != str or not value.strip():
            raise ValueError("Имя должно быть непустой строкой")
        self._name = value.strip()

    @property
    def gender(self):
        """Возвращает пол.

        Returns:
            str: Пол в нижнем регистре.
        """
        return self._gender

    @gender.setter
    def gender(self, value):
        """Устанавливает пол с валидацией.

        Args:
            value (str): Новый пол (должен входить в VALID_GENDERS).

        Returns:
            None
        """
        if type(value) != str:
            raise TypeError("Пол должен быть строкой")
        value = value.strip().lower()
        if value not in VALID_GENDERS:
            raise ValueError(
                f"Пол должен быть одним из {VALID_GENDERS}, получено: '{value}'"
            )
        self._gender = value

    @property
    def age(self):
        """Возвращает возраст.

        Returns:
            int: Возраст, приведённый к целому числу.
        """
        return self._age

    @age.setter
    def age(self, value):
        """Устанавливает возраст с валидацией.

        Args:
            value (int | float): Новый возраст в диапазоне [0; MAX_AGE].

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Возраст должен быть числом")
        if not (0 <= value <= MAX_AGE):
            raise ValueError(f"Возраст должен быть в диапазоне [0; {MAX_AGE}]")
        self._age = int(value)

    def present(self):
        """Возвращает строковое представление человека.

        Returns:
            str: Строка с именем, полом, возрастом и статусом.
        """
        status = "жив" if self.is_alive else "мёртв ☠"
        return (f"Person(имя='{self._name}', пол='{self._gender}', "
                f"возраст={self._age}, статус={status})")

    def is_adult(self):
        """Проверяет, является ли человек совершеннолетним.

        Returns:
            bool: True, если возраст не меньше ADULT_AGE.
        """
        return self._age >= ADULT_AGE

    @classmethod
    def from_variables(cls, name, gender, age):
        """Создаёт объект класса через переданные переменные.

        Args:
            name (str): Имя человека.
            gender (str): Пол.
            age (int | float): Возраст.

        Returns:
            Person: Новый экземпляр класса.
        """
        return cls(name, gender, age)

    def __str__(self):
        """Возвращает строковое представление объекта.

        Returns:
            str: Результат вызова present().
        """
        return self.present()


class Employee(Person, ABC):
    """Сотрудник: расширяет Person должностью, зарплатой и расходами."""

    def __init__(self, name, gender, age, position, salary, expenses):
        """Инициализирует сотрудника.

        Args:
            name (str): Имя сотрудника.
            gender (str): Пол.
            age (int | float): Возраст.
            position (str): Должность.
            salary (int | float): Зарплата.
            expenses (int | float): Расходы.

        Returns:
            None
        """
        super().__init__(name, gender, age)
        self.position = position
        self.salary = salary
        self.expenses = expenses
        self._check_financial_health()

    @property
    def position(self):
        """Возвращает должность.

        Returns:
            str: Название должности.
        """
        return self._position

    @position.setter
    def position(self, value):
        """Устанавливает должность с валидацией.

        Args:
            value (str): Новая должность (непустая строка).

        Returns:
            None
        """
        if type(value) != str or not value.strip():
            raise ValueError("Должность должна быть непустой строкой")
        self._position = value.strip()

    @property
    def salary(self):
        """Возвращает зарплату.

        Returns:
            float: Зарплата.
        """
        return self._salary

    @salary.setter
    def salary(self, value):
        """Устанавливает зарплату с валидацией.

        Args:
            value (int | float): Новая зарплата (неотрицательное число).

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Зарплата должна быть числом")
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        self._salary = float(value)
        self._check_financial_health()

    @property
    def expenses(self):
        """Возвращает расходы.

        Returns:
            float: Сумма расходов.
        """
        return self._expenses

    @expenses.setter
    def expenses(self, value):
        """Устанавливает расходы с валидацией.

        Args:
            value (int | float): Новые расходы (неотрицательное число).

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Расходы должны быть числом")
        if value < 0:
            raise ValueError("Расходы не могут быть отрицательными")
        self._expenses = float(value)
        self._check_financial_health()

    def _check_financial_health(self):
        """Помечает сотрудника 'мёртвым', если расходы превышают доход.

        Returns:
            None
        """
        if (hasattr(self, '_salary') and
                hasattr(self, '_expenses') and
                self._expenses > self._salary):
            self.is_alive = False

    @abstractmethod
    def do_work(self):
        """Абстрактный метод: каждая должность реализует свою работу.

        Returns:
            str: Описание выполняемой работы.
        """
        pass

    def cash_flow(self, months):
        """Рассчитывает денежный приток за указанное число месяцев.

        Args:
            months (int | float): Количество месяцев.

        Returns:
            float: Приток денег; 0, если сотрудник мёртв.
        """
        if not self.is_alive:
            return 0
        return (self._salary - self._expenses) * months

    def savings_until_retirement(self):
        """Рассчитывает накопления до выхода на пенсию.

        Returns:
            float: Сумма накоплений; 0, если мёртв/на пенсии/нет остатка.
        """
        if not self.is_alive:
            return 0
        years_left = RETIREMENT_AGE - self._age
        if years_left <= 0:
            return 0
        monthly_saving = self._salary - self._expenses
        if monthly_saving <= 0:
            return 0
        return monthly_saving * MONTHS_IN_YEAR * years_left

    def present(self):
        """Возвращает расширенное строковое представление сотрудника.

        Returns:
            str: Строка с характеристиками сотрудника.
        """
        status = "🔴 мёртв" if not self.is_alive else "🟢 жив"
        parent_info = super().present()
        return (f"{parent_info[:-1]}, "
                f"должность='{self._position}', "
                f"зарплата={self._salary:.0f}, "
                f"расходы={self._expenses:.0f}, "
                f"статус={status})")


class Manager(Employee):
    """Менеджер: управляет подчинёнными и проводит митинги."""

    def __init__(self, name, gender, age, position, salary, expenses):
        """Инициализирует менеджера.

        Args:
            name (str): Имя менеджера.
            gender (str): Пол.
            age (int | float): Возраст.
            position (str): Должность.
            salary (int | float): Зарплата.
            expenses (int | float): Расходы.

        Returns:
            None
        """
        super().__init__(name, gender, age, position, salary, expenses)
        self._subordinates = []

    @property
    def subordinates(self):
        """Возвращает копию списка подчинённых.

        Returns:
            list[Employee]: Копия списка подчинённых.
        """
        return self._subordinates.copy()

    def add_subordinate(self, employee):
        """Добавляет сотрудника в подчинение.

        Args:
            employee (Employee): Сотрудник для подчинения.

        Returns:
            None
        """
        if not isinstance(employee, Employee):
            raise TypeError("Подчинённым может быть только Employee")
        if employee in self._subordinates:
            raise ValueError("Этот сотрудник уже в подчинении")
        self._subordinates.append(employee)

    def remove_subordinate(self, employee):
        """Увольняет подчинённого.

        Args:
            employee (Employee): Сотрудник для удаления.

        Returns:
            None
        """
        if employee not in self._subordinates:
            raise ValueError("Сотрудник не в подчинении")
        self._subordinates.remove(employee)

    def hold_meeting(self):
        """Проводит митинг для подчинённых.

        Returns:
            None
        """
        print(f"\n📢 Менеджер {self._name} проводит собрание для "
              f"{len(self._subordinates)} подчинённых:")
        if len(self._subordinates) == 0:
            print("   (подчинённых нет — встреча с самим собой)")
            return
        for emp in self._subordinates:
            print(f"   👤 {emp._name} ({emp._position}) — слушает")

    def do_work(self):
        """Выполняет работу менеджера.

        Returns:
            str: Описание работы с указанием числа подчинённых.
        """
        return f"{self._name} управляет командой из {len(self._subordinates)} человек"

    def present(self):
        """Возвращает расширенное представление менеджера.

        Returns:
            str: Строка с характеристиками менеджера.
        """
        return (f"{super().present()[:-1]}, "
                f"подчинённых={len(self._subordinates)})")


class Developer(Employee):
    """Разработчик: знает языки программирования и пишет код."""

    def __init__(self, name, gender, age, position, salary, expenses, languages):
        """Инициализирует разработчика.

        Args:
            name (str): Имя разработчика.
            gender (str): Пол.
            age (int | float): Возраст.
            position (str): Должность.
            salary (int | float): Зарплата.
            expenses (int | float): Расходы.
            languages (list | tuple | set): Непустая коллекция языков.

        Returns:
            None
        """
        super().__init__(name, gender, age, position, salary, expenses)
        self.languages = languages

    @property
    def languages(self):
        """Возвращает копию списка языков.

        Returns:
            list[str]: Копия списка языков программирования.
        """
        return self._languages.copy()

    @languages.setter
    def languages(self, value):
        """Устанавливает список языков с валидацией.

        Args:
            value (list | tuple | set): Непустая коллекция непустых строк.

        Returns:
            None
        """
        self._languages = _validate_collection(value, "Языки")

    def write_code(self):
        """Пишет код на случайно выбранном языке.

        Returns:
            str: Описание действия.
        """
        lang = random.choice(self._languages)
        return f"{self._name} пишет код на {lang}"

    def do_work(self):
        """Выполняет работу разработчика.

        Returns:
            str: Результат вызова write_code().
        """
        return self.write_code()

    def present(self):
        """Возвращает расширенное представление разработчика.

        Returns:
            str: Строка с характеристиками разработчика.
        """
        return (f"{super().present()[:-1]}, "
                f"языки=[{', '.join(self._languages)}])")


class Designer(Employee):
    """Дизайнер: владеет инструментами и создаёт макеты."""

    def __init__(self, name, gender, age, position, salary, expenses, tools):
        """Инициализирует дизайнера.

        Args:
            name (str): Имя дизайнера.
            gender (str): Пол.
            age (int | float): Возраст.
            position (str): Должность.
            salary (int | float): Зарплата.
            expenses (int | float): Расходы.
            tools (list | tuple | set): Непустая коллекция инструментов.

        Returns:
            None
        """
        super().__init__(name, gender, age, position, salary, expenses)
        self.tools = tools

    @property
    def tools(self):
        """Возвращает копию списка инструментов.

        Returns:
            list[str]: Копия списка инструментов.
        """
        return self._tools.copy()

    @tools.setter
    def tools(self, value):
        """Устанавливает список инструментов с валидацией.

        Args:
            value (list | tuple | set): Непустая коллекция непустых строк.

        Returns:
            None
        """
        self._tools = _validate_collection(value, "Инструменты")

    def create_mockup(self, project_name):
        """Создаёт макет проекта.

        Args:
            project_name (str): Название проекта.

        Returns:
            str: Описание действия.
        """
        tool = random.choice(self._tools)
        return f"{self._name} создаёт макет '{project_name}' в инструменте {tool}"

    def do_work(self):
        """Выполняет работу дизайнера.

        Returns:
            str: Результат вызова create_mockup().
        """
        return self.create_mockup("UI проекта")

    def present(self):
        """Возвращает расширенное представление дизайнера.

        Returns:
            str: Строка с характеристиками дизайнера.
        """
        return (f"{super().present()[:-1]}, "
                f"инструменты=[{', '.join(self._tools)}])")


def separator(title):
    """Печатает заголовок-разделитель.

    Args:
        title (str): Текст заголовка.

    Returns:
        None
    """
    print(f"\n{'=' * SEPARATOR_WIDTH} {title} {'=' * SEPARATOR_WIDTH}")


if __name__ == "__main__":

    separator("1. Создание Person через классовый метод")
    p = Person.from_variables("Анна", "женский", 25)
    print(p.present())
    print(f"Совершеннолетняя? {p.is_adult()}")

    p_child = Person.from_variables("Миша", "мужской", 15)
    print(p_child.present())
    print(f"Совершеннолетний? {p_child.is_adult()}")

    separator("2. Валидация данных")
    try:
        Person("", "мужской", 30)
    except ValueError as e:
        print(f"Ошибка имени: {e}")

    try:
        Person("Иван", "инопланетянин", 30)
    except ValueError as e:
        print(f"Ошибка пола: {e}")

    try:
        Person("Иван", "мужской", 200)
    except ValueError as e:
        print(f"Ошибка возраста: {e}")

    separator("3. Создание сотрудников")
    manager = Manager("Олег", "мужской", 40, "Team Lead", 150000, 60000)
    dev = Developer("Алиса", "женский", 28, "Senior Dev", 200000, 80000,
                    ["Python", "Go", "Rust"])
    designer = Designer("Борис", "мужской", 32, "UI Designer", 120000, 70000,
                        ["Figma", "Sketch", "Photoshop"])

    manager.add_subordinate(dev)
    manager.add_subordinate(designer)

    separator("4. Сотрудник, который тратит больше, чем получает")
    bankrupt = Developer("Разор", "мужской", 35, "Junior Dev", 50000, 80000,
                         ["JavaScript"])
    print(bankrupt.present())
    print(f"Жив? {bankrupt.is_alive}")
    print(f"Приток денег за 3 мес.: {bankrupt.cash_flow(3)}")

    separator("5. Полиморфизм: present()")
    staff = [manager, dev, designer, bankrupt]
    for emp in staff:
        print(emp.present())

    separator("6. Полиморфизм: do_work()")
    for emp in staff:
        if emp.is_alive:
            print(f"  {emp._name}: {emp.do_work()}")
        else:
            print(f"  {emp._name}: 💀 не может работать (мёртв)")

    separator("7. Митинг менеджера")
    manager.hold_meeting()

    separator("8. Специфичные методы подклассов")
    print(dev.write_code())
    print(designer.create_mockup("Лендинг для банка"))

    separator("9. Финансовая оценка")
    for emp in staff:
        print(f"\n{emp._name} ({emp._position}):")
        print(f"  Жив: {emp.is_alive}")
        print(f"  Приток за 6 мес.: {emp.cash_flow(6):.0f}")
        print(f"  Накопления до пенсии: {emp.savings_until_retirement():.0f}")

    separator("10. Демонстрация super() в цепочке наследования")
    print("Каждый present() вызывает родительский через super():")
    print("  Manager.present()  → Employee.present() → Person.present()")
    print("  Developer.present() → Employee.present() → Person.present()")
    print("  Designer.present() → Employee.present() → Person.present()")
    print("\nПример вывода Manager:")
    print(manager.present())
    
