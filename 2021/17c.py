import sys
from math import ceil, floor, sqrt

with open(sys.argv[1], "r") as f:
	for line in f.readlines():
		line = line.strip()
		_, line = line.split(": ")
		xpart, ypart = line.split(", ")
		ax, bx = map(int, xpart[2:].split(".."))
		ay, by = map(int, ypart[2:].split(".."))

c = bx-ax+1
for vy in range(-ay-1, ay, -1):
	print(vy)
	for vx in range(floor(sqrt(2*ax+.25)-.5), bx+1):
#		print(f"\t{vx}")
		x, y, dx, dy = 0, 0, vx, vy
		while x <= bx and y >= ay:
			x += dx
			y += dy
			dx = dx - 1 if dx > 0 else 0
			dy -= 1
			if (ax <= x <= bx) and (ay <= y <= by):
				c += 1
				break

print(c)
