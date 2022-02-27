import sys
from functools import cache
import math

mass = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

@cache
def min_cost(board):
	#we define the board as a 19 character string:
	#the first 11 are the hallway from left to right,
	#then the next 4 are the tops of the rooms,
	#then the next 4 are the bottoms
	if board == "...........ABCDABCD":
		return 0
	options = {}
	for i, c in enumerate(board[11:15], 11):
		if c == "ABCD"[i-11] == board[i+4]:
			continue
		hall = (i-10)*2
		if c == '.':
			i += 4
			c = board[i]
			if c == '.' or c == "ABCD"[i-15]:
				continue
		for j in range(hall-1, -1, -1):
			if board[j] != '.':
				break
			if 2 <= j <= 8 and (j&1 == 0):
				continue
			option = board[:j] + c + board[j+1:i] + '.' + board[i+1:]
			cost = (hall - j + 1 + int(i >= 15))*mass[c]
			options[option] = cost
		for j in range(hall+1, 11):
			if board[j] != '.':
				break
			if 2 <= j <= 8 and (j&1 == 0):
				continue
			option = board[:j] + c + board[j+1:i] + '.' + board[i+1:]
			cost = (j - hall + 1 + int(i >= 15))*mass[c]
			options[option] = cost
	for i, c in enumerate(board[:11]):
		if c == '.':
			continue
		hall = (ord(c)-ord('A')+1)*2
		room = hall//2+10
		if board[room] != '.':
			continue
		if board[room+4] == '.':
			room += 4
		elif board[room+4] != c:
			continue
		for j in range(min(i, hall)+1, max(i, hall)):
			if board[j] != '.':
				break
		else:
			option = board[:i] + '.' + board[i+1:room] + c + board[room+1:]
			cost = (abs(i - hall) + 1 + int(room >= 15))*mass[c]
			options[option] = cost
	if not options:
		return math.inf
	return min(cost + min_cost(option) for (option, cost) in options.items())

print(min_cost("...........DBDACCAB"))
