'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''
import unittest, os, base64, itertools, random
from tst import TST

def strings(s='abcde'):
	out = list()
	for i in xrange(len(s)):
		l = list()
		for j in xrange(i+1):
			l.append(s)
		out += list(''.join(x) for x in itertools.product(*l))
	return out

class TestTable(unittest.TestCase):

	def test_init(self):
		t = TST()

	def insert_tester1(self, t, tup, s):
		l = list()
		for k, v in tup:
			t[k] = v
			l.append((k,v))
			for k,v in l:
				try: tv = t[k]
				except KeyError:
					print t
					self.fail('key %s should be in table, %s' % (k, str(k in s)))
				if tv != v:
					print t
				self.assertEquals(tv, v, msg='%s, %s %s' % (k, str(v), str(tv)))
		#for k, v in tup:
			#t[k] = v
		#for k, v in tup:
			#self.assertEquals(t[k], v)
		#l = list(tup)
		#l.reverse()
		#for k, v in l:
			#try: tv = t[k]
			#except KeyError:
				#print t
				#self.fail('key %s should be in table, %s' % (k, str(k in s)))
			#if tv != v:
				#print t
				#print 'arg'
			#self.assertEquals(tv, v, msg='%s, %s %s' % (k, str(v), str(tv)))
		return True


	def insert_tester2(self, t, tup, s):
		for k, v in tup:
			t[k] = v
		#for k, v in tup:
			#t[k] = v
		#for k, v in tup:
			#self.assertEquals(t[k], v)
		#l = list(tup)
		#l.reverse()
		for k, v in tup:
			try: tv = t[k]
			except KeyError:
				print t
				self.fail('key %s should be in table, %s' % (k, str(k in s)))
			if tv != v:
				print t
				print 'arg'
			self.assertEquals(tv, v, msg='%s, %s %s' % (k, str(v), str(tv)))
		return True

	#def test_insert(self):
		#t = TST()
		#self.insert_tester(t, (('b', 2), ('a', 1), ('d', 4), ('daf', 5), ('db', 6), ('dac', 3)))

	#def test_random(self):
		#for j in xrange(500):
			#s = set()
			#l = list()
			#for x in xrange(150):
				#k = base64.b64encode(os.urandom(x%10 + 1)).rstrip('=')
				#if k in s: continue
				#l.append((k, x))
				#s.add(k)
			#t = TST()
			#if not self.insert_tester1(t, l, s): break

	def test_complete(self):
		#random.seed(os.urandom(300))
		s = strings('abc')
		l = [(s,i) for i,s in enumerate(s)]
		random.shuffle(l)
		t = TST()
		self.insert_tester1(t, l, set(s))
		#print t


if __name__ == '__main__':
	unittest.main()
