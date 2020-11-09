import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math
import time
import pprint ###################GET RID OF MEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

symbols = []
height = 0
width = 0
lookup_table = {}
puzzle_dim = 0
items = []

def main():

    global symbols
    global height
    global width
    global lookup_table
    global puzzle_dim
    global items

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
        count += 1
        start = time.time()
        puzzle_dim = int(math.sqrt(len(puzzle))) # height/width of the actual puzzle, 9
        height = 0 # height of each small sub-square, 3
        width = 0 # width of each small sub-square, 3
        symbols = [str(i) for i in range(1, 10)]
        lookup_table = {i : [] for i in range(len(puzzle))}

        for i in range(int(math.sqrt(puzzle_dim)), 0, -1):
            if puzzle_dim % i == 0:
                quotient = puzzle_dim / i
                height = int(min(quotient, i))
                width = int(max(quotient, i))
                break

        if puzzle_dim == 12:
            symbols += ['A', 'B', 'C']
        elif puzzle_dim == 16:
            if '0' in puzzle:
                symbols += ['0'] + [chr(i) for i in range(65, 71)]
            else:
                symbols += [chr(i) for i in range(65, 72)]

        # setLookupTables(puzzle)




        constraint_set_count = 0
        lookup_table = {i : [] for i in range(len(puzzle))}

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
                
        items = rows + cols + sub_squares

        for i in items: # item index corresponds w lookup_table # corresponds w constraint sets index
            for j in i:
                lookup_table[j].append(constraint_set_count)
            constraint_set_count += 1



        result = solve(puzzle)
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
    
    print('total correct:', count - incorrect)

def solve(puzzle):
    # print(puzzle)
    # print('sdfkljsdfklsdjfklsdjfklsdjfkl')
    if isInvalid(puzzle):
        # print('\n\n\n\n\n\n242342342342342342')
        return ''
    if isSolved(puzzle):
        return ''.join(puzzle)

    # print('pleasdkfjsldkfjsdlkfjsdklfsdf')

    choices = []

    for i in range(len(puzzle)):
        if puzzle[i] == '.':
            for j in symbols:
                choices.append((i, j))

    # print(choices)
    
    for choice in choices:
        new_puzzle = list(puzzle)
        new_puzzle[choice[0]] = choice[1]
        new_puzzle = ''.join(new_puzzle)
        # print(new_puzzle)
        result = solve(new_puzzle)

        if result:
            return result

    return ''

def isSolved(puzzle):
    # print('sdfsdfsdfsdfsdfsdfsdfq1213231423423423423423423')
    if '.' not in puzzle and sum([int(i, 17) for i in puzzle]) == 405:
        # print()
        # print()
        # print(puzzle)
        # print()

        for index in range(len(puzzle)):
            # print(lookup_table[index])
            item_indices = items[lookup_table[index][0]], items[lookup_table[index][1]], items[lookup_table[index][2]]

            for i in item_indices:
                item_vals = set([puzzle[j] for j in i])

                if len(i) != len(item_vals):
                    # print(item_indices)
                    # print(item_vals)
                    return False

        return True

    return False

def isInvalid(puzzle):
    for index in range(len(puzzle)):
        row = items[lookup_table[index][0]]
        col = items[lookup_table[index][1]]
        square = items[lookup_table[index][2]]


        for i in (row, col, square):
            vals = [puzzle[j] for j in i if puzzle[j] != '.']
            if len(set(vals)) != len(vals):
                # print('hiii')
                # print(vals)
                # print(i)
                return True

    # if puzzle[0] == '4':
    #     print('we all good')    
    # print()
    # print('\n\n\n\n\n\n\n')

        
    return False


def setLookupTables(puzzle):
    constraint_set_count = 0
    constraint_sets = []
    lookup_table = {i : [] for i in range(len(puzzle))}

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
            
    items = rows + cols + sub_squares

    for i in items: # item index corresponds w lookup_table # corresponds w constraint sets index
        constraint_sets.append(set([puzzle[j] for j in i]))
        for j in i:
            lookup_table[j].append(constraint_set_count)
        constraint_set_count += 1

    print(lookup_table)

main()