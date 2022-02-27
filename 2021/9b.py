import sys
import heapq

def line_parts(line):
	parts = []
	in_part = False
	a, b = 0, 0
	for i, c in enumerate(line):
		if in_part:
			b = i
			if c == "9":
				in_part = False
				parts.append((a, b))
		else:
			a = i
			if c != "9":
				in_part = True
	if in_part:
		parts.append((a, len(line)))
	return parts

with open(sys.argv[1], "r") as f:
	sizes = {}
	roots = {}
	nx = 0
	rs = None
	for line in f.readlines():
		line = line.strip()
		if not line:
			break
		parts = line_parts(line)
		#print(parts)
		if rs is None:
			rs = []
			for a, b in parts:
				rs.append((a, b, nx))
				sizes[nx] = b - a
				roots[nx] = nx
				nx += 1
			continue
		rs1 = []
		rs.append((len(line), len(line), -1))
		i = 0
		ra, rb, rx = rs[i]
		for a, b in parts:
			while rb <= a:
				i += 1
				ra, rb, rx = rs[i]
			x = -1
			while ra < b:
				if x == -1:
					x = roots[rx]
					sizes[x] += b - a
				else:
					if roots[rx] != x:
						sizes[x] += sizes[roots[rx]]
						roots[rx] = x
				if rb <= b:
					i += 1
					ra, rb, rx = rs[i]
				else:
					break
			if x == -1:
				x = nx
				sizes[nx] = b - a
				roots[nx] = nx
				nx += 1
			rs1.append((a, b, x))
		rs = rs1
basins = [sizes[x] for (x, r) in roots.items() if x == r]
a, b, c = heapq.nlargest(3, basins)
#print(basins)
print(a*b*c)
