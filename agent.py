import environment
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
        self.covered = covered  # Determines if the cell is not covered
                        adjacentClues = adjacentClues + 1
                        pivots.append(field[][])        self.mine = mine  # Determines if the cell is a mine
        self.num_mines = num_mines # Determines the number of surrounding mines
        self.num_safe = num_safe # Determines the number of safe squares
        self.num_covered = num_convered # Determines of hidden squares around it
        
def settingDate(field, dim): 
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
           if(holdData.covered == True):
                print("?",end="    ")
           if(holdData.safe == True ):
                print(holdData.num_mines,end="    ")
           if(holdData.mine == True):
                print("M",end="    ")  
        print()
    print()
    
def pickCell(field, previous):
    if(previous == []):
        while(1):
            randX = randint(0, len(field)-1)
            randY = randint(0, len(field)-1)
            randomCell = field[randX][randY]
            if(randomCell.covered == True):
                return [randX,randY]
            
         
    return

def revealCell(search, environment):
    x = search[0]
    y = search[1]
    return environment[x][y]

    

#Algorithm to determine the next query given the user space. 
def Basic_agent(field, dim, environment) :
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
            print_field(field,dim)
        else:
            searchData.safe = True
            searchData.num_mines = reveal
            searchData.num_safe = (8 - reveal)
            print("Agent found a Safe Cell! (:")
            print_field(field,dim)
        return


class Node:
    def __init__ () :
        

##Advanced_agent
#If a hidden position is surrounded by two or more open, safe positions, we will perform strong inference. These open, safe positions shall be our "pivots".
#Hidden position in question shall be our "anchor".

#Perform a guess and check of all positions surrounding pivots, by initially assigning our anchor as a mine or as safe. If we come to a contradiction, backtrack through tree
#of all possible positions and try a new route through the tree. If we cannot come to a full possible assignment of the positions surrounding the pivots, then whatever we
#assigned our anchor to be is not possible, and therefore we can conclude that the anchor must be the opposite.
def Advanced_agent(field, dim, environment) :

    #Basic_agent(field, dim, environment)
    #TODO ensure proper integration of Basic_agent() algorithm.
    pivots = []
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
                    


                    

                        
                    
