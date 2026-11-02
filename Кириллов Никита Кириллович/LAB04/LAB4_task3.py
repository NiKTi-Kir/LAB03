#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from abc import ABC, abstractmethod


class Person:
    """Базовый класс человека."""

    VALID_GENDERS = {"мужской", "женский"}

    def __init__(self, name, gender, age):
        """Инициализирует объект человека.

        Args:
            name (str): Имя человека. Непустая строка.
            gender (str): Пол. Один из VALID_GENDERS.
            age (int | float): Возраст в диапазоне [0; 120].

        Returns:
            None
        """
        self.name = name
        self.gender = gender
        self.age = age
        self.is_alive = True  # флаг "жив/мёртв"

    # --- Свойства с валидацией ---
    @property
    def name(self):
        """Возвращает имя человека.

        Returns:
            str: Имя без ведущих и завершающих пробелов.
        """
        return self.__name

    @name.setter
    def name(self, value):
        """Устанавливает имя с валидацией значения.

        Args:
            value (str): Новое имя. Непустая строка.

        Raises:
            ValueError: Если value не строка или состоит только из пробелов.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя должно быть непустой строкой")
        self.__name = value.strip()

    @property
    def gender(self):
        """Возвращает пол человека.

        Returns:
            str: Пол в нижнем регистре ('мужской' или 'женский').
        """
        return self.__gender

    @gender.setter
    def gender(self, value):
        """Устанавливает пол с валидацией значения.

        Args:
            value (str): Новый пол. Должен входить в VALID_GENDERS
                (регистр и пробелы нормализуются).

        Raises:
            TypeError: Если value не является строкой.
            ValueError: Если value не входит в VALID_GENDERS.
        """
        if not isinstance(value, str):
            raise TypeError("Пол должен быть строкой")
        value = value.strip().lower()
        if value not in self.VALID_GENDERS:
            raise ValueError(
                f"Пол должен быть одним из {self.VALID_GENDERS}, получено: '{value}'"
            )
        self.__gender = value

    @property
    def age(self):
        """Возвращает возраст человека.

        Returns:
            int: Возраст, приведённый к целому числу.
        """
        return self.__age

    @age.setter
    def age(self, value):
        """Устанавливает возраст с валидацией значения.

        Args:
            value (int | float): Новый возраст в диапазоне [0; 120].

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value вне диапазона [0; 120].
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Возраст должен быть числом")
        if not (0 <= value <= 120):
            raise ValueError("Возраст должен быть в диапазоне [0; 120]")
        self.__age = int(value)

    # --- Методы ---
    def present(self):
        """Возвращает красивое строковое представление человека.

        Returns:
            str: Строка с именем, полом, возрастом и статусом
                (жив / мёртв ☠).
        """
        status = "жив" if self.is_alive else "мёртв ☠"
        return (f"Person(имя='{self.name}', пол='{self.gender}', "
                f"возраст={self.age}, статус={status})")

    def is_adult(self):
        """Проверяет, является ли человек совершеннолетним (18+).

        Returns:
            bool: True, если возраст не меньше 18.
        """
        return self.age >= 18

    # --- Классовый метод: конструирование через переменные ---
    @classmethod
    def from_variables(cls, name, gender, age):
        """Создаёт объект класса через переданные переменные.

        Args:
            name (str): Имя человека.
            gender (str): Пол.
            age (int | float): Возраст.

        Returns:
            Person: Новый экземпляр класса (или подкласса) cls.
        """
        return cls(name, gender, age)

    def __str__(self):
        """Возвращает строковое представление объекта.

        Делегирует к present().

        Returns:
            str: Строка с характеристиками человека.
        """
        return self.present()


# =====================================================================
# Класс Employee (наследует Person)
# =====================================================================
class Employee(Person, ABC):
    """Сотрудник: расширяет Person должностью, зарплатой и расходами."""

    RETIREMENT_AGE = 65  # возраст выхода на пенсию

    def __init__(self, name, gender, age, position, salary, expenses):
        """Инициализирует сотрудника.

        Args:
            name (str): Имя сотрудника.
            gender (str): Пол ('мужской' или 'женский').
            age (int | float): Возраст в диапазоне [0; 120].
            position (str): Должность (непустая строка).
            salary (int | float): Зарплата (неотрицательное число).
            expenses (int | float): Расходы (неотрицательное число).

        Returns:
            None
        """
        super().__init__(name, gender, age)
        self.position = position
        self.salary = salary
        self.expenses = expenses
        self._check_financial_health()

    # --- Свойства с валидацией ---
    @property
    def position(self):
        """Возвращает должность сотрудника.

        Returns:
            str: Название должности.
        """
        return self.__position

    @position.setter
    def position(self, value):
        """Устанавливает должность с валидацией значения.

        Args:
            value (str): Новая должность. Непустая строка.

        Raises:
            ValueError: Если value не строка или состоит только из пробелов.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Должность должна быть непустой строкой")
        self.__position = value.strip()

    @property
    def salary(self):
        """Возвращает зарплату сотрудника.

        Returns:
            float: Зарплата.
        """
        return self.__salary

    @salary.setter
    def salary(self, value):
        """Устанавливает зарплату с валидацией значения.

        Args:
            value (int | float): Новая зарплата (неотрицательное число).

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value отрицательно.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Зарплата должна быть числом")
        if value < 0:
            raise ValueError("Зарплата не может быть отрицательной")
        self.__salary = float(value)
        self._check_financial_health()

    @property
    def expenses(self):
        """Возвращает расходы сотрудника.

        Returns:
            float: Сумма расходов.
        """
        return self.__expenses

    @expenses.setter
    def expenses(self, value):
        """Устанавливает расходы с валидацией значения.

        Args:
            value (int | float): Новые расходы (неотрицательное число).

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value отрицательно.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Расходы должны быть числом")
        if value < 0:
            raise ValueError("Расходы не могут быть отрицательными")
        self.__expenses = float(value)
        self._check_financial_health()

    def _check_financial_health(self):
        """Помечает сотрудника 'мёртвым', если расходы превышают доход.

        Проверка выполняется только после того, как оба поля (salary
        и expenses) уже установлены.

        Returns:
            None
        """
        if (hasattr(self, '_Employee__salary') and
                hasattr(self, '_Employee__expenses') and
                self.__expenses > self.__salary):
            self.is_alive = False

    # --- Абстрактный метод работы ---
    @abstractmethod
    def do_work(self):
        """Абстрактный метод: каждая должность реализует свою работу.

        Returns:
            str: Описание выполняемой работы (зависит от подкласса).
        """
        pass

    # --- Методы финансовой оценки ---
    def cash_flow(self, months):
        """Рассчитывает денежный приток за указанное число месяцев.

        Формула: (зарплата − расходы) × months.

        Args:
            months (int | float): Количество месяцев.

        Returns:
            float: Приток денег за months месяцев;
                0, если сотрудник мёртв.
        """
        if not self.is_alive:
            return 0
        return (self.__salary - self.__expenses) * months

    def savings_until_retirement(self):
        """Рассчитывает накопления сотрудника до выхода на пенсию.

        Returns:
            float: Сумма накоплений до RETIREMENT_AGE;
                0, если сотрудник мёртв, уже на пенсии или
                не имеет положительного месячного остатка.
        """
        if not self.is_alive:
            return 0
        years_left = self.RETIREMENT_AGE - self.age
        if years_left <= 0:
            return 0
        monthly_saving = self.__salary - self.__expenses
        if monthly_saving <= 0:
            return 0
        return monthly_saving * 12 * years_left

    # --- Переопределение представления с super() ---
    def present(self):
        """Возвращает расширенное строковое представление сотрудника.

        Дополняет родительское представление должностью, зарплатой,
        расходами и статусом.

        Returns:
            str: Строка с характеристиками сотрудника.
        """
        status = "🔴 мёртв" if not self.is_alive else "🟢 жив"
        parent_info = super().present()
        return (f"{parent_info[:-1]}, "  # убираем закрывающую скобку родителя
                f"должность='{self.position}', "
                f"зарплата={self.__salary:.0f}, "
                f"расходы={self.__expenses:.0f}, "
                f"статус={status})")


# =====================================================================
# Класс Manager
# =====================================================================
class Manager(Employee):
    """Менеджер: управляет подчинёнными и проводит митинги."""

    def __init__(self, name, gender, age, position, salary, expenses):
        """Инициализирует менеджера.

        Args:
            name (str): Имя менеджера.
            gender (str): Пол ('мужской' или 'женский').
            age (int | float): Возраст.
            position (str): Должность.
            salary (int | float): Зарплата.
            expenses (int | float): Расходы.

        Returns:
            None
        """
        super().__init__(name, gender, age, position, salary, expenses)
        self.__subordinates = []

    @property
    def subordinates(self):
        """Возвращает копию списка подчинённых.

        Returns:
            list[Employee]: Новый список с подчинёнными менеджера.
        """
        return list(self.__subordinates)  # возвращаем копию

    def add_subordinate(self, employee):
        """Добавляет сотрудника в подчинение менеджеру.

        Args:
            employee (Employee): Сотрудник, который станет подчинённым.

        Returns:
            None

        Raises:
            TypeError: Если employee не является экземпляром Employee.
            ValueError: Если employee уже находится в подчинении.
        """
        if not isinstance(employee, Employee):
            raise TypeError("Подчинённым может быть только Employee")
        if employee in self.__subordinates:
            raise ValueError("Этот сотрудник уже в подчинении")
        self.__subordinates.append(employee)

    def remove_subordinate(self, employee):
        """Увольняет (удаляет) подчинённого.

        Args:
            employee (Employee): Сотрудник, которого нужно убрать.

        Returns:
            None

        Raises:
            ValueError: Если employee не находится в подчинении.
        """
        if employee not in self.__subordinates:
            raise ValueError("Сотрудник не в подчинении")
        self.__subordinates.remove(employee)

    def hold_meeting(self):
        """Проводит митинг для подчинённых и выводит список участников.

        Returns:
            None
        """
        print(f"\n📢 Менеджер {self.name} проводит собрание для "
              f"{len(self.__subordinates)} подчинённых:")
        if not self.__subordinates:
            print("   (подчинённых нет — встреча с самим собой)")
            return
        for emp in self.__subordinates:
            print(f"   👤 {emp.name} ({emp.position}) — слушает")

    def do_work(self):
        """Выполняет работу менеджера — управление командой.

        Returns:
            str: Описание работы с указанием числа подчинённых.
        """
        return f"{self.name} управляет командой из {len(self.__subordinates)} человек"

    def present(self):
        """Возвращает расширенное представление менеджера.

        Дополняет представление Employee информацией о числе
        подчинённых.

        Returns:
            str: Строка с характеристиками менеджера.
        """
        parent_info = super().present()
        return (f"{parent_info[:-1]}, "
                f"подчинённых={len(self.__subordinates)})")


# =====================================================================
# Класс Developer
# =====================================================================
class Developer(Employee):
    """Разработчик: знает языки программирования и пишет код."""

    def __init__(self, name, gender, age, position, salary, expenses, languages):
        """Инициализирует разработчика.

        Args:
            name (str): Имя разработчика.
            gender (str): Пол ('мужской' или 'женский').
            age (int | float): Возраст.
            position (str): Должность.
            salary (int | float): Зарплата.
            expenses (int | float): Расходы.
            languages (list | tuple | set): Непустая коллекция языков
                программирования (непустые строки).

        Returns:
            None
        """
        super().__init__(name, gender, age, position, salary, expenses)
        self.languages = languages

    @property
    def languages(self):
        """Возвращает копию списка языков программирования.

        Returns:
            list[str]: Новый список языков программирования.
        """
        return list(self.__languages)

    @languages.setter
    def languages(self, value):
        """Устанавливает список языков с валидацией значения.

        Args:
            value (list | tuple | set): Непустая коллекция непустых строк.

        Raises:
            TypeError: Если value не является коллекцией.
            ValueError: Если коллекция пуста или содержит
                нестроковые/пустые элементы.
        """
        if not isinstance(value, (list, tuple, set)):
            raise TypeError("Языки должны быть коллекцией")
        if not value:
            raise ValueError("Список языков не может быть пустым")
        for lang in value:
            if not isinstance(lang, str) or not lang.strip():
                raise ValueError("Каждый язык должен быть непустой строкой")
        self.__languages = [str(l).strip() for l in value]

    def write_code(self):
        """Пишет код на случайно выбранном языке из списка.

        Returns:
            str: Описание действия (кто и на каком языке пишет код).
        """
        lang = random.choice(self.__languages)
        return f"{self.name} пишет код на {lang}"

    def do_work(self):
        """Выполняет работу разработчика — пишет код.

        Returns:
            str: Результат вызова write_code().
        """
        return self.write_code()

    def present(self):
        """Возвращает расширенное представление разработчика.

        Дополняет представление Employee списком языков.

        Returns:
            str: Строка с характеристиками разработчика.
        """
        parent_info = super().present()
        langs = ", ".join(self.__languages)
        return (f"{parent_info[:-1]}, "
                f"языки=[{langs}])")


# =====================================================================
# Класс Designer
# =====================================================================
class Designer(Employee):
    """Дизайнер: владеет инструментами и создаёт макеты."""

    def __init__(self, name, gender, age, position, salary, expenses, tools):
        """Инициализирует дизайнера.

        Args:
            name (str): Имя дизайнера.
            gender (str): Пол ('мужской' или 'женский').
            age (int | float): Возраст.
            position (str): Должность.
            salary (int | float): Зарплата.
            expenses (int | float): Расходы.
            tools (list | tuple | set): Непустая коллекция инструментов
                (непустые строки).

        Returns:
            None
        """
        super().__init__(name, gender, age, position, salary, expenses)
        self.tools = tools

    @property
    def tools(self):
        """Возвращает копию списка инструментов дизайнера.

        Returns:
            list[str]: Новый список инструментов.
        """
        return list(self.__tools)

    @tools.setter
    def tools(self, value):
        """Устанавливает список инструментов с валидацией значения.

        Args:
            value (list | tuple | set): Непустая коллекция непустых строк.

        Raises:
            TypeError: Если value не является коллекцией.
            ValueError: Если коллекция пуста или содержит
                нестроковые/пустые элементы.
        """
        if not isinstance(value, (list, tuple, set)):
            raise TypeError("Инструменты должны быть коллекцией")
        if not value:
            raise ValueError("Список инструментов не может быть пустым")
        for tool in value:
            if not isinstance(tool, str) or not tool.strip():
                raise ValueError("Каждый инструмент должен быть непустой строкой")
        self.__tools = [str(t).strip() for t in value]

    def create_mockup(self, project_name):
        """Создаёт макет проекта, используя случайный инструмент.

        Args:
            project_name (str): Название проекта.

        Returns:
            str: Описание действия (кто, какой макет и в каком
                инструменте создаёт).
        """
        tool = random.choice(self.__tools)
        return (f"{self.name} создаёт макет '{project_name}' "
                f"в инструменте {tool}")

    def do_work(self):
        """Выполняет работу дизайнера — создаёт макет.

        Returns:
            str: Результат вызова create_mockup('UI проекта').
        """
        return self.create_mockup("UI проекта")

    def present(self):
        """Возвращает расширенное представление дизайнера.

        Дополняет представление Employee списком инструментов.

        Returns:
            str: Строка с характеристиками дизайнера.
        """
        parent_info = super().present()
        tools_str = ", ".join(self.__tools)
        return (f"{parent_info[:-1]}, "
                f"инструменты=[{tools_str}])")


# =====================================================================
# ДЕМОНСТРАЦИЯ
# =====================================================================
def separator(title):
    """Печатает заголовок-разделитель для секций демонстрации.

    Args:
        title (str): Текст заголовка, выводимый между линиями '='.

    Returns:
        None
    """
    print(f"\n{'=' * 30} {title} {'=' * 30}")


def main():
    """Демонстрирует работу иерархии классов Person → Employee → …

    Показывает:
        1. Создание Person через классовый метод from_variables.
        2. Валидацию входных данных (имя, пол, возраст).
        3. Создание сотрудников разных типов (Manager, Developer, Designer).
        4. Поведение «умирающего» сотрудника (расходы > доход).
        5. Полиморфный вызов present().
        6. Полиморфный вызов do_work().
        7. Митинг у менеджера.
        8. Специфичные методы подклассов (write_code, create_mockup).
        9. Финансовую оценку (cash_flow, savings_until_retirement).
       10. Работу super() в цепочке наследования.

    Returns:
        None
    """
    # 1. Создание через классовый метод Person.from_variables
    separator("1. Создание Person через классовый метод")
    p = Person.from_variables("Анна", "женский", 25)
    print(p.present())
    print(f"Совершеннолетняя? {p.is_adult()}")

    p_child = Person.from_variables("Миша", "мужской", 15)
    print(p_child.present())
    print(f"Совершеннолетний? {p_child.is_adult()}")

    # 2. Валидация
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

    # 3. Создание сотрудников разных типов
    separator("3. Создание сотрудников")
    manager = Manager("Олег", "мужской", 40, "Team Lead", 150000, 60000)
    dev = Developer("Алиса", "женский", 28, "Senior Dev", 200000, 80000,
                    ["Python", "Go", "Rust"])
    designer = Designer("Борис", "мужской", 32, "UI Designer", 120000, 70000,
                        ["Figma", "Sketch", "Photoshop"])

    # Подчинённые у менеджера
    manager.add_subordinate(dev)
    manager.add_subordinate(designer)

    # 4. "Умирающий" сотрудник (тратит больше, чем получает)
    separator("4. Сотрудник, который тратит больше, чем получает")
    bankrupt = Developer("Разор", "мужской", 35, "Junior Dev", 50000, 80000,
                         ["JavaScript"])
    print(bankrupt.present())
    print(f"Жив? {bankrupt.is_alive}")
    print(f"Приток денег за 3 мес.: {bankrupt.cash_flow(3)}")

    # 5. Полиморфный вызов present()
    separator("5. Полиморфизм: present()")
    staff = [manager, dev, designer, bankrupt]
    for emp in staff:
        print(emp.present())

    # 6. Полиморфный вызов do_work()
    separator("6. Полиморфизм: do_work()")
    for emp in staff:
        if emp.is_alive:
            print(f"  {emp.name}: {emp.do_work()}")
        else:
            print(f"  {emp.name}: 💀 не может работать (мёртв)")

    # 7. Митинг у менеджера
    separator("7. Митинг менеджера")
    manager.hold_meeting()

    # 8. Работа разработчика и дизайнера
    separator("8. Специфичные методы подклассов")
    print(dev.write_code())
    print(designer.create_mockup("Лендинг для банка"))

    # 9. Финансы: приток денег и накопления до пенсии
    separator("9. Финансовая оценка")
    for emp in staff:
        print(f"\n{emp.name} ({emp.position}):")
        print(f"  Жив: {emp.is_alive}")
        print(f"  Приток за 6 мес.: {emp.cash_flow(6):.0f}")
        print(f"  Накопления до пенсии: {emp.savings_until_retirement():.0f}")

    # 10. Демонстрация работы super() — видно по выводу present()
    separator("10. Демонстрация super() в цепочке наследования")
    print("Каждый present() вызывает родительский через super():")
    print("  Manager.present()  → вызывает Employee.present() → вызывает Person.present()")
    print("  Developer.present() → вызывает Employee.present() → вызывает Person.present()")
    print("  Designer.present() → вызывает Employee.present() → вызывает Person.present()")
    print("\nПример вывода Manager:")
    print(manager.present())


if __name__ == "__main__":
    main()
