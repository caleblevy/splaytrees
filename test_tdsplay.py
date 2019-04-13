"""Separate unit tests for top-down-splay, since they rely on the bottom-up
splay tree."""

import unittest
from random import randrange

from topdownsplay import (
    TDSplayTree, BinaryNode, SimpleSplayTree, tdfrompre, stdfrompre, splay
)
from propersplay import SplayTree, complete_bst_preorder
from treerank import randtree


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

    def test_td_vs_bu(self):
        """Test top-down splay vs bottom up."""
        p_odd_depth = (15, 14, 13, 12, 11, 1, 10, 2, 3, 4, 5, 9, 8, 6, 7)
        bu = SplayTree(p_odd_depth)
        td = tdfrompre(p_odd_depth)
        self.assertTrue(bu.preorder() == td.preorder() == p_odd_depth)
        bu.access(7)
        splay(td, 7)
        self.assertEqual(bu.preorder(), td.preorder())
        r_p_even_depth = p_odd_depth + (7.5, )
        bu_r = SplayTree(r_p_even_depth)
        td_r = tdfrompre(r_p_even_depth)
        l_p_even_depth = p_odd_depth + (6.5, )
        bu_l = SplayTree(l_p_even_depth)
        td_l = tdfrompre(l_p_even_depth)
        self.assertTrue(bu_r.preorder() == td_r.preorder() == r_p_even_depth)
        self.assertTrue(bu_l.preorder() == td_l.preorder() == l_p_even_depth)
        bu_r.access(7.5)
        splay(td_r, 7.5)
        self.assertNotEqual(bu_r.preorder(), td_r.preorder())
        bu_l.access(6.5)
        splay(td_l, 6.5)
        self.assertNotEqual(bu_l.preorder(), td_l.preorder())
        # Test exactly the construction of bu_r, bu_l
        td_l_after = (6.5, 1, 2, 4, 3, 5, 6, 14, 12, 11, 10, 9, 8, 7, 13, 15)
        self.assertEqual(td_l_after, td_l.preorder())
        td_r_after = (7.5, 1, 2, 4, 3, 5, 6, 7, 14, 12, 11, 10, 9, 8, 13, 15)
        self.assertEqual(td_r_after, td_r.preorder())

        n = 130
        for _ in range(10):
            p = randtree(n)
            T_bu = SplayTree(p)
            T_td = tdfrompre(p)
            for _ in range(30):
                x = randrange(1, n+1)
                _, d = T_bu._find_with_depth(x)
                if d % 2:
                    T_bu.access(x)
                    splay(T_td, x)
                    self.assertTrue(T_bu.preorder() == T_td.preorder())

    def test_missing_splays(self):
        """Test that our top-down-splay skips out at appropriate times."""
        cut_l_zig_zig = range(9, 0, -1)
        td_found = tdfrompre(cut_l_zig_zig)
        td = tdfrompre(cut_l_zig_zig)
        splay(td_found, 1)
        splay(td, 1.5)
        self.assertEqual(td_found.preorder(), td.preorder())
        cut_r_zig_zag = list(range(9, 2, -1)) + [1, 2]
        td_found = tdfrompre(cut_r_zig_zag)
        td = tdfrompre(cut_r_zig_zag)
        splay(td_found, 2)
        splay(td, 1.5)
        self.assertEqual(td_found.preorder(), td.preorder())
        cut_r_zig_zig = range(1, 10)
        td_found = tdfrompre(cut_r_zig_zig)
        td = tdfrompre(cut_r_zig_zig)
        splay(td_found, 9)
        splay(td, 8.5)
        self.assertEqual(td_found.preorder(), td.preorder())
        cut_l_zig_zag = list(range(1, 8)) + [9, 8]
        td_found = tdfrompre(cut_l_zig_zag)
        td = tdfrompre(cut_l_zig_zag)
        splay(td_found, 8)
        splay(td, 8.5)
        self.assertEqual(td_found.preorder(), td.preorder())
        # Zig cases
        cut_l_zig = range(10, 0, -1)
        td_found = tdfrompre(cut_l_zig)
        td = tdfrompre(cut_l_zig)
        splay(td_found, 1)
        splay(td, 1.5)
        self.assertEqual(td_found.preorder(), td.preorder())
        cut_l_zag = list(range(10, 2, -1)) + [1, 2]
        td_found = tdfrompre(cut_l_zag)
        td = tdfrompre(cut_l_zag)
        splay(td_found, 2)
        splay(td, 1.5)
        self.assertEqual(td_found.preorder(), td.preorder())
        cut_r_zig = range(1, 11)
        td_found = tdfrompre(cut_r_zig)
        td = tdfrompre(cut_r_zig)
        splay(td_found, 10)
        splay(td, 9.5)
        self.assertEqual(td_found.preorder(), td.preorder())
        cut_r_zag = list(range(1, 9)) + [10, 9]
        td_found = tdfrompre(cut_r_zag)
        td = tdfrompre(cut_r_zag)
        splay(td_found, 9)
        splay(td, 9.5)
        self.assertEqual(td_found.preorder(), td.preorder())

    def test_example(self):
        t = tdfrompre((1, 2, 8, 7, 6, 3, 4, 5))
        splay(t, 5)
        self.assertEqual(t.preorder(), (5, 2, 1, 3, 4, 7, 6, 8))


if __name__ == '__main__':
    unittest.main()
