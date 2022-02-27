import sys

with open(sys.argv[1], "r") as f:
	xs = [int(line) for line in f.readlines() if line.rstrip()]
	c = 0
	for i in range(1, len(xs)):
		if xs[i] > xs[i-1]:
			c += 1
	print(c)

