import sys
from functools import cache
from collections import defaultdict
with open(sys.argv[1], "r") as f:
	ids = {}
	is_big = []
	adj = defaultdict(set)
	for line in f.readlines():
		if not (line := line.strip()):
			break
		a, b = line.split("-")
		if a not in ids:
			ids[a] = len(ids)
			is_big.append(ord(a[0])<=ord("Z"))
		if b not in ids:
			ids[b] = len(ids)
			is_big.append(ord(b[0])<=ord("Z"))
		adj[ids[a]].add(ids[b])
		adj[ids[b]].add(ids[a])
	mask = (1 << len(ids)) - 1
	mask ^= 1 << ids["start"]

@cache
def Q(i, j, mask):
	if i == j:
		return 1
	return sum(
		Q(n, j, mask if is_big[n] else
		(mask ^ (1 << n)))
		for n in adj[i] if mask & (1 << n))

print(Q(ids["start"], ids["end"], mask))
