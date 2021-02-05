import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
LIMIT_AB = 14
num_games = 10
recur_limit = 5
import time
import random

corners = [0, 7, 56, 63]
csquares = [(0, 1), (7, 6), (0, 8), (7, 15), (56, 48), (63, 55), (56, 57), (63, 62)]
csquares_worse = [(0, 9), (7, 14), (56, 49), (63, 54)]

row2colb_top = [(-8, j) for j in range(10,14)]
row2colb_bottom = [(8, j) for j in range(50, 54)]
row2colb_left = [(-1, 17 + 8 * j) for j in range(4)]
row2colb_right = [(1, 22 + 8 * j) for j in range(4)]

row2colb = row2colb_top + row2colb_bottom + row2colb_left + row2colb_right

edge_top = [j for j in range(1, 7)]
edge_bottom = [j for j in range(57, 63)]
edge_left = [8 + 8 * j for j in range(6)]
edge_right = [15 + 8 * j for j in range(6)]

edges = edge_top + edge_bottom + edge_left + edge_right

inner_diagonals = [18, 27, 36, 45, 21, 28, 35, 42]

positions = {"corners" : corners, "csquares" : csquares, "csquares_worse" : csquares_worse, \
    "row2colb" : row2colb, "edges": edges, "inner_diagonals" : inner_diagonals}

def main():
    if not args:
        scores = []
        times = []
        try:
            result = playTournament(num_games, LIMIT_AB)
            scores.append(result[0][:-1])
            times.append(str(result[1])[:5])
        except KeyboardInterrupt:
            pass

        print('\n\n------------FINAL STATS (scores, times)------------')
        print(*scores)
        print(*times)

    else:
        # setup

        board = '.' * 27 + 'ox......xo' + '.' * 27
        tokenToMove = ''
        oppositeToken = ''
        possible_moves = []
        first_run = args == []

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

        findBestMove(board, tokenToMove, oppositeToken, LIMIT_AB)


# Heuristic is calculated using token counts, mobility, and square valuation

# token counts: range = [-5,5], dom = [0,1], x = current player's token cnt, a = total num tokens on board
# value = (a/50) * (11**x - 6)

# mobility:
# if x == 0: -24
# if x == 1: -18
# else: x ** 1.5 - 8

# position: 
# corner = +4, csquare = -3, diagonally-adjacent csquare = -4, row 2/col B = -1, edges = +2, inner diagonals = +1


def findBoardValue(board, tokenToMove, oppositeToken):
    num_possible_moves = len(find_or_make_moves(board, tokenToMove, oppositeToken))
    num_player_tok = board.count(tokenToMove)
    num_opp_tok = board.count(oppositeToken)
    total_tok = num_player_tok + num_opp_tok
    curr_player_score = num_player_tok / total_tok
    mobility = 0
    position_score = 0

    score_val = (total_tok / 50) * ((11 ** curr_player_score) - 6) * 1.2

    if num_possible_moves == 0:
        mobility = -24
    elif num_possible_moves == 1:
        mobility = -18
    else:
        mobility = (num_possible_moves ** 1.5) - 8

    for i in positions["corners"]:
        if board[i] == tokenToMove:
            position_score += 4
    
    for i in positions["csquares"]:
        if board[i[0]] != tokenToMove and board[i[1]] == tokenToMove:
            position_score -= 3

    for i in positions["csquares_worse"]:
        if board[i[0]] != tokenToMove and board[i[1]] == tokenToMove:
            position_score -= 4
    
    for i in positions["row2colb"]:
        if board[i[1] + i[0]] != tokenToMove and board[i[0]] == tokenToMove:
            position_score -= 1

    for i in positions["edges"]:
        if board[i] == tokenToMove:
            position_score += 2
    
    for i in positions["inner_diagonals"]:
        if board[i] == tokenToMove:
            position_score += 1

    return score_val + mobility + position_score

# finds the optimal move

def findBestMove(board, tokenToMove, oppositeToken, limitNM, verbose=True):
    moves = find_or_make_moves(board, tokenToMove, oppositeToken)
    ret = None

    if verbose and moves:
        # print first move immediately just in case 
        print(moves[0])

    final_move = None

    # if we're in the last LIMIT_AB moves of the game, run negamax all the way

    if board.count('.') < limitNM:
        if verbose:
            ret = alphabeta(board, tokenToMove, oppositeToken, -500, 500, 3, start_time=time.time())
            if ret:
                print(ret[-1])

        negamax_output = alphabeta(board, tokenToMove, oppositeToken, -65, 65) # no time limit

        if not negamax_output:
            if not ret:
                return moves[0]
            else:
                return ret[-1]
        else:
            final_move = negamax_output[-1]
    else:
        prev = None
        # otherwise, run negamax up until a certain limit
        if verbose:
            start = time.time()
            # iterative deepening
            for i in range(1, recur_limit):
                negamax_output = alphabeta(board, tokenToMove, oppositeToken, -500, 500, i, start_time=start)
                
                if negamax_output:
                    prev = negamax_output[-1]
                    print(negamax_output[-1])

        else:
            start = time.time()
            # iterative deepening
            for i in range(1, recur_limit):
                negamax_output = alphabeta(board, tokenToMove, oppositeToken, -500, 500, i, start_time=start)
                
                if negamax_output:
                    prev = negamax_output[-1]
        
        if negamax_output:
            final_move = negamax_output[-1]
        elif prev:
            final_move = prev
        else:
            final_move = moves[0]
        
    
    tokenThatMoved = tokenToMove

    if verbose:
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

        print('Possible moves for', tokenThatMoved + ':', moves)

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

        if negamax_output:
            print('Min score: ' + str(negamax_output[0]) + '; move sequence:', *(negamax_output[1:]))
            
    return final_move

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


def playGame(myTkn, limitNM):
    board = '.' * 27 + 'ox......xo' + '.' * 27
    tokenToMove = myTkn
    oppositeToken = 'o' if myTkn == 'x' else 'x'
    moveSequence = []

    while True:
        if '.' not in board:
            break

        possibleMoves = find_or_make_moves(board, tokenToMove, oppositeToken)
        if possibleMoves:
            move = None

            if tokenToMove == myTkn:
                move = findBestMove(board, tokenToMove, oppositeToken, limitNM, verbose=False)
            else:
                move = random.choice(possibleMoves)

            moveSequence.append(move)
            board = find_or_make_moves(board, tokenToMove, oppositeToken, moveIndex=move)
            tokenToMove, oppositeToken = oppositeToken, tokenToMove
            
        else:
            # tokenToMove passes, oppositeToken's turn
            tokenToMove, oppositeToken = oppositeToken, tokenToMove
            
            possibleMoves = find_or_make_moves(board, tokenToMove, oppositeToken)

            if possibleMoves:
                move = None

                if tokenToMove == myTkn:
                    move = findBestMove(board, tokenToMove, oppositeToken, limitNM, verbose=False)
                else:
                    move = random.choice(possibleMoves)

                moveSequence.append(move)
                board = find_or_make_moves(board, tokenToMove, oppositeToken, moveIndex=move)
                tokenToMove, oppositeToken = oppositeToken, tokenToMove

            else:
                # both teams pass, end of game
                break
            
    return [moveSequence, board.count(myTkn), board.count('o' if myTkn == 'x' else 'x')]

def playTournament(gameCnt, limitNM):
    start = time.time()
    myScore = 0
    oppScore = 0
    gamesWon = 0
    gamesTied = 0
    gamesLost = 0
    games = []

    print('-------------------------------------INDIVIDUAL GAME RESULTS (LIMIT:', limitNM, ')-------------------------------------')
    print()
    
    for i in range(gameCnt):
        result = playGame('xo'[i % 2], limitNM)
        myScore += result[1]
        oppScore += result[2]

        games.append((result[1] - result[2], i, result[0]))

        print(result[1] - result[2], end=' ', flush=True)

        if result[1] - result[2] > 0:
            gamesWon += 1
        elif result[1] - result[2] == 0:
            gamesTied += 1
        else:
            gamesLost += 1

        if i % 10 == 9:
            print()
    
    print()
    
    print('My token count:', myScore)
    print('Opponent token count:', oppScore)
    print('Total:', myScore + oppScore)
    print('Score:', str(myScore / (myScore + oppScore) * 100)[:4] + '%')
    print('Win %:', gamesWon / gameCnt)
    print('Draw %:', gamesTied / gameCnt)
    print('Lose %:', gamesLost / gameCnt)

    worst_game = min(games)
    print('Game', worst_game[1], 'as', 'xo'[worst_game[1] % 2], '=>', worst_game[0], *worst_game[2])
    
    games.remove(worst_game)
    
    worst_game = min(games)
    print('Game', worst_game[1], 'as', 'xo'[worst_game[1] % 2], '=>', worst_game[0], *worst_game[2])
    elapsed = time.time() - start

    print()
    print('-------------------------------------TOTAL TOURNAMENT RESULTS (LIMIT:', limitNM, ')-------------------------------------')
    print()
    print(str(myScore / (myScore + oppScore) * 100)[:4] + '%', elapsed)
    print('\n\n\n')

    return str(myScore / (myScore + oppScore) * 100)[:4] + '%', elapsed

# ground truth (my tokens - opp tokens) scaling equation:
# y = 0.000035(x+5)^3 - 0.0002x^2 + 0.28x
# where x is the score and y is the value in my units so that it is on the same level with my heuristic

def alphabeta(board, tokenToMove, oppositeToken, raw_lower, upper, level=None, start_time=0):
    # alphabeta should run for a max of 2.5s to not waste too much time (iterative deepening should cover it)
    if time.time() - start_time <= 2.5 or start_time == 0:
        lower = raw_lower
        possible_moves = find_or_make_moves(board, tokenToMove, oppositeToken)

        # bottom level, base case

        if level is not None and level <= 0:
            # skip
            if not possible_moves:
                skipped_possible_moves = find_or_make_moves(board, tokenToMove, oppositeToken)

                # if the game is already over

                if not skipped_possible_moves:
                    curr_score = board.count(tokenToMove) - board.count(oppositeToken)
                    # scaled_score = 0.000035 * ((curr_score + 5) ^ 3) - 0.0002 * (curr_score ^ 2) + 0.28 * curr_score
                    return [curr_score]

                else:
                    # just recur one more time

                    result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, 1, start_time=start_time)
                    if result:
                        return [-result[0]] + result[1:] + [-1]
                    else:
                        return

            else:
                # use my heuristic
                ret = findBoardValue(board, tokenToMove, oppositeToken) - findBoardValue(board, oppositeToken, tokenToMove)
                return [ret]


        if not possible_moves:
            # curr token cannot move, pass
            possible_moves = find_or_make_moves(board, oppositeToken, tokenToMove)

            if not possible_moves:
                # double skip or end of game 
                curr_score = board.count(tokenToMove) - board.count(oppositeToken)
                # scaled_score = 0.000035 * ((curr_score + 5) ^ 3) - 0.0002 * (curr_score ^ 2) + 0.28 * curr_score
                return [curr_score]

            result = None
            
            if level is None:
                result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, start_time=start_time)
            else:
                result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, level - 1, start_time=start_time)

            if result:
                return [-result[0]] + result[1:] + [-1]
            else:
                return

        bestSoFar = [lower - 1]

        
        for mv in possible_moves:
            newBrd = find_or_make_moves(board, tokenToMove, oppositeToken, moveIndex=mv)

            if level is None:
                result = alphabeta(newBrd, oppositeToken, tokenToMove, -upper, -lower, start_time=start_time)
            else:
                result = alphabeta(newBrd, oppositeToken, tokenToMove, -upper, -lower, level - 1, start_time=start_time)
                
            if not result:
                return

            score = -result[0]

            if score < lower:
                continue
            if score > upper:
                return [score]

            if score > bestSoFar[0]:
                bestSoFar = [score] + result[1:] + [mv]

            lower = score + 1
            
        return bestSoFar
    
    return

if __name__ == '__main__': 
    main()