
from subprocess import Popen, PIPE
from time import sleep
import re

from stream_reader import NonBlockingStreamReader

def stripEscape(string):
    """ Removes all escape sequences from the input string """
    delete = ""
    i=1
    while (i<0x27):
        delete += chr(i)
        i += 1
    t = string.translate(None, delete)
    return t

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

        string = stripEscape(output[0:-5])

        re.sub("\[.+[hdmH]", "", string)

        print string

        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DONE"

        return string

    def send_input(self, text):

        print ' -> ', text
        self.game_stream.stdin.write(text + '\n')
