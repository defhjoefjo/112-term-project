class State(object):
    def __init__(self, name):
        self.name = name

    def action(self):
        pass

    def condition(self):
        pass

    def enterAction(self):
        pass

    def exitAction(self):
        pass


class statusMachine(object):
    def __init__(self):
        self.states = {}
        self.activeState = None

    def addState(self, state):
        self.states[state.name] = state

    def check(self):
        if self.activeState is None:
            return
        self.activeState.action()
        newState = self.activeState.condition()
        if newState is not None:
            self.setState(newState)

    def setState(self, newStateName):
        if self.activeState is not None:
            self.activeState.exitAction()
        self.activeState = self.states[newStateName]
        self.activeState.enterAction()
