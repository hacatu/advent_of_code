import sys
from functools import cache
import math

mass = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

@cache
def min_cost(board):
	#[0, 11) is the hallway
	#[11, 15) is the top row
	#[15, 19) is the second row
	#[19, 23) is the third row
	#[23, 27) is the fourth row
	if board == "...........ABCDABCDABCDABCD":
		return 0
	options = {}
	#try moving the top element of each row into
	#the hallway
	for i, c in enumerate(board[11:15], 11):
		#find the top nonempty spot in this
		#room, skipping if it is empty or
		#all resdents belong there
		hall = (i-10)*2
		while c == '.' and i < 23:
			i += 4
			c = board[i]
		if c == '.':
			continue
		C = "ABCD"[(i-11)&3]
		if all(c == C for c in board[i:27:4]):
			continue
		#try hallway positions to the left
		for j in range(hall-1, -1, -1):
			if board[j] != '.':
				break
			if 2 <= j <= 8 and (j&1 == 0):
				continue
			option = board[:j] + c + board[j+1:i] + '.' + board[i+1:]
			cost = (hall - j + 1 + (i-11)//4)*mass[c]
			options[option] = cost
		#try hallway positions to the right
		for j in range(hall+1, 11):
			if board[j] != '.':
				break
			if 2 <= j <= 8 and (j&1 == 0):
				continue
			option = board[:j] + c + board[j+1:i] + '.' + board[i+1:]
			cost = (j - hall + 1 + (i-11)//4)*mass[c]
			options[option] = cost
	#try moving every element in the hallway into
	#the appropriate room
	for i, c in enumerate(board[:11]):
		if c == '.':
			continue
		hall = (ord(c)-ord('A')+1)*2
		room = hall//2+10
		#skip full rooms
		if board[room] != '.':
			continue
		while room < 23 and board[room+4] == '.':
			room += 4
			c = board[room]
		C = "ABCD"[(room-11)&3]
		if any(c != C for c in board[room:27:4]):
			continue
		for j in range(min(i, hall)+1, max(i, hall)):
			if board[j] != '.':
				break
		else:
			option = board[:i] + '.' + board[i+1:room] + c + board[room+1:]
			cost = (abs(i - hall) + 1 + (room - 11)//4)*mass[c]
			options[option] = cost
	if not options:
		return math.inf
	return min(cost + min_cost(option) for (option, cost) in options.items())

#print(min_cost("...........DBDADCBADBACCCAB"))
print(min_cost("...........BCBDDCBADBACADCA"))
