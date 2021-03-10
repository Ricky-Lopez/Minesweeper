import agent
import queue
import random
import math
import time
import copy
from random import randint


def create_minefield(dim,n): #creates a minefield given dim dimension and n mines.
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

            if((i+1) >= 0 and (i+1) < dim) : # Checks to see if space to the left is within the field
                if(field[i+1][j] == 'X') : #Checks to see if space to the left has a mine
                    mineCounter = mineCounter + 1

            if((j+1) >= 0 and (j+1) < dim and (i+1) >= 0 and (i+1) < dim) : #Checks to see if the bottom left corner is within the field
                if(field[i+1][j+1] == 'X') : #Checks to see if bottom left corner has a mine
                    mineCounter = mineCounter + 1
                
            if((j-1) >= 0 and (j-1) < dim and (i+1) >= 0 and (i+1) < dim) : #Checks to see if top left corner is within the field
                if(field[i+1][j-1] == 'X') : #Checks to see if top left corner has a mine
                    mineCounter = mineCounter + 1

            if((i-1) >= 0 and (i-1) < dim) : #Checks to see if space to the right is within the field
                if(field[i-1][j] == 'X') : #Checks to see if space to the right has a mine
                    mineCounter = mineCounter + 1

            if((j+1) >= 0 and (j+1) < dim and (i-1) >- 0 and (i-1) < dim) : #Checks to see if the bottom right corner is within the field
                if(field[i-1][j+1] == 'X') : #Checks to see if bottom right corner has a mine
                    mineCounter = mineCounter + 1
                
            if((j-1) >= 0 and (j-1) < dim and (i-1) >= 0 and (i-1) < dim) : #Checks to see if top right corner is within the field
                if(field[i-1][j-1] == 'X') : #Checks to see if top right corner has a mine
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

def print_field(field,dim): #prints out the field. 
    columns = rows = 0
    print(" ",end="      ")
    for i in range(dim):
        if(columns < 10):
            print(columns, end="    ")
        elif(columns < 100):
            print(columns, end="   ")
        elif(columns < 1000):
            print(columns, end="  ")
        else:
            print(columns, end=" ")
        columns = columns + 1

    print("\n")
    for i in range(dim):
        if(rows < 10):
            print(rows, end="      ")
        elif(rows < 100):
            print(rows, end="     ")
        elif(rows < 1000):
            print(rows, end="    ")
        else:
            print(rows, end="   ")
        rows = rows + 1
        for j in range(dim):
            print(field[i][j],end="    ")
        print()
    print()

#check_position
#real_field = actual 2Dimensional array used to hold data for mines, and mine proximities.
#user_field = 2dimensional copy that holds data hidden and non hidden spaces as the game progresses.
#   pos     = position queried by user.
def check_position(real_field, user_field, pos) : #checks if position queried is a mine, and if not, reveals space in user_field. 
    if (real_field[pos[0]][pos[1]] == 'X') : #Position queried is a mine; GAMEOVER
        user_field[pos[0]][pos[1]] = 'X'
        print("-- GAMEOVER --")
        return False

    elif (real_field[pos[0]][pos[1]] == 0) : #CLEARS MULTIPLE SPACES ON SINGULAR QUERY
        
        if(user_field[pos[0]][pos[1]] == '-') :
            if((pos[0]+1) >= 0 and (pos[0]+1) < dim) :
                user_field[pos[0]][pos[1]] = real_field[pos[0]][pos[1]]
                check_position(real_field, user_field, [pos[0]+1, pos[1]]) #checks the position on the below
                if((pos[1]+1) >= 0 and (pos[1]+1) < dim) :
                    check_position(real_field, user_field, [pos[0]+1, pos[1]+1]) #checks bottom right corner
                if((pos[1]-1) >= 0 and (pos[1]-1) < dim) :
                    check_position(real_field, user_field, [pos[0]+1, pos[1]-1]) #checks top right corner
            if((pos[0]-1) >= 0 and (pos[0]-1) < dim) :
                user_field[pos[0]][pos[1]] = real_field[pos[0]][pos[1]]
                check_position(real_field, user_field, [pos[0]-1, pos[1]]) #checks the position on the above
                if((pos[1]+1) >= 0 and (pos[1]+1) < dim) :
                    check_position(real_field, user_field, [pos[0]-1, pos[1]+1]) #checks bottom left corner
                if((pos[1]-1) >= 0 and (pos[1]-1) < dim) :
                    check_position(real_field, user_field, [pos[0]-1, pos[1]-1]) #checks top left corner
            if((pos[1]+1) >= 0 and (pos[1]+1) < dim) :
                user_field[pos[0]][pos[1]] = real_field[pos[0]][pos[1]]
                check_position(real_field, user_field, [pos[0], pos[1]+1]) #checks the position to the right
                if((pos[0]+1) >= 0 and (pos[0]+1) < dim) :
                    check_position(real_field, user_field, [pos[0]+1, pos[1]+1]) #checks bottom right corner
                if((pos[0]-1) >= 0 and (pos[0]-1) < dim) :
                    check_position(real_field, user_field, [pos[0]-1, pos[1]+1]) #checks top right corner
            if((pos[1]-1) >= 0 and (pos[1]-1) < dim) :
                user_field[pos[0]][pos[1]] = real_field[pos[0]][pos[1]]
                check_position(real_field, user_field, [pos[0], pos[1]-1]) #checks the position to the left
                if((pos[0]+1) >= 0 and (pos[0]+1) < dim) :
                    check_position(real_field, user_field, [pos[0]+1, pos[1]-1]) #checks bottom right corner
                if((pos[0]-1) >= 0 and (pos[0]-1) < dim) :
                    check_position(real_field, user_field, [pos[0]-1, pos[1]-1]) #checks top right corner
        
    else:
        user_field[pos[0]][pos[1]] = real_field[pos[0]][pos[1]]
    return True
    #TODO: add multispace clear when position queried has no mine proximities.


def win_condition(user_field) : #Checks if win condition has been met.
    for i in range(len(user_field)) :
        for j in range(len(user_field)) :
            if(user_field[i][j] == '-') :
                return False
    return True

#Main Function
if __name__ == "__main__":

    dim = int(input("Please input the size of the minefield:\n"))
    mines = int(input("Please input the amount of mines in the minefield:\n"))
    whoPlays = input("Let the Agent play? (y/n)\n")
    whoPlays.lower()
    if(whoPlays == 'y' or whoPlays == 'yes'):
        whoPlays = True
    elif(whoPlays == 'n' or whoPlays == 'no'):
        whoPlays = False
    else:
        print("I'm sorry, I don't think I understand. I'll just let the Agent play.", end="\n\n")
        whoPlays = False

    real_field = create_minefield(dim, mines)
    user_field = create_userField(dim)
    #print_field(real_field, dim)
    #print_field(user_field, dim)

    if(whoPlays) :  #Agent plays
        #TODO add Agent algorithm.
        agent = 0
    else:           #User plays
        print("\n******** MINESWEEPER *********\nRULES:\n\n1. Enter the position you would like to query in the format \"x,y\".\n2. To flag, type \"flag \" before your position. (Don't forget the space!)\n3. To quit, enter \"q\".\n4. Have fun playing!\n\n")
        gameContinue = True
        print_field(user_field, dim)
        while(gameContinue) :
            user_input = input("Please enter the position you would like to check: ")
            user_input.lower()
            if(user_input == "q") :
                gameContinue = False
            elif "flag" in user_input : # Flag Feature!
                try:
                    user_field[int(user_input[7])][int(user_input[5])] = 'F'
                    print()
                    print_field(user_field, dim)
                except ValueError:
                    print("Invalid format. Please try again.\n")
            else:
                try:
                    gameContinue = check_position(real_field, user_field, [int(user_input[2]), int(user_input[0])])
                    gameContinue = gameContinue and not(win_condition(user_field))
                    print()
                    print_field(user_field, dim)
                except ValueError:
                    print("Invalid format. Please try again.\n")

