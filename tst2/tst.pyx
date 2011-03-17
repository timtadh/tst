'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''

#from collections import deque
#import sys

cdef class node:
	cdef:
		char ch
		str key
		object val
		node l
		node m
		node r
		char accepting

	def __cinit__(self, ch, key=None, val=None, m=None):
		self.ch = ch
		self.key = key
		self.val = val
		self.l = None
		self.m = m
		self.r = None
		if key == None: self.accepting = False
		else: self.accepting = True

	def __getattribute__(self, name):
		if name == 'ch': return self.ch
		if name == 'key': return self.key
		if name == 'val': return self.val
		if name == 'l': return self.l
		if name == 'm': return self.m
		if name == 'r': return self.r
		if name == 'accepting': return self.r
		return object.__getattribute__(self, name)

	def __setattr__(self, name, val):
		if name == 'ch': self.ch = val
		if name == 'key': self.key = val
		if name == 'val': self.val = val
		if name == 'l': self.l = val
		if name == 'm': self.m = val
		if name == 'r': self.r = val
		if name == 'accepting': self.accepting = val

	cpdef internal(self):
		return self.l != None or self.m != None or self.r != None

	#def __str__(self):
		#cdef str ch
		#ch = chr(self.ch)
		#k = self.key
		#if ch == "\0": ch = "\\0"
		#if k: k = k[:-1]
		#if self.accepting: return "%s %s %s" % (ch, k, str(self.val))
		#return ch

	#def __repr__(self):
		#return str(self)


cdef class TST:
	'''A TST based symbol table:
		see Algorithms in (C|C++|Java) by Robert Sedgewick Ch. 15 Section 4'''
	cdef list heads

	def __cinit__(object self):
		self.heads = [None for x in xrange(256)]
		#o = object()
		#v = <PyObject*>o
		#self.root.val = s

	cdef __split(self, object p, object q, int d):
		cdef char pd
		cdef char qd
		cdef node t
		pd = ord(p.key[d])
		qd = ord(q.key[d])
		t = node(qd)
		if   pd <  qd: t.m = q; t.l = node(pd, m=p)
		elif pd == qd: t.m = self.__split(p, q, d+1);
		elif pd >  qd: t.m = q; t.r = node(pd, m=p)
		return t

	cdef __insert(self, node n, str symbol, object obj, int d):
		cdef char ch
		#sys.stderr.write('-->' + str(n) + ' ' + str(d) + '\n')
		if n == None:
			if d == len(symbol): ch = '\0'
			else: ch = ord(symbol[d])
			return node(ch, key=symbol, val=obj)
		if not n.internal():
			#sys.stderr.write('leaf node' + '\n')
			if len(n.key) == len(symbol) and n.key == symbol:
				#sys.stderr.write('same node' + '\n')
				n.val = obj
				return n
			else:
				#sys.stderr.write('different node' + '\n')
				ch = ord(symbol[d])
				return self.__split(node(ch, key=symbol, val=obj), n, d)
		ch = ord(symbol[d])
		#sys.stderr.write('internal node' + '\n')
		#sys.stderr.write('node' + ' ' + str(n.l) + ' ' + str(n.m) + ' ' + str(n.r) + '\n')
		if   ch <  n.ch: n.l = self.__insert(n.l, symbol, obj, d)
		elif ch == n.ch: n.m = self.__insert(n.m, symbol, obj, d+1)
		elif ch >  n.ch: n.r = self.__insert(n.r, symbol, obj, d)
		return n

	def __setitem__(object self, object symbol, object obj):
		symbol += '\0'
		self.heads[ord(symbol[0])] = self.__insert(self.heads[ord(symbol[0])], symbol, obj, 1)
		return

	def __getitem__(self, symbol):
		cdef char ch
		cdef char* sym
		cdef int length
		symbol += '\0'
		sym = symbol
		length = len(symbol)
		if length < 1:
			raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]
		next = (self.heads[sym[0]], 1)
		while next:
			n, d = next
			next = None
			##sys.stderr.write(str(n) + str(n.internal())+'\n')
			if n == None:
				raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]
			if n.internal():
				if d >= length:
					raise IndexError, "Out of bounds look up on sym length %i index %i" % (length, d)
				ch = sym[d]
				if   ch <  n.ch: next = (n.l, d);   continue
				elif ch == n.ch: next = (n.m, d+1); continue
				elif ch >  n.ch: next = (n.r, d);   continue
			elif n.key == symbol:
				return n.val
			raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]
		#should never reach ...
		raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]

	#def __str__(self):
		#s = str()
		#q = deque()
		#j = 0
		#while 1:
			#if not q and j >= len(self.heads):
				#break
			#elif not q:
				#h = None
				#end = False
				#while h == None:
					#h = self.heads[j]
					#j += 1
					#if j >= len(self.heads):
						#end = True
						#break
				#if h:
					#s += "head: " + chr(j-1) + '\n'
					#q.append((h, 1))
				#continue
			#n, m = q.pop()
			#if not n: continue
			#s += ' '*m + str(n) + '\n'
			#q.append((n.r, m+1))
			#q.append((n.m, m+1))
			#q.append((n.l, m+1))
		#return s

	#def __repr__(self):
		#return str(self)

