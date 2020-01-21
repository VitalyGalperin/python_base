# -*- coding: utf-8 -*-

# (цикл while)

# даны целые положительные числа a и b (a > b)
# Определить результат целочисленного деления a на b, с помощью цикла while,
# __НЕ__ используя ни одной из операций деления: ни деления с плавающей точкой /, ни целочисленного деления //
# и взятия остатка %
# Формат вывода:
#   Целочисленное деление ХХХ на YYY дает ZZZ

a, b = 179, 37
dividend, divider = a, b
division_count = 0
while dividend > divider:
    dividend = dividend - divider
    division_count += 1

print('Целочисленное деление ', a, ' на ', b, ' дает ', division_count, ' остаток равен ', dividend)
