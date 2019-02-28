from unittest import TestCase
from level1_selenium import Level1


class Level1Test(TestCase):

    def test_unscramble_one_word(self):
        test = Level1().get_answer(['jam1es'])
        self.assertEqual('james1', test)
