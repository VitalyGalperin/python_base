from unittest import TestCase
from bowling import get_score
import bowling


class ScoreTests(TestCase):

    def test_short_game(self):
        game_result = get_score('Х4/34-4')
        self.assertEqual(game_result, 46)

    def test_normal_game(self):
        game_result = get_score('Х4/34-452Х-/729---')
        self.assertEqual(game_result, 106)

    def test_ValueError(self):
        with self.assertRaises(ValueError):
            get_score('141/FA457X')

    def test_FrameCountError(self):
        with self.assertRaises(bowling.FrameCountError):
            get_score('ХХХХХХХХХХХ')

    def test_StrikeError(self):
        self.assertRaises(bowling.StrikeError, get_score, '1ХХХХХХХХХХ')

    def test_SpareError(self):
        self.assertRaises(bowling.StrikeError, get_score, 'ХХХХХХХХХ/1')


if __name__ == '__main__':
    unittest.main()