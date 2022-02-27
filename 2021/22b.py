import sys
import bisect

class Bitarray:
	def __init__(self, *args):
		self.dim = tuple(args)
		self.num_bits = 1
		for d in self.dim:
			self.num_bits *= d
		self.words = (self.num_bits + 63)//64
		self.words = [0]*self.words

	def _idx(self, *idxs):
		idx = 0
		for i, d in zip(idxs, self.dim):
			idx = idx*d + i
		return idx

	def get(self, *idxs):
		idx = self._idx(*idxs)
		w = idx//64
		t = idx%64
		return bool(self.words[w] & (1 << t))

	def set(self, *idxs):
		idx = self._idx(*idxs)
		w = idx//64
		t = idx%64
		self.words[w] |= 1 << t

	def clear(self, *idxs):
		idx = self._idx(*idxs)
		w = idx//64
		t = idx%64
		self.words[w] &= ~(1<<t)

with open(sys.argv[1], "r") as f:
	commands = []
	coord_slices = [set() for _ in range(3)]
	for line in f.readlines():
		line = line.strip()
		if not line:
			break
		is_on, coords = line.split()
		coords = coords.split(",")
		coords = [tok[2:].split("..") for tok in coords]
		a, b = zip(*coords)
		a = [int(x) for x in a]
		b = [int(x) + 1 for x in b]
		for i in range(3):
			if b[i] < a[i]:
				raise ValueError("Invalid range!")
			coord_slices[i].add(a[i])
			coord_slices[i].add(b[i])
		else:
			commands.append((is_on == "on", a, b))

coord_slices = [sorted(slice) for slice in coord_slices]
for i, slice in enumerate(coord_slices):
	print(f"Coordinate {i} has {len(slice)} points of interest")

#print(commands)

#cells = [[[False]*len(coord_slices[2]) for _ in coord_slices[1]] for _ in coord_slices[0]]
cells = Bitarray(*map(len, coord_slices))

for i, (is_on, a, b) in enumerate(commands):
	print(f"{i+1}/{len(commands)}")
	ai = [bisect.bisect_left(slice, ac) for (slice, ac) in zip(coord_slices, a)]
	for xi in range(ai[0], len(coord_slices[0])):
		if coord_slices[0][xi] == b[0]:
			break
		for yi in range(ai[1], len(coord_slices[1])):
			if coord_slices[1][yi] == b[1]:
				break
			for zi in range(ai[2], len(coord_slices[2])):
				if coord_slices[2][zi] == b[2]:
					break
				if is_on:
					cells.set(xi, yi, zi)
				else:
					cells.clear(xi, yi, zi)
#				print(f"setting cells[{xi}][{yi}][{zi}] to {is_on}")

c = 0
for xi in range(len(coord_slices[0])-1):
	dx = coord_slices[0][xi+1] - coord_slices[0][xi]
	for yi in range(len(coord_slices[1])-1):
		dy = coord_slices[1][yi+1] - coord_slices[1][yi]
		for zi in range(len(coord_slices[2])-1):
			if not cells.get(xi, yi, zi):
				continue
			dz = coord_slices[2][zi+1]-coord_slices[2][zi]
			c += dx*dy*dz

print(f"{c} active cells")
