"""A new version of bottom-up splay and move-to-root carrying less baggage."""

import functools
import unittest


def tuplemaker(generator):
    """Make generator function return tuple containing its output."""
    @functools.wraps(generator)
    def tupler(*args, **kwargs):
        return tuple(generator(*args, **kwargs))
    return tupler


class Placeholder(object):
    """Slot for a null node, allowing them to be linked together."""

    __slots__ = ("parent", "dual")

    def __init__(x):
        x.parent = None
        x.dual = None


class Node(object):
    """BST node with parents."""

    __slots__ = ("parent", "left", "right")

    def __init__(x):
        x.parent = None
        x.left = None
        x.right = None

    def rotate(x):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        y = x.parent
        # Ensures x < y
        if x is y.right:
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
        else:  # y is x.right
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

    @tuplemaker
    def inorder(x):
        """Traverse subtree rooted at x inorder."""
        stack = []
        while True:
            # Reach left most node of current's subtree
            if x is not None:
                # Place pointer to a tree node on the stack before traversing
                # left subtree.
                stack.append(x)
                x = x.left
            # Backtrack from empty subtree and visit node at top of stack.
            # However, if stack is empty, we are doen.
            else:
                if stack:
                    x = stack.pop()
                    yield x
                    # We have visited the node and its left subtree. Now visit
                    # right subtree.
                    x = x.right
                else:
                    break

    @tuplemaker
    def preorder(x):
        """Traverse subtree rooted at x inorder."""
        stack = []
        while True:
            if x is not None:
                yield x
                stack.append(x)
                x = x.left
            else:
                if stack:
                    x = stack.pop()
                    x = x.right
                else:
                    break

    @tuplemaker
    def postorder(x):
        """Return postorder of subtree rooted at x."""
        s1 = [x]
        s2 = []
        while s1:
            x = s1.pop()
            s2.append(x)
            # push left and right children of removed item to s1
            if x.left is not None:
                s1.append(x.left)
            if x.right is not None:
                s1.append(x.right)
            # gives us a "reverse" postorder
        while s2:
            yield s2.pop()

    def path_encoding(x):
        """Return binary string encoding path from root to x."""
        encoding = []
        while x.parent is not None:
            if x is x.parent.left:
                encoding.append("0")
            else:
                encoding.append("1")
            x = x.parent
        encoding.reverse()
        return ''.join(encoding)

    def _splay_step(x):
        """Perform zig, zig-zag or zig-zig appropriately."""
        y = x.parent
        z = y.parent  # parent checked for in "splay"
        # zig
        if z is None:
            x.rotate()
        # zig-zag
        elif (y is z.left and x is y.right) or (y is z.right and x is y.left):
            x.rotate()
            x.rotate()
        # zig-zig
        else:
            y.rotate()
            x.rotate()

    def _simple_splay_step(x):
        """Do a simple splay step."""
        y = x.parent
        z = y.parent  # parent checked for in "splay"
        # zig
        if z is None:
            x.rotate()
        elif (y is z.left and x is y.right) or (y is z.right and x is y.left):
            x.rotate()
        # zig-zig
        else:
            y.rotate()
            x.rotate()

    def splay(x):
        """Proper bottom-up splay to the top."""
        while x.parent is not None:
            x._splay_step()

    def simple_splay(x):
        """Proper bottom-up simple splay to the top."""
        while x.parent is not None:
            x._simple_splay_step()

    def move_to_root(x):
        """Move straight to the root."""
        while x.parent is not None:
            x.rotate()

    def static(x):
        """Operation of a static search tree."""
        return

    def insert_left(x):
        """Insert a node to the left of x."""
        if x.left is not None:
            raise ValueError("Node already has left child")
        x.left = Node()
        x.left.parent = x
        return x.left

    def insert_right(x):
        """Insert node to right of x"""
        if x.right is not None:
            raise ValueError("Node already has right child.")
        x.right = Node()
        x.right.parent = x
        return x.right


def _ZigZag_counts(X, optype):
    """Record the encodings of move-to-root access sequence starting from right
    path."""
    keys = sorted(set(X))  # Elements
    root = x = Node()
    key_to_node = {}
    for k in keys:
        key_to_node[k] = x
        x = x.insert_right()
    paths = []
    for k in X:
        x = key_to_node[k]
        paths.append(x.path_encoding())
        optype(x)
    counts = [1 + e.count("10") + e.count("01") for e in paths]
    return counts


def MRBound(X):
    """Return Wilber's second lower bound as described by Kozma"""
    return _ZigZag_counts(X, Node.move_to_root)


def SplayBound(X):
    """Return number of zig-zags on splay paths."""
    return _ZigZag_counts(X, Node.splay)


def SimpleBound(X):
    """Return number of zig-zags on simple splay paths."""
    return ZigZag_counts(X, Node.simple_splay)


def _test_tree():
    """Tree used for unit tests."""
    #       k
    #      /  \
    #      g  f
    #    /   \
    #   c    h
    #  / \   /\
    # a   b e  m
    k = Node()
    g = k.left = Node();  g.parent = k
    c = g.left = Node();  c.parent = g
    a = c.left = Node();  a.parent = c
    b = c.right = Node();  b.parent = c
    h = g.right = Node();  h.parent = g
    e = h.left = Node();  e.parent = h
    m = h.right = Node();  m.parent = h
    f = k.right = Node();  f.parent = k
    return [k, g, c, a, b, h, e, m, f]

class TestNode(unittest.TestCase):

    def test_rotation(self):
        """Test rotation properly changes parent pointers"""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        parent_pairs = [
            (g, k), (c, g), (a, c), (b, c), (h, g), (e, h), (m, h), (f, k)
        ]
        a.rotate()
        self.assertTrue(g.right is h)
        self.assertTrue(g.left is a)
        self.assertTrue(c.parent is a)
        self.assertTrue(a.parent is g)
        self.assertTrue(a.left is None)
        self.assertTrue(a.right is c)
        h.rotate()
        self.assertTrue(h.parent is k)
        self.assertTrue(k.left is h)
        self.assertTrue(k.right is f)
        self.assertTrue(h.right is m)
        self.assertTrue(h.left is g)
        self.assertTrue(g.parent is h)
        self.assertTrue(m.parent is h)
        self.assertTrue(e.parent is g)
        self.assertTrue(g.right is e)
        self.assertTrue(g.left is a)
        # Reverse these rotations
        c.rotate();  g.rotate()
        for x, y in parent_pairs:
            self.assertTrue(x.parent is y)

    def test_inorder(self):
        """Test inorder traversal."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue((a, c, b, g, e, h, m, k, f) == k.inorder())
        a.rotate()
        self.assertTrue((a, c, b, g, e, h, m, k, f) == k.inorder())
        h.rotate()
        self.assertTrue((a, c, b, g, e, h, m, k, f) == k.inorder())

    def test_preorder(self):
        """Test preorder traversal"""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue((k, g, c, a, b, h, e, m, f) == k.preorder())
        a.rotate()
        self.assertTrue((k, g, a, c, b, h, e, m, f) == k.preorder())
        h.rotate()
        self.assertTrue((k, h, g, a, c, b, e, m, f) == k.preorder())

    def test_postorder(self):
        """Test postorder traversal."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue((a, b, c, e, m, h, g, f, k) == k.postorder())
        a.rotate()
        self.assertTrue((b, c, a, e, m, h, g, f, k) == k.postorder())
        h.rotate()
        self.assertTrue((b, c, a, e, g, m, h, f, k) == k.postorder())

    def test_splay(self):
        """Test the splay method works."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        a.splay()
        self.assertTrue((a, k, c, g, b, h, e, m, f) == a.preorder())
        e.splay()
        self.assertTrue((e, a, c, g, b, k, h, m, f) == e.preorder())
        # sequential access
        nodes = [a, c, b, g, e, h, m, k, f]
        for x in nodes:
            x.splay()
        self.assertTrue((f, k, m, h, e, g, b, c, a) == f.preorder())
        for x in nodes:
            self.assertTrue(x.right is None)
        # Test simple splay zig-zag.
        a.splay()
        b.splay()
        self.assertTrue((b, a, c, h, g, e, k, m, f) == b.preorder())

    def test_simple_splay(self):
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        a.simple_splay()
        self.assertTrue((a, k, c, g, b, h, e, m, f) == a.preorder())
        e.simple_splay()
        # First difference from splay
        self.assertTrue((e, a, g, c, b, k, h, m, f) == e.preorder())
        # Test zig-zag difference
        a.simple_splay()
        h.simple_splay()
        self.assertTrue((h, e, a, g, c, b, k, m, f) == h.preorder())
        # sequential access
        nodes = [a, c, b, g, e, h, m, k, f]
        for x in nodes:
            x.simple_splay()
        self.assertTrue((f, k, m, h, e, g, b, c, a) == f.preorder())
        for x in nodes:
            self.assertTrue(x.right is None)

    def test_move_to_root(self):
        """Test properties of move-to-root"""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        m.move_to_root()
        self.assertTrue((m, g, c, a, b, h, e, k, f) == m.preorder())
        e.move_to_root()
        self.assertTrue((e, g, c, a, b, m, h, k, f) == e.preorder())

    def test_static(self):
        """Ensure no-op does nodda."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        nodes = [a, b, c, f, e, g, h, m]
        for x in nodes:
            x.static()
        self.assertTrue((k, g, c, a, b, h, e, m, f) == k.preorder())

    def test_path_encoding(self):
        """Ensure encodings of node paths are correct."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue("000" == a.path_encoding())
        self.assertTrue("00" == c.path_encoding())
        self.assertTrue("001" == b.path_encoding())
        self.assertTrue("0" == g.path_encoding())
        self.assertTrue("010" == e.path_encoding())
        self.assertTrue("01" == h.path_encoding())
        self.assertTrue("011" == m.path_encoding())
        self.assertTrue("" == k.path_encoding())
        self.assertTrue("1" == f.path_encoding())
        a.splay()
        self.assertTrue("" == a.path_encoding())
        self.assertTrue("10" == c.path_encoding())
        self.assertTrue("1010" == b.path_encoding())
        self.assertTrue("101" == g.path_encoding())
        self.assertTrue("10110" == e.path_encoding())
        self.assertTrue("1011" == h.path_encoding())
        self.assertTrue("10111" == m.path_encoding())
        self.assertTrue("1" == k.path_encoding())
        self.assertTrue("11" == f.path_encoding())


if __name__ == '__main__':
    unittest.main()