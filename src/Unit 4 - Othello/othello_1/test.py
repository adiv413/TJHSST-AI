board = "..................x.o.....ooxx...ooxxx.....ox.......o..........."
moves = [32, 42, 11, 12, 17, 50, 19, 51, 25, 60]
moves.sort()

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