

import unittest
from adventure.text_game.StateMachine import (StateMachine, State)

# how to run: just type nosetest in the root directoy
counter = 0


class State1(State):
    def run(self, i, machine):
        global counter
        counter += 1

    def next(self, i, machine):
        if i == 'a':
            return State2()
        else:
            return self


class State2(State):
    def run(self, i, machine):
        return

    def next(self, i, machine):
        if i == 'b':
            return State1()
        return self


class State0(State):
    def run(self, i, machine):
        return

    def next(self, i, machine):
        if i == 'b':
            return State1()
        if i == 'a':
            return State2()


class M(StateMachine):
    def __init__(self):
        StateMachine.__init__(self, State0())


class TestStateMachine(unittest.TestCase):

    def test_2(self):
        global counter
        counter = 0
        M().runAll("aabb")
        self.assertEqual(counter, 2)

    def test_3(self):
        global counter
        counter = 0
        M().runAll("baabb")
        self.assertEqual(counter, 3)

    def test_5(self):
        global counter
        counter = 0
        M().runAll("babaabbab")
        self.assertEqual(counter, 5)

if __name__ == '__main__':
    unittest.main()
