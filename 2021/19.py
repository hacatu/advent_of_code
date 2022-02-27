import sys
from collections import Counter, defaultdict
import itertools as itt
import numpy as np

with open(sys.argv[1], "r") as f:
	scanner_points = []
	for line in f.readlines():
		line = line.strip()
		if line.startswith("--- scanner "):
			scanner_points.append([])
			continue
		elif not line:
			continue
		scanner_points[-1].append(tuple(map(int, line.split(","))))

scanner_points = [np.array(points, dtype=np.int32) for points in scanner_points]

gap_counters = [Counter() for _ in scanner_points]
gap_pairs = [defaultdict(list) for _ in scanner_points]
overlap_sets = defaultdict(set)

for i, points in enumerate(scanner_points):
	gap_counter = gap_counters[i]
	gaps = gap_pairs[i]
	for a, b in itt.combinations(points, 2):
		#gap is the l1, l2, l3 distance between the points
		gap = tuple(sum(abs(x1-x2)**l for (x1, x2) in zip(a, b)) for l in (1,2,3))
		gap_counter[gap] += 1
		gaps[gap].append((a, b))
	for gap in gap_counter:
		overlap_sets[gap].add(i)

overlap_edges = defaultdict(set)
cc_parents = list(range(len(scanner_points)))
cc_count = len(scanner_points)

def root(i):
	while (j := cc_parents[i]) != i:
		i = j
	return i

def update_root(i, j_root):
	while (j := cc_parents[i]) != i:
		cc_parents[i] = j_root
		i = j
	cc_parents[i] = j_root

for gap, subset in overlap_sets.items():
	if len(subset) != 2:
		continue
	i = min(subset)
	j = max(subset)
	overlap_edges[(i, j)].add(gap)
	i_root = root(i)
	j_root = root(j)
	if i_root == j_root:
		continue
	cc_count -= 1
	if i_root < j_root:
		update_root(j, i_root)
	else:
		update_root(i, j_root)
	if cc_count == 0:
		raise ValueError("Connected component analysis failed!")

overlap_adjs = [set() for _ in scanner_points]

for i, j in overlap_edges:
	overlap_adjs[i].add(j)
	overlap_adjs[j].add(i)

class Transform:
	def __init__(self, pos, perm, ort):
		self.pos = pos
		S = np.diag([ort[0], ort[1], lcs(perm)*ort[0]*ort[1]])
		P = [[0]*3 for _ in perm]
		for i, j in enumerate(perm):
			P[i][j] = 1
		P = np.array(P)
		self.from_local = S@P
		self.to_local = P.T@S
	def pt_from_local(self, pt):
		return self.pos + self.from_local@pt

	def pt_to_local(self, pt):
		return self.to_local@(pt - self.pos)

scanner_transforms = [None for _ in scanner_points]
scanner_transforms[0] = Transform((0, 0, 0), (0, 1, 2))

unknown = set(range(1, len(scanner_points)))
frontier = {0}

while unknown:
	i = frontier.pop()
	for j in overlap_adjs:
		if j not in unknown:
			continue
		find_transform(i, j)
		unknown.remove(j)
		frontier.add(j)
		if not unknown:
			break

def find_transform(i, j):
	gaps_i = gap_pairs[i]
	gaps_j = gap_pairs[j]
	def key_fn(g):
		return (
		len(gaps_i[g])*len(gaps_j[g]),
		len(set(abs(x1-x2) for (x1, x2) in
			zip(*gaps_i[g])))))
	gap = min(overlap_edges[(min(i, j), max(i, j))],
		key=key_fn
	uniq_axes = key_fn(gap)[1]
	for seg_i, seg_j in itt.product(gaps_i[gap], gaps_j[gaps]):
		if uniq_axes == 3:
			if try_find4(i, j, seg_i, seg_j):
				break
	else:
		print("Could not find matching transform!  This could be because only common gaps with unique axes are supported, or because unluckily none of the 12 shared points have a unique distance")
		return False
	return True

def try_find4(i, j, seg_i, seg_j):
	ai, bi = seg_i
	aj, bj = seg_j
	ag = i_transform.from_local(ai)
	bg = i_transform.from_local(bi)
	dg = [abs(a-b) for (a, b) in zip(ag, bg)]
	dj = [abs(a-b) for (a, b) in zip(aj, bj)]
	i_transform = scanner_transforms[i]
	perm = [dg.index(d) for d in dj]
	pos = [None]*3
	for ort in itt.product((-1,1),(-1,1)):
		
