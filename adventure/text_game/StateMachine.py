
class State:

    def run(self, i, machine):
        assert 0, "run not implemented"

    def next(self, i, machine):
        assert 0, "next not implemented"


class StateMachine:

    def __init__(self, initialState):
        self.currentState = initialState

    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            assert(self.currentState is not None)
            self.currentState = self.currentState.next(i, self)
            self.currentState.run(i, self)
