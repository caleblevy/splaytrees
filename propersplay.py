"""Implement a proper splay tree, as described in the paper, so we know
sequential access, etc. holds exactly."""

import unittest


def complete_bst_preorder(d, root=None):
    """Return preorder sequence of complete BST of depth d on nodes
    1...2^d-1. """
    if root is None:
        root = 2**(d-1)
    yield root
    if d > 1:
        for node in complete_bst_preorder(d-1, root-2**(d-2)):
            yield node
        for node in complete_bst_preorder(d-1, root+2**(d-2)):
            yield node


class Node(object):

    def __init__(self, x):
        self.key = x
        self.parent = None
        self.left = None
        self.right = None

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % ", ".join([
            "key=%s" % self.key,
            "parent=%s" % getattr(self.parent, 'key', None),
            "left=%s" % getattr(self.left, 'key', None),
            "right=%s" % getattr(self.right, 'key', None)
        ])

    def rotate(self):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        if self.parent is None:
            return
        x = self
        y = self.parent
        # Ensures x < y
        if x.key > y.key:  # TODO: Could be done without compare
            x, y = y, x
        if x is y.left:
            # Shift around subtree
            B = x.right
            y.left = B
            if B is not None:
                B.parent = y
            # Switch up parent pointers
            z = y.parent
            x.parent = z
            if z is not None:
                if y is z.right:
                    z.right = x
                else:
                    z.left = x
            x.right = y
            y.parent = x
        elif y is x.right:  # (if y is x.right)
            B = y.left
            x.right = B
            if B is not None:
                B.parent = x
            # Switch up parent pointers
            z = x.parent
            y.parent = z
            if z is not None:
                if x is z.right:
                    z.right = y
                else:
                    z.left = y
            y.left = x
            x.parent = y

    def _splay_step(self):
        """Do one zig, zig-zig or zig-zag."""
        x = self
        y = x.parent
        if y is None:
            return
        else:
            z = y.parent
            # zig
            if z is None:
                x.rotate()
            # zig-zag
            elif (y is z.left and x is y.right) or (y is z.right and x is z.left):
                x.rotate()
                x.rotate()
            # zig-zig
            else:
                y.rotate()
                x.rotate()


def _inorder_walk(x):
    """Helper function to print nodes in order."""
    if x is not None:
        for key in _inorder_walk(x.left):
            yield key
        yield x.key
        for key in _inorder_walk(x.right):
            yield key


def _preorder_walk(x):
    """Helper function for preorder tree walk."""
    if x is not None:
        yield x.key
        for key in _preorder_walk(x.left):
            yield key
        for key in _preorder_walk(x.right):
            yield key


def _postorder_walk(x):
    """Helper function for postorder tree walk."""
    if x is not None:
        for key in _postorder_walk(x.left):
            yield key
        for key in _postorder_walk(x.right):
            yield key
        yield x.key


# TODO: implement from preorder
# TODO: Add root.


class SplayTree(object):
    """A splay tree implemented with top-down splaying."""
    # Add elements by finding them and splaying there.

    def __init__(self, iterable=None):
        self.root = None
        self.count = 0  # Total length of access paths
        if iterable is not None:
            for x in iterable:
                self._simple_add(x)

    def _find_with_depth(self, k):
        """Find a node with key k."""
        x = x_prev = self.root
        while x is not None and k != x.key:
            x_prev = x
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def _simple_add(self, v):
        """Add a node with value v to the binary search tree while maintaining
        symmetric search order."""
        z = Node(v)
        y = None
        x = self.root
        while x is not None:
            y = x
            if v < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif v < y.key:
            y.left = z
        else:
            y.right = z
        return z

    def inorder(self):
        """Output tree nodes in order."""
        return list(_inorder_walk(self.root))

    def preorder(self):
        """Output tree nodes in preorder."""
        return list(_preorder_walk(self.root))

    def postorder(self):
        """Output tree nodes in postorder."""
        return list(_postorder_walk(self.root))


class SplayTreeTests(unittest.TestCase):

    def test_basics(self):
        """Test basic binary tree operations."""
        # Feed preorder sequence, should get preorder
        a = SplayTree([4, 1, 2, 5, 7, 6])
        #   4
        #  /  \
        # 1    5
        #  \    \
        #   2   7
        #      /
        #     6
        self.assertTrue(a.root.key == 4)
        self.assertTrue(a.root.right.key == 5)
        self.assertTrue(a.root.right.right.key == 7)
        self.assertEqual([1, 2, 4, 5, 6, 7], a.inorder())
        self.assertEqual([4, 1, 2, 5, 7, 6], a.preorder())
        self.assertEqual([2, 1, 6, 7, 5, 4], a.postorder())

    def test_rotation(self):
        """Test tree rotations correctly transform the tree back and forth."""
        c = list(complete_bst_preorder(5))
        t = SplayTree(c)
        self.assertEqual(c, t.preorder())
        self.assertEqual(range(1, 32), t.inorder())
        # Rotate up on left child
        n4 = t._find_with_depth(4)
        n4.rotate()
        self.assertEqual(
            [16, 4, 2, 1, 3, 8, 6, 5, 7, 12, 10, 9, 11, 14, 13, 15,
             24, 20, 18, 17, 19, 22, 21, 23, 28, 26, 25, 27, 30, 29, 31],
            t.preorder()
        )
        # Rotate back down on right child
        n4.right.rotate()
        self.assertEqual(c, t.preorder())
        t.root.rotate()
        self.assertEqual(c, t.preorder())

    def test_splay_step(self):
        """Test the corner case of an individual splay step"""
        c = list(complete_bst_preorder(5))
        t_zigzig_right = SplayTree(c)  # right zig-zig
        n2 = t_zigzig_right._find_with_depth(2)
        n2._splay_step()
        self.assertEqual(
            [16, 2, 1, 4, 3, 8, 6, 5, 7, 12, 10, 9, 11, 14, 13, 15,
             24, 20, 18, 17, 19, 22, 21, 23, 28, 26, 25, 27, 30, 29, 31],
            t_zigzig_right.preorder()
        )
        t_zigzig_left = SplayTree(c)
        n30 = t_zigzig_left._find_with_depth(30)
        n30._splay_step()
        self.assertEqual(
            [16, 8, 4, 2, 1, 3, 6, 5, 7, 12, 10, 9, 11, 14, 13, 15,
             30, 28, 24, 20, 18, 17, 19, 22, 21, 23, 26, 25, 27, 29, 31],
            t_zigzig_left.preorder()
        )


if __name__ == '__main__':
    unittest.main()
