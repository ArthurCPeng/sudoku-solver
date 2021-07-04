import time
import random
import sys
import os

#If backtracking is needed to solve, increase the recursion limit, and set a reporting frequency
sys.setrecursionlimit(100000)
report_frequency = 100
current_steps = []
bad_steps = []
number_of_steps = 0

#Set a time limit after which the program automatically ends
time_limit = 3600
start_time = time.time()

#Set the file_directory to the file name of the sudoku you want to solve
file_directory = "Sudokus/Sudoku2.txt"
sudokutemp = open(file_directory,'r')
sudoku_list = list(sudokutemp)
sudoku = [[],[],[],[],[],[],[],[],[]]
sudokutemp.close()
blanks = 0

for i in range(9):
    for k in range(9):
        sudoku[i].append(int(sudoku_list[i][k]))
        if int(sudoku_list[i][k]) == 0:
            blanks += 1

#Function which returns the number of blanks in the current sudoku   
def num_blanks():
    n = 0
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                n += 1
    return n

#Function which returns the number of zeroes (banks) in a given list
def num_zero(input_list):
    n = 0
    for i in input_list:
        if i == 0:
            n += 1
    return n

#Function which returns the numbers out of 1-9 still missing from the given list
def usable_num(input_list):
    numbers = list(range(1,10))
    
    for x in input_list:
        if x != 0:
            numbers.remove(x)
            try:
                pass
                #numbers.remove(x)
            except:
                print(input_list)
            
    return numbers

#Function which returns a list of numbers in the given column
def column(x):
    col = []
    for j in range(9):
        col.append(sudoku[j][x])
    return col

#Function which returns a list of numbers in a 3*3 area, given the position of a cell
def nine(row, column):
    nine = []
    row = int(row / 3)
    column = int(column / 3)
    for m in range(row*3, row*3+3):
        for n in range(column*3, column*3+3):
            nine.append(sudoku[m][n])
    return nine

#Function which returns a list of numbers in a 3*3 area, given the index of the area
def nine_from_index(nine_index):
    nine = []
    
    row = int(nine_index / 3)
    col = nine_index - row * 3 
    for m in range(row*3, row*3+3):
        for n in range(col*3, col*3+3):
            nine.append(sudoku[m][n])
    return nine

#Function which returns a list of available positions (column indexes) in a given row
def available_positions_row(row):
    available_positions = []
    for col in range(9):
        if sudoku[row][col] == 0:
            available_positions.append(col)
    return available_positions

#Function which returns a list of available positions (row indexes) in a given column
def available_positions_col(col):
    available_positions = []
    for row in range(9):
        if sudoku[row][col] == 0:
            available_positions.append(row)
    return available_positions

#Function which returns a list of available positions (row, col tuples) in a given 3*3 cell
def available_positions_nine(nine_index):
    available_positions = []
    nine_row = int(nine_index / 3)
    nine_col = nine_index - nine_row * 3
    for m in range(nine_row * 3, nine_row * 3 + 3):
        for n in range(nine_col * 3, nine_col * 3 + 3):
            if sudoku[m][n] == 0:
                available_positions.append((m, n))
    return available_positions

#Function to test if the sudoku has any self-contradictions
def test():
    satisfy = 1
    for i in range(9):
        for j in range(9):
            if len(list(set(sudoku[i]))) != len(sudoku[i]):
                satisfy = 0
                #print("row: {},{}".format(i,j))
            if len(list(set(column(j)))) != len(column(j)):
                satisfy = 0
                #print("column: {},{}".format(i,j))
            if len(list(set(nine(i, j)))) != len(nine(i,j)):
                satisfy = 0
                #print("nine: {},{}".format(i,j))
    return satisfy 

def print_sudoku():
    for row in range(9):
        for col in range(9):
            print(sudoku[row][col], end = "")
        print("")
        
def print_results():
    print_sudoku()

    print("The program arrived at this solution in {} steps.".format(number_of_steps))
    if test() == 1:
        print("This solution is verified to satisfy all conditions.")

    
#Function which fills the sudoku optimally; i.e. no backtracking is needed
#I.e. for every number the program fills in, it is certain that it is the correct number
def optimal_fill():
    total_filled = 0
    
    global sudoku
    
    sudoku_backup = [r[:] for r in sudoku]
    
    while True:
        filled = 0

        #For every blank, find the possible numbers that can be filled in.
        #If a blank has only one possible number, the program fills it in.
        for row in range(9):
            for col in range(9):
                if sudoku[row][col] == 0:
                    numbers_row = sudoku[row]
                    numbers_col = column(col)
                    numbers_nin = nine(row, col)

                    usable_row = usable_num(numbers_row)
                    usable_col = usable_num(numbers_col)
                    usable_nin = usable_num(numbers_nin)

                    usable = []

                    for x in range(1,10):
                        if x in usable_row and x in usable_col and x in usable_nin:
                            usable.append(x)
                        
                    if len(usable) == 1:
                        sudoku[row][col] = usable[0]
                        filled += 1
                        total_filled += 1

                    if len(usable) == 0:
                        sudoku = [r[:] for r in sudoku_backup]
                        return -1

        #For every row, find the numbers that need to be filled in. For every such number, find all possible positions.
        #If a number has only one possible position, the program fills it in.
        for row in range(9):
            numbers_row = sudoku[row]
            usable_row = usable_num(numbers_row)
            available_positions = available_positions_row(row)

            for num in usable_row:
                available_positions_copy = available_positions[:]
                for col in available_positions:
                    numbers_col = column(col)
                    numbers_nin = nine(row, col)
                    usable_col = usable_num(numbers_col)
                    usable_nin = usable_num(numbers_nin)
                    if num not in usable_col or num not in usable_nin:
                        available_positions_copy.remove(col)
                if len(available_positions_copy) == 1:
                    sudoku[row][available_positions_copy[0]] = num
                    filled += 1
                    total_filled += 1
                if len(available_positions_copy) == 0:
                    sudoku = [r[:] for r in sudoku_backup]
                    #print("Error in optimal filling: row, row {}, num {}".format(row, num))
                    return -1

        #For every column, find the numbers that need to be filled in. For every such number, find all possible positions.
        #If a number has only one possible position, the program fills it in.
        for col in range(9):
            numbers_col = column(col)
            usable_col = usable_num(numbers_col)
            available_positions = available_positions_col(col)

            for num in usable_col:
                available_positions_copy = available_positions[:]
                for row in available_positions:
                    numbers_row = sudoku[row]
                    numbers_nin = nine(row, col)
                    usable_row = usable_num(numbers_row)
                    usable_nin = usable_num(numbers_nin)

                    if num not in usable_row or num not in usable_nin:
                        available_positions_copy.remove(row)
                if len(available_positions_copy) == 1:
                    sudoku[available_positions_copy[0]][col] = num
                    filled += 1
                    total_filled += 1
                if len(available_positions_copy) == 0:
                    sudoku = [r[:] for r in sudoku_backup]
                    #print("Error in optimal filling: col")
                    return -1
            
        #For every 3*3 area, find the numbers that need to be filled in. For every such number, find all possible positions.
        #If a number has only one possible position, the program fills it in.
        for nine_index in range(9):
            numbers_nin = nine_from_index(nine_index)
            usable_nin = usable_num(numbers_nin)
            available_positions = available_positions_nine(nine_index)

            for num in usable_nin:
        
                available_positions_copy = available_positions[:]
                
                for position in available_positions:
                    row = position[0]
                    col = position[1]
                    numbers_row = sudoku[row]
                    numbers_col = column(col)

                    usable_row = usable_num(numbers_row)
                    usable_col = usable_num(numbers_col)

                    if num not in usable_row or num not in usable_col:
                        available_positions_copy.remove(position)
                if len(available_positions_copy) == 1:
                    row_final = available_positions_copy[0][0]
                    col_final = available_positions_copy[0][1]
                    sudoku[row_final][col_final] = num
                    filled += 1
                    total_filled += 1
                if len(available_positions_copy) == 0:
                    sudoku = [r[:] for r in sudoku_backup]
                    #print("Error in optimal filling: nin")
                    return -1 

        #Exits the loop if no more blanks can be filled via optimal filling.                       
        if filled == 0:
            break

    return total_filled

def get_min_usable():
    global sudoku

    switch = 0
    
    for row in range(9):
        for col in range(9):
            if sudoku[row][col] == 0:
                numbers_row = sudoku[row]
                numbers_col = column(col)
                numbers_nin = nine(row, col)

                usable_row = usable_num(numbers_row)
                usable_col = usable_num(numbers_col)
                usable_nin = usable_num(numbers_nin)
                
                usable = []

                for x in range(1,10):
                    if x in usable_row and x in usable_col and x in usable_nin:
                        usable.append(x)

                if switch == 0:
                    min_usable = len(usable)
                    min_usable_row = [row]
                    min_usable_col = [col]
                    min_usable_nums = [usable]
                    switch = 1
                else:
                    if len(usable) == min_usable:
                        min_usable_row.append(row)
                        min_usable_col.append(col)
                        min_usable_nums.append(usable)
                    if len(usable) < min_usable:              
                        min_usable = len(usable)
                        min_usable_row = [row]
                        min_usable_col = [col]
                        min_usable_nums = [usable]

    sudoku_copy = [r[:] for r in sudoku]
    
    
    for x in range(len(min_usable_nums)):
        row = min_usable_row[x]
        col = min_usable_col[x]
        nums = min_usable_nums[x]
        for n in nums:

            if n in sudoku[row]:
                continue
            if n in column(col):
                continue
            if n in nine(row, col):
                continue
            
            sudoku[row][col] = n
            
            total_filled = optimal_fill()

            if total_filled == -1:
                min_usable_nums[x].remove(n)
    sudoku = [r[:] for r in sudoku_copy]

    return (min_usable, min_usable_row, min_usable_col, min_usable_nums)


def suboptimal_fill(current_steps):

    global number_of_steps 
    global sudoku
    global sudoku_backup
    
    
    if number_of_steps % report_frequency == report_frequency -1:
        print_sudoku()
        print("Remaining: {}".format(num_blanks()))
        pass

    if time.time() - start_time > time_limit:
        print("Timeout")
        assert False
        return
    

    number_of_steps += 1

    for step in current_steps:
        sudoku[step[0]][step[1]] = step[2]

    if num_blanks() == 0:
        #print_results()
        assert False 
        return

    
    min_usable, min_usable_row, min_usable_col, min_usable_nums = get_min_usable()

    if current_steps == []:

        for x in min_usable_nums[0]:
            if [(min_usable_row[0], min_usable_col[0], x)] in bad_steps:
                min_usable_nums[0].remove(x)
    
        if len(min_usable_nums[0]) == 1:
            
            sudoku[min_usable_row[0]][min_usable_col[0]] = min_usable_nums[0][0]
            sudoku_backup = [r[:] for r in sudoku]

            suboptimal_fill([])
        

    for x in range(len(min_usable_nums)):
        

        row = min_usable_row[x]
        col = min_usable_col[x]
        nums = min_usable_nums[x]

        fillable = 0


        for n in nums:

            current_steps.append((row, col, n))
            
            if current_steps in bad_steps:
                current_steps = current_steps[:-1]
                continue
            if n in sudoku[row]:
                current_steps = current_steps[:-1]
                continue
            if n in column(col):
                current_steps = current_steps[:-1]
                continue
            if n in nine(row, col):
                current_steps = current_steps[:-1]
                continue
            
            current_steps = current_steps[:-1]
            
            fillable = 1
            
            sudoku[row][col] = n

            if optimal_fill() == -1:
                bad_steps.append(current_steps)
                sudoku = [r[:] for r in sudoku_backup]
                suboptimal_fill(current_steps)

            current_steps.append((row, col, n))

            sudoku = [r[:] for r in sudoku_backup]

            suboptimal_fill(current_steps)

        if fillable == 0:
            bad_steps.append(current_steps)
            current_steps = current_steps[:-1]
            sudoku = [r[:] for r in sudoku_backup]
            suboptimal_fill(current_steps)
            break


def solve_sudoku(sudoku_dir):
    global sudoku
    global sudoku_backup
    global start_time
    global number_of_steps

    start_time = time.time()
    
    sudoku = [[],[],[],[],[],[],[],[],[]]

    try:
        sudokutemp = open(sudoku_dir,'r')
    except FileNotFoundError as e:
        print("File does not exist")
        return

    sudoku_list = list(sudokutemp)

    #print(sudoku_list)

    sudokutemp.close()

    number_of_steps = 0

    blanks = 0
    try:
        for i in range(9):
            for k in range(9):
                sudoku[i].append(int(sudoku_list[i][k]))
                if int(sudoku_list[i][k]) == 0:
                    blanks += 1
    except:
        return

    optimal_fill()

    sudoku_backup = [r[:] for r in sudoku]

    current_steps = []
    bad_steps = []

    if num_blanks() > 0:
        try:
            suboptimal_fill([])
        except AssertionError as e:
            pass

    print_results()


solve_sudoku(file_directory)


    
    



        
