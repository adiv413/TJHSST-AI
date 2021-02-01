import sys; args = sys.argv[1:]
# Aditya Vasantharao, pd. 4
LIMIT_AB = 12
num_games = 6
recur_limit = 5
import time
import random

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

def findBestMoveHeuristic(board, tokenToMove, oppositeToken):
    final_move = None
    best_move_value = None
    possible_moves = find_or_make_moves(board, tokenToMove, oppositeToken)
    very_good_moves = [] # edge moves
    good_moves = [] # normal moves
    bad_moves = [] # row 2/col B moves
    very_bad_moves = [] # corner-adjacent moves
    negamax_output = []

    # 1. random move for the first move to hoard time

    if board.count('x') + board.count('o') <= 5:
        final_move = possible_moves[0]

    # 2. go for a corner

    if final_move is None:
        for move in possible_moves:
            if move == 0 or move == 7 or move == 56 or move == 63:
                final_move = move
                break

    # 3. categorize moves based on position (row 2 col b + corner-adjacent)

    if final_move is None:
        for move in possible_moves:
            if not (0 <= move <= 7 or 56 <= move <= 63 or move % 8 == 0 or move % 8 == 7) \
                and (move % 8 == 1 or move % 8 == 6 or move // 8 == 1 or move // 8 == 6):

                bad_moves.append(move)
            elif (board[0] == '.' and (move == 1 or move == 8)) \
                or (board[7] == '.' and (move == 6 or move == 15)) \
                or (board[56] == '.' and (move == 48 or move == 57)) \
                or (board[63] == '.' and (move == 55 or move == 62)):
                
                very_bad_moves.append(move)

    # 4. if you can connect to a corner, play there (also collect info on which are edge moves, those are very good moves)

    if final_move is None:
        for move in possible_moves:
            if 0 <= move <= 7 or 56 <= move <= 63:
                if move not in very_bad_moves:
                    very_good_moves.append(move)

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
                if move not in very_bad_moves:
                    very_good_moves.append(move)

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

    # 5. if the move is at an edge and is surrounded by oppositeTokens (..x.x... -> o), play there

    if final_move is None:
        for move in possible_moves:
            if (0 <= move <= 7 or 56 <= move <= 63) and board[move + 1] == board[move - 1] == oppositeToken:
                final_move = move
                break

            elif (move % 8 == 0 or move % 8 == 7) and board[move + 8] == board[move - 8] == oppositeToken:
                final_move = move
                break
                

    # 6. finalize good moves

    if final_move is None:
        already_seen = very_good_moves + bad_moves + very_bad_moves

        for move in possible_moves:
            if move not in already_seen:
                good_moves.append(move)


    # 6.5. finalize score for move if already selected
    if final_move is not None:
        best_move_value = 10

    # 7. Run algorithm to find the value of a move
    # move position weighting - very good: +2.8, good: +1, bad: -1, very bad: -2

    # increase in score: raw_increase x 0.3

    # number of opponent places to move: 12 / raw_number + (og_number - raw_number) * 0.4
    # takes into account both the raw number of opponent moves as well as decrease in opponent moves

    # total value of a move: increase in score + opponent move score + move position weighting

    # I estimate that the best move values are going to be between 1-10, so the move position weighting
    # between 'very good' and 'good' accounts for approximately 25% of the total value on average,
    # with the function being 1.8 / (x + 2.8), where x is the value of a move before the move position weighting is added
    
    if final_move is None:
        # print(very_good_moves, good_moves, bad_moves, very_bad_moves)
        # print(possible_moves)
        best_move = None
        move_categories = [very_good_moves, good_moves, bad_moves, very_bad_moves]
        current_score = board.count(tokenToMove) - board.count(oppositeToken)
        current_opp_moves = len(find_or_make_moves(board, oppositeToken, tokenToMove))

        for i in range(len(move_categories)):
            move_category = move_categories[i]

            if final_move is None:
                for move in move_category:
                    new_board = find_or_make_moves(board, tokenToMove, oppositeToken, move) # make the move
                    new_opp_moves = len(find_or_make_moves(new_board, oppositeToken, tokenToMove)) # find num of opp moves

                    if new_opp_moves == 0: # if there arent any opp moves if we make this move
                        final_move = move
                        best_move_value = 12
                        break

                    new_score = new_board.count(tokenToMove) - new_board.count(oppositeToken)
                    score_improvement = new_score - current_score
                    opp_moves_improvement = current_opp_moves - new_opp_moves

                    move_value = score_improvement * 0.3 + 12 / new_opp_moves + opp_moves_improvement * 0.4

                    # account for move position weighting

                    if i == 0: # very good moves
                        move_value += 2.8
                    elif i == 1: # good moves
                        move_value += 1
                    elif i == 2: # bad moves
                        move_value -= 1
                    elif i == 3: # very bad moves
                        move_value -= 2

                    # print(move, move_value, new_opp_moves, score_improvement)

                    if best_move_value is None or move_value > best_move_value:
                        best_move_value = move_value
                        best_move = move
        
        if final_move is None:
            final_move = best_move

    # last resort in case something goes wrong
    if final_move is None:
        print('ERROR: LAST RESORT CONDITION MET')
        final_move = possible_moves[0]

    return final_move, best_move_value

# finds the optimal move

def findBestMove(board, tokenToMove, oppositeToken, limitNM, verbose=True):
    moves = find_or_make_moves(board, tokenToMove, oppositeToken)
    
    if verbose and moves:
        # print first move immediately just in case 
        print(moves[0])

    final_move = None

    # if we're in the last LIMIT_AB moves of the game, run negamax all the way

    if board.count('.') < limitNM:
        negamax_output = alphabeta(board, tokenToMove, oppositeToken, -65, 65)
        final_move = negamax_output[-1]
    else:
        # otherwise, run negamax up until a certain limit
        if verbose:
            # iterative deepening
            for i in range(recur_limit // 2 + 1):
                negamax_output = alphabeta(board, tokenToMove, oppositeToken, -65, 65, i * 2 + 1)
                print(negamax_output[-1])

        else:
            negamax_output = alphabeta(board, tokenToMove, oppositeToken, -65, 65, recur_limit)
        final_move = negamax_output[-1]
        
    
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

def alphabeta(board, tokenToMove, oppositeToken, raw_lower, upper, level=None):
    
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

                result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, 1)
                return [-result[0]] + result[1:] + [-1]

        else:
            # use my heuristic
            ret = findBestMoveHeuristic(board, tokenToMove, oppositeToken)
            return [ret[1], ret[0]]


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
            result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower)
        else:
            result = alphabeta(board, oppositeToken, tokenToMove, -upper, -lower, level - 1)

        return [-result[0]] + result[1:] + [-1]

    bestSoFar = [lower - 1]

    for mv in possible_moves:
        newBrd = find_or_make_moves(board, tokenToMove, oppositeToken, moveIndex=mv)

        if level is None:
            result = alphabeta(newBrd, oppositeToken, tokenToMove, -upper, -lower)
        else:
            result = alphabeta(newBrd, oppositeToken, tokenToMove, -upper, -lower, level - 1)
            
        score = -result[0]

        if score < lower:
            continue
        if score > upper:
            return [score]

        if score > bestSoFar[0]:
            bestSoFar = [score] + result[1:] + [mv]

        lower = score + 1

    return bestSoFar

if __name__ == '__main__': 
    main()