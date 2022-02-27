import sys
from collections import Counter

# This solution is willfully suboptimal.  At some
# point it becomes fruitful to use interval trees
# on each row and column to find all doubled up
# line segments and all lone line segments, and
# then intersect the lone segments in a second pass.
# There may even be a better solution than that.
# But instead I'll start with a dumb solution and
# only use a better one if needed

with open(sys.argv[1], "r") as f:
	cells = Counter()
	overlaps = 0
	for line in f.readlines():
		line = line.strip()
		if not line:
			break
		toks = line.split(" -> ")
		coords = toks[0].split(",") + toks[1].split(",")
		x1, y1, x2, y2 = map(int, coords)
		if x1 == x2:
			for y in range(min(y1, y2), max(y1, y2) + 1):
				if cells[(x1, y)] == 1:
					overlaps += 1
				cells[(x1, y)] += 1
		elif y1 == y2:
			for x in range(min(x1, x2), max(x1, x2) + 1):
				if cells[(x, y1)] == 1:
					overlaps += 1
				cells[(x, y1)] += 1
		else:
			dx = 1 if x1 < x2 else -1
			dy = 1 if y1 < y2 else -1
			for x, y in zip(range(x1, x2 + dx, dx), range(y1, y2 + dy, dy)):
				if cells[(x, y)] == 1:
					overlaps += 1
				cells[(x, y)] += 1
print(overlaps)

