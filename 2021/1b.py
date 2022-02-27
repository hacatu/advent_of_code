import sys

with open(sys.argv[1], "r") as f:
	xs = [int(line) for line in f.readlines() if line.rstrip()]
	c = 0
	w = sum(xs[:3])
	for i in range(3, len(xs)):
		w1 = w + xs[i] - xs[i-3]
		if w1 > w:
			c += 1
		w = w1
	print(c)

