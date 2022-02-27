import sys
import itertools as itt

with open(sys.argv[1], "r") as f:
	board = []
	for line in f.readlines():
		line = line.strip()
		if not line:
			break
		board.append([int(c) for c in line])
	if any(len(row) != len(board) for row in board):
		raise ValueError("Board is not a square!")

def step(board):
	frontier = set()
	flashed = set()
	for i, row in enumerate(board):
		for j in range(len(row)):
			row[j] += 1
			if row[j] > 9:
				frontier.add((i, j))
				flashed.add((i, j))
	while frontier:
		i, j = frontier.pop()
		i1a, i1b = max(i-1, 0), min(i+2, len(board))
		j1a, j1b = max(j-1, 0), min(j+2, len(board))
		for i1, j1 in itt.product(range(i1a, i1b), range(j1a, j1b)):
			if (i1, j1) in flashed:
				continue
			board[i1][j1] += 1
			if board[i1][j1] > 9:
				frontier.add((i1, j1))
				flashed.add((i1, j1))
	for i, j in flashed:
		board[i][j] = 0
	return len(flashed)

print(sum(step(board) for _ in range(100)))
