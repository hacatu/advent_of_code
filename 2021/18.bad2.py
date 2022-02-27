import sys
from ast import literal_parse
from functools import reduce, total_ordering
from dataclasses import dataclass

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
		self.depth = 0 if parent is None else parent.depth + 1
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

	def get_zipper(self):
		path = 1
		depth = 0
		while self.parent is not None:
			depth += 1
			if self is self.parent.right:
				path |= 1 << depth
			self = self.parent
		return BTZipper(path, depth)

	def reduce(self):
		if self.left is not None:
			self.left.reduce()
			if depth == 4:
				left, _ = self.explode()
				if left is not None:
					left.split()
					left.reduce()
			self.right.reduce()
		elif self.mag > 9:
			self.split()
			if depth == 4:
				left, _ = self.explode()
				if left is not None:
					left.split()
					left.reduce()

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
			it.mag += self.left.mag
			if it.mag > 9:
				left = it
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
			it.mag += self.right.mag
			if it.mag > 9:
				right = it
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
	a = Snum

with open(sys.argv[1], "r") as f:
	snums = (Snum(literal_parse(line)) for line in f.readlines() if line.strip())
	reduce(snums, add_snums)
