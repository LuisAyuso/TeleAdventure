
from subprocess import Popen, PIPE

from .stream_reader import NonBlockingStreamReader
from time import sleep


class Game:

    game_stream = None
    nbsr = None

    def __init__(self):
        print "new game"
        p = Popen(['frotz', '-p', '-d', '-q', '/home/luis/code/tele-adventure/games/zork_1.z5'], stdin=PIPE, stdout=PIPE, stderr=PIPE)


        self.game_stream = p

     #   # wrap p.stdout with a NonBlockingStreamReader object:
        self.nbsr = NonBlockingStreamReader(p.stdout)

    def read_game_status(self, lenght=0):
        sleep (0.5)
        output = str(self.nbsr.readline())

        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
        print "[" + output[0:-5] + "] len:"

        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "


        print " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "



        #idx = dirty.find('[m')
        #if idx > 0:
        #    print ' found!'
        #    output = dirty[idx+2:]
        #else:
        #    idx = dirty.find('[23d')
        #    if idx > 0:
        #        print ' found!'
        #        output = dirty[idx+2:]

        return output[0:-5]

       #  print " <- ", output
       #  # 0.1 secs to let the shell output the result
       #  if not output:
       #      return " no output"
       #  else:
       #    return output

    def send_input(self, text):

        print ' -> ', text
        self.game_stream.stdin.write(text + '\n')

