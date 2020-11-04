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
        dim = int(math.sqrt(len(puzzle)))
        height = 0
        width = 0

        for i in range(int(math.sqrt(dim)), 0, -1):
            if len(puzzle) % i == 0:
                quotient = len(puzzle) / i
                height = int(min(quotient, i))
                width = int(max(quotient, i))
                break

        

main()