
from subprocess import Popen, PIPE
from time import sleep

from stream_reader import NonBlockingStreamReader

from StateMachine import (State, StateMachine)

class Start(State):
    def run(self):
        print "Start filtering"

    def next(self, input):
        if ord(input) == 27:
            return EscapeSequence()
        return PainText()

class Consume(State):
    def run(self):
        print "consume one"

    def next(self, input):
        return PlainText()

class PlainText(State):
    def run(self):
        print "we are reading plain text"

    def next(self, input):
        if ord(input) == 27:
            return EscapeSequence()
        return self


class EscapeSequence(State):
    def run(self):
        print "we are reading an scape sequence"

    def next(self, input):
        if ord(input) == 109:
            return Consume()
        return self


class CleanEscapeSequences(StateMachine):

    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Start())


class Game:

    game_stream = None
    nbsr = None

    def __init__(self):
        print "new game"
        p = Popen(['frotz', '-p', '-d', '-q', '/home/luis/code/tele-adventure/games/zork_1.z5'], stdin=PIPE, stdout=PIPE, stderr=PIPE)

        self.game_stream = p

        # wrap p.stdout with a NonBlockingStreamReader object:
        self.nbsr = NonBlockingStreamReader(p.stdout)

    def read_game_status(self, lenght=0):
        print "read output"
        sleep(0.5)
        output = str(self.nbsr.readline())

        print " READ:~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
        print "[" + output[0:-5] + "]"

        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "

        string = output[0:-5]
        #for c in string:
        #    print c, " -> ", ord(c)

        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "

        CleanEscapeSequences().runAll(string)

        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DONE"

        return string

    def send_input(self, text):

        print ' -> ', text
        self.game_stream.stdin.write(text + '\n')
