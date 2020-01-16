#!/usr/bin/env python
# -*- coding: utf-8 -*-

# есть список животных в зоопарке

zoo = ['lion', 'kangaroo', 'elephant', 'monkey', ]

# посадите медведя (bear) между львом и кенгуру
#  и выведите список на консоль

zoo.insert (1,'bear')
print(zoo)

# добавьте птиц из списка birds в последние клетки зоопарка
birds = ['rooster', 'ostrich', 'lark', ]
#  и выведите список на консоль
# TODO Необходимо использовать метод extend
zoo.append(birds[0])
zoo.append(birds[1])
zoo.append(birds[2])
print(zoo)

# уберите слона
#  и выведите список на консоль
zoo.remove('elephant')
print(zoo)

# выведите на консоль в какой клетке сидит лев (lion) и жаворонок (lark).
# Номера при выводе должны быть понятны простому человеку, не программисту.

print('Лев находится в клетке №', zoo.index('lion')+1)
print('Жаворонок находится в клетке №', zoo.index('lark')+1)
