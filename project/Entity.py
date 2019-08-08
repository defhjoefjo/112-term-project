import random
from SETTINGS import *
class Entity(object):
    def __init__(self, world, inventory, health, state, size, x, y):
        self.world = world
        self.inventory = inventory
        self.stateSet = []
        self.health = health
        self.state = state
        self.size = size
        self.x = x  # the position of the entity in the board
        self.y = y
        self.dirX = 0
        self.dirY = 0






class Player(Entity):
    def __init__(self,world,inventory,health,state,size,x,y):
        super().__init__(world,inventory,health,state,size,x,y)
        self.id = 2
        self.currentWeapon = 0
        self.gridX = self.x // WALLSIZE
        self.gridY = self.y // WALLSIZE
    def move(self, dirX, dirY):
            self.x += dirX
            self.y += dirY



class Enemy(Entity):
    def __init__(self, world, inventory, health, state, size, x, y):
        super().__init__(world, inventory, health, state, size, x, y)
        self.id = 3
        self.stateSet = ['guarding','approaching','attacking']
        self.state = state
        self.openList=[]
        self.closedList = []
        self.G = WALLSIZE
        self.H = 0


    def randomMove(self):
        (self.dirX, self.dirY) = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        self.move()

    def pathFinding(self):
        HVal = dict()
        dir = [(0,1),(0,-1),(1,0),(-1,0)]
        for direc in dir:
            if self.world.board[self.y+direc[0]][self.x+direc[1]] == 0:
                self.openList.append((self.y + direc[0],self.x + direc[1]))
            else:
                self.closedList.append((self.y + direc[0], self.x + direc[1]))
        for node in self.openList:
            HVal[self.manhattanDis(node[1],node[0])] = node
        if(len(HVal.keys())!=0):
            (self.dirY)=HVal[sorted(HVal.keys())[0]][0]-self.y
            (self.dirX) = HVal[sorted(HVal.keys())[0]][1] - self.x
        self.move()
    def manhattanDis(self,x,y):
        return (abs((x - self.world.player.x))+abs((y-self.world.player.y)))*10


    def move(self):
        if(self.world.board[self.y+self.dirY][self.x+self.dirX] == 0):
            self.world.board[self.y][self.x] = 0
            self.x += self.dirX
            self.y += self.dirY
            self.world.board[self.y][self.x] = 3
    def checkCondition(self):
        if(150<(self.world.player.x-self.x)**2+(self.world.player.y-self.y)**2)**0.5 * WALLSIZE<300:
            self.state = 1
        if((self.world.player.x-self.x)**2+(self.world.player.y-self.y)**2)**0.5* WALLSIZE>300:
            self.state = 0
        if 0<((self.world.player.x-self.x)**2+(self.world.player.y-self.y)**2)**0.5* WALLSIZE<150:
            self.state = 2

    def getBound(self,data):
        (x0,y0) = (self.x * self.size - self.size*BOARDSIZE/2 +data.centerX + data.scrollX,
                   self.y * self.size - self.size*BOARDSIZE/2 +data.centerY + data.scrollY)
        (x1,y1) = (x0 + WALLSIZE, y0 + WALLSIZE)
        return (x0,y0,x1,y1)