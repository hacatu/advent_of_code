import sys
from collections import Counter

with open(sys.argv[1], "r") as f:
	counts = Counter()
	num_lines = 0
	for line in f.readlines():
		for i, b in enumerate(line.strip()[::-1]):
			if b == '1':
				counts[i] += 1
		if line.strip():
			num_lines += 1

gamma = 0
epsilon = 0
for i, c in counts.items():
	if 2*c > num_lines:
		gamma += 1 << i
	else:
		epsilon += 1 << i
print(gamma*epsilon)

