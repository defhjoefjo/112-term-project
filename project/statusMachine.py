import random
from Entity import *

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

class enemyStateGuarding(State):# at this state the enemy will make a random walk until the player enters its detection radius
    def __init__(self,enemy):
        super().__init__("guarding")
        self.enemy = enemy
    def action(self):
        (dirX, dirY) = random.choice([(1,0),(0,1),(-1,0),(0,-1)])
        self.enemy.move(dirX,dirY)
    def condition(self):
        pass