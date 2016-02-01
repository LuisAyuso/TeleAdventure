
from subprocess import Popen, PIPE
from time import sleep
import signal
import string

from stream_reader import NonBlockingStreamReader

from StateMachine import (State, StateMachine)

def print_it(str, c):
    if c in string.printable:
        print str, c, " -> ", ord(c)
    else:
        print str, "NP -> ", ord(c)

class Start(State):
    def run(self, i, machine):
        # print_it("init", i)
        return

    def next(self, i, machine):
        if ord(i) == 27:
            return EscapeSequence()
        return PlainText()

class Consume(State):
    def run(self, i, machine):
        # print_it("consume", i)
        return

    def next(self, i, machine):
        if ord(i) == 27:
            return EscapeSequence()
        if ord(i) == 226:
            return Consume()
        return PlainText()

class PlainText(State):
    def run(self, i, machine):
        # print_it("plain", i)
        machine.add_char(i)

    def next(self, i, machine):
        if ord(i) == 27:
            return EscapeSequence()
        if ord(i) == 226:
            return Consume()
        if ord(i) == 13:
            return Consume()
        return self


class EscapeSequence(State):
    def run(self, i, machine):
        # print_it("scape", i)
        return

    def next(self, i, machine):
        if ord(i) == 100:
            return Consume()
        if ord(i) == 104:
            return Consume()
        if ord(i) == 114:
            return Consume()
        if ord(i) == 66:
            return Consume()
        if ord(i) == 109:
            return Consume()
        if ord(i) == 108:
            return Consume()
        if ord(i) == 61:
            return Consume()
        if ord(i) == 72:
            return Consume()
        if ord(i) == 62:
            return Consume()
        if ord(i) == 77:
            return Consume()
        return self


class CleanEscapeSequences(StateMachine):

    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Start())
        self.output = ""

    def add_char(self, c):
        assert(c in string.printable)
        self.output += c

    def clean(self, input):
        print "proccess: ", len(input)
        self.runAll(input)
        return self.output

class Game:

    game_stream = None
    nbsr = None
    proccess = None

    def __init__(self):
        print "new game"
        p = Popen(['frotz', '-p', '-d', '-q', '/home/luis/code/tele-adventure/games/zork_1.z5'], stdin=PIPE, stdout=PIPE, stderr=PIPE)

        self.game_stream = p
        self.proccess = p

        # wrap p.stdout with a NonBlockingStreamReader object:
        self.nbsr = NonBlockingStreamReader(p.stdout)

    def read_game_status(self, lenght=0):
        sleep(0.2)
        output = str(self.nbsr.readline())
        string = CleanEscapeSequences().clean(output[lenght:-5])
        return string

    def send_input(self, text):

        print ' -> ', text
        self.game_stream.stdin.write(text + '\n')

    def is_game_alive(self):
        return self.proccess.returncode is None

    def kill_game(self):
        print "kill pid: ", self.proccess.pid
        self.proccess.send_signal(signal.SIGKILL)
        self.proccess.communicate()


