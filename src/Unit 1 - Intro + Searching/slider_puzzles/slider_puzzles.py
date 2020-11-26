# Aditya Vasantharao, pd. 4
# Solve slider puzzles as fast as possible using just BFS
# Usage: python slider_puzzles.py [start] [end]

# @param start: String representing the beginning slider puzzle, automatically
# made as square as possible with a longer width if it cannot become a square;
# the underscore represents the one empty space in the slider puzzle
# Example: ABC45678_d%f
# Actual puzzle:
# A B C 4 
# 5 6 7 8 
# _ d % f

# @param end: [optional] String representing the goal slider puzzle; this program will
# solve the start puzzle in ascending order by ASCII value if this is not provided

import sys
import time
import math

args = sys.argv[1:]

US_BUFFER = 33 # buffer so that we can store the underscore pos as a readable char 

def main():
    start = time.time()
    board = args[0]
    height = 0
    width = 0
    goal = ''

    if len(args) > 1:
        goal = args[1] + chr(args[1].index('_') + US_BUFFER)
    else:
        goal = ''.join(sorted([i for i in board if i != '_'])) + '_' + chr(len(board) - 1 + US_BUFFER)

    path = [board]
    steps = 0
    
    for i in range(int(math.sqrt(len(board))), 0, -1):
        if len(board) % i == 0:
            quotient = len(board) / i
            height = int(min(quotient, i))
            width = int(max(quotient, i))
            break

    if board != goal[:-1]:
        if len(args) == 1 and getInversionCount(board) % 2 == 1 or len(board) != len(goal) - 1: 
            steps = -1
        elif len(args) > 1 and width % 2 == 1 and getInversionCount(board) % 2 != getInversionCount(goal[:-1]) % 2:
            steps = -1
        elif len(args) > 1 and width % 2 == 0:
            board_begin = board.index('_') // width
            goal_begin = (ord(goal[-1]) - US_BUFFER) // width

            board_par = (getInversionCount(board) + board_begin) % 2
            goal_par = (getInversionCount(goal[:-1]) + goal_begin) % 2

            if board_par != goal_par:
                steps = -1
            else:
                board += chr(board.index('_') + US_BUFFER) # store the position of the underscore as the last character in the string
                path, steps = findPath(board, height, width, goal)

        else:
            board += chr(board.index('_') + US_BUFFER) # store the position of the underscore as the last character in the string
            path, steps = findPath(board, height, width, goal)

        

    ret = [[] for i in range(height)]

    for i in path:
        formatted = [[i[k + j * width] for k in range(width)] for j in range(height)]

        for j in range(height):
            ret[j].append(formatted[j])

    prev = 0
    for i in range(0, steps + 8, 6)[1:]:
        band = [ret[j][prev:i] for j in range(len(ret))]
        prev = i

        for j in band:
            for k in j:
                for l in k:
                    print(l, end=' ')
                print('   ', end='')
            print()
        print()
            


    print('Steps: ' + str(steps))
    print('Time: ' + str(time.time() - start)[:4] + 's')

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
            ret = []
            node = goal

            while node != '':
                ret.append(node[:-1])
                node = visited[node]

            ret = ret[::-1]

            return ret, len(ret) - 1
        
        
        toVisit = [i for i in getNeighbors(curr, height, width) if i not in visited.keys()]
        queue[:0] = toVisit

        for i in toVisit:
            visited[i] = curr

    return [board], -1

main()