# -*- coding: utf-8 -*-

from random import randint

# День сурка
#
# Напишите функцию one_day() которая возвращает количество кармы от 1 до 7
# и может выкидывать исключения:
# - IamGodError
# - DrunkError
# - CarCrashError
# - GluttonyError
# - DepressionError
# - SuicideError
# Одно из этих исключений выбрасывается с вероятностью 1 к 13 каждый день
#
# Функцию оберните в бесконечный цикл, выход из которого возможен только при накоплении
# кармы до уровня ENLIGHTENMENT_CARMA_LEVEL. Исключения обработать и записать в лог.
# При создании собственных исключений максимально использовать функциональность
# базовых встроенных исключений.

ENLIGHTENMENT_CARMA_LEVEL = 777


class LifeError(Exception):
    def __init__(self):
        self.message = 'Фил не отработал кармы'

    def __str__(self):
        return self.message


class IamGodError(LifeError):
    def __init__(self):
        self.message = 'Фил - БоГ!!!'

    def __str__(self):
        return self.message


class DrunkError(LifeError):
    def __init__(self):
        self.message = 'Фил напился'

    def __str__(self):
        return self.message


class CarCrashError(LifeError):
    def __init__(self):
        self.message = 'Фил разбился на машине'

    def __str__(self):
        return self.message


class GluttonyError(LifeError):
    def __init__(self):
        self.message = 'Фил обожрался'

    def __str__(self):
        return self.message


class DepressionError(LifeError):
    def __init__(self):
        self.message = 'Фил впал в депрессию'

    def __str__(self):
        return self.message


class SuicideError(LifeError):
    def __init__(self):
        self.message = 'Фил самоубился'

    def __str__(self):
        return self.message


def one_day():
    day_carma = randint(1, 7)
    life_error = randint(1, 13)
    if life_error == 13:
        life_error_number = randint(1, 6)
        if life_error_number == 1:
            raise IamGodError()
        elif life_error_number == 2:
            raise DrunkError()
        elif life_error_number == 3:
            raise CarCrashError()
        elif life_error_number == 4:
            raise GluttonyError()
        elif life_error_number == 5:
            raise DepressionError()
        elif DepressionError == 6:
            raise SuicideError()
    return day_carma


day_count = 0
total_carma = 0
with open('groundhog_day', 'w', encoding='utf8') as file:
    while True:
        try:
            day_count += 1
            total_carma += one_day()
            file.write(f'День {day_count}, Фил отработал {total_carma} кармы\n')
        except LifeError as exc:
            file.write(str(exc) + '\n')
        if total_carma >= ENLIGHTENMENT_CARMA_LEVEL:
            break
    file.write('Фил вышел из Круга!!!!\n')


# https://goo.gl/JnsDqu
