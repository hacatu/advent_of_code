import sys
import sympy

A = [[0]*9 for _ in range(9)]
for i in range(8):
	A[i][i+1] = 1
A[6][0] = 1
A[8][0] = 1
A = sympy.Matrix(A)

N = sympy.Matrix([[1]*9])@A**80

with open(sys.argv[1], "r") as f:
	X = [0]*9
	for tok in next(iter(f.readlines())).strip().split(","):
		X[int(tok)] += 1

X = sympy.Matrix([[x] for x in X])
print(N@X)
