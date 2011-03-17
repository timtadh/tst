TST - Ternary Search Trie
=========================

A fast implementation of TST in Python. Supports flexible java glob style
maching on the trie. The interface is the standard dictionary interface, so you
can use these wherever you are using dictionaries. These symbol tables are as
fast (or a little faster) as Python dict's on insert and little slower (1 order
of magnatude) on read.

##Usage

    >>> from tst.tst import TST
    >>>
    >>> t = TST()
    >>> t['asdf'] = object()
    >>> t
    {'asdf': <object object at 0x7f659d869090>}
    >>>
    >>> d = {"x": 12, "y" :324, "asdf": 23423}
    >>> t.update(d)
    >>> t
    {'y': 324, 'x': 12, 'asdf': 23423}
    >>> dict(t)
    {'y': 324, 'x': 12, 'asdf': 23423}
    >>> type(t)
    <class 'tst.TST'>
    >>> type(dict(t))
    <type 'dict'>

It supports a find interface but it is currently too slow to use. This is the experimental
section.

    >>> t.find('a*')
    <generator object find at 0x7f659d897910>
    >>> dict(t.find('a*'))
    {'asdf': 23423}
    >>>

