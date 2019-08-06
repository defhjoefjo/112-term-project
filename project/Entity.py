import random

from statusMachine import statusMachine


class Entity(object):
    def __init__(self, world, inventory, health, state, size, x, y):
        self.world = world
        self.inventory = inventory
        self.stateSet = []
        self.health = health
        self.state = state
        self.think = statusMachine()
        self.size = size
        self.x = x  # the position of the entity in the board
        self.y = y
        self.dirX = 0
        self.dirY = 0






class Player(Entity):
    def __init__(self,world,inventory,health,state,size,x,y):
        super().__init__(world,inventory,health,state,size,x,y)
        self.id = 2

    def pickUpWeapon(self):
        if(self.world.board[self.x+1][self.y] == 4):
            self.world.board[self.x + 1][self.y]=0
        if(self.world.board[self.x][self.y+1] == 4):
            pass
        if(self.world.board[self.x-1][self.y] == 4):
            pass
        if(self.world.board[self.x][self.y-1] == 4):
            pass

    def move(self, dirX, dirY):
            self.world.board[self.y][self.x] = 0
            self.x += dirX
            self.y += dirY
            self.world.board[self.y][self.x] = 2


class Enemy(Entity):
    def __init__(self, world, inventory, health, state, size, x, y):
        super().__init__(world, inventory, health, state, size, x, y)
        self.id = 3
    def randomMove(self):
        (dirX, dirY) = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.move(dirX, dirY)


    def move(self):
            self.world.board[self.y][self.x] = 0
            self.x += self.dirX
            self.y += self.dirY
            self.world.board[self.y][self.x] = 3