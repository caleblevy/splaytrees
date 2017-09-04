"""Attempt to implement Wilber 2 in code."""
from __future__ import print_function

from functools import partial
from random import shuffle

from topdownsplay import Inf, NegInf
from propersplay import complete_bst_preorder
from pathcodes import SplayBound, MRBound, Node, move_to_root, splay

import unittest


def critical_nodes(s, i):
    """Compute the inside and crossing accesses and nodes of s."""
    # Have 0 index placeholder for all lists, since Wilber's work assumes this.
    b = [None]*(i+1);  c = [None]*(i+1);  v = [None]*(i+1);  w = [None]*(i+1)
    s = [None] + s
    if i == 1:
        return ([], [], [], [])
    c[1] = i-1
    w[1] = s[i-1]
    if w[1] < s[i]:
        v[0] = Inf
    else:
        v[0] = NegInf
    l = 1
    while True:
        if w[l] == s[i]:
            break
        elif w[l] < s[i]:
            Q = {j for j in range(1, c[l]) if s[i] <= s[j] < v[l-1]}
            if not Q:
                break
            c[l+1] = max(Q)
            w[l+1] = s[c[l+1]]
            v[l] = max(s[j] for j in range(c[l+1]+1, c[l]+1) if s[j] < s[i])
            b[l] = max(j for j in range(c[l+1]+1, c[l]+1) if s[j] == v[l])
        elif w[l] > s[i]:
            Q = {j for j in range(1, c[l]) if v[l-1] < s[j] <= s[i]}
            if not Q:
                break
            c[l+1] = max(Q)
            w[l+1] = s[c[l+1]]
            v[l] = min(s[j] for j in range(c[l+1]+1, c[l]+1) if s[j] > s[i])
            b[l] = max(j for j in range(c[l+1]+1, c[l]+1) if s[j] == v[l])
        l += 1
    return (
        c[1:l+1],
        w[1:l+1],
        b[1:l],
        v[1:l]
    )


def compute_kappa(s, i):
    """Compute the Wilber 2 score for access i of request sequence s."""
    c, w, b, v = critical_nodes(s, i)
    return len(v)


def scores(s):
    """Return the scores of each access"""
    if not s:
        return []
    return [compute_kappa(s, i) for i in range(1, len(s)+1)]


def wilber2(s):
    """Compute wilber2 bound for access sequence s."""
    return len(s) + sum(scores(s))

def binaryDigits(n):
    """Map integer n to list of binary digits."""
    # Lifted from StackOverflow
    return [int(d) for d in str(bin(n))[2:]]


def bitReversal(n, k):
    """Return reversed bit string for n with k binary digits padded."""
    digits = binaryDigits(n)
    b = len(digits)
    if b > k:
        raise ValueError("%s-bit vector cannot represent %s" % (k, n))
    return list(reversed([0]*(k-b) + digits))


def bitReversalSequence(k):
    """Return bit reversed integers from 1 to 2**k-1"""
    return sorted(range(2**k), key=partial(bitReversal, k=k))


def _paths(s, algo=move_to_root):
    """Paths when using algo on s starting from right path."""
    q = sorted(set(s))
    n = len(q)
    t = Node.from_cursor("r"*(n-1))
    d = dict(zip(q, t.preorder()))
    d_inv = {node: key for key, node in d.items()}
    paths = []
    for x in s:
        y = d[x]
        path = [y]
        while y.parent is not None:
            y = y.parent
            path.append(y)
        paths.append(tuple(d_inv[node] for node in path))
        algo(d[x])
    return paths


def mr_paths(s):
    """Paths when using move-to-root on s starting from right path."""
    return _paths(s, move_to_root)


def splay_paths(s):
    """Paths when using splay on s starting from right path"""
    return _paths(s, splay)


def print_path(path):
    """Pretty print the access path."""
    x = path[0]
    strings = [" "]


def compare_mr_w2(s):
    """Compare the paths of move-to-root with Wilber 2."""
    print("Compare paths: ")
    print("s =", s, '\n')
    mrp = mr_paths(s)
    zigzags = [c-1 for c in MRBound(s)]
    for i, (x, path, za) in enumerate(zip(s, mrp, zigzags), start=1):
        prefix = str(i) + ":"
        indent = " "*len(prefix)
        c, w, b, v = critical_nodes(s, i)
        print(prefix, "x =", x)
        print(indent, "w =", w)
        print(indent, "v =", v)
        print(indent, "p =", path)
        print(indent, "score = ", len(v))
        print(indent, "zig-zags = ", za, '\n')


class TestWilber2(unittest.TestCase):

    def test_critical_nodes(self):
        """Test Wilber2 on paper example."""
        s = list("aihjgfclkendbpmoi")
        c, w, b, v = critical_nodes(s, 17)
        c_wilber = [16, 13, 9, 6, 4, 3, 2]
        b_wilber = [15, 10, 9, 5, 4, 3]
        w_wilber = list("obkfjhi")
        v_wilber = list("mekgjh")
        self.assertEqual(c, c_wilber)
        self.assertEqual(b, b_wilber)
        self.assertEqual(w, w_wilber)
        self.assertEqual(v, v_wilber)
        for access, node in zip(c, w):
            self.assertEqual(s[access-1], node)
        for access, node in zip(b, v):
            self.assertEqual(s[access-1], node)

    def test_bit_reversal_sequence(self):
        """Test bit-reversal sequence agrees with Kozma."""
        B_16 = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        self.assertEqual(bitReversalSequence(4), B_16)

    def test_wilber2(self):
        """Test on the bit-reversal sequence."""
        for k in range(1, 8):
            self.assertTrue(wilber2(bitReversalSequence(k)) >= k*(2**k)//2+1)
        self.assertEqual(0, wilber2(list("")))


if __name__ == "__main__":
    # unittest.main()
    a = list("aihjgfclkendbpmoi")
    s = [1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]
    compare_mr_w2(s)
    r = range(2**10)
    shuffle(r)
    compare_mr_w2(r)
