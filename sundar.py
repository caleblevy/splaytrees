"""Implementation of Sundar's Ackermann-like functions defined in 
	On the deque conjecture for the Splay Algorithm, 1992.
"""


def K(i, j):
	"""K(i, j) grows as A(i//2, j)"""
	if i == 1:
		return 8*j
	elif j == 2:
		return 2**(4*j)
	else:
		if j == 1:
			return i*K(i-2, i//2)
		else:
			return K(i, j-1)*K(i-2, K(i, j-1)/4)/2



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

print(A(2, 4))