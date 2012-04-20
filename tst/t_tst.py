'''
TST - A Ternary Search Trie
Author: Tim Henderson
Contact: tim.tadh@hackthology.com or timothy.henderson@case.edu

This File: Tests for the TST.

Copyright (c) 2010, Tim Henderson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
    * Neither the name TST nor the names of its contributors may
    be used to endorse or promote products derived from this software without
    specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import unittest, os, sys, base64, itertools, random, time
#from tst2.tst import TST as TST2
from tst import TST

def strings(s='abcde'):
    out = list()
    for i in xrange(len(s)):
        l = list()
        for j in xrange(i+1):
            l.append(s)
        out += list(''.join(x) for x in itertools.product(*l))
    return out

class TestTST(unittest.TestCase):

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
        sys.stderr.write('\ncomplete: '+str(round(e-s, 5))+'\n')
        #print t

    def test_remove(self):
        random.seed(os.urandom(300))
        s = strings('abcde')
        l1 = [(s,i) for i,s in enumerate(s)]
        random.shuffle(l1)
        s = time.time()
        for x in xrange(1):
            t = TST()
            self.remove_tester(t, l1)
        e = time.time()
        sys.stderr.write('\nremove: '+str(round(e-s, 5))+'\n')
            #print t

    def test_keys(self):
        s = set()
        l1 = list()
        t = TST()
        for x in xrange(100):
            k = base64.b64encode(os.urandom(x%10 + 1)).rstrip('=')
            if k in s: continue
            l1.append(k)
            t[k] = x
            s.add(k)
        l1.sort()
        self.assertEquals(l1, t.keys())

    def test_iteritems(self):
        s = set()
        l1 = list()
        t = TST()
        for x in xrange(100):
            k = base64.b64encode(os.urandom(x%10 + 1)).rstrip('=')
            if k in s: continue
            l1.append((k, x))
            t[k] = x
            s.add(k)
        l1.sort()
        self.assertEquals(l1, list(t.iteritems()))

    def test__iter__(self):
        s = set()
        l1 = list()
        t = TST()
        for x in xrange(100):
            k = base64.b64encode(os.urandom(x%10 + 1)).rstrip('=')
            if k in s: continue
            l1.append(k)
            t[k] = x
            s.add(k)
        l1.sort()
        self.assertEquals(l1, list(t))

    def test__contains__(self):
        s = set()
        l1 = list()
        t = TST()
        for x in xrange(100):
            k = base64.b64encode(os.urandom(x%10 + 1)).rstrip('=')
            if k in s: continue
            l1.append(k)
            t[k] = x
            s.add(k)
        l1.sort()
        for x in l1:
            assert x in t
            assert 'hello my darlin\'' not in t

    def test_find_simple(self):
        s = set()
        l1 = list()
        t = TST()
        for x in xrange(100):
            k = base64.b64encode(os.urandom(x%10 + 1)).rstrip('=')
            if k in s: continue
            l1.append(k)
            t[k] = x
            s.add(k)
        l1.sort()
        for x in l1:
            assert bool(tuple(t.find(x)))

    def itertest(self, size, i):
        sys.stderr.write('\n')
        string = os.urandom(size).replace('\0', '')
        s = time.time()
        hash(string)
        e = time.time()
        sys.stderr.write(str(round(e-s, 5)) + ' ' +str(round(e-s, 5)*i)+'\n')
        string2 = str(string)
        s = time.time()
        hash(string)
        e = time.time()
        sys.stderr.write(str(round(e-s, 7))+'\n')
        s = time.time()
        for x in string: pass
        e = time.time()
        sys.stderr.write(str(round(e-s, 5)*i)+'\n')
        s = time.time()
        for x in string: x
        e = time.time()
        sys.stderr.write(str(round(e-s, 5)*i)+'\n')
        s = time.time()
        print string == string
        e = time.time()
        sys.stderr.write(str(round(e-s, 5)*i)+'\n\n')

    def test_time(self):
        sys.stderr.write('\n')
        size = 10000
        i =    100
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
            sys.stderr.write('insert: '+str(round(e-s, 7))+'\n')
            #del t
            s = time.time()
            for x in strs:
                assert t[x] == 1
            e = time.time()
            sys.stderr.write('read: '+str(round(e-s, 7))+'\n\n')
        #print t

    def test_match(self):
        t = TST(sep=None)
        t['what'] = 1
        t['where'] = 1
        t['when'] = 1
        t['widget'] = 1
        t['wizard'] = 1
        t['wow'] = 1
        t['wowo'] = 1
        self.assertEquals(dict(t.find('w*e*')), {'where':1,'when':1,'widget':1})
        self.assertEquals(dict(t.find('*e')), {'where':1})
        self.assertEquals(dict(t.find('*et')), {'widget':1})
        self.assertEquals(dict(t.find('wo*')), {'wow':1, 'wowo':1})
        self.assertEquals(dict(t.find('*a*')), {'what':1, 'wizard':1})
        self.assertEquals(dict(t.find('*za*')), {'wizard':1})
        for k in t.keys():
            self.assertEquals(dict(t.find(k)), {k:1})
        self.assertEquals(dict(t.find('*dg*')), {'widget':1})
        self.assertEquals(dict(t.find('*he*')), {'when':1, 'where':1})
        #print t

    #######################################d#
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

    def test_insert_(self):
        t = TST()
        self.insert(t)
        self.assertEquals(dict(t), {'a':1,'aa':2,'aaa':3})
        self.assertEquals(dict(t.find('*')), {'a':1,'aa':2,'aaa':3})

    def test_remove_(self):
        t = TST()
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

    def test_find_(self):
        t = TST()
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
        t = TST(sep=None)
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

    def test__iter___(self):
        t = TST()
        self.paths(t)
        l1 = [x for x in t]
        l2 = dict(t).keys()
        l2.sort()
        self.assertEquals(l1, l2)


    def test__contains___(self):
        t = TST()
        self.paths(t)
        self.assertTrue('binary/**.jsp' in t)
        self.assertFalse('binary/WEB-INF/*.jsp' in t)
        self.assertFalse('source/*.jsp' in t)
        self.assertTrue('**' in t)
        self.assertFalse('*' in t)
        self.assertTrue('binary/WEB-INF/tiles/footer/footer.jsp' in t)
        for x in dict(t):
            self.assertTrue(x in t)

    def test__contains___nosep(self):
        t = TST(sep=None)
        self.paths(t)
        self.assertTrue('binary/**.jsp' in t)
        self.assertTrue('binary/WEB-INF/*.jsp' in t)
        self.assertTrue('source/*.jsp' in t)
        self.assertTrue('**' in t)
        self.assertTrue('*' in t)
        self.assertTrue('binary/WEB-INF/tiles/footer/footer.jsp' in t)
        for x in dict(t):
            self.assertTrue(x in t)
        self.assertFalse('*x*' in t)


    def test_q(self):
        t = TST()
        t['a'] =1
        t['b'] =1
        t['c'] =1
        self.assertTrue(set(dict(t.find('?')).keys()), set(t.keys()))
        t = TST()
        t['/a'] = 1
        t['/b'] = 1
        t['/c'] = 1
        self.assertEquals(set(dict(t.find('??')).keys()), set())
        self.assertEquals(set(dict(t.find('/?')).keys()), set(t.keys()))
        t = TST()
        t['dog'] = 1
        t['dig'] = 1
        t['dug'] = 1
        self.assertEquals(set(dict(t.find('d?g')).keys()),set(t.keys()))

    def test_q_nosep(self):
        t = TST(sep=None)
        t['a'] =1
        t['b'] =1
        t['c'] =1
        self.assertTrue(set(dict(t.find('?')).keys()), set(t.keys()))
        t = TST(sep=None)
        t['/a'] = 1
        t['/b'] = 1
        t['/c'] = 1
        self.assertEquals(set(dict(t.find('??')).keys()), set(t.keys()))
        self.assertEquals(set(dict(t.find('/?')).keys()), set(t.keys()))

    def test_find_q(self):
        t = TST()
        self.paths(t)
        self.assertEquals(dict(t.find('??????/**/*.jsp')),
            {
                'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
                'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
                'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
                'binary/addAccount.jsp' : 4,
                'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
                'source/dist/addClient.jsp' : 6,
            })

    def test_find_r(self):
        t = TST()
        self.paths(t)
        self.assertEquals(dict(t.find('*/*.jsp')),
            {
                'binary/addAccount.jsp' : 4
            })

    def test_copyctor(self):
        d = {
                'binary/WEB-INF/tiles/footer/footer.jsp' : 1,
                'binary/WEB-INF/tiles/form/addAccountForm.jsp' : 2,
                'binary/WEB-INF/tiles/menu/menu_empty.jsp' : 3,
                'binary/addAccount.jsp' : 4,
                'source/dist/WEB-INF/tiles/menu/menu_empty.jsp' : 5,
                'source/dist/addClient.jsp' : 6,
            }
        self.assertEquals(dict(TST(d)), d)
        self.assertEquals(dict(TST(TST(d))), d)
        self.assertEquals(dict(TST((k,v) for k,v in d.iteritems())), d)


if __name__ == '__main__':
    unittest.main()
