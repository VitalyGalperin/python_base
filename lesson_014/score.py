from bowling import get_score
import bowling as bowling

# from bowling_V1 import get_score
# import bowling_V1 as bowling

if __name__ == '__main__':

    game_score = get_score('X4/34', international=True)
    game_score = get_score('XXX347/21', international=True)
    game_score = get_score('X4/34', international=False)
    game_score = get_score('XXX347/21', international=False)
    game_score = get_score('XXX347/21XXX5/')
    game_score = get_score('X4/34-4')
    game_score = get_score('15-/X1/42')
    game_score = get_score('X4/34-452X-/729-1-')
    game_score = get_score('XXXXXXXXX')

    try:
        game_score = get_score('141/FA457X')
    except  bowling.BadStringError as exc:
        print(exc)

    try:
        game_score = get_score('XXXXXXXXX111')
    except bowling.FrameCountError as exc:
        print(exc)

    try:
        game_score = get_score('1XXXXXXXXXX')
    except bowling.StrikeError as exc:
        print(exc)

    try:
        game_score = get_score('XXXXXXXXX/1')
    except bowling.SpareError as exc:
        print(exc)

    try:
        game_score = get_score('XXXXXXXXX56')
    except bowling.TotalScoreError as exc:
        print(exc)

    try:
        game_score = get_score('XXXXXXXXX55')
    except bowling.NoSpareWarning as exc:
        print(exc)

    try:
        game_score = get_score('XXXXXXXXX1')
    except bowling.UnfinishedFrameWarning as exc:
        print(exc)

    # python 01_score.py --result X4/34-4
