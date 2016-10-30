"""Implementation of Sundar's Ackermann-like functions defined in 
	On the deque conjecture for the Splay Algorithm, 1992.
"""

from math import log as log


def lg(n):
	return log(n)/log(2)


def K(i, j):
	"""K(i, j) grows as A(i//2, j)"""
	if i == 1:
		return 8*j
	elif i == 2:
		return 2**(4*j)
	else:
		if j == 1:
			return i*K(i-2, i//2)
		else:
			return K(i, j-1)*K(i-2, K(i, j-1)//4)//2



for i in range(1, 5):
	print K(3, i)


def A(i, j):
	"""Definition of two parameter Ackermann Function"""
	if i == 0:
		return 2*j
	elif i == 1:
		return 2**j
	else:
		if j == 1:
			return A(i-1, 2)
		else:
			return A(i-1, A(i, j-1))


def a_hat(i, n):
	"""Inverse Ackermann for each i."""
	k = 1
	while A(i, k) < n:
		k += 1
	return k


def a_bar(n):
	"""Main, slow growing inverse Ackermann"""
	k = 1
	while A(k, 1) < n:
		k += 1
	return k


def a(m, n):
	"""The mysterious two-param Ackermann"""
	k = 1
	while A(k, m//n) <= lg(n):
		k += 1
	return k


