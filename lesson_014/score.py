from bowling import get_score

if __name__ == '__main__':
    game_result = 'Х4/34-4'
    game_score = get_score(game_result)
    game_result = '15-/Х1/42'
    game_score = get_score(game_result)
    game_result = 'Х4/34-452Х-/729---'
    game_score = get_score(game_result)
    game_result = '141/FA457X'
    game_score = get_score(game_result)
    game_result = 'ХХХХХХХХХ'
    game_score = get_score(game_result)
    game_result = 'ХХХХХХХХХХХ'
    game_score = get_score(game_result)
    game_result = 'ХХХХХХХХХ1'
    game_score = get_score(game_result)
    game_result = 'ХХХХХХХХХ55'
    game_score = get_score(game_result)
    game_result = 'ХХХХХХХХХ1Х'
    game_score = get_score(game_result)
    game_result = 'ХХХХХХХХХ/1'
    game_score = get_score(game_result)

    # python 01_score.py --result Х4/34-4