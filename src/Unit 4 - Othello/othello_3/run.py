import subprocess

# boards = ["d3", "d3c3", "d3c3c4", "d3c3c4e3", "d3c3c4e3d2", "d3c3c4e3d2b4", "d3c3c4e3d2b4b3", "d3c3c4e3d2b4b3d1", "d3c3c4e3d2b4b3d1f4", "d3c3c4e3d2b4b3d1f4f5", "d3c3c4e3d2b4b3d1f4f5e2", "d3c3c4e3d2b4b3d1f4f5e2e1", "d3c3c4e3d2b4b3d1f4f5e2e1f1", "d3c3b3"]
# moves = ["c3", "c4", "e3", "d2", "b4", "b3", "d1", "f4", "f5", "e2", "e1", "f1", "c2", "e3"]
# for i in boards:
#     board = [i[j:j+2] for j in range(0, len(i), 2)]
#     ret = subprocess.check_output(['python', 'othello_3.py', *board]).decode().splitlines()
#     print(ret[-1])

# for i in moves:
#     print((int(i[1]) - 1) * 8 + ord(i[0].lower()) - ord('a'))


x = open("temp.txt", "r")
for i in x:
    y = i.split()
    print("'" + y[0] + "'", end=", ")
