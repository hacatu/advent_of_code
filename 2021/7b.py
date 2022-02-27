import sys
import statistics as stat

with open(sys.argv[1], "r") as f:
	ns = [int(tok) for tok in next(iter(f.readlines())).strip().split(",")]

mean = round(stat.mean(ns))
median = round(stat.median(ns))
print(f"mean={mean}\nmedian={median}")

def dist(m):
	return sum((n := abs(x-m))*(n+1)//2 for x in ns)

a = min(mean, median)
b = max(mean, median)
m = min(range(a,b+1), key=dist)
print(f"m={m}\ndist={dist(m)}")
