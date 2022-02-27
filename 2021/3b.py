import sys

with open(sys.argv[1], "r") as f:
	ns = list(filter(len, (line.strip() for line in f.readlines())))

def bin_i(ns, i):
	i_bins = [[], []]
	for n in ns:
		 i_bins[ord(n[i])-ord('0')].append(n)
	return i_bins

i_bins = bin_i(ns, 0)
if len(i_bins[0]) > len(i_bins[1]):
	ogr_cands, csr_cands = i_bins
else:
	csr_cands, osr_cands = i_bins
for i in range(1, len(ns[0])):
	if len(ogr_cands) == 1:
		break
	#This `[::-1]` is a hack to ensure ties are awarded to '1'
	ogr_cands = max(bin_i(ogr_cands, i)[::-1], key=len)
for i in range(1, len(ns[0])):
	if len(csr_cands) == 1:
		break
	csr_cands = min(bin_i(csr_cands, i), key=len)

ogr = int(ogr_cands[0], 2)
csr = int(csr_cands[0], 2)
print(ogr*csr)
