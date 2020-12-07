import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4

def main():
    board = '.' * 27 + "ox......xo" + '.' * 27

    if args:
        board = args[0].lower() 

    if len(args) < 2:
        pass
    else:


    # even number of discs: black's turn
    # odd number of discs: white's turn
    # each turn you MUST make a move which flips discs


main()