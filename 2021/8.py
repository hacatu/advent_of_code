import sys
from collections import Counter

"""
a:0 23 56789:8
b:0   456 89:6
c:01234  789:8
d:  23456 89:7
e:0 2   6 8 :4
f:01 3456789:9
g:0 23 56 89:7
Hence if a segment occurs 4, 6, or 9
times in the set of unique displayed
segment sets, we know exactly which
it is.  Otherwise, we need to actually
consider what digits it occurs in
0:abc efg:6
1:  c  f :2
2:a cde g:5
3:a cd fg:5
4: bcd f :4
5:ab d fg:5
6:ab defg:6
7:a c  f :3
8:abcdefg:7
9:abcd fg:6
Thus we see only 1, 4, 7, and 8
contain unique numbers of segments.
Conveniently, 4 discriminates d from g
and c from a
"""

def calc_decoder(crypt10):
	counts = Counter(iter(crypt10))
	for tok in crypt10.split():
		if len(tok) == 4:
			crypt4 = tok
			break
	res = {}
	for c in "abcdefg":
		n = counts[c]
		if n == 4:
			res[c] = "e"
		elif n == 6:
			res[c] = "b"
		elif n == 9:
			res[c] = "f"
		elif n == 7:
			res[c] = "d" if c in crypt4 else "g"
		elif n == 8:
			res[c] = "c" if c in crypt4 else "a"
	return res

def decode_digit(decoder, cryptd):
	mask = 0
	for c in cryptd:
		mask |= 1 << (ord(decoder[c])-ord("a"))
	return {
		0b1110111: 0,
		0b0100100: 1,
		0b1011101: 2,
		0b1101101: 3,
		0b0101110: 4,
		0b1101011: 5,
		0b1111011: 6,
		0b0100101: 7,
		0b1111111: 8,
		0b1101111: 9
	}[mask]

with open(sys.argv[1], "r") as f:
	counts = [0]*10
	for line in f.readlines():
		line = line.strip()
		if not line:
			break
		crypt10, cryptd = line.split("|")
		crypt10 = crypt10.strip()
		cryptd = cryptd.strip()
		decoder = calc_decoder(crypt10)
		for tok in cryptd.split():
			digit = decode_digit(decoder, tok)
			counts[digit] += 1

print(sum(counts[i] for i in [1, 4, 7, 8]))
