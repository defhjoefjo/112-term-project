from Entity import Entity
class world(object):
    def __init__(self,board):
        self.entities = []
        self.board = board
        self.weapons = []

    def addEntity(self,entity):
        if not isinstance(entity,Entity):
            return None
        if(self.board[entity.x][entity.y] != 1 and
           self.board[entity.x][entity.y] != 2):
            self.entities.append(entity)

    def delEntity(self,entity):
        if(entity in self.entities):
            self.entities.remove(entity)
