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

with open(sys.argv[1], "r") as f:
	for line in f.readlines():
		bits = "".join(f"{int(c, 16):04b}" for c in line.strip())
		packet, _ = Packet.from_string(bits)
		break

print(packet.version_sum())
