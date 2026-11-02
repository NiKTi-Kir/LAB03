#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Transport:
    """Базовый класс транспортного средства."""

    def __init__(self, speed, capacity):
        """Инициализирует транспортное средство.

        Args:
            speed (int | float): Скорость транспортного средства в км/ч.
                Должна быть положительным числом.
            capacity (int | float): Вместимость транспортного средства.
                Должна быть положительным числом.

        Raises:
            TypeError: Если speed или capacity не являются числом.
            ValueError: Если speed или capacity не положительны.
        """
        # Используем сеттеры, чтобы сработала валидация при создании объекта
        self.speed = speed
        self.capacity = capacity

    # --- Свойства (properties) с валидацией ---
    @property
    def speed(self):
        """Возвращает скорость транспортного средства.

        Returns:
            int | float: Текущая скорость в км/ч.
        """
        return self.__speed

    @speed.setter
    def speed(self, value):
        """Устанавливает скорость с валидацией значения.

        Args:
            value (int | float): Новая скорость в км/ч.

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value не положительно.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Скорость должна быть числом")
        if value <= 0:
            raise ValueError("Скорость должна быть положительной")
        self.__speed = value

    @property
    def capacity(self):
        """Возвращает вместимость транспортного средства.

        Returns:
            int | float: Текущая вместимость.
        """
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        """Устанавливает вместимость с валидацией значения.

        Args:
            value (int | float): Новая вместимость.

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value не положительно.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Ёмкость должна быть числом")
        if value <= 0:
            raise ValueError("Ёмкость должна быть положительной")
        self.__capacity = value

    # --- Методы экземпляра ---
    def get_info(self):
        """Возвращает строку с основными характеристиками ТС.

        Returns:
            str: Описание со скоростью и вместимостью.
        """
        return (f"Transport: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity}")

    def is_speed_above(self, threshold):
        """Проверяет, превышает ли скорость заданный порог.

        Args:
            threshold (int | float): Пороговое значение скорости в км/ч.

        Returns:
            bool: True, если текущая скорость строго больше threshold.
        """
        return self.speed > threshold

    # --- Классовый метод: создание объекта из словаря ---
    @classmethod
    def from_dict(cls, data):
        """Создаёт объект класса из словаря с параметрами.

        Args:
            data (dict): Словарь с ключами 'speed' и 'capacity'.

        Returns:
            Transport: Новый экземпляр класса (или подкласса) cls.

        Raises:
            TypeError: Если data не является словарём.
            KeyError: Если в словаре отсутствуют нужные ключи.
        """
        if not isinstance(data, dict):
            raise TypeError("Ожидается словарь")
        return cls(data['speed'], data['capacity'])

    # --- Статический метод: вызывается без создания объекта ---
    @staticmethod
    def get_description():
        """Возвращает общее описание класса Transport.

        Метод не требует создания экземпляра.

        Returns:
            str: Текстовое описание базового класса.
        """
        return "Transport — базовый класс для всех транспортных средств."


# Класс Bus — автобус, добавляет маршрут

class Bus(Transport):
    """Автобус — транспортное средство с маршрутом."""

    def __init__(self, speed, capacity, route):
        """Инициализирует автобус.

        Args:
            speed (int | float): Скорость в км/ч (положительное число).
            capacity (int | float): Вместимость (положительное число).
            route (str): Непустая строка с названием маршрута.

        Raises:
            TypeError: Если speed или capacity не являются числом.
            ValueError: Если speed/capacity не положительны
                или route пустая строка.
        """
        super().__init__(speed, capacity)
        self.route = route

    @property
    def route(self):
        """Возвращает маршрут автобуса.

        Returns:
            str: Название маршрута.
        """
        return self.__route

    @route.setter
    def route(self, value):
        """Устанавливает маршрут с валидацией значения.

        Args:
            value (str): Непустая строка с названием маршрута.

        Raises:
            ValueError: Если value не строка или состоит только из пробелов.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Маршрут должен быть непустой строкой")
        self.__route = value

    def get_info(self):
        """Возвращает строку с характеристиками автобуса.

        Returns:
            str: Описание со скоростью, вместимостью и маршрутом.
        """
        return (f"Bus: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity} чел., "
                f"маршрут = '{self.route}'")


# Класс Truck — грузовик, добавляет грузоподъёмность и расчёт стоимости

class Truck(Transport):
    """Грузовик — транспортное средство с грузоподъёмностью."""

    def __init__(self, speed, capacity, load_capacity):
        """Инициализирует грузовик.

        Args:
            speed (int | float): Скорость в км/ч (положительное число).
            capacity (int | float): Вместимость (положительное число).
            load_capacity (int | float): Грузоподъёмность в тоннах
                (положительное число).

        Raises:
            TypeError: Если какой-либо параметр не является числом.
            ValueError: Если какой-либо числовой параметр не положителен.
        """
        super().__init__(speed, capacity)
        self.load_capacity = load_capacity

    @property
    def load_capacity(self):
        """Возвращает грузоподъёмность грузовика.

        Returns:
            int | float: Грузоподъёмность в тоннах.
        """
        return self.__load_capacity

    @load_capacity.setter
    def load_capacity(self, value):
        """Устанавливает грузоподъёмность с валидацией значения.

        Args:
            value (int | float): Новая грузоподъёмность в тоннах.

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value не положительно.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Грузоподъёмность должна быть числом")
        if value <= 0:
            raise ValueError("Грузоподъёмность должна быть положительной")
        self.__load_capacity = value

    def get_info(self):
        """Возвращает строку с характеристиками грузовика.

        Returns:
            str: Описание со скоростью, вместимостью
                и грузоподъёмностью.
        """
        return (f"Truck: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity}, "
                f"грузоподъёмность = {self.load_capacity} т")

    def calculate_cost(self, distance):
        """Рассчитывает стоимость перевозки груза.

        Формула: distance * (50 + 10 * load_capacity), где 50 руб./км —
        базовая ставка, 10 руб. — надбавка за каждую тонну на км.

        Args:
            distance (int | float): Расстояние перевозки в км.

        Returns:
            int | float: Стоимость перевозки в рублях.
        """
        return distance * (50 + 10 * self.load_capacity)


# Класс Taxi — такси, добавляет тариф и расчёт стоимости поездки

class Taxi(Transport):
    """Такси — транспортное средство с тарифом за километр."""

    def __init__(self, speed, capacity, tariff):
        """Инициализирует такси.

        Args:
            speed (int | float): Скорость в км/ч (положительное число).
            capacity (int | float): Вместимость (положительное число).
            tariff (int | float): Тариф в рублях за км
                (положительное число).

        Raises:
            TypeError: Если какой-либо параметр не является числом.
            ValueError: Если какой-либо числовой параметр не положителен.
        """
        super().__init__(speed, capacity)
        self.tariff = tariff

    @property
    def tariff(self):
        """Возвращает тариф такси.

        Returns:
            int | float: Тариф в рублях за километр.
        """
        return self.__tariff

    @tariff.setter
    def tariff(self, value):
        """Устанавливает тариф с валидацией значения.

        Args:
            value (int | float): Новый тариф в рублях за км.

        Raises:
            TypeError: Если value не является числом.
            ValueError: Если value не положительно.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Тариф должен быть числом")
        if value <= 0:
            raise ValueError("Тариф должен быть положительным")
        self.__tariff = value

    def get_info(self):
        """Возвращает строку с характеристиками такси.

        Returns:
            str: Описание со скоростью, вместимостью и тарифом.
        """
        return (f"Taxi: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity} чел., "
                f"тариф = {self.tariff} руб./км")

    def calculate_trip_cost(self, distance):
        """Рассчитывает стоимость поездки на такси.

        Args:
            distance (int | float): Расстояние поездки в км.

        Returns:
            int | float: Стоимость поездки в рублях (distance * tariff).
        """
        return distance * self.tariff


# ДЕМОНСТРАЦИЯ

def separator(title):
    """Печатает заголовок-разделитель для секций демонстрации.

    Args:
        title (str): Текст заголовка, выводимый между линиями '='.

    Returns:
        None
    """
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def main():
    """Демонстрирует работу классов Transport, Bus, Truck и Taxi.

    Показывает:
        1. Создание объектов через конструктор.
        2. Создание объекта через classmethod from_dict.
        3. Работу валидации при недопустимых значениях.
        4. Вызов статического и классового методов без экземпляра.
        5. Полиморфный вызов get_info и специфичных методов подклассов.

    Returns:
        None
    """
    # 1. Создание объектов через конструктор
    separator("1. Создание через конструктор")
    bus = Bus(speed=60, capacity=40, route="№15: Вокзал — Аэропорт")
    truck = Truck(speed=80, capacity=2, load_capacity=10)
    taxi = Taxi(speed=90, capacity=4, tariff=25)

    for t in (bus, truck, taxi):
        print(t.get_info())

    # 2. Создание объекта через классовый метод (из словаря)
    separator("2. Создание через классовый метод from_dict")
    data = {"speed": 70, "capacity": 30}
    transport_from_dict = Transport.from_dict(data)
    print("Создан из словаря:", transport_from_dict.get_info())

    # 3. Попытка задать недопустимые значения
    separator("3. Валидация: недопустимые значения")

    # 3.1. Невалидная скорость
    try:
        bad = Transport(speed=-10, capacity=5)
    except ValueError as e:
        print(f"Ошибка при создании (скорость): {e}")

    # 3.2. Невалидная ёмкость
    try:
        bad = Transport(speed=50, capacity=0)
    except ValueError as e:
        print(f"Ошибка при создании (ёмкость): {e}")

    # 3.3. Попытка изменить скорость на некорректное значение
    try:
        bus.speed = -100
    except ValueError as e:
        print(f"Ошибка при изменении скорости: {e}")

    # 3.4. Попытка изменить ёмкость на строку
    try:
        bus.capacity = "много"
    except TypeError as e:
        print(f"Ошибка при изменении ёмкости: {e}")

    # 4. Вызов методов без создания объекта (статический и классовый методы)
    separator("4. Вызов методов без создания объекта")
    print("Статический метод Transport.get_description():")
    print("  ", Transport.get_description())

    print("Классовый метод Transport.from_dict(...):")
    print("  ", Transport.from_dict({"speed": 55, "capacity": 100}).get_info())

    # 5. Полиморфный вызов методов для списка разных транспортных средств
    separator("5. Полиморфизм: список разных ТС")
    fleet = [
        Bus(speed=50, capacity=30, route="№7: Центр — Парк"),
        Truck(speed=70, capacity=2, load_capacity=15),
        Taxi(speed=100, capacity=4, tariff=30),
        Transport(speed=120, capacity=2),
    ]

    for vehicle in fleet:
        print(vehicle.get_info())
        print(f"  Скорость выше 80? -> {vehicle.is_speed_above(80)}")

    # Специфичные методы подклассов
    print("\nСпецифичные методы подклассов:")
    print(f"  Стоимость перевозки грузовиком на 200 км: "
          f"{fleet[1].calculate_cost(200)} руб.")
    print(f"  Стоимость поездки на такси (15 км): "
          f"{fleet[2].calculate_trip_cost(15)} руб.")


if __name__ == "__main__":
    main()
