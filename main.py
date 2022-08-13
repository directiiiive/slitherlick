import random
import time
import copy

class board:
	def __init__(self, size):
		self.size = size
		self.board = [0 for i in range(size**2)]
		self.whitespaces = [0 for i in range(size**2)]
		self.edges = [i for i in range(size)]+[i*size for i in range(1,size-1)]+[i*size-1 for i in range(2,size)]+[i for i in range(size*(size-1),size**2)]
		self.bounds = [i for i in range(size)]+[i*size for i in range(1,size-1)]+[i*size-1 for i in range(2,size)]+[i for i in range(size*(size-1),size**2)]
		self.count = size**2
		self.lastcut = []#all the cut spaces ever
		self.corners = []
		self.sincecut = 0

	def onecount(self, position):
		for i in [[0,1],[1,0],[0,-1],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]:
			if onecount > 1:
				return False
			pos = position + i[0]*self.size + i[1]
			if 0 <= pos < self.size**2:
				if max(-1*(pos%self.size-position%self.size), pos%self.size-position%self.size) <= 1:
					if board[pos] == 1:
						onecount += 1
						
		return True

	def directionchoose(self, position):
		directions = [[0,1],[0,-1],[1,0],[-1,0]]
		
		if not self.onecount(position):
			return []
		
		for i in [[0,1],[0,-1],[1,0],[-1,0]]:
			pos = position+i[0]*self.size+i[1]
			if pos in self.bounds or pos in self.edges or pos in self.lastcut:
				if max(pos%self.size-(position)%self.size, (position)%self.size-pos%self.size) > 1 or not (0 <= pos < self.size**2):
					directions.remove(i)
		return directions

	def lengthchoose(self, direction, position):
		counter = 1
		maxdist = 0
		
		while True:
			pos = position + counter*(direction[0]*self.size + direction[1])
			if pos not in self.bounds:
				if pos not in self.edges and pos not in self.corners:
					maxdist += 1

			else:
				break

			counter += 1

		return maxdist

	def edgesupdate(self, position):
		self.edges.remove(position)
		for i in range(self.size):
			for j in range(self.size):
				for k in [[0,1],[0,-1],[1,0],[-1,0]]:
					pos = i*self.size+j+self.size*k[0]+k[1]
					if 0 <= pos < self.size**2:
						if self.board[pos] == 1:
							if (i*self.size+j) not in self.edges and (i*self.size+j) not in self.lastcut:
								self.edges.append(i*self.size+j)
								break
				for l in [[1,1],[-1,1],[1,-1],[-1,-1]]:
					pos = i*self.size+j+self.size*l[0]+l[1]
					if 0 <= pos < self.size**2:
						if self.board[pos] == 1:
							if (i*self.size+j) not in self.corners and (i*self.size+j) not in self.lastcut:
								self.corners.append(i*self.size+j)
								break

	def cutting(self):
		random.shuffle(self.edges)
		position = self.edges[0]

		directions = self.directionchoose(position)
		
		if directions:
			random.shuffle(directions)
			direction = directions[0]
			lengthmax = self.lengthchoose(direction, position)
			print(lengthmax)
			
			if lengthmax == 0:
				self.sincecut += 1
				return 0
				
			distance = random.randint(1,lengthmax)
			if (position + distance*(direction[0]*self.size+direction[1])) not in self.bounds:
				self.sincecut = 0
				for i in range(0,distance+1):
					self.board[position+direction[0]*self.size*i+direction[1]*i] = 1
					self.lastcut.append(position+direction[0]*self.size*i+direction[1]*i)
		
				self.edgesupdate(position)
		
				return distance
			self.sincecut += 1
			return 0
		self.sincecut += 1
		return 0

	def printboard(self):
		for i in range(len(self.board)):
			if i%self.size == 0:
				print("")
			if i in self.edges and self.board[i] != 1:
				print(f"* ", end = "")
			else:
				print(f"{self.board[i]} ", end = "")
		print("")

	def multicut(self):
		while self.sincecut < 20:
			self.printboard()
			print(self.edges)
			print(self.bounds)


board = board(10)
board.multicut()
board.printboard()