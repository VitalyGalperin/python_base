import random


def make_number():
    game_number = ''
    game_number += str(random.randint(1, 9))
    for i in range(0, 3):
        while True:
            new_digit = str(random.randint(0, 9))
            if game_number.find(new_digit) == -1:
                game_number += new_digit
                break
    return game_number


def check_number(get_number, game_number):
    if not get_number.isdigit() or len(get_number) != 4:
        return False
    bulls = 0
    cows = 0
    for i, digit in enumerate(game_number, 0):
        if digit == get_number[i]:
            bulls += 1
        elif get_number.find(digit) != -1:
            cows += 1
    check_result = dict(bulls=bulls, cows=cows)
    return check_result
