from abc import ABCMeta, abstractmethod


class StrikeError(Exception):
    pass


class SpareError(Exception):
    pass


class FrameCountError(Exception):
    pass


class State(metaclass=ABCMeta):

    @abstractmethod
    def throw_calculation(self, string, prev_score, frame_count):
        """Расчет очков"""


class FirstThrow(State):
    def throw_calculation(self, string, prev_score, frame_count):
        if string == 'Х':
            score = 20
            frame_count += 1
            game_state = FirstThrow()
            return score, game_state, frame_count
        elif string == '/':
            raise SpareError
        elif string == '-':
            score = 0
        elif string.isdigit:
            score = int(string)
        else:
            raise ValueError
        game_state = SecondThrow()
        return score, game_state, frame_count


class SecondThrow(State):
    def throw_calculation(self, string, prev_score, frame_count):
        if string == 'Х':
            raise StrikeError
        elif string == '/':
            score = 15 - prev_score
        elif string == '-':
            score = 0
        elif string.isdigit:
            score = int(string)
        else:
            raise ValueError
        frame_count += 1
        game_state = FirstThrow()
        return score, game_state, frame_count


def get_score(game_result):
    game_score = prev_score = frame_count = 0
    game_state = FirstThrow()
    try:
        for string in game_result:
            score, game_state, frame_count = game_state.throw_calculation(string, prev_score, frame_count)
            game_score += score
            prev_score = score
            if frame_count > 10:
                raise FrameCountError
    except ValueError:  # TODO если вы здесь перехватываете все исключения,
        # как вы их хотите протестить? - в библиотеке это не нужно делать
        print('Некорректный символ в данных. Допустимо использовать Цифры, "-". "/", "Х"')
        game_score = frame_count = 0
    except StrikeError:
        print('Некорректные данные. Strike может быть только первым броском фрейма')
        game_score = frame_count = 0
    except SpareError:
        print('Некорректные данные. Spare может быть только вторым броском фрейма')
        game_score = frame_count = 0
    except FrameCountError:
        print('Игра состоит более чем из 10 фреймов')
    print(f'Количество очков для результатов: {game_result}  -  {game_score}, количество фреймов {frame_count} ')
    print('===============================================================================')
    return game_score

# TODO принимаются след не валидные строки
"Х"*9 + '1'
"Х"*9 + '56'
"Х"*9 + '111'

