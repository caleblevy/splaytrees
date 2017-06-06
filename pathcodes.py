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

    __slots__ = ("parent_init")

    def __init__(p):
        p.parent_init = None


class Node(object):
    """BST Node which keeps track of initial tree as nodes are inserted."""

    __slots__ = ("parent", "left", "right",
                 "parent_init", "left_init", "right_init")

    def __init__(x):
        x.parent = x.parent_init = None
        x.left = x.left_init = Placeholder()
        x.right = x.right_init = Placeholder()
        x.left.parent_init = x.right.parent_init = x

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
            if isinstance(B, Node):
                B.parent = y
            # Switch up parent pointers
            z = y.parent
            x.parent = z
            # y is the root
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
            if isinstance(B, Node):
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
            if isinstance(x, Node):
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
            if isinstance(x, Node):
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
            if isinstance(x.left, Node):
                s1.append(x.left)
            if isinstance(x.right, Node):
                s1.append(x.right)
            # gives us a "reverse" postorder
        while s2:
            yield s2.pop()

    def encoding(x):
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
        if isinstance(x.left, Node):
            raise ValueError("Node already has left child")
        x.left = Node()
        x.left.parent = x
        return x.left

    def insert_right(x):
        """Insert node to right of x"""
        if isinstance(x.right, Node):
            raise ValueError("Node already has right child")
        x.right = Node()
        x.right.parent = x
        return x.right

    def decode(x, e):
        """Extend x with encoding e."""
        for b in e:
            if b == '0':
                if isinstance(x.left, Node):
                    x = x.left
                else:
                    x = x.insert_left()
            elif b == '1':
                if isinstance(x.right, Node):
                    x = x.right
                else:
                    x = x.insert_right()
            else:
                raise ValueError("Encoding must be binary")
        return x

    def root(x):
        """Return the root of x."""
        while x.parent is not None:
            x = x.parent
        return x


# Methods extracted due to python wanting to create a wrapper around them
splay = Node.splay
simple_splay = Node.simple_splay
move_to_root = Node.move_to_root
static = Node.static


######################
# The Zig-Zag Bounds #
######################

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
        paths.append(x.encoding())
        optype(x)
    counts = [1 + e.count("10") + e.count("01") for e in paths]
    return counts


def MRBound(X):
    """Return Wilber's second lower bound as described by Kozma"""
    return _ZigZag_counts(X, move_to_root)


def SplayBound(X):
    """Return number of zig-zags on splay paths."""
    return _ZigZag_counts(X, splay)


def SimpleBound(X):
    """Return number of zig-zags on simple splay paths."""
    return ZigZag_counts(X, simple_splay)


############
# Decoders #
############

def _decoder(encodings, optype):
    """Decoding list of binary path encodings using operation type."""
    root = Node()
    nodes = []
    for e in encodings:
        x = root.decode(e)
        optype(x)
        if optype is not static:
            root = x
        nodes.append(x)
    node_to_key = {}
    for k, x in enumerate(root.inorder(), start=1):
        node_to_key[x] = k
    return tuple(map(node_to_key.__getitem__, nodes))


def static_decoder(encodings):
    """Decode the items requested from static tree."""
    return _decoder(encodings, static)


def simple_decoder(encodings):
    """Decode the items requested from simple splay using the binary paths."""
    return _decoder(encodings, simple_splay)


def splay_decoder(encodings):
    """Decode the items requested of splay using the binary paths."""
    return _decoder(encodings, splay)


def mr_decoder(encodings):
    """Decode the items requested of move-to-root using the binary paths."""
    return _decoder(encodings, move_to_root)


#########
# Tests #
#########

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
    g = k.insert_left()
    c = g.insert_left()
    a = c.insert_left()
    b = c.insert_right()
    h = g.insert_right()
    e = h.insert_left()
    m = h.insert_right()
    f = k.insert_right()
    return [k, g, c, a, b, h, e, m, f]


class TestNode(unittest.TestCase):

    def test_insert(self):
        """Test insert methods work as expected."""
        x = Node()
        y = x.insert_right()
        z = y.insert_left()
        with self.assertRaises(ValueError):
            x.insert_right()
        with self.assertRaises(ValueError):
            y.insert_left()
        self.assertTrue(y.parent is x)
        self.assertTrue(z.parent is y)
        self.assertTrue(x.parent is None)
        null_slots = [x.left, y.right, z.left, z.right]
        for obj in null_slots:
            self.assertFalse(isinstance(obj, Node))
        self.assertTrue(x.right is y)
        self.assertTrue(y.left is z)

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
        self.assertFalse(isinstance(a.left, Node))
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
        c.rotate()
        g.rotate()
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
            self.assertFalse(isinstance(x.right, Node))
        # Test simple splay zig-zag.
        a.splay()
        b.splay()
        self.assertTrue((b, a, c, h, g, e, k, m, f) == b.preorder())

    def test_simple_splay(self):
        """Test simple splay method works."""
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
            self.assertFalse(isinstance(x.right, Node))

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

    def test_encoding(self):
        """Ensure encodings of node paths are correct."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue("000" == a.encoding())
        self.assertTrue("00" == c.encoding())
        self.assertTrue("001" == b.encoding())
        self.assertTrue("0" == g.encoding())
        self.assertTrue("010" == e.encoding())
        self.assertTrue("01" == h.encoding())
        self.assertTrue("011" == m.encoding())
        self.assertTrue("" == k.encoding())
        self.assertTrue("1" == f.encoding())
        a.splay()
        self.assertTrue("" == a.encoding())
        self.assertTrue("10" == c.encoding())
        self.assertTrue("1010" == b.encoding())
        self.assertTrue("101" == g.encoding())
        self.assertTrue("10110" == e.encoding())
        self.assertTrue("1011" == h.encoding())
        self.assertTrue("10111" == m.encoding())
        self.assertTrue("1" == k.encoding())
        self.assertTrue("11" == f.encoding())

    def test_decoder(self):
        """Ensure path decodes and inserts work appropriately."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue(k is k.decode(""))
        self.assertTrue(k is not k.decode("1"))
        self.assertTrue(k.decode("00000") is a.left.left)
        self.assertTrue(f.decode("10") is k.right.right.left)
        self.assertTrue(b is g.decode("01"))
        self.assertTrue(type(b.left) is type(b.right) is not Node)
        self.assertTrue(a.left.left.parent.parent is a)
        # Test extra nodes not being inserted
        self.assertTrue(len(k.inorder()) == 13)
        with self.assertRaises(ValueError):
            k.decode("1011b")

    def test_root(self):
        """Ensure we return the proper root."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        nodes = k.inorder()
        for x in nodes:
            self.assertTrue(x.root() is k)
        a.splay()
        for x in nodes:
            self.assertTrue(x.root() is a)


class TestDecoder(unittest.TestCase):
    """Test the various methods of decoding."""

    def test_staic_decoder(self):
        """Test tree that does not change between calls."""
        standard_tree = ["000", "00", "001", "0", "010", "01", "011", "", "1"]
        self.assertTrue(tuple(range(1, 10)) == static_decoder(standard_tree))
        lr = ("0", "1", "0", "1", "", "0", "1", "1", "0", "0")
        self.assertTrue((1, 3, 1, 3, 2, 1, 3, 3, 1, 1) == static_decoder(lr))

    def test_splay_decoder(self):
        """Test that splaying works properly."""
        lr = ("0", "1", "0", "1", "", "0", "1", "1", "0", "0")
        self.assertTrue((1, 2, 1, 2, 2, 1, 2, 3, 2, 1) == splay_decoder(lr))


if __name__ == '__main__':
    unittest.main()
