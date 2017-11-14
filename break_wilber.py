"""Attempt(s) to separate Splay from Wilber2 using zig-zags."""
from __future__ import print_function

import unittest

from bst import *


def all_costs(s):
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


def depths(T):
    """Return depths of nodes of subtree rooted at x."""
    d = {}
    if not T:
        return d
    nodes = iter(T.root.preorder_nodes())
    d[next(nodes).key] = 1
    for x in nodes:
        d[x.key] = d[x.parent.key] + 1
    return d


def levels(T):
    """Number or turns to get from root to node."""
    d = {}
    if not T:
        return d
    nodes = iter(T.root.preorder_nodes())
    d[next(nodes).key] = 1
    for x in nodes:
        y = x.parent
        z = y.parent
        if z is None:
            d[x.key] = 1
        elif (x is y.left and y is z.right) or (x is y.right and y is z.left):
            d[x.key] = d[y.key] + 1
        else:
            d[x.key] = d[y.key]
    return d


class TestDepths(unittest.TestCase):
    """Test the regular, zig-zig and zig-zag depth mappings"""

    def test_depths(self):
        """Test node depths."""
        d = depths(Tree([1]))
        self.assertEqual({1: 1}, d)
        t = Tree.from_encoding("r"*30)
        t.splay(31)
        t.splay(16)
        t.splay(28)
        t_depths = depths(t)
        self.assertEqual(7, t_depths[15])
        self.assertEqual(7, t_depths[23])
        self.assertEqual(8, t_depths[13])

    def test_levels(self):
        """Test number zig-zags on splay paths is correct."""
        d = levels(Tree([1]))
        self.assertEqual({1: 1}, d)
        t = Tree.from_encoding("r"*30)
        rp_levels = levels(t)
        for k in range(1, 32):
            self.assertEqual(1, rp_levels[k])
        t.splay(31)
        t.splay(16)
        t.splay(28)
        t_levels = levels(t)
        print(t.preorder())
        self.assertEqual(4, t_levels[13])
        self.assertEqual(1, t_levels[2])
        self.assertEqual(3, t_levels[11])
        self.assertEqual(2, t_levels[29])


if __name__ == '__main__':
    s = tuple(range(1, 63)) + (1, 2, 4, 8, 16, 32)
    (M, x), (S, y) = last(dual_execution(s))
    print(M.encoding())
    print(S.encoding())
    s = list("aihjgfclkendbpmoi")
    for x in mr_nodes(s):
        print(x.crossing_nodes())
    all_costs(s)
    unittest.main()
