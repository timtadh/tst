'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''
from collections import deque
from os.path import sep as PATH_SEP

END = '\x00'
NOITEM = type('NOITEM', (object,), {'__str__':lambda self: 'NOITEM', '__repr__':lambda self: 'NOITEM'})()

class TST(object):
	'''A TST based symbol table:
		see Algorithms in (C|C++|Java) by Robert Sedgewick Ch. 15 Section 4'''

	def __init__(self):
		self.root = None

	def find(self, pattern):
		pass

	def keys(self):
		pass

	def iteritems(self):
		pass

	def __len__(self):
		pass

	def __setitem__(self, symbol, obj):
		def split(d, n):
			ch = symbol[d]
			#print d, n, len(symbol), ch, n.key[d]
			if d+1 == len(symbol) and d+1 == len(n.key):
				#print 'case1'
				if   ch <  n.ch: n.l = insert(n.l, d)
				elif ch == n.ch:
					if n.key == symbol: n.val = obj
					else: raise Exception, "same object? no ..."
				elif ch >  n.ch: n.r = insert(n.r, d)
				return n
			elif d+1 == len(n.key):
				#print 'case2'
				if   ch <  n.ch: n.l = insert(n.l, d)
				elif ch == n.ch: n.m = insert(n.m, d+1)
				elif ch >  n.ch: n.r = insert(n.r, d)
				return n
			elif d+1 == len(symbol):
				#print 'case3'
				#print symbol, n.key, n.ch, ch
				new = node(ch, key=symbol, val=obj)
				if ch <  n.ch: new.r = n
				if ch == n.ch: new.m = n
				if ch >  n.ch: new.l = n
				return new
			else:
				#print 'case4'
				#print n.key, symbol, n.ch, ch
				new = node(n.ch, m=node(n.key[d+1], key=n.key, val=n.val))
				if   ch <  n.key[d]: new.l = node(ch, key=symbol, val=obj)
				elif ch == n.key[d]: new.m = split(d+1, new.m)
				elif ch >  n.key[d]: new.r = node(ch, key=symbol, val=obj)
				return new
			raise Exception
		def insert(n, d):
			#print n, d
			ch = symbol[d]
			if n == None:
				return node(ch, key=symbol, val=obj)
			if not n.internal():
				return split(d, n)
			if n.accepting and d+1 == len(symbol) and d+1 == len(n.key) and ch == n.ch:
				if n.key == symbol:
					n.val = obj
					return n
			if   ch <  n.ch: n.l = insert(n.l, d)
			elif ch == n.ch: n.m = insert(n.m, d+1)
			elif ch >  n.ch: n.r = insert(n.r, d)
			return n
		#print
		#print
		#print 'insert', symbol, obj
		self.root = insert(self.root, 0)

	def __getitem__(self, symbol):
		def get(n, d):
			if n == None:
				raise KeyError, "Symbol '%s' is not in table." % symbol
			#print d, len(symbol)
			if n.accepting and d+1 == len(symbol) and d+1 == len(n.key):
				if n.key == symbol:
					return n.val
			if n.internal():
				ch = symbol[d]
				if   ch <  n.ch: return get(n.l, d)
				elif ch == n.ch: return get(n.m, d+1)
				elif ch >  n.ch: return get(n.r, d)
			if n.key == symbol:
				return n.val
			raise KeyError, "Symbol '%s' is not in table." % symbol
		return get(self.root, 0)

	def __delitem__(self, symbol):
		pass

	def __iter__(self):
		pass

	def __contains__(self, symbol):
		pass

	def __str__(self):
		return "{" + str(self.root) + "}"

	def __repr__(self):
		return str(self)

class node(object):
	'''A node of a TST'''

	def __init__(self, ch, key=None, val=NOITEM, m=None):
		#if ch == END:
			#assert key != None
			#assert val != NOITEM
			#assert m == None
		#else:
			#assert key == None
			#assert val == NOITEM
			#assert m != None
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
		return str((self.ch, self.key, self.val, self.accepting, [self.l, self.m, self.r]))

	def __repr__(self):
		return str(self)

if __name__ == '__main__':
	t = TST()
	t['b'] = 2
	print '>', t
	t['a'] = 1
	print '>', t
	t['d'] = 4
	t['daf'] = 5
	t['db'] = 6
	print '>', t
	t['dac'] = 3
	print '>', t
	print 'b', t['b']
	print 'a', t['a']
	print 'daf', t['daf']
	print 'dac', t['dac']
	print 'd', t['d']
	print 'db', t['db']
	#t['cddda'] = 6
	#print '>', t
	#t['cd'] = 7
	#print '>', t
	#t['cd'] = 8
	#print '>', t
	#t['cde'] = 9
	#print '>', t
