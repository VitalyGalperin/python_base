import random


def make_number():
    game_number = [0, 0, 0, 0]
    while game_number[0] == 0:
        game_number = random.sample(range(10), 4)
    return game_number


def check_number(get_number):
    if not get_number.isdigit() or len(get_number) != 4:
        return False
    else:
        for i, digit in enumerate(get_number, 0):
            if get_number.count(digit) > 1:
                return False
        return True


def compare_numbers(game_number, get_number):
    bulls = 0
    cows = 0
    for i, digit in enumerate(get_number, 0):
        if int(digit) == game_number[i]:
            bulls += 1
        elif game_number.count(int(digit)) == 1:
            cows += 1
    return bulls, cows
