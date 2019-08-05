# the template is from 112 website http://www.cs.cmu.edu/~112-n19/notes/notes-animations-demos.html#sideScrollerDemo
# Side Scroller Demo
import copy
from tkinter import *
from map import Maze
from Entity import *
from world import world

def init(data):
    # initialize and optimize the board

    data.size = 50
    maze = Maze(data.size, data.size)
    maze.initializeMap()
    for i in range(12):
        maze.optimizeMap()
    maze.setPlayer()
    data.gameWorld = world(copy.deepcopy(maze.board))# The board of the world is to process all the events
    data.wallSize = 25
    data.centerX = data.width / 2
    data.centerY = data.height / 2
    data.scrollX = -data.wallSize/2
    data.scrollY = -data.wallSize/2
    data.player = Player(data.gameWorld,[],10,None,data.wallSize/2,data.size//2,data.size//2)
    data.gameWorld.entities.append(data.player)
    data.walls = getWalls(data)
    data.timePassed = 0
    data.direction = ''
    data.road = getRoads(data)
def getPlayerBound(data):
    return (data.centerX - data.player.size, data.centerY - data.player.size,
            data.centerX + data.player.size, data.centerY + data.player.size)


def getWallBounds(data, wall):
    (x0, y0) = (data.walls[wall][0] * data.wallSize - data.wallSize*data.size/2 +data.centerX + data.scrollX,
                data.walls[wall][1] * data.wallSize - data.wallSize*data.size/2 +data.centerY + data.scrollY)
    (x1, y1) = (x0 + data.wallSize, y0 + data.wallSize)
    return (x0, y0, x1, y1)

def getRoads(data):
    allCell = copy.deepcopy(data.gameWorld.baord)
    for walls in data.walls:
        allCell.remove(walls)
    return allCell
def getWalls(data):
    walls = []
    for row in range(len(data.gameWorld.board)):
        for col in range(len(data.gameWorld.board[0])):
            if (data.gameWorld.board[row][col] == 1):
                walls.append((row, col))
    return walls


def getWallHit(data):
    # return wall that player is currently hitting
    # note: this should be optimized to only check the walls that are visible
    # or even just directly compute the wall without a loop
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


def mousePressed(event, data):
    pass


def keyPressed(event, data):
    if (event.keysym == "Left"):
        data.scrollX += data.wallSize
        data.direction = 'l'
        data.player.move(-1,0)
    elif (event.keysym == "Right"):
        data.scrollX -= data.wallSize
        data.direction = 'r'
        data.player.move(1, 0)
    elif (event.keysym == "Up"):
        data.scrollY += data.wallSize
        data.direction = 'u'
        data.player.move(0, -1)
    elif (event.keysym == "Down"):
        data.scrollY -= data.wallSize
        data.direction = 'd'
        data.player.move(0, 1)
    print('start here')


def timerFired(data):
    data.timePassed += 1
    if(data.timePassed % 1000 == 0):
        data.world.addEntity(Enemy())


def redrawAll(canvas, data):
    getWallHit(data)
    print(data.player.x,data.player.y)
    for cell in range(len(data.walls)):
        (x0, y0, x1, y1) = getWallBounds(data, cell)
        canvas.create_rectangle(x0 , y0,
                                x1 , y1,
                                fill="black")
    canvas.create_rectangle(getPlayerBound(data), fill="red")


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
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(1000,800)
