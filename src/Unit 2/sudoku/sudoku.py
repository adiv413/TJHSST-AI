import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
import math
import time

rows = None
cols  = None
sub_squares = None


def main():
    global rows
    global cols 
    global sub_squares

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

        result = solve(list(puzzle), constraints, None)
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

def solve(puzzle, constraints, new_vals):
    if new_vals:
        constraints[new_vals[1]].add(new_vals[0])

    if isSolved(puzzle):
        return ''.join(puzzle)

    choices = [[i, j] for j in constraints for i in range(len(puzzle)) if puzzle[i] == '.' and not isInvalid(i, j, constraints)]
    
    for choice in choices:
        new_puzzle = puzzle
        new_puzzle[choice[0]] = choice[1]

        result = ''

        # if not isInvalid(choice[0], choice[1], constraints):
        result = solve(new_puzzle, constraints, choice)

        if result:
            return result

    return ''

def isSolved(puzzle):
    if '.' not in puzzle and sum([int(i, 17) for i in puzzle]) == 405:
        for item in (rows, cols, sub_squares):
            for i in item:
                check = set([puzzle[j] for j in i])
                if len(check) != len(rows):
                    return False
        
        return True

    return False


def isInvalid(new_index, new_val, old_constraints):
    return new_index in old_constraints[new_val]

main()


# import sys; args = sys.argv[1:]
# # Aditya Vasantharao, pd. 4
# import math
# import time

# def main():
#     isSinglePuzzle = False
#     puzzles = []
#     count = 0
#     incorrect = 0
    
#     if '.txt' in args[0]:
#         puzzles = open(args[0], 'r').read().splitlines()
#     else:
#         isSinglePuzzle = True
#         puzzles = [args[0]]

#     for puzzle in puzzles:
#         count += 1
#         start = time.time()
#         puzzle_dim = int(math.sqrt(len(puzzle))) # height/width of the actual puzzle, 9
#         height = 0 # height of each small sub-square, 3
#         width = 0 # width of each small sub-square, 3
#         symbols = [str(i) for i in range(1, 10)]
#         constraints = {}

#         for i in range(int(math.sqrt(puzzle_dim)), 0, -1):
#             if puzzle_dim % i == 0:
#                 quotient = puzzle_dim / i
#                 height = int(min(quotient, i))
#                 width = int(max(quotient, i))
#                 break

#         if puzzle_dim == 12:
#             symbols += ['A', 'B', 'C']
#         elif puzzle_dim == 16:
#             if '0' in puzzle:
#                 symbols += ['0'] + [chr(i) for i in range(65, 71)]
#             else:
#                 symbols += [chr(i) for i in range(65, 72)]
            
#         for i in symbols:
#             constraints[i] = set()

#         rows = [[j for j in range(i, i + puzzle_dim)] for i in range(0, len(puzzle), puzzle_dim)]
#         cols = [[j for j in range(i, len(puzzle), puzzle_dim)] for i in range(puzzle_dim)]

#         sub_squares = []
#         for i in range(0, puzzle_dim, height):
#             for j in range(0, puzzle_dim, width):
#                 temp = []
#                 for k in range(i, i + height):
#                     for l in range(j, j + width):
#                         temp.append(k * puzzle_dim + l)
#                 sub_squares.append(temp)

#         for item in (rows, cols, sub_squares):
#             for i in range(len(item)):
#                 for j in item[i]:
#                     curr = puzzle[j]
#                     if curr != '.':
#                         constraints[curr] |= set(item[i])

#         result = solve(list(puzzle), constraints, None)
#         checksum = sum([int(i, 17) for i in result])

#         for item in (rows, cols, sub_squares):
#             for i in item:
#                 check = set([result[j] for j in i])
#                 if len(check) != len(rows):
#                     print('nopeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
#                     incorrect += 1
#                     break
#         else:
#             if not result:
#                 incorrect += 1
#                 result = puzzle

#         end = time.time() - start

#         if count < 10:
#             print(str(count) + ': ' + puzzle)
#             print('   ' + result, checksum, str(end) + 's')
#         else:
#             print(str(count) + ': ' + puzzle)
#             print('    ' + result, checksum, str(end) + 's')
    
#     print('total correct:', count - incorrect)




# def solve(puzzle, constraints, new_vals):
#     if new_vals:
#         constraints[new_vals[1]].add(new_vals[0])

#     if isSolved(puzzle):
#         return ''.join(puzzle)

#     choices = [[i, j] for j in constraints for i in range(len(puzzle)) if puzzle[i] == '.']
    
#     for choice in choices:
#         new_puzzle = puzzle
#         new_puzzle[choice[0]] = choice[1]

#         result = ''

#         if not isInvalid(choice[0], choice[1], constraints):
#             result = solve(new_puzzle, constraints, choice)

#         if result:
#             return result

#     return ''

# def isSolved(puzzle):
#     return '.' not in puzzle and sum([int(i, 17) for i in puzzle]) == 405

# def isInvalid(new_index, new_val, old_constraints):
#     return new_index in old_constraints[new_val]

# main()