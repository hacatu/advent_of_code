import sys

class Packet:
	def __init__(self, version, type):
		self.version = version
		self.type = type
		self.value = None
		self.operands = []

	@classmethod
	def from_string(clazz, bits):
		version = int(bits[:3], 2)
		type = int(bits[3:6], 2)
		res = Packet(version, type)
#		print(f"Parsing packet with version {version} and type {type}")
#		print(f"at {bits}")
		if type == 4:
#			print("   VVVTTT")
#			print("packet is a literal")
			value = 0
			i = 6
			while i + 4 < len(bits):
				value = (value << 4) | int(bits[i+1:i+5], 2)
				i += 5
				if bits[i-5] == "0":
					break
			res.value = value
		elif bits[6] == "0":
			tot_ops_len = int(bits[7:22], 2)
			i = 22
#			print("   VVVTTTILLLLLLLLLLLLLLL")
#			print("Packet has len type 0")
			while i < tot_ops_len + 22:
				op, length = clazz.from_string(bits[i:])
				res.operands.append(op)
				i += length
		else:
			num_ops = int(bits[7:18], 2)
			i = 18
#			print("   VVVTTTILLLLLLLLLLL")
#			print("packet has len type 1")
			for _ in range(num_ops):
				op, length = clazz.from_string(bits[i:])
				res.operands.append(op)
				i += length
		return res, i

	def version_sum(self):
		return self.version + sum(op.version_sum() for op in self.operands)

	def compute_value(self):
		if self.value is not None:
			return self.value
		for op in self.operands:
			op.compute_value()
		if self.type == 0:
			self.value = sum(op.value for op in self.operands)
		elif self.type == 1:
			res = 1
			for op in self.operands:
				res *= op.value
			self.value = res
		elif self.type == 2:
			self.value = min(op.value for op in self.operands)
		elif self.type == 3:
			self.value = max(op.value for op in self.operands)
		elif self.type == 5:
			self.value = int(self.operands[0].value > self.operands[1].value)
		elif self.type == 6:
			self.value = int(self.operands[0].value < self.operands[1].value)
		elif self.type == 7:
			self.value = int(self.operands[0].value == self.operands[1].value)
		return self.value

with open(sys.argv[1], "r") as f:
	for line in f.readlines():
		bits = "".join(f"{int(c, 16):04b}" for c in line.strip())
		packet, _ = Packet.from_string(bits)
		break

print(packet.compute_value())
