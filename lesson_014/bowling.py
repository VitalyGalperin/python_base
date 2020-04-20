# from abc import ABCMeta, abstractmethod
#
#
# class State(metaclass=ABCMeta):
#
#     @abstractmethod
#     def first_throw(self):
#         """первый бросок"""
#
#     @abstractmethod
#     def second_throw(self):
#         """первый бросок"""


def get_score(game_result):
    score = 0
    prev_step_score = 0
    for string in game_result:
        print(string)
        # try:
        if string == 'Х':
            score += 20
        elif string == '/':
            score -= prev_step_score
            score += 15
        elif string == '-':
            score += 0
        elif string.isdigit:
            score += int(string)
            prev_step_score = int(string)
        else:
            print(f'Некорректные данные. символ {string}  не может быть использован')
        print(score, '!')
        # except ValueError as err:
        #     print(f'Некорректные данные. символ {string}  не может быть использован')
    return score


game_result = 'Х4/34-4'
game_score = get_score(game_result)
print(game_score)