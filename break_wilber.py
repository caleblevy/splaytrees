"""Attempt(s) to separate Splay from Wilber2 using zig-zags."""
from __future__ import print_function

import random
import unittest

from bst import *

# Pretty Printing


def keys(iterable):
    """Return keys of given iterable."""
    return tuple(x.key for x in iterable)


def compare_costs(s):
    """Print all costs for s in a pretty fashion."""
    print("Move-to-Root:")
    print("  Crossing:", mr_crossing_cost(s))
    print("  Inside:", mr_inside_cost(s))
    print("  Critical:", mr_critical_cost(s))
    print("Splay:")
    print("  Crossing:", splay_crossing_cost(s))
    print("  Inside:", splay_inside_cost(s))
    print("  Critical:", splay_critical_cost(s))
    print("  Total:", splay_cost(s))


def compare_executions(s):
    """Print paths of splay and move-to-root in dual fashion."""
    print("Compare executions: ")
    print("s =", s, '\n')
    for i, (x, y) in enumerate(dual_nodes(s), start=1):
        compare_paths(x, y, str(i) + ":")


def compare_paths(x, y, prefix=""):
    indent = " "*len(prefix)
    print(prefix, "k =", x.key)
    print(indent, "c =", keys(x.crossing_sorted()))
    print(indent, "  =", keys(y.crossing_sorted()))
    print(indent, "b =", keys(x.inside_sorted()))
    print(indent, "  =", keys(y.inside_sorted()))
    print(indent, "a =", keys(x.critical_sorted()))
    print(indent, "  =", keys(y.critical_sorted()), '\n')
    print(indent, "p =", list(sorted(keys(y.path()))))
    print()


def break_wilber(k, e):
    """Try to break Wilber starting with sequential access on 2**k-1 nodes."""
    n = 2**k-1
    s = list(range(1, n+1))
    m = 1
    while m < n:
        s.append(m)
        m *= 2
    (M, _), (S, _) = last(dual_execution(s))
    for i in range(e):
        d = S.depths()
        l = M.levels()
        ratios = {i: d[i] - l[i] for i in range(1, n+1)}
        k = max(ratios, key=ratios.__getitem__)
        s.append(k)
        x = M.find(k)
        y = S.find(k)
        compare_paths(x, y, str(i) + ":")
        M.move_to_root(k)
        S.splay(k)
    compare_costs(s)


if __name__ == '__main__':
    break_wilber(15, 1000)
    from random import randint, shuffle
    # def randseq(k, n):
    #     return [random.randint(1, k) for _ in range(n)]
    # print(randseq(100,1000))
    # compare_costs(randseq(1000, 10000))
    # r = range(5000)
    # shuffle(r)
    # compare_costs(r)
    unittest.main()
