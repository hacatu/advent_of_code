import sys
from math import ceil, floor, sqrt

with open(sys.argv[1], "r") as f:
	for line in f.readlines():
		line = line.strip()
		_, line = line.split(": ")
		xpart, ypart = line.split(", ")
		ax, bx = map(int, xpart[2:].split(".."))
		ay, by = map(int, ypart[2:].split(".."))

slns = {(x, ay) for x in range(ax, bx+1)}
for vy in range(-ay-1, ay, -1):
#	y(t) = -t**2/2 + (vy - 1/2)*t
#	t in [T-A, T-B] U [T+B, T+A], where
#		T = (vy-1/2),
#		A = sqrt(-2ay + T**2),
#		B = sqrt(-2by + T**2)
#	The first interval is much less important:
#	for positive vy the intersection cannot occur
#	there.
	print(vy)
	Ty = vy - .5
	Ay = sqrt(-2*ay + Ty**2)
	By = sqrt(-2*by + Ty**2)
	t_min = ceil(Ty + By)
	t_max = floor(Ty + Ay)
	vx_min = ceil((ax + t_max**2/2)/t_max + .5)
	vx_max = floor((bx + t_min**2/2)/t_min + .5)
	if vx_min <= vx_max:
		slns |= {(vx, vy) for vx in range(vx_min, vx_max+1)}

correct = """
23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7
"""
correct = {tuple(map(int, tok.split(","))) for tok in correct.split()}
print("Missing slns:", correct - slns)
print("Invalid slns:", slns - correct)
