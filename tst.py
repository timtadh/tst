'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''
from collections import deque
from os.path import sep as PATH_SEP
import sys

END = '\x00'

class TST(object):
	'''A TST based symbol table:
		see Algorithms in (C|C++|Java) by Robert Sedgewick Ch. 15 Section 4'''

	def __init__(self):
		self.heads = [None for x in xrange(256)]
		#self.root =None

	#def find(self, pattern):
		#pass

	#def keys(self):
		#pass

	#def iteritems(self):
		#pass

	#def __len__(self):
		#pass

	def __setitem__(self, symbol, obj):
		symbol += END
		def split(p, q, d):
			pd = p.key[d]
			qd = q.key[d]
			t = node(qd)
			if   pd <  qd: t.m = q; t.l = node(pd, m=p)
			elif pd == qd: t.m = split(p, q, d+1);
			elif pd >  qd: t.m = q; t.r = node(pd, m=p)
			return t
		def insert(n, d):
			#sys.stderr.write('-->' + str(n) + ' ' + str(d) + '\n')
			if n == None:
				if d == len(symbol): ch = '\0'
				else: ch = symbol[d]
				return node(ch, key=symbol, val=obj)
			if not n.internal():
				#sys.stderr.write('leaf node' + '\n')
				if len(n.key) == len(symbol) and n.key == symbol:
					#sys.stderr.write('same node' + '\n')
					n.val = obj
					return n
				else:
					#sys.stderr.write('different node' + '\n')
					ch = symbol[d]
					return split(node(ch, key=symbol, val=obj), n, d)
			ch = symbol[d]
			#sys.stderr.write('internal node' + '\n')
			#sys.stderr.write('node' + ' ' + str(n.l) + ' ' + str(n.m) + ' ' + str(n.r) + '\n')
			if   ch <  n.ch: n.l = insert(n.l, d)
			elif ch == n.ch: n.m = insert(n.m, d+1)
			elif ch >  n.ch: n.r = insert(n.r, d)
			return n
		#sys.stderr.write('\n\n\ninsert ' + symbol + ' ' + str(obj)+'\n')
		self.heads[ord(symbol[0])] = insert(self.heads[ord(symbol[0])], 1)
		#self.root = insert(self.root, 0)

	def __getitem__(self, symbol):
		symbol += END
		next = (self.heads[ord(symbol[0])], 1)
		while next:
			n, d = next
			##sys.stderr.write(str(n)+'\n')
			if n == None:
				raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]
			if n.internal():
				ch = symbol[d]
				if   ch <  n.ch: next = (n.l, d);   continue
				elif ch == n.ch: next = (n.m, d+1); continue
				elif ch >  n.ch: next = (n.r, d);   continue
			elif n.key == symbol:
				return n.val
			raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]
		#should never reach ...
		raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]

	def __delitem__(self, symbol):
		symbol += END
		def check(n):
			if n == None: return None
			if not n.internal() and n.key == None:
				return None
			return n
		def remove(n, d):
			##sys.stderr.write('-->' + str(n) + ' ' + str(d) + '\n')
			if n == None:
				raise KeyError, "Symbol '%s' is not in table." % symbol
			if n.internal():
				ch = symbol[d]
				if   ch <  n.ch: n.l = check(remove(n.l, d))
				elif ch == n.ch: n.m = check(remove(n.m, d+1))
				elif ch >  n.ch: n.r = check(remove(n.r, d))
			else:
				if n.key == symbol:
					return None
				else:
					raise KeyError, "Symbol '%s' is not in table." % symbol
			return check(n)
		self.heads[ord(symbol[0])] = remove(self.heads[ord(symbol[0])], 1)

	#def __iter__(self):
		#pass

	#def __contains__(self, symbol):
		#pass

	def __str__(self):
		s = ''
		q = deque()
		#for i,x in enumerate(self.heads):
			#if x == None: continue
			#s += "head: " + chr(i) + '\n'
			#q.append((x, 1))
		j = 0
		while 1:
			if not q and j >= len(self.heads):
				break
			elif not q:
				h = None
				end = False
				while h == None:
					h = self.heads[j]
					j += 1
					if j >= len(self.heads):
						end = True
						break
				if h:
					s += "head: " + chr(j-1) + '\n'
					q.append((h, 1))
				continue
			n, m = q.pop()
			if not n: continue
			s += ' '*m + str(n) + '\n'
			q.append((n.r, m+1))
			q.append((n.m, m+1))
			q.append((n.l, m+1))
		return s

	def __repr__(self):
		return str(self)

class node(object):
	'''A node of a TST'''
	__slots__ = ['ch', 'key', 'val', 'l', 'm', 'r', 'accepting']

	def __init__(self, ch, key=None, val=None, m=None):
		self.ch = ch
		self.key = key
		self.val = val
		self.l = None
		self.m = m
		self.r = None
		if key == None: self.accepting = False
		else: self.accepting = True

	def internal(self):
		return self.l != None or self.m != None or self.r != None

	def __str__(self):
		ch = self.ch
		k = self.key
		if ch == END: ch = r'\0'
		if k: k = k[:-1]
		if self.accepting: return "%s %s %s" % (ch, k, str(self.val))
		return ch

	def __repr__(self):
		return str(self)
