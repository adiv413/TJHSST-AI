import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import time
import math
import random

US_BUFFER = 33 # buffer so that we can store the underscore pos as a readable char 

def main():
    start = time.time()
    boards = open(args[0], 'r').read().splitlines()
    goal = boards[0] + chr(boards[0].index('_') + US_BUFFER)
    count = 0
    times = []

    for board in boards:
        height = 0
        width = 0

        for i in range(int(math.sqrt(len(board))), 0, -1):
            if len(board) % i == 0:
                quotient = len(board) / i
                height = int(min(quotient, i))
                width = int(max(quotient, i))
                break

        steps = 0
        curr_elapsed = time.time()
        board += chr(board.index('_') + US_BUFFER) # store the position of the underscore as the last character in the string

        if board != goal: 
            # it's guaranteed that all puzzles given will be solvable; no need to check for impossible
            steps = findPath(board, height, width, goal)
        
        curr_elapsed = time.time() - curr_elapsed

        times.append(curr_elapsed)
        print(str(count) + ':', board[:-1], 'solved in', steps, 'steps in', str(curr_elapsed), 'seconds')
        count += 1

    print('Total process time:', sum(times))

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
    queue = [(getMD(board[:-1], goal[:-1], height, width), 0, board)] # [(h [which is MD + level], level, board)]
    visited = set()
    ptr = 0

    while queue:
        try:
            assert(len(queue) > ptr)
        except:
            print(len(queue), ptr)
            raise Exception()
        h, level, curr = min(queue[ptr:])
        idx = queue.index((h, level, curr))
        # print()
        # print(queue)
        queue[ptr], queue[idx] = queue[idx], queue[ptr]
        ptr += 1
        # print(queue)
        # print()
        if curr in visited:
            print(curr)
            continue

        visited.add(curr)

        for child in getNeighbors(curr, height, width):
            if child == goal:
                return level + 1
            elif child in visited:
                continue

            queue.append((getMD(child[:-1], goal[:-1], height, width) + level + 1, level + 1, child))

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

def getMD(board, goal, height, width): # gets Manhattan Distance from board to goal
    total_dist = 0

    for i in range(height):
        for j in range(width):
            if board[i * width + j] != '_':
                goal_pos = goal.index(board[i * width + j])
                goal_height = goal_pos // width
                goal_width = goal_pos - goal_height * width

                total_dist += abs(goal_height - i) + abs(goal_width - j)
    
    return total_dist

start = time.time()
main()
print('Total time time:', time.time() - start)