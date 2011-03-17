'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''
import unittest, os, sys, base64, itertools, random, time
from tst import TST

#TST = dict

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

	def test_simple(self):
		t = TST()
		t['ba'] = 'ba'

	def insert_tester1(self, t, tup, s):
		l = list()
		for k, v in tup:
			t[k] = v
			l.append((k,v))
			for k,v in l:
				try: tv = t[k]
				except KeyError:
					print t
					#self.fail('key %s should be in table, %s' % (k, str(k in s)))
					raise
				if tv != v:
					print t
				self.assertEquals(tv, v, msg='%s, %s %s' % (k, str(v), str(tv)))
		return True


	def insert_tester2(self, t, tup, s):
		for k, v in tup:
			t[k] = v
		for k, v in tup:
			try: t[k] = v
			except:
				print t
				print k, v, t[k]
				raise
		for k, v in tup:
			self.assertEquals(t[k], v)
		l = list(tup)
		l.reverse()
		for k, v in l:
			try: tv = t[k]
			except KeyError:
				print t
				self.fail('key %s should be in table, %s' % (k, str(k in s)))
			if tv != v:
				print t
				print 'arg'
			self.assertEquals(tv, v, msg='%s, %s %s' % (k, str(v), str(tv)))
		return True


	def insert_tester3(self, t, l1, l2):
		for k, v in l1:
			t[k] = v
		for k, v in l2:
			try: t[k] = v
			except:
				print t
				print k, v, t[k]
				raise
		for k, v in l2:
			self.assertEquals(t[k], v)
		return True

	def remove_tester(self, t, l):
		for k, v in l:
			t[k] = v
		l2 = list()
		for x in xrange(len(l)/5):
			c = random.choice(l)
			del t[c[0]]
			l.remove(c)
			l2.append(c)
		for k, v in l:
			self.assertEquals(t[k], v)
		for k, v in l2:
			self.assertRaises(KeyError, t.__getitem__, k)
		for k, v in l2:
			try: t[k] = v
			except:
				print t
				print k, v
				raise
		l += l2
		for k, v in l:
			self.assertEquals(t[k], v)
		l2 = list()
		for x in xrange(len(l)/2):
			c = random.choice(l)
			del t[c[0]]
			l.remove(c)
			l2.append(c)
		for k, v in l:
			self.assertEquals(t[k], v)
		for k, v in l2:
			self.assertRaises(KeyError, t.__getitem__, k)
		for k, v in l2:
			try: t[k] = v
			except:
				print t
				print k, v
				raise
		l += l2
		for k, v in l:
			self.assertEquals(t[k], v)
		l2 = list(l)
		#print '{\n', t, '\n}'
		for x in xrange(len(l)):
			c = random.choice(l2)
			del t[c[0]]
			l2.remove(c)
		for k, v in l:
			self.assertRaises(KeyError, t.__getitem__, k)
		#print '{\n', t, '\n}'

	def test_insert(self):
		t = TST()
		self.insert_tester1(t, (('b', 2), ('a', 1), ('d', 4), ('daf', 5), ('db', 6), ('dac', 3)), list())

	def test_random(self):
		for j in xrange(100):
			s = set()
			l1 = list()
			for x in xrange(100):
				k = base64.b64encode(os.urandom(x%10 + 1)).rstrip('=')
				if k in s: continue
				l1.append((k, x))
				s.add(k)
			l2 = [(s,i+15) for s,i in l1]
			t = TST()
			if not self.insert_tester3(t, l1, l2): break

	def test_complete(self):
		random.seed(os.urandom(300))
		s = strings('abcde')
		l1 = [(s,i) for i,s in enumerate(s)]
		random.shuffle(l1)
		l2 = [(s,i+15) for s,i in l1]
		t = TST()
		s = time.time()
		self.insert_tester3(t, l1, l2)
		e = time.time()
		sys.stderr.write('complete: '+str(round(e-s, 5))+'\n')
		#print t

	def test_time(self):
		size = 10000
		i =    1000
		#self.itertest(size, i)
		#s = set()
		l = list()
		for x in xrange(i):
			k = ''.join(chr(ord(c)%127) for c in os.urandom(size).replace('\0', ''))
			#if k in s: continue
			l.append(k)
			#s.add(k)
		strs = l#[(''.join(strings(s)), i) for i,s in enumerate(itertools.permutations('abcdef'))]
		#strs =
		for clazz in [dict, TST]:
			sys.stderr.write(str(clazz)+'\n')
			t = clazz()
			s = time.time()
			for x in strs:
				t[x] = 1
			e = time.time()
			sys.stderr.write(str(round(e-s, 5))+'\n')
			#del t
			s = time.time()
			for x in strs:
				assert t[x] == 1
			e = time.time()
			sys.stderr.write(str(round(e-s, 5))+'\n\n')
		#print t


if __name__ == '__main__':
	unittest.main()
