

from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK


class NonBlockingStreamReader:

    def __init__(self, stream):
        print "init nbsr"
        self._s = stream
        flags = fcntl(self._s, F_GETFL)
        fcntl(self._s, F_SETFL, flags | O_NONBLOCK)

    def readline(self):
        print "attempt read"
        text = ""
        try:
            text = self._s.read()
        except:
            pass
        return text
