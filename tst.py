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
			ch = symbol[d]
			if n == None:
				return node(ch, key=symbol, val=obj)
			if not n.internal():
				return split(node(ch, key=symbol, val=obj), n, d)
			if   ch <  n.ch: n.l = insert(n.l, d)
			elif ch == n.ch: n.m = insert(n.m, d+1)
			elif ch >  n.ch: n.r = insert(n.r, d)
			return n
		#print
		#print
		#sys.stderr.write('\n\n\ninsert ' + symbol + ' ' + str(obj)+'\n')
		self.heads[ord(symbol[0])] = insert(self.heads[ord(symbol[0])], 1)
		#self.root = insert(self.root, 0)

	def __getitem__(self, symbol):
		symbol += END
		next = (self.heads[ord(symbol[0])], 1)
		while next:
			n, d = next
			#sys.stderr.write(str(n)+'\n')
			if n == None:
				raise KeyError, "Symbol '%s' is not in table." % symbol
			if n.internal():
				ch = symbol[d]
				if   ch <  n.ch: next = (n.l, d);   continue
				elif ch == n.ch: next = (n.m, d+1); continue
				elif ch >  n.ch: next = (n.r, d);   continue
			elif n.key == symbol:
				return n.val
			raise KeyError, "Symbol '%s' is not in table." % symbol
		#should never reach ...
		raise KeyError, "Symbol '%s' is not in table." % symbol

	def __delitem__(self, symbol):
		symbol += END
		def remove(n, d):
			#sys.stderr.write('-->' + str(n) + ' ' + str(d) + '\n')
			if n == None:
				raise KeyError, "Symbol '%s' is not in table." % symbol
			if n.internal():
				ch = symbol[d]
				if   ch <  n.ch: n.l = remove(n.l, d)
				elif ch == n.ch: n.m = remove(n.m, d+1)
				elif ch >  n.ch: n.r = remove(n.r, d)
			else:
				if n.key == symbol:
					return None
				else:
					raise KeyError, "Symbol '%s' is not in table." % symbol
			return n
		self.heads[ord(symbol[0])] = remove(self.heads[ord(symbol[0])], 1)

	#def __iter__(self):
		#pass

	#def __contains__(self, symbol):
		#pass

	#def __str__(self):
		#q = deque()
		#q.append((self.root, 0))
		#i = 0
		#nodes = dict()
		#edges = dict()
		#while len(q) > 0:
			#n, m = q.pop()
			#if not n: continue
			#q.append((n.r, 0))
			#q.append((n.m, 1))
			#q.append((n.l, 2))
			#if n not in nodes:
				###sys.stderr.write(str(m) + ' ' + str(n.accepting) + '\n')
				#nodes[n] = ('node' + str(i), m, n.accepting)
				#i += 1
			#if n not in edges:
				#edges[n] = list()
			#if n.l != None: edges[n].append(n.l)
			#if n.m != None: edges[n].append(n.m)
			#if n.r != None: edges[n].append(n.r)
		#s = 'digraph tst {\n'
		#for k,v in nodes.iteritems():
			#name, shape, accept = v
			#style = ''
			#label = '\\' + str(k)
			#if accept: style = 'style="filled" fillcolor="#63ADD0"'
			#if shape == 1: n = '%s[shape="box" %s label="%s"];\n' % (name, style, label)
			#elif shape == 2: n = '%s[shape="diamond" %s label="%s"];\n' % (name, style, label)
			#else: n = '%s[%s label="%s"];\n' % (name, style, label)
			#s += n
			###sys.stderr.write(n)
		#for k,v in edges.iteritems():
			#n1, a, b = nodes[k]
			#for e in v:
				#n2, a, b = nodes[e]
				#s += '%s -> %s;\n' % (n1, n2)
		#s += '}\n'
		#return s

	#def __repr__(self):
		#return str(self)

class node(object):
	'''A node of a TST'''
	__slots__ = ['ch', 'key', 'val', 'l', 'm', 'r', 'accepting']

	def __init__(self, ch, key=None, val=NOITEM, m=None):
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

	#def __hash__(self):
		#return hash((self.ch, self.key, self.val, self.l, self.m, self.r, self.accepting))

	#def __eq__(self, a):
		#return hash(self) == hash(a)

	#def __ne__(self, a):
		#return hash(self) != hash(a)

	#def __str__(self):
		#ch = self.ch
		#k = self.key
		#if ch == END: ch = r'\0'
		#if k: k = k[:-1]
		#if self.accepting: return "%s %s %s" % (ch, k, str(self.val))
		#return ch

	#def __repr__(self):
		#return str(self)

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