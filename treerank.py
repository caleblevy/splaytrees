"""Functions based on "A numbering system for binary trees," Gary Knott,
1977."""


import unittest
from random import randrange


# For fun
four_node_trees = [
    (4, 3, 2, 1), (1, 2, 3, 4),  # Il, Ir
    (3, 2, 1, 4), (2, 1, 3, 4),  # Vl, Vr
    (4, 1, 3, 2), (1, 4, 2, 3),  # Zl, Zr
    (4, 1, 2, 3), (1, 4, 3, 2),  # Pl, Pr
    (3, 1, 2, 4), (2, 1, 4, 3),  # Ul, Ur
    (4, 3, 1, 2), (1, 2, 4, 3),  # Ll, Lr
    (4, 2, 1, 3), (1, 3, 2, 4),  # Yl, Yr
]


class memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


@memoize
def B(n):
    """Quick way to compute Catalan #'s; B(n)=(1/(n+1))*(2n n)"""
    if n == 0:
        return 1
    else:
        return 4*B(n-1) - 6*B(n-1)//(n+1)


@memoize
def G(j, n):
    """The number of binary trees with n nodes whose left subtree has j
    nodes."""
    return B(j)*B(n-j-1)


@memoize
def irank(i, n):
    p = [0]*n
    j = 0
    while i > G(j, n):
        i = i - G(j, n)
        j = j + 1
    p[0] = j+1
    i2 = 1 + (i-1) % B(n-j-1)
    i1 = (i-i2)//B(n-j-1) + 1
    for k in range(2, j+2):
        p[k-1] = irank(i1, j)[k-2]
    for k in range(j+2, n+1):
        p[k-1] = irank(i2, n-j-1)[k-j-2] + j + 1
    return p


def treegen(n):
    """Generate BST preorders on n nodes."""
    if n:
        for i in range(1, B(n)+1):
            yield tuple(irank(i, n))
    else:
        yield ()


def randtree(n):
    """Generate random BST on n nodes."""
    i = randrange(1, B(n)+1)
    return irank(i, n)


class TestTreeranks(unittest.TestCase):

    def test_catalan(self):
        """Test B(n) and treegen are in agreement on OEIS A000108."""
        catalan = [1, 1, 2, 5, 14, 42, 132, 429, 1430]
        for i, b in enumerate(catalan):
            self.assertEqual(b, B(i))
            trees = list(treegen(i))
            self.assertEqual(b, len(trees))
            self.assertEqual(b, len(set(trees)))

    def test_preorders(self):
        """Test by brute force on lenth 4."""
        four_node_trees = [
            (1, 2, 3, 4), (1, 2, 4, 3),
            (1, 3, 2, 4), (1, 4, 2, 3),
            (1, 4, 3, 2), (2, 1, 3, 4),
            (2, 1, 4, 3), (3, 1, 2, 4),
            (3, 2, 1, 4), (4, 1, 2, 3),
            (4, 1, 3, 2), (4, 2, 1, 3),
            (4, 3, 1, 2), (4, 3, 2, 1)
        ]
        self.assertEqual(four_node_trees, list(treegen(4)))
        self.assertEqual(sorted(list(treegen(6))), list(treegen(6)))


if __name__ == '__main__':
    unittest.main()
