#!/usr/bin/env python3
# -*- coding: utf-8 -*-

SEPARATOR_WIDTH = 20
SPEED_THRESHOLD = 80
COST_BASE_RATE = 50
COST_PER_TON = 10
TRIP_DISTANCE = 200
TAXI_TRIP_DISTANCE = 15


class Transport:
    """ Базовый класс транспортного средства."""

    def __init__(self, speed, capacity):
        """ Инициализирует транспортное средство.

        Args:
            speed (int | float): Скорость в км/ч.
            capacity (int | float): Вместимость.

        Returns:
            None
        """
        self.speed = speed
        self.capacity = capacity

    @property
    def speed(self):
        """ Возвращает скорость.

        Returns:
            int | float: Текущая скорость в км/ч.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """ Устанавливает скорость с валидацией.

        Args:
            value (int | float): Новая скорость в км/ч.

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Скорость должна быть числом")
        if value <= 0:
            raise ValueError("Скорость должна быть положительной")
        self._speed = value

    @property
    def capacity(self):
        """ Возвращает вместимость.

        Returns:
            int | float: Текущая вместимость.
        """
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        """ Устанавливает вместимость с валидацией.

        Args:
            value (int | float): Новая вместимость.

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Ёмкость должна быть числом")
        if value <= 0:
            raise ValueError("Ёмкость должна быть положительной")
        self._capacity = value

    def __str__(self):
        """ Строковое представление ТС.

        Returns:
            str: Описание со скоростью и вместимостью.
        """
        return (f"Transport: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity}")

    def is_speed_above(self, threshold):
        """ Проверяет, превышает ли скорость порог.

        Args:
            threshold (int | float): Пороговое значение в км/ч.

        Returns:
            bool: True, если скорость строго больше порога.
        """
        return self.speed > threshold

    @classmethod
    def from_dict(cls, data):
        """ Создаёт объект из словаря.

        Args:
            data (dict): Словарь с ключами 'speed' и 'capacity'.

        Returns:
            Transport: Новый экземпляр класса cls.
        """
        if type(data) != dict:
            raise TypeError("Ожидается словарь")
        return cls(data['speed'], data['capacity'])

    @staticmethod
    def get_description():
        """ Возвращает описание класса.

        Returns:
            str: Текстовое описание базового класса.
        """
        return "Transport — базовый класс для всех транспортных средств."


class Bus(Transport):
    """ Автобус с маршрутом."""

    def __init__(self, speed, capacity, route):
        """ Инициализирует автобус.

        Args:
            speed (int | float): Скорость в км/ч.
            capacity (int | float): Вместимость.
            route (str): Название маршрута.

        Returns:
            None
        """
        super().__init__(speed, capacity)
        self.route = route

    @property
    def route(self):
        """ Возвращает маршрут.

        Returns:
            str: Название маршрута.
        """
        return self._route

    @route.setter
    def route(self, value):
        """ Устанавливает маршрут с валидацией.

        Args:
            value (str): Непустая строка с названием маршрута.

        Returns:
            None
        """
        if type(value) != str or not value.strip():
            raise ValueError("Маршрут должен быть непустой строкой")
        self._route = value

    def __str__(self):
        """ Строковое представление автобуса.

        Returns:
            str: Описание со скоростью, вместимостью и маршрутом.
        """
        return (f"Bus: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity} чел., "
                f"маршрут = '{self.route}'")


class Truck(Transport):
    """ Грузовик с грузоподъёмностью."""

    def __init__(self, speed, capacity, load_capacity):
        """ Инициализирует грузовик.

        Args:
            speed (int | float): Скорость в км/ч.
            capacity (int | float): Вместимость.
            load_capacity (int | float): Грузоподъёмность в тоннах.

        Returns:
            None
        """
        super().__init__(speed, capacity)
        self.load_capacity = load_capacity

    @property
    def load_capacity(self):
        """ Возвращает грузоподъёмность.

        Returns:
            int | float: Грузоподъёмность в тоннах.
        """
        return self._load_capacity

    @load_capacity.setter
    def load_capacity(self, value):
        """ Устанавливает грузоподъёмность с валидацией.

        Args:
            value (int | float): Новая грузоподъёмность в тоннах.

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Грузоподъёмность должна быть числом")
        if value <= 0:
            raise ValueError("Грузоподъёмность должна быть положительной")
        self._load_capacity = value

    def __str__(self):
        """ Строковое представление грузовика.

        Returns:
            str: Описание со скоростью, вместимостью и грузоподъёмностью.
        """
        return (f"Truck: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity}, "
                f"грузоподъёмность = {self.load_capacity} т")

    def calculate_cost(self, distance):
        """ Рассчитывает стоимость перевозки.

        Args:
            distance (int | float): Расстояние в км.

        Returns:
            int | float: Стоимость в рублях.
        """
        return distance * (COST_BASE_RATE + COST_PER_TON * self.load_capacity)


class Taxi(Transport):
    """ Такси с тарифом."""

    def __init__(self, speed, capacity, tariff):
        """ Инициализирует такси.

        Args:
            speed (int | float): Скорость в км/ч.
            capacity (int | float): Вместимость.
            tariff (int | float): Тариф в рублях за км.

        Returns:
            None
        """
        super().__init__(speed, capacity)
        self.tariff = tariff

    @property
    def tariff(self):
        """ Возвращает тариф.

        Returns:
            int | float: Тариф в рублях за км.
        """
        return self._tariff

    @tariff.setter
    def tariff(self, value):
        """ Устанавливает тариф с валидацией.

        Args:
            value (int | float): Новый тариф в рублях за км.

        Returns:
            None
        """
        if type(value) not in (int, float):
            raise TypeError("Тариф должен быть числом")
        if value <= 0:
            raise ValueError("Тариф должен быть положительным")
        self._tariff = value

    def __str__(self):
        """ Строковое представление такси.

        Returns:
            str: Описание со скоростью, вместимостью и тарифом.
        """
        return (f"Taxi: скорость = {self.speed} км/ч, "
                f"вместимость = {self.capacity} чел., "
                f"тариф = {self.tariff} руб./км")

    def calculate_trip_cost(self, distance):
        """ Рассчитывает стоимость поездки.

        Args:
            distance (int | float): Расстояние в км.

        Returns:
            int | float: Стоимость в рублях.
        """
        return distance * self.tariff


def separator(title):
    """ Печатает заголовок-разделитель.

    Args:
        title (str): Текст заголовка.

    Returns:
        None
    """
    print(f"\n{'=' * SEPARATOR_WIDTH} {title} {'=' * SEPARATOR_WIDTH}")


if __name__ == "__main__":

    separator("1. Создание через конструктор")
    bus = Bus(speed=60, capacity=40, route="№15: Вокзал — Аэропорт")
    truck = Truck(speed=80, capacity=2, load_capacity=10)
    taxi = Taxi(speed=90, capacity=4, tariff=25)

    for t in (bus, truck, taxi):
        print(t)

    separator("2. Создание через from_dict")
    data = {"speed": 70, "capacity": 30}
    print("Создан из словаря:", Transport.from_dict(data))

    separator("3. Валидация")
    try:
        Transport(speed=-10, capacity=5)
    except ValueError as e:
        print(f"Ошибка (скорость): {e}")

    try:
        Transport(speed=50, capacity=0)
    except ValueError as e:
        print(f"Ошибка (ёмкость): {e}")

    try:
        bus.speed = -100
    except ValueError as e:
        print(f"Ошибка скорости: {e}")

    try:
        bus.capacity = "много"
    except TypeError as e:
        print(f"Ошибка ёмкости: {e}")

    separator("4. Методы без объекта")
    print("  ", Transport.get_description())
    print("  ", Transport.from_dict({"speed": 55, "capacity": 100}))

    separator("5. Полиморфизм")
    fleet = [
        Bus(speed=50, capacity=30, route="№7: Центр — Парк"),
        Truck(speed=70, capacity=2, load_capacity=15),
        Taxi(speed=100, capacity=4, tariff=30),
        Transport(speed=120, capacity=2),
    ]

    for vehicle in fleet:
        print(vehicle)
        print(f"  Скорость выше {SPEED_THRESHOLD}? -> {vehicle.is_speed_above(SPEED_THRESHOLD)}")

    print(f"\n  Перевозка грузовиком ({TRIP_DISTANCE} км): "
          f"{fleet[1].calculate_cost(TRIP_DISTANCE)} руб.")
    print(f"  Поездка на такси ({TAXI_TRIP_DISTANCE} км): "
          f"{fleet[2].calculate_trip_cost(TAXI_TRIP_DISTANCE)} руб.")
    
