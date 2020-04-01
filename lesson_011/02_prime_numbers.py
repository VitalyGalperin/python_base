# -*- coding: utf-8 -*-


# Есть функция генерации списка простых чисел
from functools import reduce


def get_prime_numbers(n):
    prime_numbers = []
    for number in range(2, n + 1):
        for prime in prime_numbers:
            if number % prime == 0:
                break
        else:
            prime_numbers.append(number)
    return prime_numbers


# Часть 1
# На основе алгоритма get_prime_numbers создать класс итерируемых обьектов,
# который выдает последовательность простых чисел до n
#
# Распечатать все простые числа до 10000 в столбик


class PrimeNumbers:

    def __init__(self, n):
        self.number, self.n = 1, n
        self.prime_numbers = []

    def __iter__(self):
        self.number = 1
        return self

    def __next__(self):
        self.number += 1
        for i in range(self.number, self.n + 1):
            for prime in self.prime_numbers:
                if i % prime == 0:
                    break
            else:
                self.prime_numbers.append(i)
                self.number = i
                return self.number
        raise StopIteration()


prime_number_iterator = PrimeNumbers(n=10000)
for number in prime_number_iterator:
    print(number)


# Часть 2
# Теперь нужно создать генератор, который выдает последовательность простых чисел до n
# Распечатать все простые числа до 10000 в столбик


def prime_numbers_generator(n):
    prime_numbers = []
    number = 2
    for i in range(number, n + 1):
        if i >= n:
            return
        for prime in prime_numbers:
            if i % prime == 0:
                break
        else:
            prime_numbers.append(i)
            number = i
            yield number


for number in prime_numbers_generator(n=10000):
    print(number)


# Часть 3
# Написать несколько функций-фильтров, которые выдает True, если число:
# 1) "счастливое" в обыденном пониманиии - сумма первых цифр равна сумме последних
#       Если число имеет нечетное число цифр (например 727 или 92083),
#       то для вычисления "счастливости" брать равное количество цифр с начала и конца:
#           727 -> 7(2)7 -> 7 == 7 -> True
#           92083 -> 92(0)83 -> 9+2 == 8+3 -> True
# 2) "палиндромное" - одинаково читающееся в обоих направлениях. Например 723327 и 101
# 3) придумать свою (https://clck.ru/GB5Fc в помощь)
#
# Подумать, как можно применить функции-фильтры к полученной последовательности простых чисел
# для получения, к примеру: простых счастливых чисел, простых палиндромных чисел,
# простых счастливых палиндромных чисел и так далее. Придумать не менее 2х способов.
#
# Подсказка: возможно, нужно будет добавить параметр в итератор/генератор.


def numbers_generator(n, happy=False, palindrome=False, order=False):
    prime_numbers = []
    number = 2
    for i in range(number, n + 1):
        if i >= n:
            return
        for prime in prime_numbers:
            if i % prime == 0:
                break
        else:
            prime_numbers.append(i)
            number = i
            if happy and not check_happy(number, happy):
                continue
            if palindrome and not check_palindrome(number, palindrome):
                continue
            if order and not check_order(number, order):
                continue
            yield number


def check_happy(number, happy):
    number = str(number)
    half_len = len(number) // 2
    return sum(map(int, number[:half_len])) == sum(map(int, number[len(number) - half_len::]))


def check_palindrome(number, palindrome):
    return str(number) == str(number)[::-1]


# В числе есть как цифры, идущие продяд в естественном порядке (23, 56, 89)
def check_order(number, order):
    number = str(number)
    for char in number[:len(number) - 1]:
        if int(char) + 1 == int(number[number.find(char) + 1]):
            return True
    return False


for number in numbers_generator(n=14000, happy=True, palindrome=False, order=False):
    print(number, ' Счастливое число')

for number in numbers_generator(n=14000, happy=False, palindrome=True, order=False):
    print(number, ' Число - полиндром')

for number in numbers_generator(n=14000, happy=True, palindrome=True, order=False):
    print(number, ' Счастливое Число - полиндром')

for number in numbers_generator(n=10000, happy=False, palindrome=False, order=True):
    print(number, 'есть последовательные цифры в числе')
