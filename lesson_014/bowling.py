def get_score(game_result):
    score = 0
    prev_step_score = 0
    try:
        for string in game_result:
            if string == 'Х':
                score += 20
            elif string == '/':
                score -= prev_step_score
                score += 15
            elif string == '-':
                score += 0
                prev_step_score = 0
            elif string.isdigit:
                score += int(string)
                prev_step_score = int(string)
            else:
                raise ValueError
    except ValueError:
        print(f'Некорректные данные')
        score = 0
    print(f'Количество очков для результатов: {game_result}  -  {score}')
    return score





