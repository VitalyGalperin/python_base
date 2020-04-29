from abc import ABCMeta, abstractmethod


class StrikeError(Exception):
    pass


class SpareError(Exception):
    pass


class FrameCountError(Exception):
    pass


class TotalScoreError(Exception):
    pass


class UnfinishedFrameWarning(Exception):
    pass


class NoSpareWarning(Exception):
    pass


class State(metaclass=ABCMeta):

    @abstractmethod
    def throw_calculation(self, string, prev_score, frame_count):
        """Расчет очков"""


class FirstThrow(State):
    def throw_calculation(self, string, prev_score, frame_count):
        if string == 'Х' or string == 'X':
            score = 20
            frame_count += 1
            game_state = FirstThrow()
            return score, game_state, frame_count
        elif string == '/':
            raise SpareError('Некорректные данные. Spare может быть только вторым броском фрейма')
        elif string == '-':
            score = 0
        elif string.isdigit():
            score = int(string)
        else:
            raise ValueError(
                f"Некорректный символ в данных {string}. Допустимо использовать Цифры, \"-\", \"/\", \"Х\"")
        frame_count += 1
        game_state = SecondThrow()
        return score, game_state, frame_count


class SecondThrow(State):
    def throw_calculation(self, string, prev_score, frame_count):
        if string == 'Х' or string == 'X':
            raise StrikeError('Некорректные данные. Strike может быть только первым броском фрейма')
        elif string == '/':
            score = 15 - prev_score
        elif string == '-':
            score = 0
        elif string.isdigit():
            score = int(string)
            if prev_score + score > 10:
                raise TotalScoreError('Некорректные данные. Сумма двух бросков не может превышать 10 очков')
            if prev_score + score == 10:
                raise NoSpareWarning(f'Некорректные данные. Записано {prev_score}{score}, ожидается {prev_score}/')
        else:
            raise ValueError(
                f"Некорректный символ в данных {string}. Допустимо использовать Цифры, \"-\", \"/\", \"Х\"")
        game_state = FirstThrow()
        return score, game_state, frame_count


def get_score(game_result):
    game_score = prev_score = frame_count = 0
    game_state = FirstThrow()
    for string in game_result:
        score, game_state, frame_count = game_state.throw_calculation(string, prev_score, frame_count)
        game_score += score
        prev_score = score
        if frame_count > 10:
            raise FrameCountError('Игра состоит более чем из 10 фреймов')
    if isinstance(game_state, SecondThrow):
        raise UnfinishedFrameWarning('Игра закончена на недоигранном фрейме')
    # print(f'Количество очков для результатов: {game_result}  -  {game_score}, количество фреймов {frame_count} ')
    # print('===============================================================================')
    return game_score

