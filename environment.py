import agent
import queue
import random
import math
import time
import copy
from random import randint


def create_minefield(dim,n): # creates a minefield given dim dimension and n mines.
    field=[]
    for i in range(dim): #minefield creation
        c=[]
        for j in range(dim):
            j = "-"
            c.append(j)
        field.append(c)
    
    mines = n
    while (mines): #adding mines
        x = randint(0, dim-1)
        y = randint(0, dim-1)
        if (field[x][y] == 'X'):
            continue
        field[x][y] = 'X'
        mines = mines - 1

    for i in range(dim):
        for j in range(dim):
            mineCounter = 0
            if(field[i][j] == 'X') :
                continue

            if((i+1) >= 0 and (i+1) < dim) : # Checks to see if space to the right is within the field
                if(field[i+1][j] == 'X') : #Checks to see if space to the right has a mine
                    mineCounter = mineCounter + 1

                if((j+1) >= 0 and (j+1) < dim) : #Checks to see if the bottom right corner is within the field
                    if(field[i+1][j+1] == 'X') : #Checks to see if bottom right corner has a mine
                        mineCounter = mineCounter + 1
                
                if((j-1) >= 0 and (j-1) < dim) : #Checks to see if top right corner is within the field
                    if(field[i+1][j-1] == 'X') : #Checks to see if top right corner has a mine
                        mineCounter = mineCounter + 1
            if((i-1) >= 0 and (i-1) < dim) : #Checks to see if space to the left is within the field
                if(field[i-1][j] == 'X') : #Checks to see if space to the left has a mine
                    mineCounter = mineCounter + 1

                if((j+1) >= 0 and (j+1) < dim) : #Checks to see if the bottom left corner is within the field
                    if(field[i-1][j+1] == 'X') : #Checks to see if bottom left corner has a mine
                        mineCounter = mineCounter + 1
                
                if((j-1) >= 0 and (j-1) < dim) : #Checks to see if top left corner is within the field
                    if(field[i-1][j-1] == 'X') : #Checks to see if top left corner has a mine
                        mineCounter = mineCounter + 1

            if((j+1) >= 0 and (j+1) < dim) : #Checks to see if the space below is within the field
                if(field[i][j+1] == 'X') : #Checks to see if the space below has a mine
                    mineCounter = mineCounter + 1 
            
            if((j-1) >= 0 and (j-1) < dim) : #Checks to see if the space above is within the field
                if(field[i][j-1] == 'X') : #Checks to see if the space above has a mine 
                    mineCounter = mineCounter + 1
        
            field[i][j] = mineCounter       

    return field # returns a two dimensional array representing the field

def create_userField(dim) : #field duplicate for user exploration
    field = []
    for i in range(dim) :
        c = []
        for j in range(dim) :
            j = "-"
            c.append(j)
        field.append(c)
    return field

def print_field(field,dim): #prints out the field, with all numbers and mines unhidden. 
    for i in range(dim):
        for j in range(dim):
            print(field[i][j],end="    ")
        print()
    print()
 
#Main Function
if __name__ == "__main__":

    dim = int(input("Please input the size of the minefield: "))
    mines = int(input("Please input the amount of mines in the minefield: "))

    minefield = create_minefield(dim, mines)
    userField = create_userField(dim)
    print_field(minefield, dim)
    print_field(userField, dim)
    