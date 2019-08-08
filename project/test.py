# Side Scroller Demo
#run function from http://www.cs.cmu.edu/~112-n19/notes/notes-animations-part2.html
import copy
import math
import random
from tkinter import *
from map import Maze
from Entity import *
from world import world
from SETTINGS import *
from PIL import ImageTk,Image
from weapon import *
def imageRegister(name):
    image = Image.open(name)
    photo = ImageTk.PhotoImage(image)
    return photo


class bullet(object):
    def __init__(self, x, y, speed, vector,origin):
        self.size = BULLETSIZE
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = 2
        self.dx = self.speed * -1*vector[0]
        self.dy = self.speed * -1*vector[1]
        self.origin = origin
        self.deviationX = 0
        self.deviationY = 0

    def move(self,data):
        self.x += self.dx * data.player.inventory[data.player.currentWeapon].bulSpedMulti
        self.y += self.dy * data.player.inventory[data.player.currentWeapon].bulSpedMulti

    def getEnemyHit(self,other,data):
        print(data.bullet)
        if(isinstance(self.origin,Player)):
            (a0,b0,a1,b1)=getEnemyBound(data,other)
            if(abs(self.x-(a0+a1)/2)<BULLETSIZE+WALLSIZE/2 and
               abs(self.y-(b0+b1)/2)<BULLETSIZE+WALLSIZE/2):
                other.health -= self.damage * data.player.inventory[data.player.currentWeapon].damageMultiplier
                if(self in data.bullet):
                    data.bullet.remove(self)
        if(isinstance(self.origin, Enemy)):
            if (abs(self.x - data.width / 2) < BULLETSIZE + WALLSIZE / 2 and
                    abs(self.y - data.height / 2) < BULLETSIZE + WALLSIZE / 2):
                data.player.health -= self.damage
                if(self in data.bullet):
                    data.bullet.remove(self)

    def getWallHit(self,data):
        for cell in range(len(data.walls)):
            (x0, y0, x1, y1) = getWallBounds(data, cell)
            wallCX = (x0 + x1)/2
            wallCY = (y0 + y1)/2
            if(abs(self.x+self.deviationX-wallCX)<BULLETSIZE+WALLSIZE/2 and
               abs(self.y+self.deviationY-wallCY)<BULLETSIZE+WALLSIZE/2):
                if(self in data.bullet):
                   data.bullet.remove(self)
        print(data.bullet)


    def getBound(self):
        return (self.x - BULLETSIZE +self.deviationX, self.y - BULLETSIZE+self.deviationY,
                self.x + BULLETSIZE +self.deviationX, self.y + BULLETSIZE+self.deviationY)
    def draw(self, canvas):
        canvas.create_oval(self.getBound(),
                           fill="green")
##########################################################################

def init(data):
    # initialize and optimize the board
    data.weaponSet={100:glock(random.uniform(0.5,1.5),random.uniform(0.5,1.5)),
                    101:awp(random.randint(5,10),random.randint(3,4))}
    data.mode = 'start'
    data.size = BOARDSIZE
    maze = Maze(data.size, data.size)
    maze.initializeMap()
    for i in range(12):
        maze.optimizeMap()
    data.wallImg = imageRegister('wall.png')
    data.roadImg = imageRegister('road.png')
    data.healthImg = imageRegister('health.png')
    data.enemyImg = imageRegister('enemy.png')
    data.glockImg = imageRegister('glock.png')
    data.score = 0
    data.wallSize = WALLSIZE
    data.centerX = data.width / 2
    data.centerY = data.height / 2
    if BOARDSIZE%2!=0:
        data.scrollX = 0
        data.scrollY = 0
    else:
        data.scrollX = -WALLSIZE/2
        data.scrollY = -WALLSIZE/2
    data.gameWorld = world(copy.deepcopy(
        maze.board))  # The board of the world is to process all the events
    data.defaultWeapon = data.weaponSet[101]
    data.player = Player(data.gameWorld,[data.weaponSet[100],data.weaponSet[101]],PLAYER_HEALTH,None,data.wallSize/2,data.size//2,data.size//2)
    data.gameWorld.player = data.player
    data.timePassed = 0
    data.direction = ''
    data.road = []
    data.enemy = []
    data.gameOver = False
    data.gunX = 0
    data.gunY = 0
    data.bullet =[]
    data.health = []
    data.walls = []
    data.playerWeaponImg = None
    data.mouseX = 0
    data.mouseY = 0
def getPlayerBound(data):
    return (data.centerX - data.player.size, data.centerY - data.player.size,
            data.centerX + data.player.size, data.centerY + data.player.size)


def getWallBounds(data, wall):
    (x0, y0) = (data.walls[wall][1] * data.wallSize - data.wallSize*data.size/2 +data.centerX + data.scrollX,
                data.walls[wall][0] * data.wallSize - data.wallSize*data.size/2 +data.centerY + data.scrollY)
    (x1, y1) = (x0 + data.wallSize, y0 + data.wallSize)
    return (x0, y0, x1, y1)

def getRoadBound(data,road):
    (x0, y0) = (data.road[road][
                    1] * data.wallSize - data.wallSize * data.size / 2 + data.centerX + data.scrollX,
                data.road[road][
                    0] * data.wallSize - data.wallSize * data.size / 2 + data.centerY + data.scrollY)
    (x1, y1) = (x0 + data.wallSize, y0 + data.wallSize)
    return (x0, y0, x1, y1)

def getHealthBounds(data, health):
    (x0, y0) = (data.health[health][1] * data.wallSize - data.wallSize*data.size/2 +data.centerX + data.scrollX,
                data.health[health][0] * data.wallSize - data.wallSize*data.size/2 +data.centerY + data.scrollY)
    (x1, y1) = (x0 + data.wallSize, y0 + data.wallSize)
    return (x0, y0, x1, y1)

def getEnemyBound(data,enemy):
        (x0, y0) = (enemy.x * data.wallSize - data.wallSize * data.size / 2 + data.centerX + data.scrollX,
                    enemy.y * data.wallSize - data.wallSize * data.size / 2 + data.centerY + data.scrollY)
        (x1, y1) = (x0 + data.wallSize, y0 + data.wallSize)
        return (x0, y0, x1, y1)

def getCenter(a,b,c,d):
    return ((a+c)/2,(b+d)/2)

def getCell(data):
    data.road = []
    data.walls = []
    data.health = []
    for i in range(data.size):
        for j in range(data.size):
            if(data.gameWorld.board[i][j] == 0):
                data.road.append((i,j))
            if(data.gameWorld.board[i][j] == 1):
                data.walls.append((i,j))
            if(data.gameWorld.board[i][j] == 5):
                data.health.append((i,j))



def getEnemyCell(data):
    for i in range(data.size):
        for j in range(data.size):
            if(data.gameWorld.board[i][j]==3):
                if((i,j) not in data.enemy):
                    data.enemy.append((i,j))
            if((i,j) in data.enemy and data.gameWorld.board[i][j]==0):
                data.enemy.remove((i,j))




def getWallHit(data):
    for cell in range(len(data.walls)):
        (ax0,ay0,ax1,ay1)=getPlayerBound(data)
        (bx0,by0,bx1,by1)=getWallBounds(data,cell)
        if(ax0 == bx0 and ay0 == by0 and ax1==bx1 and ay1 == by1):
            if(data.direction =='u'):
                data.scrollY -= data.wallSize
                data.player.move(0,1)
            if(data.direction == 'd'):
                data.scrollY += data.wallSize
                data.player.move(0, -1)
            if(data.direction =='r'):
                data.scrollX += data.wallSize
                data.player.move(-1,0)
            if(data.direction == 'l'):
                data.scrollX -= data.wallSize
                data.player.move(1, 0)



################################################################################
def mousePressed(event, data):
    if(data.mode == 'start'): startMousePressed(event,data)
    if(data.mode == 'game'): gameMousePressed(event,data)
def timerFired(data):
    if (data.mode == 'start'): startTimerFired(data)
    if (data.mode == 'game'): gameTimerFired(data)
def keyPressed(event, data):
    if (data.mode == 'game'): gameKeyPressed(event,data)
    if (data.mode == 'start'): startKeyPressed(event,data)
def redrawAll(canvas, data):
    if (data.mode == 'game'): gameRedrawAll(canvas,data)
    if (data.mode == 'start'): startRedrawAll(canvas,data)

def mouseMoved(event,data):
    if(data.mode =='game'):
        gameMouseMoved(event,data)
############################START SCREEN########################################
def startMousePressed(event,data):
    if(data.width/2 - 50<event.x<data.width/2 + 50):
        data.mode = 'game'

def startKeyPressed(event,data):
    pass
def startTimerFired(data):
    pass
def startRedrawAll(canvas,data):
    canvas.create_rectangle(data.width/2 - 50, data.height-60,data.width/2+50,data.height-30)
    canvas.create_text(data.width/2,data.height-45,text="start Game!")
    canvas.create_text(data.width/2,50,text ="use WASD to move around, click to shoot, don't get shoot by the enemy, r to start, \n sorry about the plain ui:)")
#############################GAME MODE##########################################

def gameMousePressed(event, data):
    vector = [data.width/2-event.x,data.height/2-event.y]
    data.bullet.append(bullet(data.width/2,data.height/2,BULLETSPEED,vector,data.player))

def gameKeyPressed(event, data):
    if (data.gameOver == False):
        if(event.keysym == '0' and len(data.player.inventory)>=1):
            data.player.currentWeapon = 0
        if(event.keysym == '1' and len(data.player.inventory)>=2):
            data.player.currentWeapon = 1
        if (event.keysym == "a"):
            for bulet in data.bullet:
                bulet.deviationX += data.wallSize
            data.scrollX += data.wallSize
            data.direction = 'l'
            (data.player.dirX, data.player.dirY) = (-1,0)
        elif (event.keysym == "d"):
            for bulet in data.bullet:
                bulet.deviationX -= data.wallSize
            data.scrollX -= data.wallSize
            data.direction = 'r'
            (data.player.dirX, data.player.dirY) = (1,0)
        elif (event.keysym == "w"):
            for bulet in data.bullet:
                bulet.deviationY += data.wallSize
            data.scrollY += data.wallSize
            data.direction = 'u'
            (data.player.dirX, data.player.dirY) = (0,-1)
        elif (event.keysym == "s"):
            for bulet in data.bullet:
                bulet.deviationY -= data.wallSize
            data.scrollY -= data.wallSize
            data.direction = 'd'
            (data.player.dirX, data.player.dirY) = (0,1)
    if(event.keysym == 'r'):
        init(data)

    data.player.move(data.player.dirX,data.player.dirY)


def gameMouseMoved(event,data):
    vector = [event.x - data.width / 2, event.y - data.height / 2]
    distance = ((event.x - data.width / 2) ** 2 + (
                event.y - data.height / 2) ** 2) ** 0.5
    normalizedVector = [vector[0] / distance,
                        vector[1] / distance]
    data.gunX = (data.width / 2 + 32 * normalizedVector[0])
    data.gunY = (data.height / 2 + 32 * normalizedVector[1])
    if (event.x - data.width / 2 == 0):
        angle = math.atan((data.height / 2 - event.y) / 0.01)
    else:
        angle = math.atan((data.height / 2- event.y )/(event.x - data.width / 2))

    if(event.x-data.width/2>0):
        data.playerWeaponImg = ImageTk.PhotoImage(Image.open('%s.png'
        %data.player.inventory[data.player.currentWeapon].name).transpose\
            (Image.FLIP_LEFT_RIGHT).rotate(angle/math.pi*180))
    else:
        data.playerWeaponImg = ImageTk.PhotoImage(
            Image.open('%s.png'
                       % data.player.inventory[data.player.currentWeapon].name).rotate(
                angle / math.pi * 180))
def gameTimerFired(data):

    if(data.gameOver == False):
        data.timePassed += 1
        if(data.timePassed % 50 == 0):
            x = random.choice(data.road)[1]
            y = random.choice(data.road)[0]
            data.gameWorld.addEnemy(Enemy(data.gameWorld,[],ENEMY_HEALTH,None,data.wallSize/2,
                        x,y))
            getEnemyCell(data)
        if(data.timePassed %10 == 0):

            for enemy in data.gameWorld.entities:
                enemy.checkCondition()
                if(enemy.stateSet[enemy.state]=='guarding'):
                   enemy.randomMove()
                if(enemy.stateSet[enemy.state]=='approaching'):
                    enemy.pathFinding()
                if(enemy.stateSet[enemy.state]=='attacking'):
                    (x0,y0,x1,y1)=getEnemyBound(data,enemy)
                    centerX = (x0+x1)/2
                    centerY = (y0+y1)/2
                    vector = [centerX-data.width/2,centerY-data.height/2]
                    data.bullet.append(bullet(centerX,centerY,BULLETSPEED,vector,enemy))
                    enemy.pathFinding()

        if(data.timePassed % 100 == 0):
            road = random.choice(data.road)
            data.gameWorld.board[road[0]][road[1]] = 5
        for bullets in data.bullet:
            bullets.move(data)

def gameRedrawAll(canvas, data):
    getCell(data)
    if (data.gameWorld.board[data.player.y][data.player.x] == 5):
        data.player.health += random.randint(1, 5)
        data.gameWorld.board[data.player.y][data.player.x] = 0
        if(data.player.health > PLAYER_HEALTH):
            data.player.health = PLAYER_HEALTH
    getWallHit(data)
    for road in range(len(data.road)):
        (a, b, c, d) = getRoadBound(data, road)
        canvas.create_rectangle(a,b,c,d, width = 0)
    for cell in range(len(data.walls)):
        (x0, y0, x1, y1) = getWallBounds(data, cell)
        canvas.create_image(getCenter(x0, y0, x1, y1),image = data.wallImg)
    for enemy in data.gameWorld.entities:
        (x0,y0,x1,y1) = getEnemyBound(data,enemy)
        canvas.create_image(getCenter(x0,y0,x1,y1),image=data.enemyImg)
        if(enemy.health <=0):
            data.gameWorld.entities.remove(enemy)
            data.score += 1


    for health in range(len(data.health)):
        (a,b,c,d) = getHealthBounds(data,health)
        canvas.create_image(getCenter(a,b,c,d),image = data.healthImg)
    for bullets in data.bullet:
        bullets.draw(canvas)
        for enemy in data.gameWorld.entities:
            bullets.getEnemyHit(enemy,data)
        bullets.getWallHit(data)
    canvas.create_image(data.gunX,data.gunY,image = data.playerWeaponImg)
    canvas.create_oval(getPlayerBound(data), fill="red", width=0)
    if(data.player.health <0):
        data.gameOver = True
        canvas.create_text(data.width/2,data.height/2,text='You Died')
    canvas.create_rectangle(10,10,100,30)
    canvas.create_rectangle(10,10,10+data.player.health/PLAYER_HEALTH*90,30,fill = "green")
    print(Image.open('awp.png').mode)
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    def mouseMotionWrapper(event,canvas,data):
        mouseMoved(event,data)
        redrawAllWrapper(canvas,data)
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10  # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
    mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
    keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.bind('<Motion>', lambda event:
    mouseMotionWrapper(event, canvas, data))
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(1000,800)