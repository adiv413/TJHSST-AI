# Aditya Vasantharao, pd. 4
# Test slider puzzle algorithm for speed by generating 500 3x3s and testing the algorithm on that
# Usage: python stress_test.py

import sys
import time
import math
import random

US_BUFFER = 33 # buffer so that we can store the underscore pos as a readable char 

def main():
    start = time.time()
    boards = [getRandomPuzzle() for i in range(500)]
    stats = [0] * 5 # #impos., #possible, impos total time, pos total time, sum of path lengths

    for board in boards:
        height = 3
        width = 3
        goal = ''.join(sorted([i for i in board if i != '_'])) + '_' + chr(len(board) - 1 + US_BUFFER)
        steps = 0
        curr_elapsed = time.time()

        if board != goal[:-1]:
            if getInversionCount(board) % 2 == 1: 
                steps = -1
            else:
                board += chr(board.index('_') + US_BUFFER) # store the position of the underscore as the last character in the string
                steps = findPath(board, height, width, goal)
        
        curr_elapsed = time.time() - curr_elapsed

        if steps == -1:
            stats[0] += 1
            stats[2] += curr_elapsed
        else:
            stats[1] += 1
            stats[3] += curr_elapsed
            stats[4] += steps

    print(*stats)

def getInversionCount(board): 
    # gets the number of inversions (the number of pairs of numbers on the board where the 
    # number from the outer loop/left side is less than the number from the inner loop/right side)
    # basically just sees how many pairs of numbers are out of order, because all pairs should be sorted
    # for the board to be solved

    filtered_board = [i for i in board if i != '_']
    inversions = 0

    for i in range(len(filtered_board)):
        for j in range(i + 1, len(filtered_board)):
            if filtered_board[i] > filtered_board[j]:
                inversions += 1

    return inversions

def getNeighbors(board, height, width):
    underscore = ord(board[-1]) - US_BUFFER
    neighbors = set()
    neighbor_indices = []

    # note: len(board) = actual length of puzzle + 1 because theres an extra value at the end (pos of underscore)
    # split it up into finding out how many strings to return, and then changing pos of the underscore

    # 2 neighbors (corner case)

    if underscore == 0: # top left corner: add right, bottom
        if height > 1:
            neighbor_indices = [underscore + 1, underscore + width]
        else:
            neighbor_indices = [underscore + 1]

    elif underscore == width - 1: # top right corner: add left, bottom
        if height > 1:
            neighbor_indices = [underscore - 1, underscore + width]
        else:
            neighbor_indices = [underscore - 1]

    elif underscore == len(board) - 1 - width: # bottom left corner: add right, top
        neighbor_indices = [underscore + 1, underscore - width]

    elif underscore == len(board) - 2: # bottom right corner: add left, top
        neighbor_indices = [underscore - 1, underscore - width]

    # 3 neighbors (edge case)

    elif 0 < underscore < width: # top edge: add left, right, bottom
        if height > 1:
            neighbor_indices = [underscore - 1, underscore + 1, underscore + width]
        else:
            neighbor_indices = [underscore - 1, underscore + 1]
    
    elif len(board) - 1 - width < underscore < len(board) - 2: # bottom edge: add left, right, top
        neighbor_indices = [underscore - 1, underscore + 1, underscore - width]

    elif underscore % width == 0: # left edge: add top, bottom, right
        neighbor_indices = [underscore + 1, underscore + width, underscore - width]
    
    elif (underscore + 1) % width == 0: # right edge: add top, bottom, left
        neighbor_indices = [underscore - 1, underscore + width, underscore - width]

    # 4 neighbors (center case): add left, right, top, bottom

    else:
        neighbor_indices = [underscore + 1, underscore - 1, underscore + width, underscore - width]

    # parse neighbor_indices and return all the strings from those underscore index lists

    for i in neighbor_indices: # swap i with underscore and last character of the string = i
        neighbor = list(board)
        neighbor[-1] = chr(i + US_BUFFER)
        neighbor[i], neighbor[underscore] = '_', board[i]
        neighbor = ''.join(neighbor)
        neighbors.add(neighbor)

    return neighbors

def findPath(board, height, width, goal):
    queue = [board]
    visited = {board : ''}

    while queue:
        curr = queue.pop()

        if curr == goal:
            count = 0
            node = goal

            while node != '':
                count += 1
                node = visited[node]

            return count
        
        
        toVisit = [i for i in getNeighbors(curr, height, width) if i not in visited.keys()]
        queue[:0] = toVisit

        for i in toVisit:
            visited[i] = curr

    return -1

def getRandomPuzzle():
    ret = ''

    for i in range(8):
        next = random.randint(0, 9)

        if next == 3 and '_' not in ret:
            ret += '_'
        elif next == 3:
            ret += str(random.randint(0, 8))
        else:
            if next < 3:
                ret += str(next)
            else:
                ret += str(next - 1)
    
    if '_' not in ret:
        ret += '_'
    else:
        ret += str(random.randint(0, 8))
    
    return ret

start = time.time()
main()
print(time.time() - start)