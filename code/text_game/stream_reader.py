

from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read


class NonBlockingStreamReader:

    def __init__(self, stream):

        self._s = stream
        flags = fcntl(self._s, F_GETFL)
        fcntl(self._s, F_SETFL, flags | O_NONBLOCK)

    def readline(self):
        text = ""
        try:
            text = self._s.read()
        except:
            pass
        return text






#
#from threading import Thread
#from Queue import Queue, Empty
#
#
#class NonBlockingStreamReader:
#
#    def __init__(self, stream):
#        '''
#        stream: the stream to read from.
#        Usually a process' stdout or stderr.
#        '''
#
#        self._s = stream
#        self._q = Queue()
#
#        def _populateQueue(stream, queue):
#
#            while True:
#                line = stream.readline()
#                if line:
#                    print 'newline'
#                    queue.put(line)
#                else:
#                    raise UnexpectedEndOfStream
#
#        self._t = Thread(target=_populateQueue, args=(self._s, self._q))
#        self._t.daemon = True
#        self._t.start()
#
#    def readline(self, timeout=None):
#        print ' read input'
#        try:
#            return self._q.get(block=timeout is not None, timeout=timeout)
#        except Empty:
#            return None
#
#
#
#class UnexpectedEndOfStream(Exception):
#    pass
