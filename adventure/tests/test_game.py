

import unittest
from adventure.text_game import Game

#how to run: just type nosetest in the root directoy

class TestTextGame(unittest.TestCase):

    def test_success(self):
        print "hello"
        self.assertTrue(True)

    def test_success2(self):
        print "hello"
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
