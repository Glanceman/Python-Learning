"""
     ///////////////////////////////////
     // CS4386 Semester B, 2021-2022
     // Assignment 1
     // Name: Xian Jia Le
     // Student ID: 56214537
     ///////////////////////////////////
"""

from asyncio.windows_events import NULL
import copy
from ctypes import alignment
from math import inf as infinity
from pickle import NONE
import numpy as np


class AIPlayer(object):
    def __init__(self, name, symbole, isAI=False):
        self.name = name
        self.symbole = symbole  # 'X' 'O'
        self.isAI = isAI
        self.score = 0
        self.virtualSequenceGrid = np.full((6, 6), None)
        self.lastSquence = 0
        self.virtualOpponentScore = 0

    def stat(self):
        return self.name + " won " + str(self.won_games) + " games, " + str(self.draw_games) + " draw."

    def __str__(self):
        return self.name

    def get_isAI(self):
        return self.isAI

    def get_symbole(self):
        return self.symbole

    def get_score(self):
        return self.score

    def add_score(self, score):
        self.score += score

    def empty_cells(self, state):
        cells = []

        for x, row in enumerate(state):
            for y, cell in enumerate(row):
                if cell is None:
                    cells.append([x, y])
        return cells

    def get_possible_cells(self, searchPos, state,numberOfExtra):
        cells = []
        if searchPos!=NULL:
            # top-left
            if (searchPos[0]-1>=0 and searchPos[1]-1>=0) and state[searchPos[0]-1][searchPos[1]-1] is None:
                cells.append([searchPos[0]-1, searchPos[1]-1])
            # top
            if (searchPos[1]-1>=0) and state[searchPos[0]][searchPos[1]-1] is None:
                cells.append([searchPos[0], searchPos[1]-1])
            # top-right
            if (searchPos[0]+1<6 and searchPos[1]-1>=0) and state[searchPos[0]+1][searchPos[1]-1] is None:
                cells.append([searchPos[0]+1, searchPos[1]-1])
            # left
            if (searchPos[0]-1>=0) and state[searchPos[0]-1][searchPos[1]] is None:
                cells.append([searchPos[0]-1, searchPos[1]])
            # right
            if (searchPos[0]+1<6) and state[searchPos[0]+1][searchPos[1]] is None:
                cells.append([searchPos[0]+1, searchPos[1]])
            # bottom-left
            if (searchPos[0]-1>=0 and searchPos[1]+1<6) and state[searchPos[0]-1][searchPos[1]+1] is None:
                cells.append([searchPos[0]-1, searchPos[1]+1])
            # bottom
            if (searchPos[1]+1<6) and state[searchPos[0]][searchPos[1]+1] is None:
                cells.append([searchPos[0], searchPos[1]+1])
            # bottom-right
            if (searchPos[0]+1<6 and searchPos[1]+1<6) and state[searchPos[0]+1][searchPos[1]+1] is None:
                cells.append([searchPos[0]+1, searchPos[1]+1])

        if len(cells)< 8+numberOfExtra:
             for x, row in enumerate(state):
                for y, cell in enumerate(row):
                    if [x,y] not in cells:
                        if cell is None:
                            cells.append([x,y])
                    if len(cells)>=8+numberOfExtra:
                        return cells

        return cells

    # alignement(grid.grid,x,y) get score of current score and add to player "add_Score"
    # state boardstate player: playerSymbol
    # get_score return current player score
    def get_move(self, state, player):
        # find opponet move from state
        different = self.find_different_of_two_Grid(
            state, self.virtualSequenceGrid)  # get opponent cell
        # print(different)
        if different != NULL:  # re-organise move sequence
            # print("Oops get in null ")
            self.lastSquence = self.lastSquence+1
            self.virtualSequenceGrid[different[0]
                                     ][different[1]] = self.lastSquence
            # calc opponent score
            self.virtualOpponentScore = self.virtualOpponentScore + \
                alignement(state, different[0], different[1])

        print(player, self.score, " vs ", "Opponent ", self.virtualOpponentScore)
        # perform mini max
        #games = self.empty_cells(state)
        games=self.get_possible_cells(different,state,1)
        print(games)
        val, move = self.find_move_mini_Max(state.copy(
        ), games, player, self.score, self.virtualOpponentScore, True, -1000, 1000)
        print(val)
        random_move = move

        # mark the squence in grid virtual grid
        self.lastSquence = self.lastSquence+1
        self.virtualSequenceGrid[random_move[0]
                                 ][random_move[1]] = self.lastSquence
        # print("after:",self.virtualSequenceGrid)
        return random_move

    def find_move_mini_Max(self, currentBoardState, possibleMove, player, prevScore, prevOppScore, isMax, alpha, beta):
        # print(len(possibleMove))
        if(len(possibleMove) == 0):
            return 0, NULL
        maxVal = -1000
        minVal = 1000

        for i, move in enumerate(possibleMove):
            stateCopy = currentBoardState.copy()
            possibleMoveCopy = possibleMove.copy()
            possibleMoveCopy.pop(i)
            if(isMax == True):
                update(stateCopy, move[0], move[1], player)
                curScore = alignement(stateCopy, move[0], move[1])+prevScore
                evalVal, evalMove = self.find_move_mini_Max(stateCopy.copy(
                ), possibleMoveCopy, player, curScore, prevOppScore, not(isMax), alpha, beta)
                eval = curScore+evalVal-prevOppScore
                alpha = max(alpha, eval)
                if(eval > maxVal):
                    maxVal = eval
                    moveSelected = move
                if(beta <= alpha):
                    return maxVal, moveSelected

            else:
                update(stateCopy, move[0], move[1], "O"if player == "X"else"X")
                curOppScore = alignement(
                    stateCopy, move[0], move[1])+prevOppScore
                evalVal, evalMove = self.find_move_mini_Max(stateCopy.copy(
                ), possibleMoveCopy, player, prevScore, curOppScore, not(isMax), alpha, beta)
                eval = prevScore+evalVal-curOppScore
                beta = min(beta, eval)
                if(eval < minVal):
                    minVal = eval
                    moveSelected = move
                if(beta <= alpha):
                    return minVal, moveSelected
        # find the score of two player seperately, current self score is Known, opponent score is unknown
        if(isMax == True):
            return maxVal, moveSelected
        else:
            return minVal, moveSelected

    def find_different_of_two_Grid(self, ref_Grid, grid):
        # print("before:",grid)
        for x, row in enumerate(ref_Grid):
            for y, cell in enumerate(row):
                if(ref_Grid[x][y] != None and grid[x][y] == None):
                    print(x, " ", y)
                    return [x, y]
        return NULL


def alignement(grid, x, y):
    # print("xy:",x,y)
    score = 0

    # 1.check horizontal
    if((grid[x][0] != None) and (grid[x][1] != None) and (grid[x][2] != None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5] != None)):
        score += 6
    else:
        if (grid[x][0] != None) and (grid[x][1] != None) and (grid[x][2] != None) and (grid[x][3] == None):
            score += 3
        elif (grid[x][0] == None) and (grid[x][1] != None) and (grid[x][2] != None) and (grid[x][3] != None) and (grid[x][4] == None):
            score += 3
        elif (grid[x][1] == None) and (grid[x][2] != None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5] == None):
            score += 3
        elif (grid[x][2] == None) and (grid[x][3] != None) and (grid[x][4] != None) and (grid[x][5] != None):
            score += 3

    # 2.check vertical
    if((grid[0][y] != None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y] != None) and (grid[5][y] != None)):
        score += 6
    else:
        if (grid[0][y] != None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] == None):
            score += 3
        elif (grid[0][y] == None) and (grid[1][y] != None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y] == None):
            score += 3
        elif (grid[1][y] == None) and (grid[2][y] != None) and (grid[3][y] != None) and (grid[4][y] != None) and (grid[5][y] == None):
            score += 3
        elif (grid[2][y] == None) and (grid[3][y] != None) and (grid[4][y] != None) and (grid[5][y] != None):
            score += 3

    return score


def update(grid, x, y, symbol):
    if(grid[x][y] is None):
        grid[x][y] = symbol
        return True
    print("Cell already used!")
    return False
