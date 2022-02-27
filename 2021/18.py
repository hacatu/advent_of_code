import sys
from ast import literal_eval
from functools import reduce

def bit_count(x):
	res = 0
	while x:
		if x&1:
			res += 1
		x >>= 1
	return res

def reduce_snum(data):
	working = True
	while working:
		working = False
		while explode(data):
			working = True
		if split(data):
			working = True

def explode(data, root = None, path = 1):
	if root is None:
		root = data
	if isinstance(data, int):
		return False
#	print(f"Exploding {path} > {data}")
	if path >= 16:
		if isinstance(data[0], list) or isinstance(data[1], list):
			raise ValueError("Attempt to explode nested pair")
		pred = root
		prefix = path
		while bit_count(prefix) > 2:
			pred = pred[prefix&1]
			prefix >>= 1
		if bit_count(prefix) == 2:
			while not (prefix&1):
				pred = pred[0]
				prefix >>= 1
			if isinstance(pred[0], int):
				pred[0] += data[0]
			else:
				pred = pred[0]
				while isinstance(pred[1], list):
					pred = pred[1]
				pred[1] += data[0]
		pred = root
		prefix = path
		if bit_count(prefix + 1) != 1:
			while bit_count(prefix + 2) != 1:
				pred = pred[prefix&1]
				prefix >>= 1
			if bit_count(prefix + 2) == 1:
#				print(prefix)
				if isinstance(pred[1], int):
					pred[1] += data[1]
				else:
					pred = pred[1]
					while isinstance(pred[0], list):
						pred = pred[0]
					pred[0] += data[1]
		pred = root
		prefix = path
		while prefix >= 4:
			pred = pred[prefix&1]
			prefix >>= 1
		pred[prefix&1] = 0
		return True
	hi_bit = 1 << (path.bit_length() - 1)
	if explode(data[0], root, path + hi_bit):
		return True
	return explode(data[1], root, path + 2*hi_bit)

def split(data):
	if isinstance(data[0], int):
		if data[0] > 9:
			data[0] = [data[0]//2, (data[0]+1)//2]
			return True
	elif split(data[0]):
		return True
	if isinstance(data[1], int):
		if data[1] > 9:
			data[1] = [data[1]//2, (data[1]+1)//2]
			return True
		return False
	return split(data[1])

def magnitude(data):
	return data if isinstance(data, int) else (3*magnitude(data[0]) + 2*magnitude(data[1]))

def add_snums(a, b):
	res = [a, b]
	reduce_snum(res)
	return res

with open(sys.argv[1], "r") as f:
	snums = (literal_eval(line) for line in f.readlines() if line.strip())
	s = reduce(add_snums, snums)
	print(s)
	print(magnitude(s))

