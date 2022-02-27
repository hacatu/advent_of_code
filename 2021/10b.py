import sys
from statistics import median

closing_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
missing_scores = {")": 1, "]": 2, "}": 3, ">": 4}

with open(sys.argv[1], "r") as f:
	scores = []
	for line in f.readlines():
		line = line.strip()
		if not line:
			break
		ctx_stack = []
		for c in line:
			end = closing_pairs.get(c, None)
			if end is not None:
				ctx_stack.append(end)
			elif c == ctx_stack[-1]:
				ctx_stack.pop()
			else:
				#print("skipping corrupted line")
				break
		else:
			score = 0
			#print("".join(ctx_stack[::-1]))
			for c in ctx_stack[::-1]:
				score = score*5 + missing_scores[c]
			#print(score)
			scores.append(score)
print(median(scores))
