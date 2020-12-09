import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4

def main():
    board = '.' * 27 + 'ox......xo' + '.' * 27
    tokenToMove = ''
    oppositeToken = ''

    if args and args[0] and len(args[0]) == 64:
        board = args[0].lower() 

    if len(args) < 2:
        num_tokens = 64 - board.count('.')

        if num_tokens % 2 == 0:
            tokenToMove = 'x'
        else:
            tokenToMove = 'o'

    else:
        tokenToMove = args[1].lower()
    
    oppositeToken = 'o' if tokenToMove == 'x' else 'x'

    moves = find_moves(board, tokenToMove, oppositeToken)

    for i in moves:
        board = board[:i] + '*' + board[i + 1:] 

    for i in range(8):
        for j in range(8):
            print(board[i * 8 + j], end=' ')
        print()

    if moves:
        print(*moves)
    else:        
        print('No moves possible')

    

    # even number of discs: black's turn
    # odd number of discs: white's turn
    # each turn you MUST make a move which flips discs

    # for making moves:
    # xo.    <- putting an x here turns both the o's
    #   o 
    #   x

def find_moves(board, tokenToMove, oppositeToken):
    moves = []
    # left, right, up, down, upleft, upright, downleft, downright
    start = 0
    end = len(board)

    if 'x' in board and 'o' in board:
        start = min(board.index('x'), board.index('o'))
        start = max(start - 9, 0)

        end = max(board.rindex('x'), board.rindex('o'))
        end = min(end + 10, len(board))
    # print(tokenToMove, oppositeToken)

    # current has to be dot, next has to be opposite, keep going in same direction until you reach same token as tokenToMove
    for i in range(start, end):
        curr = board[i]

        if curr == '.':
            completed = False

            # right
            if i % 8 < 6 and board[i + 1] == oppositeToken:
                next_idx = i + 2

                while next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx += 1

            # left
            if i % 8 > 1 and board[i - 1] == oppositeToken and not completed:
                next_idx = i - 2

                while next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx -= 1

            # up
            if i // 8 > 1 and board[i - 8] == oppositeToken and not completed:
                next_idx = i - 16

                while next_idx // 8 != -1:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx -= 8

            # down
            if i // 8 < 6 and board[i + 8] == oppositeToken and not completed:
                next_idx = i + 16

                while next_idx // 8 != 8:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx += 8

            # upleft
            if i // 8 > 1 and i % 8 > 1 and board[i - 9] == oppositeToken and not completed:
                next_idx = i - 18

                while next_idx // 8 != -1 and next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx -= 9

            # upright
            if i // 8 > 1 and i % 8 < 6 and board[i - 7] == oppositeToken and not completed:
                next_idx = i - 14

                while next_idx // 8 != -1 and next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx -= 7

            # downleft
            if i // 8 < 6 and i % 8 > 1 and board[i + 7] == oppositeToken and not completed:
                next_idx = i + 14

                while next_idx // 8 != 8 and next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx += 7

            # downright 
            if i // 8 < 6 and i % 8 < 6 and board[i + 9] == oppositeToken and not completed:
                next_idx = i + 18

                while next_idx // 8 != 8 and next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        break
                    elif board[next_idx] == '.':
                        break

                    next_idx += 9

    return moves



main()