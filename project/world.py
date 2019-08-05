from Entity import *
class world(object):
    def __init__(self,board):
        self.entities = []
        self.board = board
        self.weapons = []

    def addEnemy(self,entity):
        if not isinstance(entity,Enemy):
            return None
        if(self.board[entity.y][entity.x] != 1 and
           self.board[entity.y][entity.x] != 2):
            self.entities.append(entity)
            self.board[entity.y][entity.x]=entity.id

    def delEnemy(self,entity):
        if(entity in self.entities):
            self.entities.remove(entity)
