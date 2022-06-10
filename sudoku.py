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
        self.value = value
        self.position_row = i
        self.position_column = j
        self.possible_number = set()
    

class Sudoku(object):

    def __init__(self, path):
        self.sudoku, self.missing_positions = self.sudoku_creator(path)
         

    def sudoku_creator(self,path_to_sudoku:str) -> tuple[np.array, list]:
        """This function reads the file with the sudoku and generates the sudoku as a numpy
        array

        Args:
            path_to_sudoku (str): path to the file with the sudoku
            sudoku (np.array): all zeros numpy array of 9 x 9 dimensions

        Returns:
            np.array: the sudoku numpy array with the given numbers as strings and the missing as int
            list: x and y position of the missing values
        """
        sudoku = [ [0]*9 for i in range(9)] #first generate the table (np.zeros((9,9)).astype(int))

        missing_positions = []
        with open(path_to_sudoku) as file_with_sudoku: #Here we open the file:
            for i,line in enumerate(file_with_sudoku): #Get the number of the line
                for j,num in enumerate(line.split()): #Get the number of the column and get the value in that position in the sudoku 
                    if num != '0':    
                        sudoku[i][j] = num #Change the value of 0 to the value in the sudoku
                    else:
                        missing_positions.append((i,j)) #If is a 0 save the position
                        sudoku[i][j] = Missing_value(0,i,j)
        return sudoku, missing_positions

    def get_column(self,j:int) -> list:
        col = [row[j] for row in self.sudoku]
        for i in range(9):
            if(type(col[i]) == Missing_value):
                col[i] = col[i].value
        return col
    
    def get_row(self,i:int) -> list:
        row = self.sudoku[i]
        for i in range(9):
            if(type(row[i]) == Missing_value):
                row[i] = row[i].value
        return row
    
    def make_square(self,i,j):
        """
        This function generates the square corresponding to that possition
        
        :param table: numpy array representing the sudoku  
        :param i: int row index
        :param j: int column index
        :return: list correponding to the numbers in the square
        """
        square = []
        if i in range(0,3): #Top squares
            if j in range(0,3): #Left square
                for x in range(0,3):
                    for y in range(0,3):
                        square.append(self.sudoku[x][y])
            elif j in range(3,6): #Middel square
                for x in range(0,3):
                    for y in range(3,6):
                        square.append(self.sudoku[x][y])
            else: #Right Square
                for x in range(0,3):
                    for y in range(6,9):
                        square.append(self.sudoku[x][y])
        elif i in range(3,6): #Middel Squares
            if j in range(0,3): #Left Squeare
                for x in range(3,6):
                    for y in range(0,3):
                        square.append(self.sudoku[x][y])
            elif j in range(3,6): #Middel Square
                for x in range(3,6):
                    for y in range(3,6):
                        square.append(self.sudoku[x][y])
            else: #Right Square
                for x in range(3,6):
                    for y in range(6,9):
                        square.append(self.sudoku[x][y])
        else: #Bottom Squares
            if j in range(0,3): #Left Squre
                for x in range(6,9):
                    for y in range(0,3):
                        square.append(self.sudoku[x][y])
            elif j in range(3,6): #Middel Square
                for x in range(6,9):
                    for y in range(4,6):
                        square.append(self.sudoku[x][y])
            else: #Right Square
                for x in range(6,9):
                    for y in range(6,9):
                        square.append(self.sudoku[x][y])
        for i in range(9):
            if(type(square[i]) == Missing_value):
                square[i] = square[i].value
        return square

    def evaluate_missing_positions(self):
        """This function will go through each missing position and evaluate its missing value
        """
        
        while True:
            position_filled = []
            for i,position in enumerate(self.missing_positions):
                print(self.sudoku)
                row,column = position
                missing = self.sudoku[row][column]
                #print(self.sudoku)
                #print("is",self.sudoku[row][column])
                self.evaluate(row,column)
                if len(missing.possible_number) == 1:
                    self.sudoku[row][column] = missing.possible_number[0]
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
        self.possible_number = set(not_possibilities).difference(list(range(10)))

    def solve(self,index):
        """
        This function solves the sudoku

        :param index: int index of the positions list
        :return: list[np.array(np.array(int)),bool] The sudoku table and a bool True when the table i correct and full False try a different number
        """
        if index == len(self.missing_positions): #base case (when we locked all the positions)
            return self.sudoku,True
        else:
            flag_return = False
            i,j = self.missing_positions[index] #look at one position in the list
            for x in self.sudoku[i,j].possible_number:
                self.sudoku[i][j].value = x #Try one number
                if self.check(self.sudoku,i,j): #If that number fits correcly
                    self.sudoku,flag_return = solve(index+1) #Look at the next coord in the list
                    if flag_return: #If the self.sudoku is posible 
                        break #sotp trying numbers
            if flag_return: #if sudoku possible
                return self.sudoku,True #return the sudoku
            self.sudoku[i][j].value = 0 #Backtracking
            return self.sudoku,False    
    
    def check(self,i:int,j:int) -> bool:
        """
        This function chakes if a number at a possition is valid
        
        :param table: np.array with where the sudoku is stored
        :param i: int row index
        :param j: int column index 
        :retun: bool True if number is correct, False if number is incorrect
        """
        number = self.sudoku[i][j].value #First get the number we want to check
        if self.get_row.count(number) > 1: #check the row possition   
            return False
        if self.get_column.count(number) > 1:#Here we check the column
            return False
        my_square = make_square(i,j) #Get the square corresponding to that number
        if np.count_nonzero(my_square == number) > 1:
            return False
        return True

def sudoku_solver():
    my_sudoku = Sudoku(sys.argv[1])
    my_sudoku.evaluate_missing_positions()
    #my_sudoku.solve()
    #print(my_sudoku.sudoku)

if __name__ == "__main__":
    sudoku_solver()
