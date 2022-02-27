import sys
from math import ceil, floor, sqrt

"""
We want to find the largest integer vy so that a
solution vx, vy exists which sends the probe through
a target area: x=ax..bx, y=ay..by at an integer time.
The probe starts at 0, 0 and moves vx, vy units.
Then vx is brought 1 closer to 0 and vy is decreased
by 1.  Clearly vx, vy for any point in the target
region, albeit probably a bad one.  So we know there
is at least one solution.

If ax is 0, the problem is ill founded since 0, vy
is always a solution.  So we assume ax is not 0.
Regardless of vy, the total x distance travelled is
at most |vx|*(|vx|+1)/2.
|vx|**2/2 + |vx|/2 >= min(|ax|, |bx|)
(|vx|**2 + |vx| + 1/4) >= 1/4 + 2*min(|ax|, |bx|)
|vx| + 1/2 >= sqrt(1/4 + 2*min(|ax|, |bx|))
max(|ax|, |bx|) >= |vx| >= sqrt(1/4 + 2*min(|ax|, |bx|)) - 1/2

If we minimize vx, we should be able to maximize vy.
Note that in fact if ax..bx contains any triangular
number, there are infinitely many solutions so we can
assume this is not the case.

But in fact, this may not be true because the line is
explicitly not continuous.

We can notice that y(t) really is a parabola even
though y(x) isn't.  In particular, the y values going
up (if vy is positive) repeat going down.

If ay is > 0, we get a lower bound on y and
an upper bound just as for x.

We always have max(|ay|, |by|) as an upper bound for
y.
"""

with open(sys.argv[1], "r") as f:
	for line in f.readlines():
		line = line.strip()
		_, line = line.split(": ")
		xpart, ypart = line.split(", ")
		ax, bx = map(int, xpart[2:].split(".."))
		ay, by = map(int, ypart[2:].split(".."))

max_y = 0
for vy in range(-ay-1, 0, -1):
#	y(t) = -t**2/2 + (vy - 1/2)*t
#	t in [T-A, T-B] U [T+B, T+A], where
#		T = (vy-1/2),
#		A = sqrt(-2ay + T**2),
#		B = sqrt(-2by + T**2)
#	The first interval is much less important:
#	for positive vy the intersection cannot occur
#	there.
	Ty = vy - .5
	Ay = sqrt(-2*ay + Ty**2)
	By = sqrt(-2*ay + Ty**2)
	t_min = ceil(Ty + By)
	t_max = floor(Ty + Ay)
	vx_min = ceil((ax + t_max**2/2)/t_max + .5)
	vx_max = ceil((bx + t_min**2/2)/t_min + .5)
	if vx_min <= vx_max:
		max_y = vy*(vy+1)/2
		break

print(max_y)
