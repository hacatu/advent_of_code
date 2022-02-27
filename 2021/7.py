import sys
from statistics import median

with open(sys.argv[1], "r") as f:
	ns = [int(tok) for tok in next(iter(f.readlines())).strip().split(",")]
m = round(median(ns))
print(f"m={m}")
print(sum(abs(x-m) for x in ns))
