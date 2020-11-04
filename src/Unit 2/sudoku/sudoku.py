import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math
import time

def main():
    isSinglePuzzle = False
    puzzles = []
    
    if '.txt' in args[0]:
        puzzles = open(args[0], 'r').read().splitlines()
    else:
        isSinglePuzzle = True
        puzzles = [args[0]]

    for puzzle in puzzles:
        puzzle_dim = int(math.sqrt(len(puzzle))) # height/width of the actual puzzle, 9
        height = 0 # height of each small sub-square, 3
        width = 0 # width of each small sub-square, 3
        symbols = [str(i) for i in range(1, 10)]
        constraints = {}

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
            
        for i in symbols:
            constraints[i] = set()

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

        for item in (rows, cols, sub_squares):
            for i in range(len(item)):
                for j in item[i]:
                    curr = puzzle[j]
                    if curr != '.':
                        constraints[curr] |= set(item[i])

        


main()