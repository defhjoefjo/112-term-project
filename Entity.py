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

    def move(self, dirX, dirY):
            self.world.board[self.y][self.x] = 0
            self.x += dirX
            self.y += dirY
            self.world.board[self.y][self.x] = 1

    def pickUp(self):
        pass



class Player(Entity):
    def __init__(self,world,inventory,health,state,size,x,y):
        super().__init__(world,inventory,health,state,size,x,y)


class Enemy(Entity):
    def __init__(self):
        super().__init__()