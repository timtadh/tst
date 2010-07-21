'''
Cactus - The Python Task Runner
Author: Tim Henderson
Contact: tim.tadh@hackthology.com
Copyright (c) 2010 All Rights Reserved.
Licensed under a BSD style license see the LICENSE file.
'''
import unittest
from table import match_globs, SymbolTable
class TestMatchGlobs(unittest.TestCase):

	def test_match(self):
		tests = [('ab*cd', 'abcd', True), ('ab*cd', 'abedcd', True),
				('ab*cd', 'abed*cd', True),
				('ab*cd', 'ab*edcd', True),
				('ab*cd', 'a*edcd', True),
				('ab*cd', 'acd', False),
				('abc*cd', 'ad', False),
				('*cd', 'abcd', True),
				('abcd', 'ab*', True),
				('ab*', '*', True),
				('ab*', '*cd', True),
				('abc*cd*', 'a*xy*', True),
				('ab*ac*c', '*ab*cd', False)]
		for test in tests:
			if test[0]: m = 'matched'
			else: m = 'not matched'
			self.assert_(match_globs(test[0], test[1]) == test[2], '"%s" and "%s" should have %s' % (test[0], test[1], m))

class TestTable(unittest.TestCase):

	def test_init(self):
		t = SymbolTable()

	def insert(self,t):
		t['a'] = 1
		t['aa'] = 2
		t['aaa'] = 3

	def paths(self, t):
		t['binary/WEB-INF/tiles/footer/footer.jsp'] = 1
		t['binary/WEB-INF/tiles/form/addAccountForm.jsp'] = 2
		t['binary/WEB-INF/tiles/menu/menu_empty.jsp'] = 3
		t['binary/addAccount.jsp'] = 4
		t['source/dist/WEB-INF/tiles/menu/menu_empty.jsp'] = 5
		t['source/dist/addClient.jsp'] = 6

	def test_insert(self):
		t = SymbolTable()
		self.insert(t)
		self.assertEquals(dict(t), {'a':1,'aa':2,'aaa':3})
		self.assertEquals(dict(t.find('*')), {'a':1,'aa':2,'aaa':3})

	def test_remove(self):
		t = SymbolTable()
		self.insert(t)
		del t['aaa']
		self.assertEquals(dict(t), {'a':1,'aa':2})
		self.assertEquals(dict(t.find('*')), {'a':1,'aa':2})
		del t['aa']
		self.assertEquals(dict(t), {'a':1,})
		self.assertEquals(dict(t.find('*')), {'a':1,})
		del t['a']
		self.assertEquals(dict(t), {})
		self.assertEquals(dict(t.find('*')), {})
		self.insert(t)
		self.assertEquals(dict(t), {'a':1,'aa':2,'aaa':3})
		self.assertEquals(dict(t.find('*')), {'a':1,'aa':2,'aaa':3})

	def test_find(self):
		t = SymbolTable()
		self.paths(t)
		self.assertEquals(dict(t),
			{
				'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
				'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
				'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
				'binary/addAccount.jsp' : 4,
				'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
				'source/dist/addClient.jsp' : 6,
			})
		self.assertEquals(dict(t.find('*')), {})
		self.assertEquals(dict(t.find('**')),
			{
				'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
				'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
				'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
				'binary/addAccount.jsp' : 4,
				'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
				'source/dist/addClient.jsp' : 6,
			})
		self.assertEquals(dict(t.find('**.jsp')),
			{
				'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
				'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
				'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
				'binary/addAccount.jsp' : 4,
				'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
				'source/dist/addClient.jsp' : 6,
			})
		self.assertEquals(dict(t.find('binary/**.jsp')),
			{
				'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
				'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
				'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
				'binary/addAccount.jsp' : 4,
			})
		self.assertEquals(dict(t.find('binary/*.jsp')),
			{
				'binary/addAccount.jsp' : 4,
			})
		self.assertEquals(dict(t.find('*/*/*.jsp')),
			{
				'source/dist/addClient.jsp' : 6,
			})

	def test_find_nosep(self):
		t = SymbolTable(sep=None)
		self.paths(t)
		self.assertEquals(dict(t),
			{
				'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
				'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
				'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
				'binary/addAccount.jsp' : 4,
				'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
				'source/dist/addClient.jsp' : 6,
			})
		self.assertEquals(dict(t.find('*')),
			{
				'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
				'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
				'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
				'binary/addAccount.jsp' : 4,
				'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
				'source/dist/addClient.jsp' : 6,
			})
		self.assertEquals(dict(t.find('**')),
			{
				'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
				'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
				'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
				'binary/addAccount.jsp' : 4,
				'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
				'source/dist/addClient.jsp' : 6,
			})

if __name__ == '__main__':
	unittest.main()
