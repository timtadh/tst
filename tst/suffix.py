'''
TST - A Ternary Search Trie
Author: Tim Henderson
Contact: tim.tadh@hackthology.com or timothy.henderson@case.edu

This File: Suffix Tree Implementation.

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

from collections import deque, MutableMapping

from tst import TST

START = '\x01'

class SuffixTree(MutableMapping):
    
    def __init__(self, *args, **kwargs):
        '''
        @params *args, **kwargs = passed to self.update see documentation for
            update for more info (basically a copy constructor) use like dict().

        eg:
            t = TST({'ab':12, 'cd':34}, sep=None)
            t = TST(((k, v) for k,v in {'ab':12, 'cd':34}.iteritems()), sep=None)
        '''
        self.tst = TST()
        self.update(*args, **kwargs)
    
    def find(self, substr): 
        if not substr:
            for k,v in self.iteritems():
                yield k,v
        root = None
        next = (self.tst.heads[ord(substr[0])], 1)
        while next:
            n, d = next
            if n == None:
              return
            if n.internal():
                if d == len(substr):
                    root = n
                    break;
                ch = substr[d]
                if   ch <  n.ch: next = (n.l, d);   continue
                elif ch == n.ch: next = (n.m, d+1); continue
                elif ch >  n.ch: next = (n.r, d);   continue
            elif n.key[:len(substr)] == substr:
                root = n
                break;
            return
        # now expand root
        q = deque()
        found = set()
        q.appendleft(root)
        while q:
            n = q.pop()
            if not n: continue
            if n.accepting:
                found |= n.val
            q.append(n.r)
            q.append(n.m)
            q.append(n.l)
        for k in found:
            yield k[1:], self.tst.get(k)

    def keys(self):
        return [k for k, v in self.iteritems()]
    
    def iteritems(self):
        q = deque()
        h = self.tst.heads[ord(START)]
        if h == None: return
        q.appendleft(h)
        while q:
            n = q.pop()
            if not n: continue
            if n.accepting:
                yield n.key[1:-1], n.val
            q.append(n.r)
            q.append(n.m)
            q.append(n.l)
    
    def __len__(self):
        return len(self.iteritems())

    def __setitem__(self, key, value):
        fullkey = START + key
        self.tst[fullkey] = value
        for i in xrange(0, len(key)):
            curkey = key[i:]
            keys = self.tst.get(curkey, set())
            keys.add(fullkey)
            self.tst[curkey] = keys

    def __getitem__(self, key):
        fullkey = START + key
        return self.tst[fullkey]

    def __delitem__(self, key):
        raise RuntimeError, 'Removing from SuffixTree is not allowed'

    def __iter__(self):
        for k,v in self.iteritems():
            yield k
    
    def __contains__(self, pattern):
        try:
            x = self[pattern]
        except KeyError:
            #try: return bool(tuple(self.find(pattern)))
            #except KeyError: return False
            return False
        return True

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return str(self)

