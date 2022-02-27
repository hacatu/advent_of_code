import sys

x = 0
y = 0
a = 0

with open(sys.argv[1], "r") as f:
	for line in f.readlines():
		toks = line.split()
		if toks[0] == "forward":
			d = int(toks[1])
			x += d
			y += a*d
		elif toks[0] == "up":
			a -= int(toks[1])
		elif toks[0] == "down":
			a += int(toks[1])

print(x*y)


