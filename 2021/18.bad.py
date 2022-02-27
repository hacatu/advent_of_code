import sys
from ast import literal_eval

def reduce_snum(data):
	parents = []
	return reduce_r(data, parents)

def reduce_r(data, parents):
	if isinstance(data, list):
		if len(parents) == 4:
			explode_r(data, parents)
		parents.append(data)
		reduce_r(data[0], parents)
		reduce_r(data[1], parents)
		parents.pop()
	elif data > 9:
		split_r(data, parents)

def explode_r(data, parents):
	it = data
	for i in range(len(parents)-1, -1, -1):
		parent = parents[i]
		if it is parent[1]:
			if isinstance(parent[0], int):
				parent[0] += data[0]
				if parent[0] > 9:
					split_r(parent[0], parents[:i])
			else:
				it = parent[0]
				i += 1
				while isinstance(it[1], list):
					it = it[1]
					i += 1
				it[1] += data[0]
				if it[1] > 9:
					split_r(it[1], parents[:i])
		it = parent
	it = data
	for i in range(len(parents)-1, -1, -1):
		parent = parents[i]
		if it is parent[0]:
			if isinstance(parent[1], int):
				parent[1] += data[0]
		it = parent
	if parents[-1][0] is data:
		parents[-1][0] = 0
	else:
		parents[-1][1] = 0

def split_r(data, parents):
	if data is parents[-1][0]:
		parents[-1][0] = [data//2, (data+1)//2]
