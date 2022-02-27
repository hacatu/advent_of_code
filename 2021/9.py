import sys

def row_risk(r1, r2, r3):
	res = 0
	for i, a in enumerate(r2):
		if i > 0:
			if r2[i-1] <= a:
				continue
		if i < len(r2) - 1:
			if r2[i+1] <= a:
				continue
		if r1 is not None:
			if r1[i] <= a:
				continue
		if r3 is not None:
			if r3[i] <= a:
				continue
		res += a + 1
	return res

with open(sys.argv[1], "r") as f:
	res = 0
	row1 = None
	row2 = None
	for line in f.readlines():
		line = line.strip()
		if not line:
			break
		row3 = [int(c) for c in line]
		if row2 is None:
			row1, row2, row3 = row2, row3, None
			continue
		elif len(row3) != len(row2):
			raise ValueError("Array is not rectangular")
		res += row_risk(row1, row2, row3)
		row1, row2, row3 = row2, row3, None
	res += row_risk(row1, row2, row3)
print(res)

