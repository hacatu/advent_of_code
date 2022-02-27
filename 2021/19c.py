import sys
import itertools as itt
from collections import defaultdict

class Scanner:
	def __init__(self):
		self.pos = (0, 0, 0)
		self.rotation = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
		self.points = []
		self.is_transformed = False

	def add_point(self, point):
		self.points.append(point)
	
	def compute_dists(self):
		self.dist_pairs = defaultdict(list)
		for i, j in itt.combinations(range(len(self.points)), 2):
			dist_profile = tuple(sorted([abs(self.points[i][k] - self.points[j][k]) for k in range(3)]))
			self.dist_pairs[dist_profile].append((i, j))

rotations = []
for i in range(3):
	ei = [int(l == i) for l in range(3)]
	for j in range(3):
		if j == i:
			continue
		ej = [int(l == j) for l in range(3)]
		ek = [0]*3
		ek[3 - i - j] = 1 if (i + 1)%3 == j else -1
		rotations.append(tuple((ei[l], ej[l], ek[l]) for l in range(3)))
		rotations.append(tuple((-ei[l], -ej[l], ek[l]) for l in range(3)))
		rotations.append(tuple((-ei[l], ej[l], -ek[l]) for l in range(3)))
		rotations.append(tuple((ei[l], -ej[l], -ek[l]) for l in range(3)))

def rotate(point, rot):
	return tuple(sum(a*b for (a, b) in zip(row, point)) for row in rot)

def have_same_octant(ai, bi, aj, bj):
	return all((bi[k] - ai[k])*(bj[k] - aj[k]) >= 0 for k in range(3))

with open(sys.argv[1]) as f:
	print("Reading scanners...")
	scanners = []
	for line in f.readlines():
		line = line.strip()
		if not line:
			continue
		if line.startswith("---"):
			scanners.append(Scanner())
			continue
		scanners[-1].add_point(tuple(int(tok) for tok in line.split(",")))

print(f"Found {len(scanners)} scanners")
dist_scanners = defaultdict(list)

# For each scanner, bin pairs of points according to distance profile
# (not just the (L2) distance, but the L1 and L3 distances as well)
# (in fact the distance profile is just stored as a sorted list of coordinatewise distances)
for i, scanner in enumerate(scanners):
	scanner.compute_dists()
	for dist_profile in scanner.dist_pairs:
		dist_scanners[dist_profile].append(i)

print(f"There are {len(dist_scanners)} distance profiles")

potential_neighbors = defaultdict(lambda:defaultdict(list))
num_potential_overlaps = 0

for dist_profile, ids in dist_scanners.items():
	if len(ids) == 2:
		potential_neighbors[ids[0]][ids[1]].append(dist_profile)
		potential_neighbors[ids[1]][ids[0]].append(dist_profile)
		num_potential_overlaps += 1

print(f"Found {num_potential_overlaps} potential overlaps")

num_untransformed = len(scanners) - 1
scanners[0].is_transformed = True
frontier = {0}

while frontier and num_untransformed:
	i = frontier.pop()
	pos_i = scanners[i].pos
	print(f"Checking potential neighbors for scanner {i}")
	for j, dist_profiles in potential_neighbors[i].items():
		del potential_neighbors[j][i]
		if scanners[j].is_transformed:
			continue
		print(f"  -> to scanner {j}")
		# scanners[i] has points in global coordinates, so try all rotations of scanners[j]
		for dist_profile in dist_profiles:
			print(f"    -> with distance profile {dist_profile}")
			print(f"       {len(scanners[i].dist_pairs[dist_profile])}*{len(scanners[j].dist_pairs[dist_profile])} candidate point pairs")
			for ai, bi in scanners[i].dist_pairs[dist_profile]:
				ai = scanners[i].points[ai]
				bi = scanners[i].points[bi]
				for rot in rotations:
					for aj, bj in scanners[j].dist_pairs[dist_profile]:
						aj = rotate(scanners[j].points[aj], rot)
						bj = rotate(scanners[j].points[bj], rot)
						# first we confirm that this rotation makes the coordinatewise distances line up
						if any(abs(bj[k] - aj[k]) != abs(bi[k] - ai[k]) for k in range(3)):
							#print("        skipping obviously invalid rotation")
							continue
						# next we need to confirm the pair of points seen by j is actually a rotation of those seen by i
						# note that this is complicated by the existence of 0 coordinates
						if not have_same_octant(ai, bi, aj, bj):
							aj, bj = bj, aj
							if not have_same_octant(ai, bi, aj, bj):
								#print("        skipping invalid parity rotation")
								continue
						displacement = tuple(ai[k] - aj[k] for k in range(3))
						pos_j = displacement
						print(f"        candidate center is {pos_j}")
						points1 = [rotate(point, rot) for point in scanners[j].points]
						points1 = [tuple(point[k] + displacement[k] for k in range(3)) for point in points1]
						# now we need to check that the set of points in the overlap is consistent
						bl = tuple(max(pos_i[k], pos_j[k]) - 1000 for k in range(3))
						tr = tuple(min(pos_i[k], pos_j[k]) + 1000 for k in range(3))
						overlap_a = {point for point in scanners[i].points if all(bl[i] <= point[i] <= tr[i] for i in range(3))}
						overlap_b = {point for point in points1 if all(bl[i] <= point[i] <= tr[i] for i in range(3))}
						if overlap_a != overlap_b:
							continue
						# the rules state there must be at least 12 points overlapping
						if len(overlap_a) < 12:
							continue
						# finally we have an overlap !
						print(f"        overlap successful")
						scanners[j].points = points1
						scanners[j].pos = pos_j
						scanners[j].is_transformed = True
						frontier.add(j)
						num_untransformed -= 1
			break
	del potential_neighbors[i]

print(f"There are {num_untransformed} remaining untransformed scanners")
points = set()
for scanner in scanners:
	if not scanner.is_transformed:
		raise ValueError("Not all scanners ranges could be combined!")
	for point in scanner.points:
		points.add(point)

print(f"There are {len(points)} unique beacons")

max_scanner_sep = max(
	sum(abs(x - y) for (x, y) in zip(scanner1.pos, scanner2.pos))
	for (scanner1, scanner2) in itt.combinations(scanners, 2))

print(f"The max separation of any beacons is {max_scanner_sep}")

