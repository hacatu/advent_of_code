import sys
from functools import cache

roll_weights = {
	3: 1,
	4: 3,
	5: 6,
	6: 7,
	7: 6,
	8: 3,
	9: 1
}

@cache
def wins(x1, s1, x2, s2, which):
	if which == 1:
		if s2 >= 21:
			return 0, 1
		w1, w2 = 0, 0
		for roll, weight in roll_weights.items():
			nx1 = (x1 + roll - 1)%10 + 1
			ns1 = s1 + nx1
			d1, d2 = wins(nx1, ns1, x2, s2, 3 - which)
			w1 += weight*d1
			w2 += weight*d2
		return w1, w2
	else:
		if s1 >= 21:
			return 1, 0
		w1, w2 = 0, 0
		for roll, weight in roll_weights.items():
			nx2 = (x2 + roll - 1)%10 + 1
			ns2 = s2 + nx2
			d1, d2 = wins(x1, s1, nx2, ns2, 3 - which)
			w1 += weight*d1
			w2 += weight*d2
		return w1, w2

with open(sys.argv[1], "r") as f:
	x1, x2 = [int(line.split(": ")[1].strip()) for line in f.readlines() if line.strip()]

print(max(wins(x1, 0, x2, 0, 1)))
