'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''
import unittest
from tst import TST

class TestTable(unittest.TestCase):

	def test_init(self):
		t = TST()

	def insert_tester(self, t, tup):
		for k, v in tup:
			t[k] = v
		for k, v in tup:
			t[k] = v
		for k, v in tup:
			self.assertEquals(t[k], v)
		l = list(tup)
		l.reverse()
		for k, v in l:
			self.assertEquals(t[k], v)

	def test_insert(self):
		t = TST()
		self.insert_tester(t, (('b', 2), ('a', 1), ('d', 4), ('daf', 5), ('db', 6), ('dac', 3)))


if __name__ == '__main__':
	unittest.main()
