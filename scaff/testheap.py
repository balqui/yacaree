class itset(set):
	
	def __init__(self, s, p):
		set.__init__(self, s)
		self.support = p
		
	def __repr__(self):
		return set.__repr__(self) + "/" + str(self.support)

class heapitset(itset):
	
	def __init__(self, k):
#		itset.__init__(self)
		self.k = k
	
	def __repr__(self):
		return itset.__repr__(self) + "|" + str(self.k)

	def __le__(self, other):
		'override comparison for heap'
		return self.k >= other.k


	
from random import randrange
import heapq

for z in range(4):
	'repeat 4 experiments'
	h = []
	for y in range(4):
		'prepare a heap with 4 sets'
		u = randrange(1, 20)
		s = set(range(randrange(u), u))
		t = itset(s, randrange(100, 120))
		h.append(heapitset(t, randrange(1000, 1020)))
	heapify(h)
	print("Exp", z)
	for x in h:
		print("   in h: ", list(x))
	while h:
		x = pop(h)
		t = itset(x)
		s = set(t)
		print("   ordered:", x, type(x), t, type(t), s, type(s))
	
