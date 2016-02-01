
class State:

    def run(self):
        assert 0, "run not implemented"

    def next(self, input):
        assert 0, "next not implemented"


class StateMachine:

    def __init__(self, initialState):
        print "init the f machine "
        self.currentState = initialState
        self.currentState.run()
        print "yo!"

    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            assert(self.currentState is not None)
            self.currentState = self.currentState.next(i)
            self.currentState.run()
