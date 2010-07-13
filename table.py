'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''
from collections import deque

# Instructions
MATCH = 0
CHAR = 1
SPLIT = 2
JMP = 3

# Other constants
WILDCARD = 0x11FFFF
INF = 0x10FFFF

def match_globs(a, b):
	def endpoints(s):
		if '*' not in s: return s, s[-1::-1]
		start = s[:s.index('*')]
		end = s[len(s) - s[-1::-1].index('*'):][-1::-1]
		return start, end
	astart, aend = endpoints(a)
	bstart, bend = endpoints(b)
	#print astart, bstart
	#print aend, bend
	#print
	for i, ch in enumerate(astart):
		if len(bstart) <= i:
			if bstart == b and b == bend[-1::-1]: return False
			break
		if ch != bstart[i]: return False
	for i, ch in enumerate(aend):
		if len(bend) <= i:
			if bstart == b and b == bend[-1::-1]: return False
			break
		if ch != bend[i]: return False
	return True

class SymbolTable(object):

	def __init__(self):
		self.root = Node(None, None)
		self.objs = dict()

	def find(self, pattern):
		insts = list()
		for ch in pattern:
			if ch != '*':
				insts.append((CHAR, ord(ch), ord(ch)))
			else:
				i = len(insts)
				insts.append((SPLIT, len(insts)+1, len(insts)+3))
				insts.append((CHAR, WILDCARD, WILDCARD))
				insts.append((JMP, i, 0))
		insts.append((MATCH, 0, 0))
		def items(symbol, insts):
			matches = hendersonvm(insts, self.root)
			try: 
				match = matches.next()
			except StopIteration: 
				raise KeyError, \
					"Symbol pattern '%s' not found in table." % symbol
			yield match
			for match in matches:
				yield match
		return items(pattern, insts)

	def keys(self): return self.objs.keys()
	
	def iteritems(self): return self.objs.iteritems()

	def __len__(self): return len(self.objs)

	def __setitem__(self, symbol, obj):
		if symbol in self.objs:
			self.objs[symbol].obj = obj
		else:
			n = self.root
			for c in symbol:
				if c not in n:
					n[c] = Node(c, n)
				n = n[c]
			n.accepting = True
			n.symbol = symbol
			n.obj = obj
			self.objs[symbol] = n

	def __getitem__(self, symbol):
		return self.objs[symbol].obj

	def __delitem__(self, symbol):
		if symbol not in self.objs:
			raise KeyError, "Symbol '%s' not in table." % symbol
		n = self.objs[symbol]
		del self.objs[symbol]
		n.accepting = False
		n.symbol = None
		n.obj = None
		while not n.edges:
			if n.fromch == None and n.parent == None: return
			del n.parent[n.fromch]
			n = n.parent

	def __iter__(self):
		for k in self.objs: yield k

	def __contains__(self, symbol):
		try: return bool(tuple(self[symbol]))
		except KeyError: return False

	def __str__(self):
		if not len(self): return '{}'
		return str(dict(self['*']))
	
	def __repr__(self):
		return str(self)

class Node(object):

	def __init__(self, fromch, parent):
		self.fromch = fromch
		self.parent = parent
		self.obj = None
		self.accepting = False
		self.symbol = None
		self.edges = dict()

	def __len__(self):
		return len(self.edges)

	def __setitem__(self, ch, node):
		if ch in self.edges:
			raise KeyError, "Character %s already in Node" % ch
		self.edges[ch] = node

	def __getitem__(self, ch):
		return self.edges[ch]

	def __delitem__(self, ch):
		del self.edges[ch]

	def __iter__(self):
		for k in self.edges: yield k

	def __contains__(self, ch):
		return ch in self.edges

	def __str__(self):
		if self.accepting: return str((self.symbol, self.obj))
		return str(self.edges)

	def __repr__(self):
		return str(self)

class Thread(object):
	def __init__(self, prog, node):
		self.prog = prog
		self.node = node
	def __eq__(self, b): return self.prog == b.prog and self.node == b.node
	def __nq__(self, b): return self.prog != b.prog and self.node != b.node
	def __lt__(self, b): return self.prog < b.prog
	def __le__(self, b): return self.prog <= b.prog
	def __gt__(self, b): return self.prog > b.prog
	def __ge__(self, b): return self.prog >= b.prog
	def __repr__(self): return str(self)
	def __str__(self): return str((self.prog, self.node))

def hendersonvm(program, node):
	def addthread(l, thread):
		if thread not in l: l.append(thread)

	def addnode(d, t, node):
		if not d.has_key(t):
			d[t] = set()
		if node not in d[t]: d[t].add(node)

	def dupnodes(d, t, t2):
		if not d.has_key(t2):
			d[t2] = set()
		d[t2] |= d[t]

	if not program: return
	if not node: return
	clist = deque()
	nlist = deque()
	cnodes = dict()
	nnodes = dict()

	addthread(clist, 0)
	addnode(cnodes, 0, node)

	while clist:
		while clist:
			pc = clist.popleft()
			inst = program[pc]
			if inst[0] == JMP:
				addthread(clist, inst[1])
				dupnodes(cnodes, pc, inst[1])
			elif inst[0] == SPLIT:
				addthread(clist, inst[1])
				addthread(clist, inst[2])
				dupnodes(cnodes, pc, inst[1])
				dupnodes(cnodes, pc, inst[2])
			elif cnodes.has_key(pc):
				for n in cnodes[pc]:
					if inst[0] == CHAR:
						for ch in n:
							x, y = inst[1], inst[2]; c = ord(ch)
							if (y and x <= c <= y) or c == x or x == WILDCARD:
								addthread(nlist, pc+1)
								addnode(nnodes, pc+1, n[ch])
					elif inst[0] == MATCH:
						if n.accepting:
							yield n.symbol, n.obj
		cnodes = nnodes
		nnodes = dict()
		clist = nlist
		nlist = deque()

if __name__ == '__main__':
	t = SymbolTable()
	t['xyz'] = 1
	t['xysdfz'] = 2
	t['ysdfz'] = 3
	print dict(t)
	print dict(t.find('xyz'))
	print dict(t.find('x*'))
	for x in t:
		print x
	#print tuple(t['xyz'])
	#print t
	#print 'x*' in t
	#print 'xyq' in t
	#print 'xyz' in t
	#print len(t)
	#print
	#print [(k, tuple(t[k])) for k in t]
	#print
	#del t['xyz']
	#print t
	#del t['xysdfz']
	#print t
	#del t['ysdfz']
	#print t
