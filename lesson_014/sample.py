from abc import ABC, abstractmethod
from contextlib import contextmanager
import unittest


class UnexpectedSymbol(Exception):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    def __str__(self):
        return "Unexpected symbol {}".format(self.symbol)


class ScoreOverflow(Exception):
    def __str__(self):
        return "Sum of score in one frame is more than 10"


class InvalidFramesNumber(Exception):
    def __str__(self):
        return "Invalid frames number"


class InvalidThrowsNumber(Exception):
    def __str__(self):
        return "Invalid throws number"


class FrameManager:

    STRIKE_SYMBOL = 'X'
    SPARE_SYMBOL = '/'
    MISS_SYMBOL = '-'

    class Throw(ABC):
        def process(self, symbol):
            if symbol == FrameManager.STRIKE_SYMBOL:
                return self.strike()
            elif symbol == FrameManager.SPARE_SYMBOL:
                return self.spare()
            elif symbol == FrameManager.MISS_SYMBOL:
                return 0
            elif '1' <= symbol <= '9':
                return int(symbol)
            else:
                raise UnexpectedSymbol(symbol)

        @abstractmethod
        def strike(self):
            pass

        @abstractmethod
        def spare(self):
            pass

    class FirstThrow(Throw):
        def strike(self):
            return 20

        def spare(self):
            raise UnexpectedSymbol(FrameManager.SPARE_SYMBOL)

    class SecondThrow(Throw):
        def strike(self):
            raise UnexpectedSymbol(FrameManager.STRIKE_SYMBOL)

        def spare(self):
            return 15

    FIRST_THROW = FirstThrow()
    SECOND_THROW = SecondThrow()

    def __init__(self):
        self.current_throw = self.FIRST_THROW
        self.total_frames = 0
        self.prev_throw_score = 0
        self.total_score = 0

    def process(self, symbol):
        is_first_throw = self.current_throw is self.FIRST_THROW
        self.total_frames += is_first_throw

        score = self.current_throw.process(symbol)
        self.total_score += score

        if not is_first_throw:
            if symbol == self.SPARE_SYMBOL:
                self.total_score -= self.prev_throw_score
            elif score + self.prev_throw_score >= 10:
                raise ScoreOverflow()

            self.current_throw = self.FIRST_THROW
        elif symbol != self.STRIKE_SYMBOL:
            self.current_throw = self.SECOND_THROW

        self.prev_throw_score = score

    def game_end(self, total_frames):
        if total_frames is not None and total_frames != self.total_frames:
            raise InvalidFramesNumber()

        if self.current_throw is not self.FIRST_THROW:
            raise InvalidThrowsNumber()


@contextmanager
def game_handler(total_frames=None):
    frame_manager = FrameManager()
    yield frame_manager
    frame_manager.game_end(total_frames)


def process_game(input_data, total_frames=None):
    with game_handler(total_frames) as frame_manager:
        for symbol in input_data.upper():
            frame_manager.process(symbol)

        return frame_manager.total_score


class TestBowling(unittest.TestCase):
    def test_bad_symbols(self):
        with self.assertRaises(UnexpectedSymbol):
            process_game('XXXXXXXXXXXXXa')

        with self.assertRaises(UnexpectedSymbol):
            process_game('fffff')

    def test_unexpected_symbol(self):
        with self.assertRaises(UnexpectedSymbol):
            process_game('123X')

        with self.assertRaises(UnexpectedSymbol):
            process_game('XX/', 10)

    def test_score_overflow(self):
        with self.assertRaises(ScoreOverflow):
            process_game('99', 1)

    def test_invalid_number(self):
        with self.assertRaises(InvalidFramesNumber):
            process_game('XXX', 4)

        with self.assertRaises(InvalidThrowsNumber):
            process_game('X-/118', 4)

    def test_valid_input(self):
        self.assertEqual(0, process_game(''))
        self.assertEqual(200, process_game('XXXXXXXXXX', 10))
        self.assertEqual(75, process_game('1/2/3/4/5/', 5))
        self.assertEqual(20, process_game('----------X', 6))
        self.assertEqual(25, process_game('12345/', 3))


if __name__ == '__main__':
    unittest.main()