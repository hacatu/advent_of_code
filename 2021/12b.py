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
	s = ids["start"]
	t = ids["end"]
	mask = (1 << len(ids)) - 1
	mask ^= 1 << s

@cache
def Q(i, j, mask, can_revisit):
	if i == j:
		return 1
	res = 0
	for n in adj[i]:
		if is_big[n]:
			res += Q(n, j, mask, can_revisit)
		elif mask & (1 << n):
			res += Q(n, j, mask ^ (1 << n), can_revisit)
		elif can_revisit and n != s:
			res += Q(n, j, mask, False)
	return res

print(Q(s, t, mask, True))
