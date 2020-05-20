from unittest import TestCase
# from bowling import get_score
# import bowling

from bowling import get_score
import bowling as bowling


class ScoreTests(TestCase):

    def test_short_game(self):
        self.assertEqual(get_score('Х4/34-4', international=False), 46)

    def test_normal_game(self):
        self.assertEqual(get_score('Х4/34-452Х-/729---', international=False), 106)

    def test_short_game_international(self):
        self.assertEqual(get_score('ХXX347/21'), 92)

    def test_normal_game_international(self):
        self.assertEqual(get_score('ХXX347/21XXX5/'), 177)

    def test_BadStringError(self):
        self.assertRaises(bowling.BadStringError, get_score, '141/FA457X')

    def test_FrameCountError(self):
        self.assertRaises(bowling.FrameCountError, get_score, 'ХХХХХХХХХ111')

    def test_StrikeError(self):
        self.assertRaises(bowling.StrikeError, get_score, '1ХХХХХХХХХХ')

    def test_SpareError(self):
        self.assertRaises(bowling.SpareError, get_score, 'ХХХХХХХХХ/1')

    def test_TotalScoreError(self):
        self.assertRaises(bowling.TotalScoreError, get_score, 'ХХХХХХХХХ56')

    def test_NoSpareWarning(self):
        self.assertRaises(bowling.NoSpareWarning, get_score, 'ХХХХХХХХХ55')

    def test_UnfinishedFrameWarning(self):
        self.assertRaises(bowling.UnfinishedFrameWarning, get_score, 'ХХХХХХХХХ1')


if __name__ == '__main__':
    unittest.main()
