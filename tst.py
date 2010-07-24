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
				sys.stderr.write('case1\n')
				sys.stderr.write(str((symbol, n.key, n.ch, ch))+'\n')
				if   ch <  n.ch: n.l = insert(n.l, d)
				elif ch == n.ch:
					if n.key == symbol: n.val = obj
					else:
						print self
						raise Exception, "same object? no ..."
				elif ch >  n.ch: n.r = insert(n.r, d)
				return n
			elif d+1 == len(n.key):
				sys.stderr.write('case2\n')
				sys.stderr.write(str((symbol, n.key, n.ch, ch))+'\n')
				if   ch <  n.ch: n.l = insert(n.l, d)
				elif ch == n.ch: n.m = insert(n.m, d+1)
				elif ch >  n.ch: n.r = insert(n.r, d)
				return n
			elif d+1 == len(symbol):
				sys.stderr.write('case3\n')
				sys.stderr.write(str((symbol, n.key, n.ch, ch))+'\n')
				new = node(ch, key=symbol, val=obj)
				if ch <  n.ch: new.r = n
				if ch == n.ch: new.m = n
				if ch >  n.ch: new.l = n
				return new
			else:
				sys.stderr.write('case4\n')
				sys.stderr.write(str((symbol, n.key, n.ch, ch, ch<n.ch, ch==n.ch, ch>n.ch))+'\n')
				new = node(n.ch, m=node(n.key[d+1], key=n.key, val=n.val))
				if   ch <  n.key[d]: new.l = node(ch, key=symbol, val=obj)
				elif ch == n.key[d]: new.m = split(d+1, new.m)
				elif ch >  n.key[d]: new.r = node(ch, key=symbol, val=obj)
				return new
			raise Exception
		def insert(n, d):
			sys.stderr.write('-->' + str(n) + ' ' + str(d) + '\n')
			if d >= len(symbol):
				sys.stderr.write(str((d, len(symbol), symbol,n))+'\n')
				print self
			ch = symbol[d]
			if n == None:
				sys.stderr.write('case0\n')
				#sys.stderr.write(str((symbol, n.key, n.ch, ch))+'\n')
				return node(ch, key=symbol, val=obj)
			if not n.internal():
				return split(d, n)
			if d+1 == len(symbol) and ch == n.ch:
				if n.accepting and n.key == symbol:
					sys.stderr.write('case5\n')
					sys.stderr.write(str((symbol, n.key, n.ch, ch))+'\n')
					n.val = obj
					return n
				elif n.accepting:
					sys.stderr.write('case6\n')
					sys.stderr.write(str((symbol, n.key, n.ch, ch))+'\n')
				else:
					sys.stderr.write('case7\n')
					sys.stderr.write(str((symbol, n.key, n.ch, ch))+'\n')
					#new = node(ch, key=symbol, val=obj)
					n.key = symbol
					n.val = obj
					n.accepting = True
					#if ch <  n.ch: new.r = n
					#if ch == n.ch: new.m = n
					#if ch >  n.ch: new.l = n
					return n
			sys.stderr.write('case8\n')
			sys.stderr.write(str((symbol, n.key, n.ch, ch, ch<n.ch, ch==n.ch, ch>n.ch))+'\n')
			if   ch <  n.ch: n.l = insert(n.l, d)
			elif ch == n.ch: n.m = insert(n.m, d+1)
			elif ch >  n.ch: n.r = insert(n.r, d)
			return n
		#print
		#print
		sys.stderr.write('\n\n\ninsert ' + symbol + ' ' + str(obj)+'\n')
		self.root = insert(self.root, 0)

	def __getitem__(self, symbol):
		def get(n, d):
			sys.stderr.write(str(n)+'\n')
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
		sys.stderr.write('\n\n\nget ' + symbol +'\n')
		return get(self.root, 0)

	def __delitem__(self, symbol):
		pass

	def __iter__(self):
		pass

	def __contains__(self, symbol):
		pass

	def __str__(self):
		q = deque()
		q.append((self.root, 0))
		i = 0
		nodes = dict()
		edges = dict()
		while len(q) > 0:
			n, m = q.pop()
			if not n: continue
			q.append((n.r, 0))
			q.append((n.m, 1))
			q.append((n.l, 2))
			if n not in nodes:
				#sys.stderr.write(str(m) + ' ' + str(n.accepting) + '\n')
				nodes[n] = ('node' + str(i), m, n.accepting)
				i += 1
			if n not in edges:
				edges[n] = list()
			if n.l != None: edges[n].append(n.l)
			if n.m != None: edges[n].append(n.m)
			if n.r != None: edges[n].append(n.r)
		s = 'digraph tst {\n'
		for k,v in nodes.iteritems():
			name, shape, accept = v
			style = ''
			if accept: style = 'style="filled" fillcolor="#63ADD0"'
			if shape == 1: n = '%s[shape="box" %s label="%s"];\n' % (name, style, str(k))
			elif shape == 2: n = '%s[shape="diamond" %s label="%s"];\n' % (name, style, str(k))
			else: n = '%s[%s label="%s"];\n' % (name, style, str(k))
			s += n
			#sys.stderr.write(n)
		for k,v in edges.iteritems():
			n1, a, b = nodes[k]
			for e in v:
				n2, a, b = nodes[e]
				s += '%s -> %s;\n' % (n1, n2)
		s += '}\n'
		return s

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

	def __hash__(self):
		return hash((self.ch, self.key, self.val, self.l, self.m, self.r, self.accepting))

	def __eq__(self, a):
		return hash(self) == hash(a)

	def __ne__(self, a):
		return hash(self) != hash(a)

	def __str__(self):
		if self.accepting: return "%s %s %s" % (self.ch, self.key, str(self.val))
		return self.ch

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
