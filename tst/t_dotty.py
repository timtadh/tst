
#TST - A Ternary Search Trie
#Author: Tim Henderson
#Contact: tim.tadh@hackthology.com or timothy.henderson@case.edu

#This File: Dotty Test

#Copyright (c) 2010, Tim Henderson
#All rights reserved.


from tst import TST

tst = TST()
tst['abc'] = 1
tst['abcde'] = 2
tst['abe'] = 3
tst['abefg'] = 4
tst['abce'] = 5
tst['aba'] = 6
tst['boy'] = 7
tst['bad'] = 8
tst['buster'] = 9
tst['cactus'] = 10

print tst.dotty()
