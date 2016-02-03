
from subprocess import Popen, PIPE
from time import sleep
import signal
import string

from stream_reader import NonBlockingStreamReader

from StateMachine import (State, StateMachine)


def print_it(str, c):
    """
        DEBUG method
    """
    # if c in string.printable:
    #     print str, c, " -> ", ord(c)
    # else:
    #     print str, "NP -> ", ord(c)
    return


class Start(State):
    def run(self, i, machine):
        print_it("init", i)
        return

    def next(self, i, machine):
        if ord(i) == 27:
            return EscapeSequence()
        return PlainText()


class PlainText(State):
    def run(self, i, machine):
        print_it("plain", i)
        machine.add_char(i)

    def next(self, i, machine):
        if ord(i) == 27:
            return EscapeSequence()
        if ord(i) == 226:
            return Consume()
        if ord(i) == 13:
            return Replace("\n")
        return self


class Replace(State):

    def __init__(self, replacement):
        self.replacement = replacement

    def run(self, i, machine):
        machine.add_char(self.replacement)

    def next(self, i, machine):
        if ord(i) == 27:
            return EscapeSequence()
        if ord(i) == 226:
            return Consume()
        if ord(i) == 13:
            return Replace("\n")
        return self


class Consume(State):
    def run(self, i, machine):
        print_it("consume", i)
        return

    def next(self, i, machine):
        if ord(i) == 27:
            return EscapeSequence()
        if ord(i) == 226:
            return Consume()
        return PlainText()


class Ignore(Consume):

    def __init__(self, token, code):
        self.token = token
        self.code = code

    def run(self, i, machine):
        #print "Ignore: ", self.token[1:], self.code
        return


class Color(Consume):

    def __init__(self, token, code):
        self.token = token
        self.code = code

    def run(self, i, machine):
        #print "Change Color: ", self.token[1:], self.code
        return


class Reset(Consume):

    def __init__(self, token, code):
        self.token = token
        self.code = code

    def run(self, i, machine):
        #rint "Reset Color: ", self.token[1:], self.code
        return


class NewLine(Consume):

    def __init__(self, token, code):
        return

    def run(self, i, machine):
        machine.add_char("\n")


class ReadScore(Consume):

    def __init__(self):
        self.score

    def run(self, i, machine):
        self.score += i

    def next(self, i, machine):
        if i in string.digits:
            return self
        machine.set_score(self.score)
        return Start()


class EscapeSequence(State):
    """
        https://en.wikipedia.org/wiki/ANSI_escape_code
    """
    def __init__(self):
        self.token = ""
        self.terminals = "ABCDEFGHIJKSMTfinsuhrmd="

        self.handlers = dict()

        self.handlers["h"] = Ignore
        self.handlers["A"] = Ignore
        self.handlers["B"] = Ignore
        self.handlers["C"] = Ignore
        self.handlers["D"] = Ignore
        self.handlers["R"] = Ignore
        self.handlers["F"] = Ignore
        self.handlers["G"] = Ignore
        self.handlers["H"] = Reset
        self.handlers["I"] = Ignore
        self.handlers["J"] = Ignore
        self.handlers["K"] = Ignore
        self.handlers["S"] = Ignore
        self.handlers["M"] = Ignore
        self.handlers["T"] = Ignore
        self.handlers["f"] = Ignore
        self.handlers["i"] = Ignore
        self.handlers["n"] = Ignore
        self.handlers["s"] = Ignore
        self.handlers["u"] = Ignore
        self.handlers["h"] = Ignore
        self.handlers["r"] = Ignore
        self.handlers["m"] = Color
        self.handlers["d"] = Ignore
        self.handlers["="] = Ignore

    def run(self, i, machine):
        print_it("scape", i)
        self.token += i
        return

    def next(self, i, machine):

        if i in self.terminals:
            return self.handlers[i](self.token, i)
        return self


class CleanEscapeSequences(StateMachine):

    def __init__(self):
        # Initial state
        StateMachine.__init__(self, Start())
        self.message = ""
        self.location = ""
        self.score = ""

    def set_score(self, score):
        self.score = score

    def add_char(self, c):
        assert(c in string.printable)
        self.message += c

    def add_location_char(self, c):
        assert(c in string.printable)
        self.location += c

    def clean(self, input):
        print " ~~~~~~~~~~~~~~~~~~~~~~~~~: ", len(input)
        self.runAll(input)
        print " ~~~~~~~~~~~~~~~~~~~~~~~~~ "

        return self.message


class Game:

    game_stream = None
    nbsr = None
    proccess = None

    def __init__(self):
        print "new game"
        p = Popen(['frotz',  '-d', '-q',
                   '/home/luis/code/tele-adventure/games/zork_1.z5'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)

        self.game_stream = p
        self.proccess = p

        # wrap p.stdout with a NonBlockingStreamReader object:
        self.nbsr = NonBlockingStreamReader(p.stdout)

    def read_game_status(self,):
        sleep(0.2)
        output = str(self.nbsr.readline())
        string = CleanEscapeSequences().clean(output)
        lines = string.split("\n")[1:-1]
        return "\n".join(lines)

    def send_input(self, text):

        print ' -> ', text
        self.game_stream.stdin.write(text + '\n')

    def is_game_alive(self):
        return self.proccess.returncode is None

    def kill_game(self):
        print "kill pid: ", self.proccess.pid
        self.proccess.send_signal(signal.SIGKILL)
        self.proccess.communicate()
