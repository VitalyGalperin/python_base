from abc import ABCMeta, abstractmethod
import unittest


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


def get_score(game_result, international=True):
    game_score = prev_score = frame_count = string_count = bonus = 0
    game_state = FirstThrow()
    for string in game_result:
        string_count += 1
        game_score += bonus
        score, game_state, frame_count, bonus = game_state.throw_calculation(string, prev_score, frame_count,
                                                                             game_result, string_count, international)
        game_score += score
        prev_score = score
        if frame_count > 10:
            raise FrameCountError()
    if isinstance(game_state, SecondThrow):
        raise UnfinishedFrameWarning()
    # print(f'Количество очков для результатов: {game_result}  -  {game_score}, количество фреймов {frame_count} ')
    # print('===============================================================================')
    return game_score


class ScoreTests(unittest.TestCase):

    def test_short_game(self):
        self.assertEqual(get_score('Х4/34-4', international=False), 46)

    def test_normal_game(self):
        self.assertEqual(get_score('Х4/34-452Х-/729---', international=False), 106)

    def test_short_game_international(self):
        self.assertEqual(get_score('ХXX347/21'), 92)

    def test_normal_game_international(self):
        self.assertEqual(get_score('ХXX347/21XXX5/'), 177)

    def test_BadStringError(self):
        self.assertRaises(BadStringError, get_score, '141/FA457X')

    def test_FrameCountError(self):
        self.assertRaises(FrameCountError, get_score, 'ХХХХХХХХХ111')

    def test_StrikeError(self):
        self.assertRaises(StrikeError, get_score, '1ХХХХХХХХХХ')

    def test_SpareError(self):
        self.assertRaises(SpareError, get_score, 'ХХХХХХХХХ/1')

    def test_TotalScoreError(self):
        self.assertRaises(TotalScoreError, get_score, 'ХХХХХХХХХ56')

    def test_NoSpareWarning(self):
        self.assertRaises(NoSpareWarning, get_score, 'ХХХХХХХХХ55')

    def test_UnfinishedFrameWarning(self):
        self.assertRaises(UnfinishedFrameWarning, get_score, 'ХХХХХХХХХ1')


if __name__ == '__main__':
    unittest.main()
