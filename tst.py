'''
TST - A Ternary Search Trie
Author: Tim Henderson
Contact: tim.tadh@hackthology.com or timothy.henderson@case.edu

This File: TST Implementation.

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
from os.path import sep as PATH_SEP
import sys, itertools

END = '\x00'
# Instructions
MATCH = 0
CHAR = 1
SPLIT = 2
JMP = 3

# Other constants
WILDCARD = 0x11FFFF
INF = 0x10FFFF

class TST(MutableMapping):
    '''
    A TST based symbol table:
    see Algorithms in (C|C++|Java) by Robert Sedgewick Ch. 15 Section 4

    NB:
        works on byte strings if you are using unicode strings encode to a byte
        string before passing it to this class
        ex:
        >>> x = u'\u03A0'  # capital greek letter Pi
        >>> x
        u'\u03a0'
        >>> x.encode('utf8')
        '\xce\xa0'
        >>> t[x.encode('utf8')] = 123
        >>> t
        {'\xce\xa0': 123}
        >>> t[x] = 123
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "tst.py", line 241, in __setitem__
            self.heads[ord(symbol[0])] = insert(self.heads[ord(symbol[0])], 1)
        IndexError: list index out of range

        a good python unicode resource can be found at:
        http://boodebr.org/main/python/all-about-python-and-unicode


    TST supports flexible matching using Java style glob patterns. However
    if you can override this behavior, and use a non-java glob interpretation.
    The Java vs. Non-Java glob are controlled by whether or not a path seperator
    has been set. By default it is set to os.path.sep and therefore uses Java
    style matching.

    Syntax to Regular Expression:
        if sep != None:
            **    --> .*
            **SEP --> .*
            *     --> [^SEP]*
            ?     --> [^SEP]
            c     --> c        ie. any other character is just that character

        if sep == None:
            ** --> .*
            *  --> .*
            ?  --> .
            c  -->             ie. any other character is just that character

    Examples:
        t = TST()
        Java Glob Matching:
            SEP = os.path.sep [eg. '/' on unix]
            **/*.jsp = .*[^/]*\.jsp
            /**/*.jsp = /.*[^/]*\.jsp
            binary/**/WEB-INF/*.jsp = binary/.*WEB-INF/[^/]*\.jsp
            ???/*.jsp = [^/][^/][^/]/[^/]*\.jsp

        t = TST(sep=None)
        Flexible Matching
            SEP = None
            **/*.jsp = .*/.*\.jsp
            /**/*.jsp = /.*/.*\.jsp
            binary/**/WEB-INF/*.jsp = binary/.*/WEB-INF/.*\.jsp
            ???/*.jsp = .../.*\.jsp

        you can set sep to any character ex:
        t = TST(sep=':')
        Custom SEP:
            SEP = ':'
            **/*.jsp = .*/[^:]*\.jsp
            /**/*.jsp = /.*/[^:]*\.jsp
            binary/**/WEB-INF/*.jsp = binary/.*/WEB-INF/[^:]*\.jsp
            ???/*.jsp = [^:][^:][^:]/[^:]*\.jsp
            */lib/*:/bin/*:** = [^:]*/lib/[^:]*:/bin/[^:]*:.*

    NB:
        Using this flexible matching only pays off verses naive use of a regex
        loop in the case of lots of strings. For hundreds of strings this table
        may be slower than a naive loop
        eg.
            set(f for f in files if re.match(p, f))

        however for lots of files the TST will be increasingly faster especially
        if the patterns prune at the root of the string.
        eg
            sometext*
        rather than
            *sometext

        The TST may perform worse for *sometext as it will have to iterate
        through every node in the trie. A better a approach than a TST in this
        case would be a Suffix Tree however Suffix Trees are very expensive to
        build. A TST can be the basis of a Suffix Tree. See Sedgewick for a
        discussion.

    '''

    def __init__(self, *args, **kwargs):
        '''
        @params sep = the seperator for Java style glob matching  pass None to
            disable see class documentations for more info.

        @params *args, **kwargs = passed to self.update see documentation for
            update for more info (basically a copy constructor) use like dict().

        eg:
            t = TST({'ab':12, 'cd':34}, sep=None)
            t = TST(((k, v) for k,v in {'ab':12, 'cd':34}.iteritems()), sep=None)
        '''
        self.heads = [None for x in xrange(256)]
        #self.root = None
        self.sep = kwargs.pop('sep', PATH_SEP)
        self.update(*args, **kwargs)

    def find(self, pattern):
        '''
        finds all key, value pairs matching the pattern (see class documentation
        for pattern syntax).

        @params pattern = the pattern to match
        @returns generator object of tuple(key, value) pairs

        ex:
            dict(t.find('**')) (all items in the table as a python dictionary)
        '''
        if '*' not in pattern and '?' not in pattern:
            try:
                yield pattern, self[pattern]
            except KeyError:
                return
            return
        pattern += END
        insts = list()
        p = None
        pp = None
        # the query compiler.
        for ch in pattern:
            if self.sep != None and pp == '*' and p == '*' and ch == self.sep:
                pass
            elif ch != '*' and ch != '?':
                insts.append((CHAR, ord(ch), ord(ch)))
            elif self.sep == None and ch == '?':
                insts.append((CHAR, WILDCARD, WILDCARD))
            elif ch == '?':
                i = len(insts)
                insts.append((SPLIT, len(insts)+1, len(insts)+3))
                insts.append((CHAR, 0, ord(self.sep)-1))
                insts.append((JMP, len(insts)+2, 0))
                insts.append((CHAR, ord(self.sep)+1, INF))
            elif self.sep == None and p == '*' and ch == '*':
                pass
            elif self.sep == None and ch == '*':
                i = len(insts)
                insts.append((SPLIT, len(insts)+1, len(insts)+3))
                insts.append((CHAR, WILDCARD, WILDCARD))
                insts.append((JMP, i, 0))
            elif ch == '*' and p == '*':
                insts = insts[:-6]
                i = len(insts)
                insts.append((SPLIT, len(insts)+1, len(insts)+3))
                insts.append((CHAR, WILDCARD, WILDCARD))
                insts.append((JMP, i, 0))
            else:
                i = len(insts)
                insts.append((SPLIT, len(insts)+1, len(insts)+6))
                insts.append((SPLIT, len(insts)+1, len(insts)+3))
                insts.append((CHAR, 0, ord(self.sep)-1))
                insts.append((JMP, len(insts)+2, 0))
                insts.append((CHAR, ord(self.sep)+1, INF))
                insts.append((JMP, i, 0))
            pp = p
            p = ch
        insts.append((MATCH, 0, 0))
        #print insts
        matches = [(x for x in [])]
        for i,h in enumerate(self.heads):
            if h == None: continue
            accept, clist = acceptone(insts, chr(i), 0)
            if accept:
                matches.append(hendersonvm(insts, h, 1, clist))
        for match in itertools.chain(*matches):
            yield match

    def keys(self):
        '''
        All the keys in the table in sorted in byte order.
        '''
        return [k for k in self]

    def iteritems(self):
        '''
        All the items [tuple(key, value) pairs] in the table sorted in byte
        order of their keys.
        '''
        q = deque()
        for h in self.heads:
            if h == None: continue
            q.appendleft(h)
        #q.append(self.root)
        j = 0
        while q:
            n = q.pop()
            if not n: continue
            if n.accepting:
                yield n.key[:-1], n.val
            q.append(n.r)
            q.append(n.m)
            q.append(n.l)

    def __len__(self):
        return len(self.keys())

    def __setitem__(self, symbol, obj):
        ## a modified version of the algorithm given by sedgewicks
        ## fixes some bugs
        symbol += END
        # node split
        def split(p, q, d):
            pd = p.key[d] # chr for p
            qd = q.key[d] # chr for q
            # get the next chr for q so we can update its ch field
            if d+1 < len(q.key): nqd = q.key[d+1]
            else: nqd = END
            t = node(qd) # the new node that will be the parent of both p, and q
            # update the char fields necessary, because if you don't they may be
            # wrong and cause problems in the regex matching.
            q.ch = nqd
            p.ch = pd
            if   pd <  qd: t.m = q; t.l = p
            elif pd == qd: t.m = split(p, q, d+1);
            elif pd >  qd: t.m = q; t.r = p
            return t
        # recursive insert
        def insert(n, d):
            if n == None:
                # if the node is None we found the spot make a new node and
                # return it
                if d == len(symbol): ch = '\0'
                else: ch = symbol[d]
                return node(ch, key=symbol, val=obj)
            if not n.internal():
                # if it a leaf node we either have found the symbol or we need
                # to split a node.
                if len(n.key) == len(symbol) and n.key == symbol:
                    # found the symbol
                    n.val = obj
                    return n
                else:
                    # split the node
                    ch = symbol[d]
                    return split(node(ch, key=symbol, val=obj), n, d)
            # it is an internal node
            ch = symbol[d]
            if   ch <  n.ch: n.l = insert(n.l, d)
            elif ch == n.ch: n.m = insert(n.m, d+1) # matches current chr so d+1
            elif ch >  n.ch: n.r = insert(n.r, d)
            return n
        # start at the "head" of the trie rooted at the first chacter of the
        # symbol.
        self.heads[ord(symbol[0])] = insert(self.heads[ord(symbol[0])], 1)
        #self.root = insert(self.root, 0)

    def __getitem__(self, symbol):
        ## an iterative version of the algorithm given by sedgewick
        ## I made it iterative because it is faster that way.
        symbol += END
        next = (self.heads[ord(symbol[0])], 1)
        #next = (self.root, 0)
        while next:
            n, d = next
            if n == None:
                raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]
            if n.internal():
                ch = symbol[d]
                if   ch <  n.ch: next = (n.l, d);   continue
                elif ch == n.ch: next = (n.m, d+1); continue
                elif ch >  n.ch: next = (n.r, d);   continue
            elif n.key == symbol:
                return n.val
            raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]
        #should never reach ...
        raise KeyError, "Symbol '%s' is not in table." % symbol[:-1]

    def __delitem__(self, symbol):
        ## not given by sedgewick inferred by Tim Henderson
        ## the algorithm is very similar to the get algorithm.
        symbol += END
        def check(n):
            # ensure the node is valid.
            if n == None: return None
            if not n.internal() and n.key == None:
                return None
            return n
        def remove(n, d):
            if n == None:
                raise KeyError, "Symbol '%s' is not in table." % symbol
            if n.internal():
                ch = symbol[d]
                if   ch <  n.ch: n.l = check(remove(n.l, d))
                elif ch == n.ch: n.m = check(remove(n.m, d+1))
                elif ch >  n.ch: n.r = check(remove(n.r, d))
            else:
                if n.key == symbol:
                    return None
                else:
                    raise KeyError, "Symbol '%s' is not in table." % symbol
            return check(n)
        self.heads[ord(symbol[0])] = remove(self.heads[ord(symbol[0])], 1)
        #self.root = remove(self.root, 0)

    def __iter__(self):
        '''
        returns the keys in sorted byte order.
        '''
        q = deque()
        for h in self.heads:
            if h == None: continue
            q.appendleft(h)
        #q.append(self.root)
        j = 0
        while q:
            n = q.pop()
            if not n: continue
            if n.accepting:
                yield n.key[:-1]
            q.append(n.r)
            q.append(n.m)
            q.append(n.l)

    def __contains__(self, pattern):
        '''
        checks to see if the pattern is in the dictionary. first checks to see
        if it is a symbol name, if not checks if it the pattern matches anything
        if not returns false.
        '''
        try:
            x = self[pattern]
        except KeyError:
            try: return bool(tuple(self.find(pattern)))
            except KeyError: return False
            return False
        return True

    def __getstate__(self):
        '''Used by pickle to save the state of this table.'''
        return {'sep':self.sep, 'dict':dict(self)}

    def __setstate__(self, val):
        '''Used by pickle to restore the state of this table.'''
        self.__init__(val['dict'], sep=val['sep'])

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return str(self)

class node(object):
    '''A node of a TST'''
    __slots__ = ['ch', 'key', 'val', 'l', 'm', 'r', 'accepting']

    def __init__(self, ch, key=None, val=None, m=None):
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
        ch = self.ch
        k = self.key
        if ch == END: ch = r'\0'
        if k: k = k[:-1]
        if self.accepting: return "%s %s %s" % (ch, k, str(self.val))
        return ch

    def __getstate__(self):
        d = dict((attr, getattr(self, attr)) for attr in self.__slots__)
        return d

    def __setstate__(self, s):
        for k,v in s.iteritems():
            setattr(self, k, v)

    def __repr__(self):
        return str(self)

def acceptone(program, text, pc):
    '''
    checks one character and sees if it matches. if it does returns True and
    a the next queue of program counters [pc] to excute. If it doesn't match
    returns False and None. see thompsonvm citation for a very through
    explanation of the theory behind this algorithm.
    '''
    tc = 0
    cqueue, nqueue = deque(), deque()
    cqueue.append(pc)
    while cqueue:
        pc = cqueue.pop()
        inst = program[pc]
        if inst[0] == JMP:
            cqueue.append(inst[1])
        if inst[0] == SPLIT:
            cqueue.append(inst[1])
            cqueue.append(inst[2])
        if inst[0] == CHAR:
            if tc >= len(text): continue
            x, y = inst[1], inst[2]; c = ord(text[tc])
            if (y and x <= c <= y) or c == x or x == WILDCARD:
                nqueue.append(pc+1)
        if inst[0] == MATCH:
            if tc == len(text):
                return True, [0]
    if nqueue:
        return True, nqueue
    return False, None

def thompsonvm(program, text, tc, pc):
    '''
    A version of the Thompson Virtual Machine as defined by Russ Cox in:
        http://swtch.com/~rsc/regexp/regexp2.html
        this article provides a very through explanation of regular expression
        NFA matching as implemented in this module.
    This version modifies the algorithm to start at a later position in the
    string, and regular expression. Used to match the end of the string stored
    in the leaves of the TST.
    '''
    cqueue, nqueue = deque(), deque()
    cqueue.append(pc)
    while tc <= len(text):
        while cqueue:
            pc = cqueue.pop()
            inst = program[pc]
            if inst[0] == JMP:
                cqueue.append(inst[1])
            if inst[0] == SPLIT:
                cqueue.append(inst[1])
                cqueue.append(inst[2])
            if inst[0] == CHAR:
                if tc >= len(text): continue
                x, y = inst[1], inst[2]; c = ord(text[tc])
                if (y and x <= c <= y) or c == x or x == WILDCARD:
                    nqueue.append(pc+1)
            if inst[0] == MATCH:
                if tc == len(text):
                    return True
        cqueue = nqueue
        nqueue = deque()
        tc += 1
    return False

def hendersonvm(program, node, d, clist):
    '''
    A Regex Virtual Machine for matching regular expressions stored in a trie.
    Originally implemented for a N-Way trie, this version has been modified for
    use on a TST. For more details contact Tim Henderson at
        tim.tadh@gmail.com or timothy.henderson@case.edu

    Note this algorithm starts at text position d and with thread list clist.
    '''
    #print clist, d
    def addthread(l, thread):
        if thread not in l: l.appendleft(thread)

    def addnode(d, t, node):
        if not d.has_key(t):
            d[t] = set()
        if node not in d[t]: d[t].add(node)

    def dupnodes(d, t, t2):
        #print d
        if not d.has_key(t2):
            d[t2] = set()
        d[t2] |= d[t]

    if not program: return
    if not node: return

    nlist = deque()
    cnodes = dict()
    nnodes = dict()

    for pc in clist:
        addnode(cnodes, pc, (node,d))

    while clist:
        while clist:
            pc = clist.popleft()
            inst = program[pc]
            if inst[0] == JMP:
                addthread(clist, inst[1])
                dupnodes(cnodes, pc, inst[1])
            elif inst[0] == SPLIT:
                addthread(clist, inst[2])
                addthread(clist, inst[1])
                dupnodes(cnodes, pc, inst[1])
                dupnodes(cnodes, pc, inst[2])
            elif cnodes.has_key(pc):
                for n, d in cnodes[pc]:
                    if n == None: continue
                    if inst[0] == CHAR:
                        x, y = inst[1], inst[2]; c = ord(n.ch)
                        if (x < c or x == WILDCARD) and n.l != None:
                            addthread(nlist, pc)
                            addnode(nnodes, pc, (n.l, d))
                        if x == c or y == c or (x < c < y) or x == WILDCARD:
                            if not n.internal():
                                if thompsonvm(program, n.key, d+1, pc+1):
                                    #print n.key, inst, pc, program
                                    yield n.key[:-1], n.val
                            elif n.m != None:
                                addthread(nlist, pc+1)
                                addnode(nnodes, pc+1, (n.m, d+1))
                        if (y > c or x == WILDCARD) and n.r != None:
                            addthread(nlist, pc)
                            addnode(nnodes, pc, (n.r, d))
                    elif inst[0] == MATCH:
                        if d == len(n.key):
                            yield n.key[:-1], n.val
        cnodes = nnodes
        nnodes = dict()
        clist = nlist
        nlist = deque()
    #print
    #print

