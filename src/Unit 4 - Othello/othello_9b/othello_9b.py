# Aditya Vasantharao, pd. 4
import sys; args = sys.argv[1:]
import time
import random

# LIMIT_AB = 14
# num_games = 10
# recur_limit = 13
# time_limit = 10

LIMIT_AB = 14
recur_limit = 5
num_games = 10
time_limit = 0.4

use_opening_book = True

alphabeta_time_limit = time_limit # change to 0 if no alphabeta time limit

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
x_moves = [26, 19, 13, 21, 5, 29, 10, 17, 3, 1, 24, 25, 43, 0, 6, 39, 40, 8, 49, 42, 44, 53, 56, 15, 59, 60, 23, 57, 62, 63, 47, 46]              
o_moves = [34, 21, 20, 37, 18, 10, 26, 33, 24, 8, 40, 49, 56, 30, 47, 55, 58, 50, 0, 3, 4, 14, 42, 5, 51, 15, 60, 39, 63, 62]

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

        print(findBestMove(board, tokenToMove, oppositeToken, LIMIT_AB, recur_limit))


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

def findBestMove(board, tokenToMove, oppositeToken, limitNM, recur_limit, verbose=True, best_move_obj=None):
    moves = find_or_make_moves(board, tokenToMove, oppositeToken)
        
    if tokenToMove == 'x':
        move = x_moves[(60 - board.count('.')) // 2]
        if move in moves:
            print('sd')
            return move

    if tokenToMove == 'o':
        move = o_moves[(60 - board.count('.')) // 2]
        if move in moves:
            return move

    ret = None

    if use_opening_book:
        if board in opening_book:
            for i in opening_book[board]:
                if i in moves:
                    print("opening book")
                    return i

    if best_move_obj and moves:
        # print first move immediately just in case 
        best_move_obj.value = moves[0]
    elif verbose and moves:
        print(moves[0])

    final_move = None

    # if we're in the last LIMIT_AB moves of the game, run negamax all the way

    if board.count('.') < limitNM:
        if verbose:
            ret = alphabeta(board, tokenToMove, oppositeToken, -500, 500, 4, start_time=time.time())
            if ret:
                if best_move_obj:
                    best_move_obj.value = ret[-1]
                elif verbose:
                    print(ret[-1])

        negamax_output = alphabeta(board, tokenToMove, oppositeToken, -65, 65, start_time=alphabeta_time_limit)

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
        start = time.time()
        # iterative deepening
        for i in range(1, recur_limit):
            negamax_output = alphabeta(board, tokenToMove, oppositeToken, -500, 500, i, start_time=start)
            
            if negamax_output:
                prev = negamax_output[-1]
                if best_move_obj:
                    best_move_obj.value = negamax_output[-1]
                elif verbose:
                    print(negamax_output[-1])
        
        if negamax_output:
            final_move = negamax_output[-1]
        elif prev:
            final_move = prev
        else:
            final_move = moves[0]
    
    if best_move_obj:
        best_move_obj.value = final_move
    elif verbose:
        print(final_move)
        
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
                move = findBestMove(board, tokenToMove, oppositeToken, limitNM, recur_limit, verbose=False)
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
                    move = findBestMove(board, tokenToMove, oppositeToken, limitNM, recur_limit, verbose=False)
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

def alphabeta(board, tokenToMove, oppositeToken, raw_lower, upper, level=None, start_time=0):
    # alphabeta should run for a max of 2.5s to not waste too much time (iterative deepening should cover it)
    if time.time() - start_time <= time_limit or start_time == 0:
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

def rotate(board):
    width = 8
    height = 8
    board_list = set()

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

    return board_list

class Strategy():
    logging = True
    

    def best_strategy(self, board, player, best_move, still_running):
        oppositeToken = 'o' if player == 'x' else 'x'
        moves = find_or_make_moves(board, player, oppositeToken)
        
        if player == 'x':
            move = x_moves[(60 - board.count('.')) // 2]
            if move in moves:
                best_move.value = move
            else:
                best_move.value = findBestMove(board, player, oppositeToken, LIMIT_AB, recur_limit, best_move_obj=best_move)

        if player == 'o':
            move = o_moves[(60 - board.count('.')) // 2]

            if move in moves:
                best_move.value = move
            else:
                best_move.value = findBestMove(board, player, oppositeToken, LIMIT_AB, recur_limit, best_move_obj=best_move)

        print(board, best_move.value)

        # best_move.value = findBestMove(board, player, oppositeToken, LIMIT_AB, recur_limit, best_move_obj=best_move)


opening_book_raw = ['C4c3D3c5B3f4B5b4C6d6F5', 'C4c3D3c5B4d2C2f4D6c6F5e6F7', 'C4c3D3c5B6c6B5', 'C4c3D3c5D6f4B4c6B5b3B6e3C2a4A5a6D2', 'C4c3D3c5D6f4B4b6B5c6B3', 'C4c3D3c5D6f4B4e3B3', 'C4c3D3c5D6f4F5d2G4d7', 'C4c3D3c5D6f4F5d2B5', 'C4c3D3c5D6f4F5e6C6d7', 'C4c3D3c5D6f4F5e6F6', 'C4c3D3c5F6e3C6f5F4g5', 'C4c3D3c5F6e2C6', 'C4c3E6c5', 'C4c3F5c5', 'C4e3F4c5D6f3E6c3D3e2B5f5B4f6C2e7D2c7', 'C4e3F4c5D6f3D3c3', 'C4e3F4c5D6f3E6c3D3e2B6f5B4f6G5d7', 'C4e3F4c5D6f3E6c3D3e2B5f5B3', 'C4e3F4c5D6f3E6c3D3e2B6f5G5f6', 'C4e3F5b4F3f4E2e6G5f6D6c6', 'C4e3F5e6F4c5D6c6F7g5G6', 'C4e3F6e6F5c5C3c6D3d2E2b3C1c2B4a3A5b5A6a4A2', 'C4e3F6e6F5c5C3b4D6c6B5a6B6c7', 'C4e3F6e6F5c5C3c6D6', 'C4e3F6e6F5c5F4g5G4f3C6d3D6b3C3b4E2b6', 'C4e3F6e6F5c5F4g6F7d3', 'C4e3F6e6F5g6E7c5']
opening_book = {}

for i in opening_book_raw:
    curr_opening_moves_raw = [i[j:j+2] for j in range(0, len(i), 2)]
    curr_opening_moves = [(int(m[1]) - 1) * 8 + ord(m[0].lower()) - ord('a') for m in curr_opening_moves_raw]
    curr_board = '.' * 27 + 'ox......xo' + '.' * 27
    temp_tokenToMove = 'x'
    temp_oppositeToken = 'o'

    for j in range(len(curr_opening_moves) - 1):
        curr_board = find_or_make_moves(curr_board, temp_tokenToMove, temp_oppositeToken, curr_opening_moves[j])
        temp_tokenToMove, temp_oppositeToken = temp_oppositeToken, temp_tokenToMove

        if curr_board not in opening_book:
            opening_book[curr_board] = set()

        index_to_replace = curr_opening_moves[j + 1]
        temp_curr_board = curr_board[:index_to_replace] + '*' + curr_board[index_to_replace + 1:]
        x = rotate(temp_curr_board)

        for k in x:
            index_to_add = k.index('*')
            board_to_add = k[:index_to_add] + '.' + k[index_to_add + 1:]
            if board_to_add not in opening_book:
                opening_book[board_to_add] = set()
                
            if index_to_add not in opening_book[board_to_add]:
                opening_book[board_to_add].add(index_to_add)

if __name__ == '__main__':
    main() 