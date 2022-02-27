import sys

closing_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
error_scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

with open(sys.argv[1], "r") as f:
	score = 0
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
				score += error_scores[c]
				break
print(score)
