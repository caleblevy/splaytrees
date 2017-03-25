"""Test the effect of a subsequence on a random tree."""

from random import shuffle

from experiments import access_depths
from propersplay import SplayTree
from wilber import wilber2


def subseq_1(n):
    """Test subsequence on random tree, removing first element"""
    a = range(1, n+1)
    shuffle(a)
    b = list(a)
    # shuffle(b)
    T1 = SplayTree(a)
    T2 = SplayTree(a)
    # print(T1.preorder() == T1.preorder() == T2.preorder())  # Great...
    X = access_depths(T1, b)
    Y = access_depths(T2, b[2:])
    print(X)
    print(" ", Y)
    print(sum(X), sum(Y))


def subseq_perm(n):
    """Subsequence with multiple removals under natural permutationt tree."""
    a = range(1, n+1)
    shuffle(a)
    T1 = SplayTree(a)
    T2 = SplayTree(a)
    b = list(a)
    popped_elems = [20]
    for i in popped_elems:
        b.pop(i)
    X = access_depths(T1, a)
    Y = access_depths(T2, b)
    print(X)
    print(Y)
    print(sum(X), sum(Y), sum(Y) - sum(X), sum(X[i] for i in popped_elems))


if __name__ == "__main__":
    # subseq_1(100)
    subseq_perm(2000)
    a = range(1, 2001)
    shuffle(a)
    print(wilber2(a))
    a.pop(20)
    print(wilber2(a))