import sys

fold_x_prefix = "fold along x="
fold_y_prefix = "fold along y="

def fold(points, i, pos):
	res = set()
	for p in points:
		coord = p[i]
		if coord > pos:
			p = p[:i] + (2*pos - coord,) + p[i+1:]
		res.add(p)
	return res

with open(sys.argv[1], "r") as f:
	points = set()
	num_folds = 0
	for line in f.readlines():
		if not (line := line.strip()):
			continue
		if line.startswith(fold_x_prefix):
			points = fold(points, 0, int(line[len(fold_x_prefix):]))
			if num_folds := num_folds + 1:
				break
		elif line.startswith(fold_y_prefix):
			points = fold(points, 1, int(line[len(fold_y_prefix):]))
			if num_folds := num_folds + 1:
				break
		else:
			points.add(tuple(map(int, line.split(","))))

print(len(points))
width = max(x for (x,y) in points)
height = max(y for (x,y) in points)
#for y in range(height+1):
#	print("".join("#" if (x,y) in points else "." for x in range(width+1)))
