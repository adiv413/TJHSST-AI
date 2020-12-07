# Aditya Vasantharao, pd. 4
# Solves sudoku puzzles of any size using an optimized brute-force method
# Usage: python sudoku.py [puzzle/text file]
# Examples:
#   python sudoku.py 63..........5....8..5674.......2......34.1.2.......345.....7..4.8.3..9.29471...8.
#   python sudoku.py puzzles.txt
# puzzles.txt contains 128 9x9 puzzles which increase in difficulty

import sys
import math
import time

args = sys.argv[1:]

symbols = []
height = 0
width = 0
lookup_table = {}
puzzle_dim = 0
constraint_sets = []
neighbors = []

def main():

    global symbols
    global height
    global width
    global lookup_table
    global puzzle_dim
    global constraint_sets
    global neighbors

    isSinglePuzzle = False
    puzzles = []
    count = 0
    
    if '.txt' in args[0]:
        puzzles = open(args[0], 'r').read().splitlines()
    else:
        isSinglePuzzle = True
        puzzles = [args[0]]

    for puzzle in puzzles:

        # initialization and setting up globals/lookup tables

        count += 1
        start = time.time()
        puzzle_dim = int(math.sqrt(len(puzzle))) # height/width of the actual puzzle
        height = 0 # height of each small sub-square
        width = 0 # width of each small sub-square
        symbols = [str(i) for i in range(1, 10)]
        lookup_table = {i : [] for i in range(len(puzzle))}
        neighbors = {}
        neighbor_values = {}
        lookup_count = 0

        for i in range(int(math.sqrt(puzzle_dim)), 0, -1):
            if puzzle_dim % i == 0:
                quotient = puzzle_dim / i
                height = int(min(quotient, i))
                width = int(max(quotient, i))
                break

        # find symbol set

        if puzzle_dim == 12:
            symbols += ['A', 'B', 'C']
        elif puzzle_dim == 16:
            if '0' in puzzle:
                symbols += ['0'] + [chr(i) for i in range(65, 71)]
            else:
                symbols += [chr(i) for i in range(65, 72)]

        symbols = set(symbols)

        # initialize lookup table and constraint sets

        lookup_table = {i : [] for i in range(len(puzzle))} # lookup table from puzzle index to constraint set indices

        rows = [[j for j in range(i, i + puzzle_dim)] for i in range(0, len(puzzle), puzzle_dim)]
        cols = [[j for j in range(i, len(puzzle), puzzle_dim)] for i in range(puzzle_dim)]

        sub_squares = []
        for i in range(0, puzzle_dim, height):
            for j in range(0, puzzle_dim, width):
                temp = []
                for k in range(i, i + height):
                    for l in range(j, j + width):
                        temp.append(k * puzzle_dim + l)
                sub_squares.append(temp)
                
        constraint_sets = rows + cols + sub_squares

        for i in constraint_sets:
            for j in i:
                lookup_table[j].append(lookup_count)
            lookup_count += 1
        
        # initialize neighbors/neighbor values lookup table

        for i in range(len(puzzle)):
            neighbors[i] = set(constraint_sets[lookup_table[i][0]]) | set(constraint_sets[lookup_table[i][1]]) | set(constraint_sets[lookup_table[i][2]]) 
            neighbors[i].remove(i)
            
            neighbor_values[i] = {puzzle[j] for j in neighbors[i] if puzzle[j] != '.'} 
        

        # run brute-force algorithm

        result = bruteForce(puzzle, None, neighbor_values)
        checksum = sum([int(i, 17) for i in result])
        
        if not result:
            result = puzzle

        end = time.time() - start

        if count < 10:
            print(str(count) + ': ' + puzzle)
            print('   ' + result, checksum, str(end) + 's')
        elif count < 100:
            print(str(count) + ': ' + puzzle)
            print('    ' + result, checksum, str(end) + 's')
        else:
            print(str(count) + ': ' + puzzle)
            print('     ' + result, checksum, str(end) + 's')

def getSymbolChoices(puzzle, neighbor_vals, max_len):
    symbol_dot_list = []
    best_symbol = ''

    for cset in constraint_sets:
        for sym in symbols:
            curr_sym_dot_list = [i for i in cset if puzzle[i] == '.' and sym not in neighbor_vals[i]]

            if len(curr_sym_dot_list) != 0 and (len(symbol_dot_list) == 0 or len(curr_sym_dot_list) < len(symbol_dot_list)):
                symbol_dot_list = curr_sym_dot_list
                best_symbol = sym

            if len(symbol_dot_list) == 1:
                return [[idx, best_symbol] for idx in symbol_dot_list]

    if len(symbol_dot_list) < max_len:
        return [[idx, best_symbol] for idx in symbol_dot_list]

    return []

def bruteForce(puzzle, new_index, neighbor_vals):
    # if new_index and isInvalid(puzzle, new_index, neighbor_vals): # the first call to bruteforce has new_index as None
    #     return ''
    if isSolved(puzzle):
        return puzzle
    # elif '.' not in puzzle:
    #     return ''

    pos = [i for i in range(len(puzzle)) if puzzle[i] == '.']
    min_pos = None

    for i in pos:
        curr = (len(symbols) - len(neighbor_vals[i]), i)
        if curr[0] < 2:
            min_pos = curr
            break
        elif min_pos and min_pos > curr or not min_pos:
            min_pos = curr

    choices = [[min_pos[1], j] for j in symbols if j not in neighbor_vals[min_pos[1]]]

    if len(choices) >= 2:
        temp_choices = getSymbolChoices(puzzle, neighbor_vals, len(choices))
        if temp_choices:
            choices = temp_choices
    
    # create set of choices 

    for choice in choices: # process choices with the least number of spaces first
        # put the symbol into the blank space in the puzzle
        new_puzzle = list(puzzle)
        new_puzzle[choice[0]] = choice[1]
        new_puzzle = ''.join(new_puzzle)
        new_neighbor_vals = {}

        # make a copy of neighbor_vals, if necessary
        if len(choices) != 1:
            new_neighbor_vals = {k : {*neighbor_vals[k]} for k in neighbor_vals}
        else:
            new_neighbor_vals = neighbor_vals

        # edit the copy to include the most recent update to the puzzle
        for neighbor_index in neighbors[choice[0]]:
            new_neighbor_vals[neighbor_index].add(choice[1])

        # recur with the new puzzle value
        result = bruteForce(new_puzzle, choice[0], new_neighbor_vals)

        if result:
            return result

    return ''

def isSolved(puzzle):
    return '.' not in puzzle #and sum([int(i, 17) for i in puzzle]) == 405

# not used
def isInvalid(puzzle, index, neighbor_vals):
    # get the current character from each neighbor index (except the current one)
    # if the current character is in the set of neighbor characters, the puzzle is invalid
    
    index_neighbor_vals = neighbor_vals[index]
    return puzzle[index] in index_neighbor_vals

main()