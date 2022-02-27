import sys
import itertools as itt

with open(sys.argv[1], "r") as f:
	lut = None
	img = []
	bg = "."
	for line in f.readlines():
		line = line.strip()
		if not line:
			continue
		if lut is None:
			lut = line
			continue
		img.append(list(line))

def step(img, bg):
	irows = len(img)
	icols = len(img[1])
	res = [[None]*(icols + 2) for _ in range(irows + 2)]
	for row, col in itt.product(range(2, irows), range(2, icols)):
		nmask = 0
		for dy, dx in itt.product((-2, -1, 0), (-2, -1, 0)):
			nmask <<= 1
			nmask |= int(img[row + dy][col + dx] == "#")
		res[row][col] = lut[nmask]
	for row, col in itt.chain(
		itt.product((0, 1, irows, irows+1), range(icols+2)),
		itt.product(range(2, irows), (0, 1, icols, icols+1))
	):
		nmask = 0
		for dy, dx in itt.product((-2, -1, 0), (-2, -1, 0)):
			nmask <<= 1
			x = col + dx
			y = row + dy
			if not (0 <= x < icols and 0 <= y < irows):
				nmask |= int(bg == "#")
			else:
				nmask |= int(img[y][x] == "#")
		res[row][col] = lut[nmask]
	return res, lut[511*int(bg == "#")]

def show(img):
	for row in img:
		print("".join(row))

print("input:")
#show(img)
for i in range(50):
	img, bg = step(img, bg)
	print(f"step {i+1}:")
#	show(img)
lit = 0
for c in itt.chain.from_iterable(img):
	if c == "#":
		lit += 1
print(f"{lit} lit px")
