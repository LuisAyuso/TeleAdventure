

import unittest
import string
from adventure.text_game.game import Game, CleanEscapeSequences


#how to run: just type nosetest in the root directoy

class TestTextGame(unittest.TestCase):

    def test_lifetime(self):
        print "hello"
        self.assertTrue(True)

        g = Game()
        self.assertTrue(g.is_game_alive())
        g.kill_game()
        self.assertFalse(g.is_game_alive())


class TestTextParsing(unittest.TestCase):

    def test_parsing(self):
        f = open("adventure/tests/capture","rb")
        buff = f.read()
        f.close()

        out = CleanEscapeSequences().clean(buff)

        print out
        self.assertNotEquals(len(out), 0)


class TestRealGame(unittest.TestCase):

    def test_parsing(self):
        g = Game()
        self.assertTrue(g.is_game_alive())

        out = g.read_game_status()
        self.assertNotEquals(len(out), 0)
        print out
        out = ""

        g.send_input("open door")
        out = g.read_game_status()
        self.assertNotEquals(len(out), 0)
        print out
        out = ""

        g.send_input("go north")
        out = g.read_game_status()
        self.assertNotEquals(len(out), 0)
        print out
        out = ""

        g.send_input("go north")
        out = g.read_game_status()
        self.assertNotEquals(len(out), 0)
        print out
        out = ""

        g.send_input("open window")
        out = g.read_game_status()
        self.assertNotEquals(len(out), 0)
        print out
        out = ""

        self.assertFalse(True)

if __name__ == '__main__':
    unittest.main()
