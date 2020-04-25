from bowling import get_score
import bowling

if __name__ == '__main__':

    game_score = get_score('Х4/34-4')
    game_score = get_score('15-/Х1/42')
    game_score = get_score('Х4/34-452Х-/729-1-')
    game_score = get_score('ХХХХХХХХХ')
    try:
        game_score = get_score('141/FA457X')
    except ValueError as exc:
        print(exc)

    try:
        game_score = get_score('ХХХХХХХХХ111')
    except bowling.FrameCountError as exc:
        print(exc)

    try:
        game_score = get_score('1ХХХХХХХХХХ')
    except bowling.StrikeError as exc:
        print(exc)

    try:
        game_score = get_score('ХХХХХХХХХ/1')
    except bowling.SpareError as exc:
        print(exc)

    try:
        game_score = get_score('ХХХХХХХХХ56')
    except bowling.TotalScoreError as exc:
        print(exc)

    try:
        game_score = get_score('ХХХХХХХХХ1')
    except bowling.UnfinishedFrameWarning as exc:
        print(exc)

    # python 01_score.py --result Х4/34-4
