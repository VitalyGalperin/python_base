from bowling import get_score


if __name__ == '__main__':
    game_result = 'Х4/34-4'
    game_score = get_score(game_result)

    game_result = '15-/Х1/42'
    game_score = get_score(game_result)

    game_result = '14/FA457X'
    game_score = get_score(game_result)