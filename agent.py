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
            if(randomCell.covered == True):
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
        search = pickCell(field,searchNext)
        print("Agent going to search " , search)
        x = search[0]
        y = search[1]
        searchData = field[x][y]
        searchData.covered = False
        reveal = revealCell(search, environment)
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