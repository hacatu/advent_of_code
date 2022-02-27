import sys
from dataclasses import dataclass
from numbers import Real

@dataclass
class PNode:
	dist: Real
	key: object
	child: "PNode" = None
	sibling: "PNode" = None
	parent: "PNode" = None

class PQ:
	def __init__(self):
		self.nodes = {}
		self.root = None

	def add_dist(self, key, dist):
		node = self.nodes.get(key, None)
		if node is not None:
			if node.dist <= dist:
				return
			node.dist = dist
			if node.parent is None:
				return
			if node.parent.child is node:
				node.parent.child = node.sibling
			else:
				it = node.parent.child
				while it.sibling is not node:
					it = it.sibling
				it.sibling = node.sibling
			node.parent = None
			node.sibling = None
			self.root = self._meld(self.root, node)
		else:
			node = PNode(dist, key)
			self.nodes[key] = node
			self.root = self._meld(self.root, node)

	@staticmethod
	def _meld(a, b):
		if a is None:
			return b
		if b is None:
			return a
		if a.dist <= b.dist:
			b.sibling = a.child
			a.child = b
			b.parent = a
			return a
		a.sibling = b.child
		b.child = a
		a.parent = b
		return b

	def pop_nearest(self):
		if self.root is None:
			raise IndexError("PQ is empty!")
		res = self.root
		self.root = self._merge_pairs(self.root.child)
		if self.root is not None:
			self.root.parent = None
		res.child = None
		res.sibling = None
		return res

	@staticmethod
	def _merge_pairs(ll):
		if ll is None or ll.sibling is None:
			return ll
		next = ll.sibling.sibling
		return PQ._meld(PQ._meld(ll, ll.sibling), PQ._merge_pairs(next))

with open(sys.argv[1], "r") as f:
	grid = []
	for line in f.readlines():
		if not (line := line.strip()):
			break
		grid.append([int(c) for c in line])
	if any(len(row) != len(grid[0]) for row in grid[1:]):
		raise IndexError("row length mismatch!")

new_grid = [[0]*(5*len(grid[0])) for _ in range(5*len(grid))]
for i, row in enumerate(grid):
	for j, dist in enumerate(row):
		new_grid[i][j] = dist
		for k in range(1, 9):
			kdist = (dist-1+k)%9+1
			for ii in range(max(0, k-4), min(5,k+1)):
				jj = k-ii
				new_grid[ii*len(grid)+i][jj*len(grid[0])+j] = kdist
grid = new_grid

#for row in grid:
#	print("".join(map(str, row)))

frontier = PQ()
frontier.add_dist((0,0), 0)

while frontier.root is not None:
	node = frontier.pop_nearest()
	i, j = node.key
	if i == len(grid) - 1 and j == len(grid[0]) - 1:
		print(node.dist)
		break
	if i:
		frontier.add_dist((i-1,j), node.dist + grid[i-1][j])
	if j:
		frontier.add_dist((i,j-1), node.dist + grid[i][j-1])
	if i < len(grid) - 1:
		frontier.add_dist((i+1,j), node.dist + grid[i+1][j])
	if j < len(grid[0]) -1:
		frontier.add_dist((i,j+1), node.dist + grid[i][j+1])
