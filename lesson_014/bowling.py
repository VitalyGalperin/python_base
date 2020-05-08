from abc import ABCMeta, abstractmethod


class StrikeError(Exception):
    def __str__(self):
        return 'Некорректные данные. Strike может быть только первым броском фрейма'


class SpareError(Exception):
    def __str__(self):
        return 'Некорректные данные. Spare может быть только вторым броском фрейма'


class FrameCountError(Exception):
    def __str__(self):
        return 'Игра состоит более чем из 10 фреймов'


class TotalScoreError(Exception):
    def __str__(self):
        return 'Некорректные данные. Сумма двух бросков не может превышать 10 очков'


class BadStringError(Exception):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return f'Некорректный символ в данных {self.string}. Допустимо использовать Цифры, \"-\", \"/\", \"Х\"'


class UnfinishedFrameWarning(Exception):

    def __str__(self):
        return 'Игра закончена на недоигранном фрейме'


class NoSpareWarning(Exception):
    def __init__(self, prev_score, score):
        super().__init__()
        self.prev_score = prev_score
        self.score = score

    def __str__(self):
        return f'Некорректные данные. Записано {self.prev_score}{self.score}, ожидается {self.prev_score}/'


class State(metaclass=ABCMeta):

    @abstractmethod
    def throw_calculation(self, string, prev_score, frame_count, game_result, string_count, international):
        """Расчет очков"""


class FirstThrow(State):
    def throw_calculation(self, string, prev_score, frame_count, game_result, string_count, international):
        bonus = 0
        if string == 'Х' or string == 'X':
            if international:
                score = 10
                try:
                    if game_result[string_count + 1] == '/':
                        bonus = 10
                    else:
                        for i, bonus_string in enumerate(game_result[string_count: string_count + 2]):
                            # print(bonus_string, type(bonus_string), string_count, i)
                            if bonus_string == 'Х' or bonus_string == 'X':
                                bonus += 10
                            elif bonus_string.isdigit():
                                bonus += int(bonus_string)
                except IndexError:
                    bonus = 0
            else:
                score = 20
            frame_count += 1
            game_state = FirstThrow()
            return score, game_state, frame_count, bonus
        elif string == '/':
            raise SpareError()
        elif string == '-':
            score = 0
        elif string.isdigit():
            score = int(string)
        else:
            raise BadStringError(string)
        frame_count += 1
        game_state = SecondThrow()
        return score, game_state, frame_count, bonus


class SecondThrow(State):
    def throw_calculation(self, string, prev_score, frame_count, game_result, string_count, international):
        bonus = 0
        if string == 'Х' or string == 'X':
            raise StrikeError()
        elif string == '/':
            if international:
                score = 10 - prev_score
                try:
                    bonus_string = game_result[string_count]
                    if bonus_string == 'Х' or bonus_string == 'X':
                        bonus = 10
                    elif bonus_string.isdigit():
                        bonus = int(bonus_string)
                except IndexError:
                    bonus = 0
            else:
                score = 15 - prev_score
        elif string == '-':
            score = 0
        elif string.isdigit():
            score = int(string)
            if prev_score + score > 10:
                raise TotalScoreError()
            if prev_score + score == 10:
                raise NoSpareWarning(prev_score, score)
        else:
            raise BadStringError(string)
        game_state = FirstThrow()
        return score, game_state, frame_count, bonus


def get_score(game_result, international=False):
    game_score = prev_score = frame_count = string_count = bonus = 0
    game_state = FirstThrow()
    for string in game_result:
        string_count += 1
        game_score += bonus
        score, game_state, frame_count, bonus = game_state.throw_calculation(string, prev_score, frame_count,
                                                                             game_result, string_count, international)
        game_score += score
        prev_score = score
        # print(string_count, string, 'score=', score, '+' , bonus, game_score)
        if frame_count > 10:
            raise FrameCountError()
    if isinstance(game_state, SecondThrow):
        raise UnfinishedFrameWarning()
    print(f'Количество очков для результатов: {game_result}  -  {game_score}, количество фреймов {frame_count} ')
    print('===============================================================================')
    return game_score


