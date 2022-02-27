import sys
from ast import literal_eval
from functools import reduce, total_ordering
from dataclasses import dataclass
import heapq

@total_ordering
@dataclass
class BTZipper:
	path: int
	depth: int

	def __le__(self, other):
		if self.depth < other.depth:
			return (self.path << (other.depth - self.depth)) <= other.path
		elif self.depth > other.depth:
			return self.path <= (other.path << (self.depth - other.depth))
		return self.path <= other.path

class Snum:
	def __init__(self, data, parent = None):
		self.parent = parent
		if isinstance(data, int):
			self.left = None
			self.right = None
			self.mag = data
		elif not isinstance(data, list) or len(data) != 2:
			raise ValueError("data is not formatted correctly!")
		else:
			self.left = Snum(data[0], self)
			self.right = Snum(data[1], self)
			self.mag = None

	def __str__(self):
		if self.left is None:
			return str(self.mag)
		return f"[{str(self.left)}, {str(self.right)}]"

	def get_zipper(self):
		path = 1
		depth = 0
		while self.parent is not None:
			depth += 1
			if self is self.parent.right:
				path |= 1 << depth
			self = self.parent
		return BTZipper(path, depth)

	def _collect_reductions(self, prefix = None, out = None):
		is_root = out is None
		if out is None:
			prefix = BTZipper(0, 0)
			out = []
		path = BTZipper((prefix.path << 1) | 1, prefix.depth)
		if self.left is not None:
			if prefix.depth == 4:
				out.append((False, path, self))
			else:
				path = BTZipper(prefix.path << 1, prefix.depth + 1)
				self.left._collect_reductions(path, out)
				path = BTZipper((prefix.path << 1) | 1, prefix.depth + 1)
				self.right._collect_reductions(path, out)
		if is_root:
			heapq.heapify(out)
			return out

	def reduce(self):
		reductions = self._collect_reductions()
		while reductions:
			is_split, zipper, pair = heapq.heappop(reductions)
			if is_split:
				pair.split()
				if zipper.depth == 4:
					heapq.heappush(reductions, (False, zipper, pair))
			else:
				for s in pair.explode():
					if s is not None:
						heapq.heappush(reductions, (True, s.get_zipper(), s))

	def explode(self):
		if self.left is None:
			raise TypeError("Cannot explode a regular number!")
		if self.left.left is not None or self.right.left is not None:
			raise TypeError("Cannot explode nested list!")
		it = self
		left = None
		while it.parent is not None:
			if it is it.parent.right:
				it = it.parent.left
				break
			it = it.parent
		if it.parent is not None:
			while it.right:
				it = it.right
			if it.mag <= 9 and it.mag + self.left.mag > 9:
				left = it
			it.mag += self.left.mag
		it = self
		right = None
		while it.parent is not None:
			if it is it.parent.left:
				it = it.parent.right
				break
			it = it.parent
		if it.parent is not None:
			while it.left:
				it = it.left
			if it.mag <= 9 and it.mag + self.right.mag > 9:
				right = it
			it.mag += self.right.mag
		self.left = None
		self.right = None
		self.mag = 0
		return left, right

	def split(self):
		self.left = Snum(self.mag//2)
		self.left.parent = self
		self.right = Snum((self.mag+1)//2)
		self.right.parent = self

def add_snums(a, b):
	res = Snum(0)
	res.left = a
	a.parent = res
	res.right = b
	b.parent = res
	res.mag = None
	res.reduce()
	return res

with open(sys.argv[1], "r") as f:
	snums = (Snum(literal_eval(line)) for line in f.readlines() if line.strip())
	print(reduce(add_snums, snums))

