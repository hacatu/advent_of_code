import sys
from collections import Counter

class Board:
	def __init__(self):
		self.coords = {}
		self.width = 0
		self.height = 0
		self.col_counts = Counter()
		self.row_counts = Counter()
		self.score = 0

	def add_row(self, str):
		ents = [int(tok) for tok in str.split()]
		if not self.height:
			self.width = len(ents)
		elif self.width != len(ents):
			raise IndexError("Row size mismatch!")
		for i, x in enumerate(ents):
			self.coords[x] = (self.height, i)
			self.score += x
		self.height += 1

	def mark_number(self, n):
		col, row = self.coords.get(n, (-1, -1))
		if col == -1:
			return False
		self.score -= n
		self.col_counts[col] += 1
		if self.col_counts[col] == self.width:
			return True
		self.row_counts[row] += 1
		if self.row_counts[row] == self.height:
			return True
		return False

with open(sys.argv[1], "r") as f:
	numbers = None
	boards = []
	board = None
	for line in f.readlines():
		line = line.strip()
		if not line:
			if board is not None:
				boards.append(board)
				board = None
		elif numbers is None:
			numbers = [int(tok) for tok in line.split(",")]
		else:
			if board is None:
				board = Board()
			board.add_row(line)

max_turns = -1
max_score = 0
for board in boards:
	for i, n in enumerate(numbers):
		if board.mark_number(n):
			if i > max_turns:
				max_turns = i
				max_score = board.score*n
			break
print(max_score)
