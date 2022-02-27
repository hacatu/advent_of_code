import sys

x = 0
y = 0

with open(sys.argv[1], "r") as f:
	for line in f.readlines():
		toks = line.split()
		if toks[0] == "forward":
			x += int(toks[1])
		elif toks[0] == "up":
			y -= int(toks[1])
		elif toks[0] == "down":
			y += int(toks[1])

print(x*y)


