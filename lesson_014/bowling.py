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
        return 'Некорректные данные. Сумма двуX бросков не может превышать 10 очков'


class BadStringError(Exception):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return f'Некорректный символ в данныX {self.string}. Допустимо использовать Цифры, \"-\", \"/\", \"X\"'


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


class GameHandler:
    STRIKE_SYMBOL = 'X'
    SPARE_SYMBOL = '/'
    MISS_SYMBOL = '-'

    def __init__(self):
        self.game_result = ''
        self.game_score = self.bonus = self.prev_score = self.string_count = self.frame_count = 0
        self.first_throw = True
        self.international = True

    class State(metaclass=ABCMeta):

        @abstractmethod
        def throw_calculation(self):
            """Расчет очков"""

    def calc_score(self, game_result, international):
        self.game_result = game_result
        self.international = international
        for string in game_result:
            self.string_count += 1
            self.game_score += self.bonus
            self.bonus = 0
            if string == self.MISS_SYMBOL:
                score = 0
            elif string.isdigit():
                score = int(string)
                if not self.first_throw and self.prev_score + score > 10:
                    raise TotalScoreError()
                if not self.first_throw and self.prev_score + score == 10:
                    raise NoSpareWarning(self.prev_score, score)
            elif string == self.STRIKE_SYMBOL:
                if self.first_throw:
                    if self.international:
                        score = self.strike_intern()
                    else:
                        score = 20
                else:
                    raise StrikeError()
            elif string == self.SPARE_SYMBOL:
                if not self.first_throw:
                    if self.international:
                        score = self.spare_intern()
                    else:
                        score = 15 - self.prev_score
                else:
                    raise SpareError()
            else:
                raise BadStringError(string)
            if self.first_throw and string != self.STRIKE_SYMBOL:
                self.first_throw = False
            else:
                self.first_throw = True
                self.frame_count += 1
            self.game_score += score
            self.prev_score = score
            if self.frame_count > 10:
                raise FrameCountError()
        if not self.first_throw:
            raise UnfinishedFrameWarning()
        # print(f'Количество очков для результатов: {game_result} - {self.game_score}, количество фреймов {
        # self.frame_count} ')
        # print('===============================================================================')
        return self.game_score

    def strike_intern(self):
        score = 10
        try:
            if self.game_result[self.string_count + 1] == self.SPARE_SYMBOL:
                self.bonus = 10
            else:
                for i, bonus_string in enumerate(self.game_result[self.string_count: self.string_count + 2]):
                    if bonus_string == self.STRIKE_SYMBOL:
                        self.bonus += 10
                    elif bonus_string.isdigit():
                        self.bonus += int(bonus_string)
        except IndexError:
            self.bonus = 0
        return score

    def spare_intern(self):
        score = 10 - self.prev_score
        try:
            bonus_string = self.game_result[self.string_count]
            if bonus_string == self.STRIKE_SYMBOL:
                self.bonus = 10
            elif bonus_string.isdigit():
                self.bonus = int(bonus_string)
        except IndexError:
            self.bonus = 0
        return score


def get_score(game_result, international=True):
    calc = GameHandler()
    return calc.calc_score(game_result, international)


class ScoreTests(unittest.TestCase):

    def test_short_game(self):
        self.assertEqual(get_score('X4/34-4', international=False), 46)

    def test_normal_game(self):
        self.assertEqual(get_score('X4/34-452X-/729---', international=False), 106)

    def test_short_game_international(self):
        self.assertEqual(get_score('XXX347/21'), 92)

    def test_normal_game_international(self):
        self.assertEqual(get_score('XXX347/21XXX5/'), 177)

    def test_BadStringError(self):
        self.assertRaises(BadStringError, get_score, '141/FA457X')

    def test_FrameCountError(self):
        self.assertRaises(FrameCountError, get_score, 'XXXXXXXXXXXXX')

    def test_StrikeError(self):
        self.assertRaises(StrikeError, get_score, '1XXXXXXXXXX')

    def test_SpareError(self):
        self.assertRaises(SpareError, get_score, 'XXXXXXXXX/1')

    def test_TotalScoreError(self):
        self.assertRaises(TotalScoreError, get_score, 'XXXXXXXXX56')

    def test_NoSpareWarning(self):
        self.assertRaises(NoSpareWarning, get_score, 'XXXXXXXXX55')

    def test_UnfinishedFrameWarning(self):
        self.assertRaises(UnfinishedFrameWarning, get_score, 'XXXXXXXXX1')


if __name__ == '__main__':
    unittest.main()


