from unittest import TestCase
from bowling import get_score
import bowling


class ScoreTests(TestCase):

    def test_short_game(self):
        self.assertEqual(get_score('Х4/34-4'), 46)

    def test_normal_game(self):
        self.assertEqual(get_score('Х4/34-452Х-/729---'), 106)

    def test_ValueError(self):
        self.assertRaises(ValueError, get_score, '141/FA457X')

    def test_FrameCountError(self):
        self.assertRaises(bowling.FrameCountError, get_score, 'ХХХХХХХХХ111')

    def test_StrikeError(self):
        self.assertRaises(bowling.StrikeError, get_score, '1ХХХХХХХХХХ')

    def test_SpareError(self):
        self.assertRaises(bowling.SpareError, get_score, 'ХХХХХХХХХ/1')

    def test_TotalScoreError(self):
        self.assertRaises(bowling.TotalScoreError, get_score, 'ХХХХХХХХХ56')

    def NoSpareWarning(self):
        self.assertRaises(bowling.TotalScoreError, get_score, 'ХХХХХХХХХ55')

    def test_UnfinishedFrameWarning(self):
        self.assertRaises(bowling.UnfinishedFrameWarning, get_score, 'ХХХХХХХХХ1')


if __name__ == '__main__':
    unittest.main()
