from pickle import NONE
from itertools import chain 
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
class Missing_value(object): 
    """This class represents the missing value
    """
    def __init__(self,value:int,i:int,j:int):
        self.__value__ = value
        self.position_row = i
        self.position_column = j
        self.possible_number = set()
    
    def set_value(self,value) -> None:
        self.__value__ = value
    
    def get_value(self) -> int:
        return self.__value__

    def __repr__(self) -> str:
        return str(self.get_value())
    
class Value_sudoku():
    def __init__(self,value, i, j):
        self.given_value = None
        self.missing_value = None
        self.set_value(value,i,j)

    def __repr__(self):
        if self.given_value == None:
            return str(self.missing_value.get_value())
        return str(self.given_value)

    def set_value(self,value,i,j):
        if value == '0':
            self.missing_value = Missing_value(value,i,j)
            self.given_value = None
        else:
            self.given_value = value
            self.missing_value = None
    
    def from_missing_to_given(self,value):
        self.given_value = value
        self.missing_value = None
    
    def get_value(self):
        if self.given_value == None:
            return int(self.missing_value.get_value())
        return int(self.given_value)

class Sudoku(object):

    def __init__(self, path):
        self.sudoku, self.missing_positions = self.sudoku_creator(path)
         

    def sudoku_creator(self,path_to_sudoku:str) -> tuple[np.array, list]:
        """This function reads the file with the sudoku and generates the sudoku as a numpy
        array

        Args:
            path_to_sudoku (str): path to the file with the sudoku
        Returns:
            np.array: the sudoku numpy array with the given numbers as strings and the missing as int
            list: x and y position of the missing values
        """
        sudoku = [ [0]*9 for i in range(9)] #first generate the table (np.zeros((9,9)).astype(int))
        missing_positions = []

        with open(path_to_sudoku) as file_with_sudoku: #Here we open the file:
            for i,line in enumerate(file_with_sudoku): #Get the number of the line
                for j,num in enumerate(line.split()): #Get the number of the column and get the value in that position in the sudoku 
                    sudoku[i][j] = Value_sudoku(num,i,j)
                    if num == '0': 
                        missing_positions.append((i,j)) #If is a 0 save the position

        return sudoku, missing_positions

    def get_column(self,j:int) -> list:
        col = [row[j].get_value() for row in self.sudoku]
        return col
    
    def get_row(self,row_number:int) -> list:
        row = self.sudoku[row_number].copy()
        for i in range(9):
            row[i] = row[i].get_value()
        return row
    
    def make_square(self,i:int,j:int) -> list:
        """
        This function generates the square corresponding to that possition
        
        :param i: int row index
        :param j: int column index
        :return: list correponding to the numbers in the square
        """
        square = []
        if i in range(0,3): #Top squares
            if j in range(0,3): #Left square
                for x in range(0,3):
                    for y in range(0,3):
                        square.append(self.sudoku[x][y].get_value())
            elif j in range(3,6): #Middel square
                for x in range(0,3):
                    for y in range(3,6):
                        square.append(self.sudoku[x][y].get_value())
            else: #Right Square
                for x in range(0,3):
                    for y in range(6,9):
                        square.append(self.sudoku[x][y].get_value())
        elif i in range(3,6): #Middel Squares
            if j in range(0,3): #Left Squeare
                for x in range(3,6):
                    for y in range(0,3):
                        square.append(self.sudoku[x][y].get_value())
            elif j in range(3,6): #Middel Square
                for x in range(3,6):
                    for y in range(3,6):
                        square.append(self.sudoku[x][y].get_value())
            else: #Right Square
                for x in range(3,6):
                    for y in range(6,9):
                        square.append(self.sudoku[x][y].get_value())
        else: #Bottom Squares
            if j in range(0,3): #Left Squre
                for x in range(6,9):
                    for y in range(0,3):
                        square.append(self.sudoku[x][y].get_value())
            elif j in range(3,6): #Middel Square
                for x in range(6,9):
                    for y in range(3,6):
                        square.append(self.sudoku[x][y].get_value())
            else: #Right Square
                for x in range(6,9):
                    for y in range(6,9):
                        square.append(self.sudoku[x][y].get_value())
        return square

    def evaluate_missing_positions(self):
        """This function will go through each missing position and evaluate its missing value
        """
        while True:
            position_filled = []
            for i,position in enumerate(self.missing_positions):
                row,column = position
                missing = self.sudoku[row][column]
                self.evaluate(row,column)
                if len(missing.missing_value.possible_number) == 1:
                    self.sudoku[row][column].from_missing_to_given(missing.missing_value.possible_number[0])
                    position_filled.append(i)
            if len(position_filled) >= 1:
                del self.missing_positions[position_filled]
            else: 
                return None
  
    def evaluate(self, i,j) -> None:
        """
        This function updates the possible numbers

        :param i: int row index
        :param j: int column index
        """

        not_possibilities = []
        row = self.get_row(i)
        for num in row:
            if num != 0:
                not_possibilities.append(num)
        column = self.get_column(j)
        for num in column:
            if num != 0:
                not_possibilities.append(num)
        square = self.make_square(i,j)
        for num in square:
            if num != 0:
                not_possibilities.append(num)
        not_possibilities = set(not_possibilities)
        self.sudoku[i][j].missing_value.possible_number = not_possibilities.difference(set(range(1,10)))

    def inspection(self):
        change_done = True
        while change_done:
            change_done = False
            for row_number in range(9):
                row = self.get_row(row_number)
                if 0 in row:
                    row_missing_index = list(np.where(np.array(row) == 0)[0])
                    missing_in_row = []
                    for col_number in row_missing_index:
                        col = self.get_column(col_number)
                        sqr = self.make_square(row_number,col_number)
                        row_test = self.get_row(row_number)
                        numbers_given = set(col + sqr + row_test)
                        numbers_given.remove(0)
                        missing_in_row.append(list(set(range(1,10)).difference(numbers_given)))
                    change_done = True
                    if row_number == 4:
                        print(missing_in_row)
                    while change_done:
                        change_done = False
                        for x in range(len(missing_in_row)):
                            test = set(missing_in_row.pop(0)) 
                            rest = missing_in_row.copy()
                            rest = set(list(chain.from_iterable(rest)))
                            aveliable = test.difference(rest)
                            if len(aveliable) == 1:
                                index_col = row_missing_index.pop(x) 
                                self.sudoku[row_number][index_col].from_missing_to_given(list(aveliable)[0])
                                change_done = True
                            else: 
                                missing_in_row.append(test)
                

    def solve(self,index):
        """
        This function solves the sudoku

        :param index: int index of the positions list
        :return: list, bool The sudoku table and a bool True when the table i correct and full False try a different number
        """
        if index == len(self.missing_positions): #base case (when we locked all the positions)
            return self.sudoku,True
        else:
            flag_return = False
            i,j = self.missing_positions[index] #look at one position in the list
            for x in self.sudoku[i][j].missing_value.possible_number:
                self.sudoku[i][j].value = x #Try one number
                if self.check(self.sudoku,i,j): #If that number fits correcly
                    self.sudoku,flag_return = self.solve(index+1) #Look at the next coord in the list
                    if flag_return: #If the self.sudoku is posible 
                        break #sotp trying numbers
            if flag_return: #if sudoku possibleç
                self.sudoku[i][j].from_missing_to_given(self.sudoku[i][j].get_value())
                return self.sudoku,True #return the sudoku
            self.sudoku[i][j].value = 0 #Backtracking
            return self.sudoku,False    
    
    def check(self,i:int,j:int) -> bool:
        """
        This function chakes if a number at a possition is valid
        
        :param i: int row index
        :param j: int column index 
        :retun: bool True if number is correct, False if number is incorrect
        """
        number = self.sudoku[i][j].value #First get the number we want to check
        if self.get_row.count(number) > 1: #check the row possition   
            return False
        if self.get_column.count(number) > 1:#Here we check the column
            return False
        my_square = self.make_square(i,j) #Get the square corresponding to that number
        if np.count_nonzero(my_square == number) > 1:
            return False
        return True

    def print_sudoku(self):
        for x in range(9):    
            print(self.sudoku[x][0:3],"|",self.sudoku[x][3:6],"|",self.sudoku[x][6:9])
            if x == 2 or x == 5:
                print("-"*33)

def sudoku_solver():
    my_sudoku = Sudoku(sys.argv[1])
    my_sudoku.print_sudoku()
    print("\n"*2)
    my_sudoku.evaluate_missing_positions()
    my_sudoku.inspection()
    my_sudoku.print_sudoku()


    #my_sudoku.solve(0)
    #my_sudoku.print_sudoku()

if __name__ == "__main__":
    sudoku_solver()
