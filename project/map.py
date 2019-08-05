import random

import pygame
from pygame.locals import *


def checkWalls(board, layers, i,
               j):  # check the neighbour at different levels of out layers are walls
    count = 0
    for rows in range(i - layers + 1, i + layers):
        if j - layers > 0:
            if 0 <= rows < len(board):
                if board[rows][j - layers] == 1:
                    count += 1
        if j + layers < len(board[0]):
            if 0 <= rows < len(board):
                if board[rows][j + layers] == 1:
                    count += 1
    for cols in range(j - layers + 1, j + layers):
        if i - layers > 0:
            if 0 <= cols < len(board[0]):
                if board[i - layers][cols] == 1:
                    count += 1
        if i + layers < len(board):
            if 0 <= cols < len(board[0]):
                if board[i + layers][cols] == 1:
                    count += 1
    if 0 < i - layers < len(board) and 0 < j - layers < len(board[0]):
        if board[i - layers][j - layers] == 1:
            count += 1
    if 0 < i - layers < len(board) and 0 < j + layers < len(board[0]):
        if board[i - layers][j + layers] == 1:
            count += 1
    if 0 < i + layers < len(board) and 0 < j - layers < len(board[0]):
        if board[i + layers][j - layers] == 1:
            count += 1
    if 0 < i + layers < len(board) and 0 < j + layers < len(board[0]):
        if board[i + layers][j + layers] == 1:
            count += 1

    return count


class Maze(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [([0] * self.width) for rows in range(self.height)]

    def initializeMap(self):
        for row in range(1, self.height - 1):
            for col in range(1, self.width - 1):
                possibility = random.randint(1, 100)
                if possibility < 27:
                    self.board[row][col] = 1  # initialize the block as wall
                else:
                    self.board[row][col] = 0  # initialize the block as road
        for horizontal in range(self.width):  # set bound for the map
            self.board[0][horizontal] = 1
            self.board[-1][horizontal] = 1
        for vertical in range(self.height):
            self.board[vertical][0] = 1
            self.board[vertical][-1] = 1

    def optimizeMap(self):  # use cellular automata to optimize map
        for row in range(self.height):
            for col in range(self.width):
                for i in range(4):
                    if checkWalls(self.board, 1, row, col) >= 5 or (checkWalls(
                            self.board, 2, row, col) + checkWalls(
                            self.board, 1, row, col)) <= 2:
                        self.board[row][col] = 1
                for i in range(3):
                    if checkWalls(self.board, 1, row, col) >= 5:
                        self.board[row][col] = 1

        for row in range(self.height):
            for col in range(self.width):
                if checkWalls(self.board, 1, row, col) == 0:
                    self.board[row][col] = 0  # clear some single block

    def setPlayer(self):
        self.board[self.width//2][self.height//2] = 2
