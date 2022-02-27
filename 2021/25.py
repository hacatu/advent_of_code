import sys

with open(sys.argv[1], "r") as f:
	board = []
	d_fish = []
	r_fish = []
	for line in f.readlines():
		line = line.strip()
		if not line:
			continue
		i = len(board)
		boardline = []
		for j, c in enumerate(line):
			if c == 'v':
				boardline.append(2)
				d_fish.append((i, j, False))
			elif c == '>':
				boardline.append(1)
				r_fish.append((i, j, False))
			else:
				boardline.append(0)
		board.append(boardline)
	height = len(board)
	width = len(board[0])
	if any(len(boardline) != width for boardline in board[1:]):
		raise ValueError("Row length mismatch!")

def step(board, d_fish, r_fish):
	did_move = False
	for i, (row, col, _) in enumerate(r_fish):
		can_move = board[row][(col+1)%width] == 0
		r_fish[i] = (row, col, can_move)
	for i, (row, col, can_move) in enumerate(r_fish):
		if not can_move:
			continue
		board[row][col] = 0
		board[row][(col+1)%width] = 1
		r_fish[i] = (row, (col+1)%width, False)
		did_move = True
	for i, (row, col, _) in enumerate(d_fish):
		can_move = board[(row+1)%height][col] == 0
		d_fish[i] = (row, col, can_move)
	for i, (row, col, can_move) in enumerate(d_fish):
		if not can_move:
			continue
		board[row][col] = 0
		board[(row+1)%height][col] = 2
		d_fish[i] = ((row+1)%height, col, False)
		did_move = True
	return did_move

def show(board):
	for boardline in board:
		print("".join(".>v"[c] for c in boardline))

i = 1
while step(board, d_fish, r_fish):
	i += 1
	print(i)

#print(i)
#show(board)
