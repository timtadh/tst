build:
	cython tst.pyx
	gcc -O3 -c -fPIC -I/usr/include/python2.6/ tst.c
	gcc -shared tst.o -o tst.so

