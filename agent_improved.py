import queue
import random
import math
import time
import copy
from random import randint
from pip._vendor.chardet.enums import ProbingState
from dataclasses import field


class data:
    def __init__(self, position,surrounding, surroundingCovered, surroundingUncovered, safe, covered, mine, num_mines,num_safe, num_convered, probability, surroundingProbability) :
        self.position = position #Saves the cells positions 
        self.surrounding = surrounding
        self.surroundingCovered = surroundingCovered # Saves surrounding positions
        self.surroundingUncovered = surroundingUncovered
        self.safe = safe # Determines if the cell is safe
        self.covered = covered  # Determines if the cell is covered
        self.mine = mine  # Determines if the cell is a mine
        self.num_mines = num_mines # Determines the number of surrounding mines
        self.num_safe = num_safe # Determines the number of safe squares
        self.num_covered = num_convered # Determines of hidden squares around it
        self.probability = probability #Determines the probability of contaning mines
        self.surroundingProbability = surroundingProbability#Determines the probability that a surrounding position is a mine
        

        
        
def settingDate(field, dim, numMines): # Sets the Data
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
            if((j+1) >= 0 and (j+1) < dim and (i-1) >= 0 and (i-1) < dim) : #Checks to see if the bottom right corner is within the field
                surrounding.append([i-1,j+1])
            if((j-1) >= 0 and (j-1) < dim and (i-1) >= 0 and (i-1) < dim) : #Checks to see if top right corner is within the field
                surrounding.append([i-1,j-1])
            if((j+1) >= 0 and (j+1) < dim) : #Checks to see if the space below is within the field
                surrounding.append([i,j+1])
            if((j-1) >= 0 and (j-1) < dim) : #Checks to see if the space above is within the field
                surrounding.append([i,j-1])  
            
            numCovered = len(surrounding) #gets number of covered cells
            
            totalCells = dim * dim #gets number of total cells 
            
            prob = numMines / totalCells # gets prob of the cell contaning a cell 
            
                 
            holdData = data([i,j], surrounding, surrounding, [],  False, True, False, 0,0,numCovered, prob, 0)
            
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
                print(holdData.num_mines,  end="    ")
            elif(holdData.covered == True):
                print("{:.2f}".format(holdData.probability) ,end="%   ")
                #print("?",end="    ")
             
        print()
    print()
    
def pickCell(field, dim): #picks the next cell the search
    nextCell = getlowestProb(field, dim)
    return nextCell

def revealCell(search, environment):# Reveals the cell
    x = search[0]
    y = search[1]
    return environment[x][y]

    

#Algorithm to determine the next query given the user space. 
def Improved_agent(field, dim, environment, numMines) :
    numCells = dim * dim   #gets total number of cells
    numSafeCells = numCells - numMines # gets total number of cells that are safe
    settingDate(field,dim, numMines) # sets all cells Data
    print_field(field, dim)
    numMinesMissing = numMines
    index = 0
    while(numSafeCells > index):
        search = pickCell(field,dim) # picks cell to search
        print("Agent going to search " , search)
        x = search[0]
        y = search[1]
        searchData = field[x][y]
        searchData.covered = False
        searchData.probability = 0
        reveal = revealCell(search, environment) # reveals the cell
        print(reveal)
        if(reveal == "X"): # if revealed cell is a mine, Game Over
            searchData.mine = True
            print("Agent found a Mine! Agent Lost ):")
            return -1
        else:
            searchData.safe = True
            searchData.num_mines = reveal
            searchData.num_safe = (8 - reveal)
            searchData.num_covered = len(searchData.surroundingCovered)
            # Sets the probability that a surrounding cell is a mine
            if(reveal > 0):
                searchData.surroundingProbability = (reveal / searchData.num_covered) 
            else:
                searchData.surroundingProbability = 0
            
            
            updateSurrounding(searchData, field) # updates the surrounding cells after reveal
            numMinesFound = updateProbability(field, dim, numMinesMissing) # updates probability of all cells
            
            numMinesMissing = numMines - numMinesFound
            
            print_field(field,dim)
            
            index = index + 1
    
    #Agent Wins  
    print("Agent found all the mines")
    print_field(field,dim)
    print("Agent success!!")
    return 1
    

def updateSurrounding(cellData, field):# updates the surrounding cells after getting revealed
    cellPosition = cellData.position
    totalCells = cellData.surroundingCovered + cellData.surroundingUncovered
    for i in range(len(totalCells )):
        position = totalCells[i]
        x = position[0]
        y = position[1]
        updateCell = field[x][y]
        #Moves the reveal cell from covered list to unCovered list for each surrounding reveal cell
        updateCell.surroundingCovered.remove(cellPosition)
        updateCell.surroundingUncovered.append(cellPosition)
        updateCell.num_covered = len(updateCell.surroundingCovered)
   


def updateProbability(field, dim, numMines):# Updates the probability of all cells after revealing a cell
    found = 0
    for i in range(dim):
        for j in range(dim):
            #loop through each cell
            holderCell = field[i][j]
            if(holderCell.safe == True and holderCell.covered == False): #if cell is already revealed
                if(holderCell.num_mines == getNumMinesFound(holderCell, field)):
                    holderCell.surroundingProbability = 0
                elif(holderCell.num_mines > 0):
                    holderCell.surroundingProbability = (holderCell.num_mines / holderCell.num_covered)
                else:
                    holderCell.surroundingProbability = 0
            else:
                numCovered = holderCell.num_covered # gets number of covered cells
                numUnCovered = len(holderCell.surroundingUncovered) #gets of uncovered cells
                totalCells = len(holderCell.surroundingUncovered) + len(holderCell.surroundingCovered) # gets total cells
                surroundingUnCovered = holderCell.surroundingUncovered #Gets the uncovered cells that surrounds the cell

                if(numUnCovered == 0):
                    holderCell.probability = numMines / (dim * dim) #if no revealed cell surrounding, set prob to low
                else:
                    if(holderCell.mine == False):
                        Probs = []
                        for k in range(len(surroundingUnCovered)): #loops through all surrounding cells
                            position = surroundingUnCovered[k]
                            x = position[0]
                            y = position[1]
                            updateCell = field[x][y]
                            #print(updateCell.surroundingProbability)
                            Probs.append(updateCell.surroundingProbability)
                        if(Probs.count(1) >= 1): # if a surrounding prob is 1, cell is 100% a mine
                            holderCell.probability = 1
                            found = found + 1
                            holderCell.mine = True
                        elif(Probs.count(0) >= 1): #if a surrounding prob is 0, cell is 0& a mine
                            holderCell.probability = 0
                        else: #if neither, get the average surrounding prob 
                            average = 0
                            for l in range(len(Probs)):
                                average = average + Probs[l]
                            average = average / numUnCovered
                            holderCell.probability = average # average prob 
    return found


def getlowestProb(field, dim): # returns the lowest probability of the field
    first = True
    currentLowest = []
    lowestProb = 0
    for i in range(dim):
        for j in range(dim):
            check = field[i][j]
            if(check.covered == True):
                if(first == True):
                    lowestProb = check.probability
                    first = False
                prob = check.probability
                if(prob <= lowestProb):
                    lowestProb = prob
                    currentLowest = check.position
    print(currentLowest)
    return currentLowest

def getNumMinesFound(holderCell, field):
    numMinesFound = 0
    for i in range(len(holderCell.surroundingCovered )):
        position = holderCell.surroundingCovered[i]
        x = position[0]
        y = position[1]
        checkCell = field[x][y]
        if(checkCell.mine == True):
            numMinesFound = numMinesFound + 1
    return numMinesFound
            
    

