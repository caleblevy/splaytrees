"""Emperically determine whether number of zig-zigs on the search paths is
bounded by size of initial tree + wilber 2."""
from __future__ import print_function

import unittest

from pathcodes import Node, splay, SplayBound, SplayZigs


def depths(x):
    """Return depths of nodes of subtree rooted at x."""
    d = {}
    k = x.node_to_key()
    p = iter(x.preorder())
    d[k[next(p)]] = 0
    for x in p:
        d[k[x]] = d[k[x.parent]] + 1
    return d


def zagzig_depths(x):
    """Returns zig-zag depths of nodes of subtree rooted at x."""
    d = {}
    k = x.node_to_key()
    p = iter(x.preorder())
    d[k[next(p)]] = 0
    for y in p:
        z = y.parent
        if z.parent is x.parent:
            d[k[y]] = 0
        else:
            w = z.parent
            if (z is w.right and y is z.left) or (z is w.left and y is z.right):
                d[k[y]] = d[k[z]] + 1
            else:
                d[k[y]] = d[k[z]]
    return d


def zigzig_depths(x):
    """Returns zig-zag depths of nodes of subtree rooted at x."""
    d = {}
    k = x.node_to_key()
    p = iter(x.preorder())
    d[k[next(p)]] = 0
    for y in p:
        z = y.parent
        if z.parent is x.parent:
            d[k[y]] = 0
        else:
            w = z.parent
            if (z is w.right and y is z.right) or (z is w.left and y is z.left):
                d[k[y]] = d[k[z]] + 1
            else:
                d[k[y]] = d[k[z]]
    return d


def tree_nodes(movements):
    """Return mapping of 1...n to the nodes described by the cursor
    movements."""
    t = Node.from_cursor(movements)
    return dict(enumerate(t.inorder(), start=1))


def padded(k):
    """Do splay zig-zig count on w2 example with added padding."""
    s = [1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]
    return list(range(1, k+1)) + list(range(k, 0, -1)) + [x+k for x in s]


class TestDepths(unittest.TestCase):
    """Test the regular, zig-zig and zig-zag depth mappings"""

    def test_depths(self):
        """Test node depths."""
        d = depths(Node())
        self.assertEqual({1: 0}, d)
        t = tree_nodes("r"*30)
        t[31].splay()
        t[16].splay()
        t[28].splay()
        t_depths = depths(t[28])
        self.assertEqual(6, t_depths[15])
        self.assertEqual(6, t_depths[23])
        self.assertEqual(7, t_depths[13])
        sub_depths = depths(t[22])
        self.assertEqual(3, sub_depths[7])
        self.assertEqual(1, sub_depths[2])

    def test_zagzig_depths(self):
        """Test number zig-zags on splay paths is correct."""
        d = zagzig_depths(Node())
        self.assertEqual({1: 0}, d)
        t = tree_nodes("r"*30)
        rp_depths = zagzig_depths(t[1])
        for k in range(1, 32):
            self.assertEqual(0, rp_depths[k])
        t[31].splay()
        t[16].splay()
        t[28].splay()
        t_depths = zagzig_depths(t[28])
        self.assertEqual(3, t_depths[13])
        self.assertEqual(0, t_depths[2])
        self.assertEqual(2, t_depths[11])
        self.assertEqual(1, t_depths[29])
        sub_depths = zagzig_depths(t[14])
        self.assertEqual(0, sub_depths[5])
        self.assertEqual(1, sub_depths[3])
        self.assertEqual(0, sub_depths[2])

    def test_zigzig_depths(self):
        """Test number of zig-zigs on splay paths is correct."""
        d = zigzig_depths(Node())
        self.assertEqual({1: 0}, d)
        t = tree_nodes("r"*30)
        rp_depths = zigzig_depths(t[1])
        for k in range(1, 31):
            self.assertEqual(max(0, k-2), rp_depths[k])
        t[31].splay()
        t[16].splay()
        t[28].splay()
        t_depths = zigzig_depths(t[28])
        self.assertEqual(3, t_depths[14])
        self.assertEqual(3, t_depths[12])
        self.assertEqual(4, t_depths[11])
        self.assertEqual(0, t_depths[30])
        self.assertEqual(0, t_depths[17])
        sub_depths = zigzig_depths(t[22])
        self.assertEqual(1, sub_depths[5])
        self.assertEqual(0, sub_depths[7])


if __name__ == '__main__':
    unittest.main()
    s = [1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]
    print(sum(SplayBound(s)))
    print(SplayBound(s))
    print(SplayZigs(s))
    print(sum(SplayZigs(padded(30))))
    print(sum(SplayBound(padded(30))))
