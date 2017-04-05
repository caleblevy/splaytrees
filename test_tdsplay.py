"""Separate unit tests for top-down-splay, since it was most complicated to
implement, and not based on reference implementation."""

import unittest

from topdownsplay import TDSplayTree, BinaryNode, SimpleSplayTree
from propersplay import SplayTree
from treerank import randtree


def _tree_from_preorder(preorder):
    """Slow way to build a tree from the preorder permutation p."""
    if preorder:
        root_item = preorder[0]
        left_items = [item for item in preorder if item < root_item]
        right_items = [item for item in preorder if item > root_item]
        root = BinaryNode(root_item)
        root.left = _tree_from_preorder(left_items)
        root.right = _tree_from_preorder(right_items)
        return root


def tdfrompre(preorder):
    root = _tree_from_preorder(preorder)
    T = TDSplayTree()
    T.root = root
    return T


def stdfrompre(preorder):
    root = _tree_from_preorder(preorder)
    T = SimpleSplayTree()
    T.root = root
    return T


def splay(T, x):
    x in T


class TestTDSplay(unittest.TestCase):

    def test_td_vs_std(self):
        """Test where top-down splay should compare with simple topdown."""
        empty = TDSplayTree()
        self.assertTrue(1 not in empty)
        # Tests zig-zig and zig cases identical to simple splay
        for n in range(1, 99):  # Six gets interesting
            r_nodes = range(n, 0, -1)
            l_nodes = list(reversed(r_nodes))
            td_r = tdfrompre(r_nodes)
            std_r = stdfrompre(r_nodes)
            td_l = tdfrompre(l_nodes)
            std_l = tdfrompre(l_nodes)
            if n <= 5:
                for k in l_nodes:
                    splay(td_r, k)
                    splay(std_r, k)
                    self.assertTrue(std_r.preorder() == td_r.preorder())
                for k in r_nodes:
                    splay(td_l, k)
                    splay(std_l, k)
                    self.assertTrue(std_l.preorder(), td_l.preorder())
            else:
                splay(td_r, 1)
                splay(std_r, 1)
                self.assertEqual(std_r.preorder(), td_r.preorder())
                splay(td_r, 2)
                splay(std_r, 2)
                self.assertNotEqual(td_r.preorder(), std_r.preorder())
                # Test reflected
                splay(td_l, n)
                splay(std_l, n)
                self.assertEqual(std_l.preorder(), td_l.preorder())
                splay(td_l, n-1)
                splay(std_l, n-1)
                self.assertEqual(std_l.preorder(), td_l.preorder())


if __name__ == '__main__':
    unittest.main()
