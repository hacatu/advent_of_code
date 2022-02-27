import sys
from sympy import Matrix as M
from collections import Counter

with open(sys.argv[1], "r") as f:
	rules = []
	for line in f.readlines():
		if not (line := line.strip()):
			continue
		toks = line.split(" -> ")
		if len(toks) == 2:
			rules.append(tuple(toks))
		else:
			text = line

char_idx = set()
for c in text:
	char_idx.add(c)
for (a, b), c in rules:
	char_idx.add(a)
	char_idx.add(b)
	char_idx.add(c)
char_idx = {c: i for (i, c) in enumerate(char_idx)}
idx_rules = {(char_idx[a], char_idx[b]): char_idx[c] for (a, b), c in rules}

n_pairs = len(char_idx)**2
T = [[0]*n_pairs for _ in range(n_pairs)]
for i in range(len(char_idx)):
	for j in range(len(char_idx)):
		k = idx_rules.get((i, j), -1)
		col = i*len(char_idx) + j
		if k == -1:
			T[col][col] = 1
		else:
			row = i*len(char_idx) + k
			T[row][col] = 1
			row = k*len(char_idx) + j
			T[row][col] = 1
T = M(T)

V = [0]*n_pairs
for a, b in zip(text, text[1:]):
	V[char_idx[a]*len(char_idx) + char_idx[b]] += 1
V = M(n_pairs, 1, V)

V = T**40 @ V
idx_counts = [0]*len(char_idx)
for row, c in enumerate(V):
	idx_counts[row//len(char_idx)] += c
	idx_counts[row%len(char_idx)] += c
idx_counts[char_idx[text[0]]] += 1
idx_counts[char_idx[text[-1]]] += 1

print((max(idx_counts)-min(idx_counts))//2)
