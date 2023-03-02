import os
import math
import copy
test_file_name = "hard.txt"
horizontal_border = '-+---+---+---+---+---+---+---+---+---+-'
vertical_border = '   '

# TODO:
#   - handle implicit decisions
#       - e.g. this cell is the only one in the square that can have a 4

def run_sudoku_solver():
    file_string = read_sudoku_file()
    row_list = generate_row_list(file_string)
    print_puzzle(row_list)
    solved_puzzle, nbr_cycles = solve(row_list)
    print_puzzle(solved_puzzle)
    print("cycles: " + str(nbr_cycles))
    
def solve(sudoku, nbr_cycles = 0):

    if is_solved(sudoku):
        print('Solved in:', nbr_cycles)
        return (copy.deepcopy(sudoku), nbr_cycles)

    possibilities_by_cell = {}
    fixed_sudoku = copy.deepcopy(sudoku)

    for y in range(len(fixed_sudoku[0])):
        for x in range(len(fixed_sudoku[0])):
            solution = evaluate_deterministic(x, y, fixed_sudoku, possibilities_by_cell)
            if solution != None:
                fixed_sudoku[y][x] = solution

    if is_stumped(sudoku, fixed_sudoku):
        print('Stumped after', nbr_cycles, 'cycles')
        print('possibilities:\n', possibilities_by_cell)
        return (sudoku, nbr_cycles)

    return solve(fixed_sudoku, nbr_cycles + 1, possibilities_by_cell)

def is_solved(sudoku):
    is_solved = True
    for row in sudoku:
        for cell in row:
            if cell == ' ':
                is_solved = False

    return is_solved

def is_stumped(before, after):
    stumped = True

    for i in range(len(before)):
        for j in range(len(before[i])):
            if before[i][j] != after[i][j]:
                stumped = False
    
    return stumped

def evaluate_deterministic(x, y, sudoku, possibilities_by_cell):

    if sudoku[y][x] != ' ':
        possibilities_by_cell[x,y] = sudoku[y][x]
        return None

    row = get_row(y, sudoku)
    column = get_column(x, sudoku)
    square = get_square(x, y, sudoku)
    possibilities = []

    for i in range(1, len(sudoku) + 1):
        possibilities.append(str(i))

    for nbr in row:
        if nbr in possibilities:
            possibilities.remove(nbr)

    for nbr in column:
        if nbr in possibilities:
            possibilities.remove(nbr)

    for nbr in square:
        if nbr in possibilities:
            possibilities.remove(nbr)

    possibilities_by_cell[(x, y)] = possibilities

    if (len(possibilities) == 1):
        return possibilities[0]
    else:
        return None
    
def evaluate_implicit(x, y, sudoku, possibilities_by_cell):
    # Given cell x,y: for each possibility z in possibilities_by_cell, check possibilities iin square, in column, and in row.
    # If z doesnt appear in at least one of those sets, sudoku[x,y] = z
    return

def generate_row_list(sudoku_string):
    line_list = []
    unparsed_lines = sudoku_string.splitlines()
    for line in unparsed_lines:
        line_list.append(line.split('|'))

    return line_list

def get_row(y, sudoku_string):
    return sudoku_string[y]

def get_column(x, sudoku_string):
    column = []
    for line in sudoku_string:
        column.append(line[x])

    return column

def get_square(x, y, sudoku_string):
    # determine square based on position
    # assemble square
    start_row = math.floor(y/3) * 3
    end_row = (math.floor(y/3) + 1) * 3
    start_column = math.floor(x/3) * 3
    end_column = (math.floor(x/3) + 1) * 3

    square = []

    for col in range(start_row, end_row):
        for row in range(start_column, end_column):
            square.append(sudoku_string[col][row])

    return square

def print_puzzle(sudoku_list):
    print("Puzzle:\n")

    output_string = horizontal_border + '\n'
    for line in sudoku_list:
        line_string = vertical_border

        for cell in line:
            line_string += cell + vertical_border

        output_string += line_string + '\n' + horizontal_border + '\n'

    print(output_string)

def read_sudoku_file():
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, test_file_name)
    sudoku_file = open(abs_file_path, "r")
    return sudoku_file.read()    

def main():
    run_sudoku_solver()

if __name__ == "__main__":
    main()