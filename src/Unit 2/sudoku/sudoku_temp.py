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
# import pprint ###################GET RID OF MEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE

# symbols = []
# height = 0
# width = 0
# lookup_table = {}
# puzzle_dim = 0
# constraint_sets = []
# items = []

# def main():

#     global symbols
#     global height
#     global width
#     global lookup_table
#     global puzzle_dim
#     global constraint_sets
#     global items

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
#         constraint_sets = []
#         lookup_table = {i : [] for i in range(len(puzzle))}

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

#         constraint_set_count = 0

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
                
#         items = rows + cols + sub_squares

#         for i in items: # item index corresponds w lookup_table # corresponds w constraint sets index
#             constraint_sets.append(set([puzzle[j] for j in i]))
#             for j in i:
#                 lookup_table[j].append(constraint_set_count)
#             constraint_set_count += 1

#         # print(len(items))
#         # print(constraint_sets)
#         # print(items[lookup_table[12][0]])
#         # print(lookup_table[12][0])
#         # print(constraint_sets[lookup_table[12][0]])

#         #uncomment here and below

#         result = solve(puzzle, None)
#         checksum = sum([int(i, 17) for i in result])
        
#         if not result:
#             incorrect += 1
#             result = puzzle

#         end = time.time() - start

#         if count < 10:
#             print(str(count) + ': ' + puzzle)
#             print('   ' + result, checksum, str(end) + 's')
#         else:
#             print(str(count) + ': ' + puzzle)
#             print('    ' + result, checksum, str(end) + 's')
    
#     print('total correct:', count - incorrect)

# def solve(puzzle, index):
#     # print(puzzle + 'sdfkljsdflksjdflksdjflsdkjfdslf', index)
#     if index is not None and isInvalid(puzzle, index):
#         return ''
#     if isSolved(puzzle):
#         return ''.join(puzzle)

#     if index:
#         for i in range(3): #re-set constraint sets
#             curr_index = lookup_table[index][i]
#             curr = items[curr_index] # get the list of indices in the row/col/square

#             constraint_sets[curr_index] = set([puzzle[j] for j in curr]) # re-set the current constraint set

#     choices = []

#     for i in range(len(puzzle)):
#         if puzzle[i] == '.':
#             for j in symbols:
#                 neighbors = constraint_sets[lookup_table[i][0]] | constraint_sets[lookup_table[i][1]] | constraint_sets[lookup_table[i][2]]
#                 total = 2 * puzzle_dim + height * width - height - width - len(neighbors)
                
#                 # if j not in neighbors:
#                 choices.append((total, i, j))

#     # print(puzzle)
#     # print(choices)
#     # if choices:
#     #     print(puzzle[choices[0][1]])
#     # print()
    
#     for choice in choices:
#         new_puzzle = list(puzzle)
#         new_puzzle[choice[1]] = choice[2]
#         new_puzzle = ''.join(new_puzzle)
#         result = solve(new_puzzle, choice[1])

#         if result:
#             return result

#     return ''

# def isSolved(puzzle):
#     if '.' not in puzzle and sum([int(i, 17) for i in puzzle]) == 405:
#         # print('2342432423423423423432432')
#         for index in range(len(puzzle)):
#             puzzle_dim = int(math.sqrt(len(puzzle)))
#             start = (index // puzzle_dim) * puzzle_dim
#             row = [puzzle[i] for i in range(start, start + puzzle_dim)]
#             col = [puzzle[i] for i in range(index % puzzle_dim, len(puzzle), puzzle_dim)]
#             sub_square_h = index // puzzle_dim - (index // puzzle_dim) % height
#             sub_square_w = index % puzzle_dim - (index % puzzle_dim) % width

#             sub_square = []

#             for i in range(sub_square_h, sub_square_h + height):
#                 for j in range(sub_square_w, sub_square_w + width):
#                     sub_square.append(puzzle[i * puzzle_dim + j])

#             if len(row) != len(set(row)) or len(col) != len(set(col)) or len(sub_square) != len(set(sub_square)):
#                 print('row:', row)
#                 print('col:', col)
#                 print('square:', sub_square)
#                 print(sub_square_h, sub_square_w)
#                 temp = [[puzzle[i * puzzle_dim + j] for j in range(9)] for i in range(9)]
#                 pprint.pprint(temp)
#                 print()
#                 print()
#                 return False

#         return True

#     return False


# # def isInvalid(new_index, new_val, old_constraints):
# #     return new_index in old_constraints[new_val]

# def isInvalid(puzzle, index):
#     # print('SDKLFJSDKLFSJDFKLSDJFKSLDJFKSLDJFSDKLFJSDKLJFSDF')
#     # print(index)
#     # print(lookup_table[index])

#     neighbors = set()

#     for i in lookup_table[index]:
#         # print(items[i])
#         neighbors |= set([puzzle[j] for j in items[i]])

#     if puzzle[index] in neighbors:
#         # print(puzzle[index])
#         # print(neighbors)
#         # print()
#         return True
    
#     return False



# main()