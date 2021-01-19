import sys; args = sys.argv[1:]
# Aditya Vasantharao and Brian Lai, Pd. 4
import math

def main():

    board = ""
    width = 0
    height = 0
    board_list = set()

    if len(args) == 1:
        board = args[0]

        for i in range(int(math.sqrt(len(board))), 0, -1):
            if len(board) % i == 0:
                quotient = len(board) / i
                height = int(min(quotient, i))
                width = int(max(quotient, i))
                break

    else:
        board = args[0]
        width = int(args[1])
        height = int(len(board) / width)

    temp_board = board

    # four rotations

    for i in range(4):
        raw_clock_90 = [[i * width + j for i in range(height)][::-1] for j in range(width)] 
        clock_90 = []

        for i in raw_clock_90:
            clock_90 += i

        temp_board = ''.join([temp_board[clock_90[i]] for i in range(len(temp_board))])
        board_list.add(temp_board)

        height, width = width, height

    # flip horizontally

    myMap=[i//width*width+width-i%width-1 for i in range(len(board))]
    temp_board = ''.join([board[myMap[i]] for i in range(len(board))])
    board_list.add(temp_board)

    # flip vertically

    myMap=[(height-(i//width)-1)*width+i%width for i in range(len(board))]
    temp_board = ''.join([board[myMap[i]] for i in range(len(board))])
    board_list.add(temp_board)

    # transpose: right rotation + flip horizontally

    raw_clock_90 = [[i * width + j for i in range(height)][::-1] for j in range(width)] 
    clock_90 = []

    for i in raw_clock_90:
        clock_90 += i

    temp_board = ''.join([board[clock_90[i]] for i in range(len(board))])

    height, width = width, height

    myMap=[i//width*width+width-i%width-1 for i in range(len(board))]
    temp_board = ''.join([temp_board[myMap[i]] for i in range(len(board))])
    board_list.add(temp_board)

    # revert height and width

    height, width = width, height

    # anti-transpose: flip vertically + left rotation

    myMap=[(height-(i//width)-1)*width+i%width for i in range(len(board))]
    temp_board = ''.join([board[myMap[i]] for i in range(len(board))])

    # left rotation = 3x right rotation

    for i in range(3):
        raw_clock_90 = [[i * width + j for i in range(height)][::-1] for j in range(width)] 
        clock_90 = []

        for i in raw_clock_90:
            clock_90 += i

        temp_board = ''.join([temp_board[clock_90[i]] for i in range(len(temp_board))])
        

        height, width = width, height

    board_list.add(temp_board)

    for i in board_list:
        print(i)

main()