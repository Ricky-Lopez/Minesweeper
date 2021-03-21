import queue
import random
import math
import time
import copy
from random import randint


class data:
    def __init__(self, position, surroundingPositions, safe, covered, mine, num_mines,num_safe, num_convered) :
        self.position = position #Saves the cells positions 
        self.surroundingPositions = surroundingPositions # Saves surrounding positions
        self.safe = safe # Determines if the cell is safe
        self.covered = covered  # Determines if the cell is covered
        self.mine = mine  # Determines if the cell is a mine
        self.num_mines = num_mines # Determines the number of surrounding mines
        self.num_safe = num_safe # Determines the number of safe squares
        self.num_covered = num_convered # Determines of hidden squares around it

        # Probability that will be used for strong inference. If uncovered, probability variable will determine the probability of there
        # being a mine at any of its surrounding positions, which is calculated by: # of hidden surrounding mines / # of hidden surrounding cells.
        # if covered, the probability variable will hold the probability of there being a mine in that position, which is calculated by:
        # sum of the uncovered, adjacent position's probabilities / amount of uncovered, adjacent positions.
        self.probability = 0 
        
def settingDate(field, dim): # Sets the Data
    for i in range(dim):
        for j in range(dim):
            surrounding = []
            if((i+1) >= 0 and (i+1) < dim) : # Checks to see if space to the left is within the field
                surrounding.append([i+1,j])
            if((j+1) >= 0 and (j+1) < dim and (i+1) >= 0 and (i+1) < dim) : #Checks to see if the bottom left corner is within the field
                surrounding.append([i+1,j+1])
            if((j-1) >= 0 and (j-1) < dim and (i+1) >= 0 and (i+1) < dim) : #Checks to see if top left corner is within the field
                surrounding.append([i+1,j-1])
            if((i-1) >= 0 and (i-1) < dim) : #Checks to see if space to the right is within the field
                surrounding.append([i-1,j])
            if((j+1) >= 0 and (j+1) < dim and (i-1) >- 0 and (i-1) < dim) : #Checks to see if the bottom right corner is within the field
                surrounding.append([i-1,j+1])
            if((j-1) >= 0 and (j-1) < dim and (i-1) >= 0 and (i-1) < dim) : #Checks to see if top right corner is within the field
                surrounding.append([i-1,j-1])
            if((j+1) >= 0 and (j+1) < dim) : #Checks to see if the space below is within the field
                surrounding.append([i,j+1])
            if((j-1) >= 0 and (j-1) < dim) : #Checks to see if the space above is within the field
                surrounding.append([i,j-1])  
            
            numCovered = len(surrounding)
                 
            holdData = data([i,j], surrounding, False, True, False, 0,0,numCovered)
            
            field[i][j] = holdData

    return

def print_field(field,dim): #prints out the field. 
    print()
    print("Agent Field:")
    print()
    for i in range(dim):
        for j in range(dim):
            holdData = field[i][j]
            if(holdData.mine == True):
                print("M",end="    ") 
            elif(holdData.safe == True ):
                print(holdData.num_mines,end="    ")
            elif(holdData.covered == True):
                print("?",end="    ")
             
        print()
    print()
    
def pickCell(field, nextCell): #picks the next cell the search
    if(nextCell == []):
        while(1):
            randX = randint(0, len(field)-1)
            randY = randint(0, len(field)-1)
            randomCell = field[randX][randY]
            if(randomCell.covered == True and not(randomCell.mine) ):
                return [randX,randY]        
    nextData = nextCell.pop()  
    return nextData

def revealCell(search, environment):# Reveals the cell
    x = search[0]
    y = search[1]
    return environment[x][y]

    

#Algorithm to determine the next query given the user space. 
def Basic_agent(field, dim, environment, numMines) :
    numRevealedMines = 0
    settingDate(field,dim)
    print_field(field, dim)
    searchNext = []
    while(1):
        if(searchNext) : #searchNext is not empty

            search = pickCell(field,searchNext)
            print("Agent going to search " , search)
            x = search[0]
            y = search[1]
            searchData = field[x][y]
            searchData.covered = False
            reveal = revealCell(search, environment)
        else : #searchNext is empty
            advancedList = Advanced_agent(field, dim, environment)
            nextCell = pickCell(field, advancedList)
            x = nextCell[0]
            y = nextCell[1]
            searchData = field[x][y]
            searchData.covered = False
            reveal = revealCell(nextCell, environment)
        print(reveal)
        if(reveal == "X"):
            searchData.mine = True
            print("Agent found a Mine! Agent Lost ):")
            return
        else:
            searchData.safe = True
            searchData.num_mines = reveal
            searchData.num_safe = (8 - reveal)
            coveredAmount = getCoveredNum(searchData.surroundingPositions, field)
            print("Agent found a Safe Cell! (:")
            print_field(field,dim)
            if(reveal == 0):
                coveredCells = findCovered(searchData.surroundingPositions, field, searchNext)
                searchNext.extend(coveredCells)
            if(reveal - numRevealedMines == coveredAmount):
                for i in range(len(searchData.surroundingPositions)):
                    position = searchData.surroundingPositions[i]
                    x = position[0]
                    y = position[1]
                    holderCell = field[x][y]
                    if(holderCell.covered == True):
                        holderCell.mine = True
                        numRevealedMines = numRevealedMines + 1
                        print("Agent found mine")
                        print_field(field,dim)
            coveredAmount = getCoveredNum(searchData.surroundingPositions, field)
            uncoveredAmount = 8 - coveredAmount
            if(searchData.num_safe - uncoveredAmount == coveredAmount):
                coveredCells = findCovered(searchData.surroundingPositions, field, searchNext)
                searchNext.extend(coveredCells)
        if(numRevealedMines == numMines):
            print("Agent found all the mines")
            print_field(field,dim)
            return
                    
                
                
    return

def findCovered(surrounding , field, searchNext): #Return all covered cells
    coveredCell = []
    for i in range(len(surrounding)):
        position = surrounding[i]
        x = position[0]
        y = position[1]
        check = field[x][y]
        if(check.covered == True and searchNext.count(position) == 0 and check.mine == False):
            coveredCell.append(surrounding[i])
    return coveredCell

def getCoveredNum(surrounding, field):# Return amount of covered cells 
    coveredAmount = 0
    for i in range(len(surrounding)):
        position = surrounding[i]
        x = position[0]
        y = position[1]
        check = field[x][y]
        if(check.covered == True):
            coveredAmount = coveredAmount + 1
    return coveredAmount
        

def getSolvedMines(surrounding, field):# Return amount of mines that have been discovered
    mineAmount = 0
    for i in range(len(surrounding)):
        position = surrounding[i]
        x = position[0]
        y = position[1]
        check = field[x][y]
        if(check == 'M'):
            mineAmount = mineAmount + 1
    return mineAmount

##Advanced_agent
#If a hidden position is surrounded by two or more open, safe positions, we will perform strong inference. These open, safe positions shall be our "pivots".
#Hidden position in question shall be our "anchor".

#Perform a guess and check of all positions surrounding pivots, by initially assigning our anchor as a mine or as safe. If we come to a contradiction, backtrack through tree
#of all possible positions and try a new route through the tree. If we cannot come to a full possible assignment of the positions surrounding the pivots, then whatever we
#assigned our anchor to be is not possible, and therefore we can conclude that the anchor must be the opposite.
def Advanced_agent(field, dim, environment) :

    print("BEGINNING ADVANCED AGENT.. ")
    #Basic_agent(field, dim, environment)
    #TODO ensure proper integration of Basic_agent() algorithm.
    pivots = []
    potentialQueries = []
    for i in range(dim) :
        for j in range(dim) :
            adjacentClues = 0
            if(field[i][j].covered) : #The position in question is covered.
                
                if((i+1) >= 0 and (i+1) < dim) : # Checks to see if space to the left is within the field
                    if(not(field[i+1][j].covered) ) : #Checks to see if space to the left is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i+1][j])                        

                if((j+1) >= 0 and (j+1) < dim and (i+1) >= 0 and (i+1) < dim) : #Checks to see if the bottom left corner is within the field
                    if(not(field[i+1][j+1].covered) ) : #Checks to see if bottom left corner is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i+1][j+1])                        
                    
                if((j-1) >= 0 and (j-1) < dim and (i+1) >= 0 and (i+1) < dim) : #Checks to see if top left corner is within the field
                    if(not(field[i+1][j-1].covered) ) : #Checks to see if top left corner is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i+1][j-1])                        

                if((i-1) >= 0 and (i-1) < dim) : #Checks to see if space to the right is within the field
                    if(not(field[i-1][j].covered) ) : #Checks to see if space to the right is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i-1][j])                        

                if((j+1) >= 0 and (j+1) < dim and (i-1) >- 0 and (i-1) < dim) : #Checks to see if the bottom right corner is within the field
                    if(not(field[i-1][j+1].covered) ) : #Checks to see if bottom right corner is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i-1][j+1])                        
                    
                if((j-1) >= 0 and (j-1) < dim and (i-1) >= 0 and (i-1) < dim) : #Checks to see if top right corner is within the field
                    if(not(field[i-1][j-1].covered) ) : #Checks to see if top right corner is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i-1][j-1])                        

                if((j+1) >= 0 and (j+1) < dim) : #Checks to see if the space below is within the field
                    if(not(field[i][j+1].covered) ) : #Checks to see if the space below is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i][j+1])                         

                if((j-1) >= 0 and (j-1) < dim) : #Checks to see if the space above is within the field
                    if(not(field[i][j-1].covered) ) : #Checks to see if the space above is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[i][j-1])

                if(adjacentClues > 1) : #There are two or more clues next to the position in question, therefore we shall perform strong inference.
                    pos = field[i][j]
                    totalProb = 0
                    for pivot in pivots: # solves for the probability of the adjacent pivots.
                        coveredPositions = getCoveredNum(pivot.surroundingPositions, field)
                        solvedMines = getSolvedMines(pivot.surroundingPositions, field)
                        pivot.probability = (pivot.num_mines - solvedMines) / coveredPositions
                        totalProb = totalProb + pivot.probability
                    pos.probability = totalProb / len(pivots) #final probability of position in question. 
                    potentialQueries.append(pos)
    
    if(not(potentialQueries)) : #potentialQueries is empty, resort to guessing.
        return []
    safestPosition = potentialQueries[0]
    for position in potentialQueries:
        if(position.probability < safestPosition.probability) :
            safestPosition = position
    safestPositionList = []
    safestPositionList.append(safestPosition.position) #Had to put the safest position in a list to pass it to the revealCell() function.
    return safestPositionList

                                            


                    

                        
                    
