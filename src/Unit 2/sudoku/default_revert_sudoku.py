import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math
import time

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
    incorrect = 0
    
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
        
        # initialize neighbors lookup table

        for i in range(len(puzzle)):
            neighbors[i] = set(constraint_sets[lookup_table[i][0]]) | set(constraint_sets[lookup_table[i][1]]) | set(constraint_sets[lookup_table[i][2]]) 

        # run brute-force algorithm

        result = bruteForce(puzzle, None)
        checksum = sum([int(i, 17) for i in result])
        
        if not result:
            incorrect += 1
            result = puzzle

        end = time.time() - start

        if count < 10:
            print(str(count) + ': ' + puzzle)
            print('   ' + result, checksum, str(end) + 's')
        else:
            print(str(count) + ': ' + puzzle)
            print('    ' + result, checksum, str(end) + 's')
    
    # print('total correct:', count - incorrect)

def bruteForce(puzzle, new_index):
    if new_index and isInvalid(puzzle, new_index): # the first call to bruteforce has new_index as None
        return ''
    if isSolved(puzzle):
        return puzzle
    elif '.' not in puzzle:
        return ''

    pos = puzzle.index('.')

    choices = [[pos, j] for j in symbols]

    # create set of choices 

    # for i in range(len(puzzle)):
    #     if puzzle[i] == '.':
    #         neighbor_values = [puzzle[j] for j in neighbors[i]] # find the actual sudoku characters from each index in neighbors
    #         dots = neighbor_values.count('.') # number of empty spaces in the puzzle
    #         neighbor_values = set(neighbor_values)

    #         for j in symbols:
    #             if j not in neighbor_values: # if the current symbol is not a duplicate with any neighbor
    #                 choices.append((dots, i, j)) # num dots, index, symbol

    for choice in choices: # process choices with the least number of spaces first
        # put the symbol into the blank space in the puzzle
        new_puzzle = list(puzzle)
        new_puzzle[choice[0]] = choice[1]
        new_puzzle = ''.join(new_puzzle)

        # recur with the new puzzle value
        result = bruteForce(new_puzzle, choice[0])

        if result:
            return result

    return ''

def isSolved(puzzle):
    return '.' not in puzzle and sum([int(i, 17) for i in puzzle]) == 405

def isInvalid(puzzle, index):
    # get the current character from each neighbor index (except the current one)
    # if the current character is in the set of neighbor characters, the puzzle is invalid
    
    neighbor_values = {puzzle[j] for j in neighbors[index] if j != index} 
    return puzzle[index] in neighbor_values


main()