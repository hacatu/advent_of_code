import sys
import bisect

"""
This is very simple.  Each player's score is mostly
independent.  Let x1, x2 be the positions of player
1 and player 2 and s1, s2 their scores.  Initially,
x1 = 4, x2 = 8, and s1 = s2 = 0.  Player 1 moves
1+2+3 spaces to x1 = 10 thus increasing s1 by 10.
Then player 2 moves 4+5+6 spaces to 3 scoring 3 points.
Now we notice that even though the die is 100 sided,
it might as well be 10 sided because board positions
effectively exist mod 10.  Therefore we see that on
player 1's nth turn, they move 3*6*(n-1) + 1 + 2 + 3
= 8*n - 2 spaces (mod 10).  And so after k turns they
will have moved 4*k*(k+1) - 2*k = 2*k*(2*k+1) spaces
overall.  Therefore, when k or 2k-1 is a multiple of 5,
p1 should be on the original space.  This is equivalent
to saying k or 2k+1 is 0 mod 5, or k is 0 or 2 mod 5
4 + 1+2+3 = 10
10 + 7+8+9 = 4
4 + 3+4+5 = 6
6 + 9+0+1 = 6
6 + 5+6+7 = 4
We can now easily find a closed form for p1's score
after k turns:
s1(k) = 30*floor(k/5) + {0 if k = 0 mod 5
                         10 if k = 1 mod 5
			 14 if k = 2 mod 5
			 20 if k = 3 mod 5
			 26 if k = 4 mod 5
We can do a similar analysis for p2:
8 + 4+5+6 = 3
3 + 0+1+2 = 6
6 + 6+7+8 = 7
7 + 2+3+4 = 3
3 + 8+9+0 = 10
s2(k) = 29*floor(k/5) + {...
"""

with open(sys.argv[1], "r") as f:
	x0s = []
	for line in f.readlines():
		line = line.strip()
		toks = line.split(": ")
		if len(toks) != 2:
			continue
		x0s.append(int(toks[1]))
	x1, x2 = x0s
	del x0s

o1s = [3*(6*k - 4)%10 for k in range(1, 11)]
o2s = [3*(6*k - 1)%10 for k in range(1, 11)]

s1 = 0
s2 = 0

s1s = []
s2s = []

for o in o1s:
	x1 = (x1 + o - 1)%10 + 1
	s1 += x1
	s1s.append(s1)

for o in o2s:
	x2 = (x2 + o - 1)%10 + 1
	s2 += x2
	s2s.append(s2)

def turns_till(s_tab, score):
	k = score//s_tab[-1]
	r = score - k*s_tab[-1]
	k *= len(s_tab)
	k += bisect.bisect_left(s_tab, r) + 1
	return k

def score_after(s_tab, k):
	res = s_tab[-1]*(k//len(s_tab))
	if k%len(s_tab):
		res += s_tab[k%len(s_tab)-1]
	return res

print(f"Player 1 score table: {s1s}")
print(f"Player 2 score table: {s2s}")

k1 = turns_till(s1s, 1000)
k2 = turns_till(s2s, 1000)

print(f"Player 1 reaches 1000 in {k1} turns")
print(f"Player 2 reaches 1000 in {k2} turns")

if k1 <= k2:
	rolls = 6*k1 - 3
	losing_score = score_after(s2s, k1-1)
else:
	rolls = 6*k2
	losing_score = score_after(s1s, k2)

print(f"{rolls}*{losing_score}={rolls*losing_score}")
