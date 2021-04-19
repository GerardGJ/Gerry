import sys
import numpy as np
#Possible input:
#5 3 0 0 7 0 0 0 0
#6 0 0 1 9 5 0 0 0
#0 9 8 0 0 0 0 6 0
#8 0 0 0 6 0 0 0 3
#4 0 0 8 0 3 0 0 1
#7 0 0 0 2 0 0 0 6
#0 6 0 0 0 0 2 8 0
#0 0 0 4 1 9 0 0 5
#0 0 0 0 8 0 0 7 9

#0 = missing numbers

table = np.zeros((9,9)).astype(int) #first generate the table 

#This function will generate the table where the numbers are stored
def table_modi(name,table):
    positions = []
    to_do = open(name) #Here we open the file
    for i,line in enumerate(to_do): #Get the number of the line
        for j,num in enumerate(line.split()): #Get the number of the column and get the value in that position in the sudoku 
            if num != '0':    
                table[i][j] = num #Change the value of 0 to the value in the sudoku
            else:
                positions.append((i,j)) #If is a 0 save the position
    return table,positions

def check(table,i,j):
    number = table[i][j] #First get the number we want to check
    for x,l in enumerate(table[i]): #Here we check the line 
        if l == number and j != x: #If is the same number and is in a different position   
            return False
    for x,l in enumerate(table[:,j]):#Here we check the column
        if l == number and i != x: #If is the same number and is in a different position
            return False
    my_square = make_square(table,i,j) #Get the square corresponding to that number
    repeated = 0 
    for l in my_square: #Get the number of times the number is repeated
        if l == number:
            repeated +=1
        if repeated>1: #If repeated more than one time
            return False
    return True

def possible_numbers(table,i,j):
    not_possibilities = []
    line = table[i]
    for num in line:
        if num != 0:
            not_possibilities.append(num)
    column = table[:,j]
    for num in column:
        if num not in not_possibilities and num != 0:
            not_possibilities.append(num)
    square = make_square(table,i,j)
    for num in square:
        if num not in not_possibilities and num != 0:
            not_possibilities.append(num)
    return not_possibilities

#This function make the squares            
def make_square(table,i,j):
    square = []
    if i in range(0,3): #Top squares
        if j in range(0,3): #Left square
            for x in range(0,3):
                for y in range(0,3):
                    square.append(table[x,y])
        elif j in range(3,6): #Middel square
            for x in range(0,3):
                for y in range(3,6):
                    square.append(table[x,y])
        else: #Right Square
            for x in range(0,3):
                for y in range(6,9):
                    square.append(table[x,y])
    elif i in range(3,6): #Middel Squares
        if j in range(0,3): #Left Squeare
            for x in range(3,6):
                for y in range(0,3):
                    square.append(table[x,y])
        elif j in range(3,6): #Middel Square
            for x in range(3,6):
                for y in range(3,6):
                    square.append(table[x,y])
        else: #Right Square
            for x in range(3,6):
                for y in range(6,9):
                    square.append(table[x,y])
    else: #Bottom Squares
        if j in range(0,3): #Left Squre
            for x in range(6,9):
                for y in range(0,3):
                    square.append(table[x,y])
        elif j in range(3,6): #Middel Square
            for x in range(6,9):
                for y in range(4,6):
                    square.append(table[x,y])
        else: #Right Square
            for x in range(6,9):
                for y in range(6,9):
                    square.append(table[x,y])
    return square

#This function will fill the different spaces of the sudoku
def solve(table,index,positions):
    if index == len(positions): #base case (when we locked all the positions)
        return table,True
    else:
        flag_return = False
        i,j = positions[index] #look at one position in the list
        not_poss = possible_numbers(table,i,j)
        for x in range(1,10):
            if x not in not_poss:
                table[i][j] = x #Try one number
                if check(table,i,j): #If that number fits correcly
                    table,flag_return = solve(table,index+1,positions) #Look at the next coord in the list
                    if flag_return: #If the table is posible 
                        break #sotp trying numbers
        if flag_return: #if table possible
            return table,True #return the table
        table[i][j]= 0 #Backtracking
        return table,False    

table,positions = table_modi(sys.argv[1],table)
print(solve(table,0,positions))

