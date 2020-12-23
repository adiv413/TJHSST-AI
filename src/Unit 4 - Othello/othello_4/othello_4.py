import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4

def main():
    # setup

    board = '.' * 27 + 'ox......xo' + '.' * 27
    tokenToMove = ''
    oppositeToken = ''
    possible_moves = []
    first_run = args == []
    final_move = None

    while args or first_run:
        if args and args[0].startswith('-'):
            args.pop(0)
            continue

        if args and len(args[0]) == 64:
            board = args[0].lower()
            args.pop(0)

        if args and args[0].isalpha():
            tokenToMove = args[0].lower()
            args.pop(0)
        elif not tokenToMove:
            num_tokens = 64 - board.count('.')

            if num_tokens % 2 == 0:
                tokenToMove = 'x'
            else:
                tokenToMove = 'o'

        if args and args[0]:
            if args[0].isdigit():
                temp_move = int(args[0])
                if 0 <= temp_move <= 63:
                    possible_moves.append(temp_move)
                    args.pop(0)
            else:
                if len(args[0]) == 2 and 'a' <= args[0][0].lower() <= 'h' and args[0][1].isdigit() and 0 <= int(args[0][1]) <= 8:
                    possible_moves.append((int(args[0][1]) - 1) * 8 + ord(args[0][0].lower()) - ord('a'))
                    args.pop(0)

        first_run = False

    oppositeToken = 'o' if tokenToMove == 'x' else 'x'
    
    # find final move
    possible_moves = find_or_make_moves(board, tokenToMove, oppositeToken)
    edge_moves = []
    good_moves = []
    bad_moves = []

    # 1. random move for the first move

    if board == '.' * 27 + 'ox......xo' + '.' * 27:
        final_move = possible_moves[0]

    # 2. go for a corner

    if final_move is None:
        for move in possible_moves:
            if move == 0 or move == 7 or move == 56 or move == 63:
                final_move = move
                break

    # 3. if you can connect to a corner, play there (also collect info on which are edge moves)

    if final_move is None:
        for move in possible_moves:
            if 0 <= move <= 7 or 56 <= move <= 63:
                edge_moves.append(move)

                # check going to the right
                temp = move + 1
                while temp % 8 != 7 and board[temp] == oppositeToken: temp += 1

                if move % 8 != 6 and temp % 8 == 7 and board[temp] == tokenToMove:
                    final_move = move
                    break

                # check going to the left
                temp = move - 1
                while temp % 8 != 0 and board[temp] == oppositeToken: temp -= 1

                if move % 8 != 1 and temp % 8 == 0 and board[temp] == tokenToMove:
                    final_move = move
                    break

            elif move % 8 == 0 or move % 8 == 7:
                edge_moves.append(move)

                # check going up
                temp = move - 8
                while temp // 8 != 0 and board[temp] == oppositeToken: temp -= 8

                if move // 8 != 1 and temp // 8 == 0 and board[temp] == tokenToMove:
                    final_move = move
                    break

                # check going down
                temp = move + 8
                while temp // 8 != 7 and board[temp] == oppositeToken: temp += 8

                if move // 8 != 6 and temp // 8 == 7 and board[temp] == tokenToMove:
                    final_move = move
                    break


    #DELETE THIS LATER LAST RESORTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
    if final_move is None:
        final_move = possible_moves[0]

    

    

    # first snapshot 
    final_board = find_or_make_moves(board, tokenToMove, oppositeToken, final_move)

    tokenThatMoved = tokenToMove
    tokenToMove, oppositeToken = oppositeToken, tokenToMove

    final_moves = find_or_make_moves(final_board, tokenToMove, oppositeToken)

    print()

    for i in range(8):
        for j in range(8):
            print(board[i * 8 + j], end=' ')
        print()

    print(board)

    print(str(board.count('x')) + '/' + str(board.count('o')))

    print('Possible moves for', tokenThatMoved + ':', possible_moves)

    print()

    # second snapshot

    for i in range(8):
        for j in range(8):
            print(final_board[i * 8 + j], end=' ')
        print()

    print(final_board)

    if '.' in final_board and final_moves:
        print('Possible moves for', tokenToMove + ':', final_moves)
    elif '.' in final_board and not final_moves:
        tokenToMove, oppositeToken = oppositeToken, tokenToMove
        print('Possible moves for', tokenToMove + ':', find_or_make_moves(final_board, tokenToMove, oppositeToken))

    print(str(final_board.count('x')) + '/' + str(final_board.count('o')))

    print(tokenThatMoved, 'moves to', final_move)

# returns the possible set of moves if moveIndex is not provided, otherwise returns the updated board    

def find_or_make_moves(board, tokenToMove, oppositeToken, moveIndex=None):
    moves = []
    tokensToFlip = []
    # left, right, up, down, upleft, upright, downleft, downright
    start = 0
    end = len(board)

    if moveIndex is None and 'x' in board and 'o' in board:
        start = min(board.index('x'), board.index('o'))
        start = max(start - 9, 0)

        end = max(board.rindex('x'), board.rindex('o'))
        end = min(end + 10, len(board))
    # print(tokenToMove, oppositeToken)

    loopBounds = None

    if moveIndex is None:
        loopBounds = (start, end)
    else:
        loopBounds = (moveIndex, moveIndex + 1)

    # current has to be dot, next has to be opposite, keep going in same direction until you reach same token as tokenToMove
    for i in range(*loopBounds):
        curr = board[i]

        if curr == '.':
            completed = False

            # right
            if i % 8 < 6 and board[i + 1] == oppositeToken:
                tempTokensToFlip = [i, i + 1]
                next_idx = i + 2

                while next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 1

            # left
            if i % 8 > 1 and board[i - 1] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 1]
                next_idx = i - 2

                while next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 1

            # up
            if i // 8 > 1 and board[i - 8] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 8]
                next_idx = i - 16

                while next_idx // 8 != -1:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 8

            # down
            if i // 8 < 6 and board[i + 8] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i + 8]
                next_idx = i + 16

                while next_idx // 8 != 8:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 8

            # upleft
            if i // 8 > 1 and i % 8 > 1 and board[i - 9] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 9]
                next_idx = i - 18

                while next_idx // 8 != -1 and next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 9

            # upright
            if i // 8 > 1 and i % 8 < 6 and board[i - 7] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i - 7]
                next_idx = i - 14

                while next_idx // 8 != -1 and next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx -= 7

            # downleft
            if i // 8 < 6 and i % 8 > 1 and board[i + 7] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i + 7]
                next_idx = i + 14

                while next_idx // 8 != 8 and next_idx % 8 != 7:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        completed = True
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 7

            # downright 
            if i // 8 < 6 and i % 8 < 6 and board[i + 9] == oppositeToken and (not completed or moveIndex is not None):
                tempTokensToFlip = [i, i + 9]
                next_idx = i + 18

                while next_idx // 8 != 8 and next_idx % 8 != 0:
                    if board[next_idx] == tokenToMove:
                        moves.append(i)
                        tokensToFlip += tempTokensToFlip
                        break
                    elif board[next_idx] == '.':
                        break

                    if moveIndex is not None:
                        tempTokensToFlip.append(next_idx)

                    next_idx += 9

    if moveIndex is not None:
        updated_board = board

        for i in tokensToFlip:
            updated_board = updated_board[:i] + tokenToMove + updated_board[i + 1:] 
        return updated_board

    return moves

main()