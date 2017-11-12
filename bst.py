"""Simple, bare-bones implementation of a splay tree and a binary search
tree."""

import functools
import unittest


Left = False
Right = True


@functools.total_ordering
class Node(object):
    """Node object maintaining all properties under rotation."""

    __slots__ = ("_left", "_right", "_parent", "key")

    def __init__(x, key):
        assert not is_node(key)
        x.key = key
        x._left = x._right = x._parent = None

    def __repr__(x):
        return "%s(%r)" % (x.__class__.__name__, x.key)

    # Ordering operations

    def __lt__(x, y):
        if is_node(y):
            return x.key < y.key
        else:
            return x.key < y

    def __eq__(x, y):
        if is_node(y):
            return x.key == y.key
        else:
            return x.key == y

    def __ne__(x, y):
        return not x == y

    # Pointer Adjustment

    @property
    def left(x):
        return x._left

    @property
    def right(x):
        return x._right

    @property
    def parent(x):
        return x._parent

    @left.setter
    def left(x, y):
        if y is None:
            detach(x.left)
        else:
            assert is_node(y) and y.parent is None
            detach(x.left)
            x._left = y
            y._parent = x

    @right.setter
    def right(x, y):
        if y is None:
            detach(x.right)
        else:
            assert is_node(y) and y.parent is None
            detach(x.right)
            x._right = y
            y._parent = x

    def insert_left(x, k):
        """Insert new node with key k to the left of x."""
        assert x.left is None
        x.left = Node(k)
        return x.left

    def insert_right(x, k):
        """Insert new node with key k to the right of x."""
        assert x.right is None
        x.right = Node(k)
        return x.right

    def rotate(x):
        """Rotate the edge between x and its parent."""
        y = x.parent
        z = y.parent
        w = x.right if x is y.left else x.left
        y_dir = child_type(y)
        x_dir = child_type(x)
        detach(w)
        detach(x)
        detach(y)
        # Do the main rotation
        if x_dir is Left:
            x.right = y
            y.left = w
        elif x_dir is Right:
            x.left = y
            y.right = w
        # Connect to pair's parent
        if y_dir is Left:
            z.left = x
        elif y_dir is Right:
            z.right = x
        else:
            return

    # The various walks

    def _walk(x, order=None):
        """Do all three edge traversals at once."""
        z = x.parent
        l = r = False  # l is true if all node's in x.left are visited
        while True:
            if order is None:
                yield x
            if not l:
                if order == -1:
                    yield x
                y = x.left
                if y is None:
                    l = True
                else:
                    if order == "":
                        yield "l"
                    x = y
            elif not r:
                if order == 0:
                    yield x
                y = x.right
                if y is None:
                    r = True
                else:
                    if order == "":
                        yield "r"
                    x = y
                    l = False
            else:
                if order == 1:
                    yield x
                y = x.parent
                if y is z:
                    return
                elif x is y.left:
                    r = False
                if order == "":
                    yield "p"
                x = y

    def subtree_encoding(x):
        """Encode cursor movements traversing the subtree rooted at x."""
        return "".join(x._walk(""))

    def _walk_nodes(x, order=None):
        return tuple(x._walk(order))

    def walk_nodes(x):
        """Depth first search of tree edges, always going left before right."""
        return x._walk_nodes()

    def preorder_nodes(x):
        return x._walk_nodes(-1)

    def inorder_nodes(x):
        return x._walk_nodes(0)

    def postorder_nodes(x):
        return x._walk_nodes(1)

    def _walk_keys(x, order=None):
        """Return tuple of the keys a given walk."""
        return tuple(n.key for n in x._walk(order))

    def walk_keys(x):
        return x._walk_keys()

    def preorder_keys(x):
        return x._walk_keys(-1)

    def inorder_keys(x):
        return x._walk_keys(0)

    def postorder_keys(x):
        return x._walk_keys(1)

    # Self-Adjustment

    def _splay_step(x):
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
        while x.parent is not None:
            x._splay_step()

    def simple_splay(x):
        while x.parent is not None:
            x._simple_splay_step()

    def move_to_root(x):
        while x.parent is not None:
            x.rotate()


def is_node(x):
    return isinstance(x, Node)


def detach(x):
    """Detach node x from its parent."""
    if x is None:
        return
    y = x.parent
    if y is None:
        return
    else:
        if x is y._right:
            y._right = None
        else:
            y._left = None
        x._parent = None


def child_type(x):
    """Return whether x is a left child, right child or None."""
    y = x.parent
    if y is None:
        return None
    elif x is y.right:
        return Right
    elif x is y.left:
        return Left


class Tree(object):
    """A binary search tree."""

    def __init__(T, iterable=None):
        T.root = None
        if iterable is not None:
            for k in first_appearances(iterable):
                T.splay(k)

    @classmethod
    def from_encoding(cls, encoding):
        x = Node(None)
        for action in encoding:
            if action == 'l':
                x = x.insert_left(None)
            elif action == 'r':
                x = x.insert_right(None)
            elif action == 'p':
                x = x.parent
            else:
                raise ValueError("invalid movement, expected one of: l, r, p")
        while x.parent is not None:
            x = x.parent
        for k, z in enumerate(x.inorder_nodes(), start=1):
            z.key = k
        T = cls()
        T.root = x
        return T

    def findsert(T, k):
        """Find node in tree with key k, and create it if not present."""
        x = T.root
        y = None
        while x is not None:
            y = x
            if k < x:
                x = x.left
            elif k > x:
                x = x.right
            else:
                x = None
        if y is None:
            y = T.root = Node(k)
        if y > k:
            return y.insert_left(k)
        elif y < k:
            return y.insert_right(k)
        else:
            return y

    def splay(T, k):
        x = T.findsert(k)
        x.splay()
        T.root = x

    def move_to_root(T, k):
        x = T.findsert(k)
        x.move_to_root()
        T.root = x

    def simple_splay(T, k):
        x = T.findsert(k)
        x.simple_splay()
        T.root = x

    def inorder(T):
        return T.root.inorder_keys()

    def preorder(T):
        return T.root.preorder_keys()

    def postorder(T):
        return T.root.postorder_keys()

    def encoding(T):
        return T.root.subtree_encoding()


def first_appearances(s):
    """Return subsequence of s consisting of first occurance of each item.
    E.g. [1, 2, 4, 2, 3, 8, 4, 8, 5] -> [1, 2, 4, 3, 8, 5]"""
    seen = set()
    for x in s:
        if x not in seen:
            yield x
            seen.add(x)


def _test_tree():
    """Tree used for unit tests."""
    #        k
    #      /   \
    #      g   f
    #    /   \
    #   c    h
    #  / \   /\
    # a   b e  m
    k = Node("k")
    g = k.insert_left("g")
    c = g.insert_left("c")
    a = c.insert_left("a")
    b = c.insert_right("b")
    h = g.insert_right("h")
    e = h.insert_left("e")
    m = h.insert_right("m")
    f = k.insert_right("f")
    return [k, g, c, a, b, h, e, m, f]


class TestNode(unittest.TestCase):

    # Ordering Tests

    def test_equality(self):
        """Test that nodes compare equal in the expected way."""
        a = [Node(1), Node(1), Node(2), Node(3)]
        b = [Node(1), Node(1), Node(2), Node(3)]
        c = [Node(1), Node(2), Node(1), Node(3)]
        self.assertTrue(a == b)
        self.assertFalse(a == c)

    def test_ordering(self):
        """Test nodes all behave in correct fashion."""
        a = Node(5)
        b = Node(7)
        c = Node(5)
        self.assertTrue(a < b)
        self.assertFalse(b < a)
        self.assertTrue(a <= b)
        self.assertFalse(b <= a)
        self.assertTrue(a == c)
        self.assertFalse(a is c)
        # Compare with other objects
        self.assertTrue(a < 7)
        self.assertFalse(7 < a)
        self.assertTrue(5 < b)
        self.assertFalse(b < 5)
        self.assertTrue(a <= 7)
        self.assertFalse(7 <= a)

    # Pointer Change Tests

    def test_assignment_errors(self):
        """Test that the error checks work."""
        a = Node(5)
        b = a.right = Node(10)
        c = b.left = Node(4)
        d = c.right = Node(9)
        with self.assertRaises(AssertionError):
            c.left = 3
        with self.assertRaises(AssertionError):
            d.left = c
        self.assertTrue(a.right is b)
        self.assertTrue(b.left is c)
        self.assertTrue(c.right is d)
        self.assertTrue(
            a.left is
            b.right is
            c.left is
            d.left is
            d.right is
            a.parent is
            None
        )
        self.assertTrue(c is d.parent)
        self.assertTrue(b is c.parent)
        self.assertTrue(a is b.parent)

    def test_pointer_changes(self):
        """Ensure ThreadedNode has correct left/right pointers."""
        a = Node(5)
        b = Node(7)
        c = Node(3)
        d = Node(6)
        e = Node(4)
        a.right = b
        a.right.left = d
        a.left = c
        a.left.right = e
        self.assertTrue(a.right is b)
        self.assertTrue(a.right.left is d)
        self.assertTrue(a.right.right is None)
        self.assertTrue(a.right.left.left is None)
        self.assertTrue(a.left is c)
        self.assertTrue(a.left.right is e)
        self.assertTrue(a.left.left is None)
        self.assertTrue(a.left.right.left is None)
        # Test parents
        self.assertTrue(a.parent is None)
        self.assertTrue(b.parent is a)
        self.assertTrue(d.parent is b)
        self.assertTrue(c.parent is a)
        self.assertTrue(e.parent is c)
        b_new = Node(8)
        a.right = b_new
        # Test on removed block b
        self.assertTrue(b.left is d)
        self.assertTrue(b.parent is None)
        self.assertTrue(d.parent is b)
        # Test on old block
        self.assertTrue(c.parent is a)
        self.assertTrue(b_new.parent is a)
        self.assertTrue(a.right.left is None)
        l = a.left
        r = a.right
        a.left = None
        a.right = None
        self.assertTrue(l.parent is None)
        self.assertTrue(r.parent is None)
        self.assertTrue(a.left is a.right is a.parent is None)

    def test_insert(self):
        """Test insert methods work as expected."""
        x = Node("x")
        y = x.insert_right("y")
        z = y.insert_left("z")
        with self.assertRaises(AssertionError):
            x.insert_right("")
        with self.assertRaises(AssertionError):
            y.insert_left("")
        self.assertTrue(y.parent is x)
        self.assertTrue(z.parent is y)
        self.assertTrue(x.parent is None)
        null_slots = [x.left, y.right, z.left, z.right]
        for obj in null_slots:
            self.assertTrue(obj is None)
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
        c.rotate()
        g.rotate()
        for x, y in parent_pairs:
            self.assertTrue(x.parent is y)

    # Test walks

    def test_inorder(self):
        """Test inorder traversal."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue((a, c, b, g, e, h, m, k, f) == k.inorder_nodes())
        self.assertTrue((a, c, b, g, e, h, m, k, f) == k.inorder_keys())
        a.rotate()
        self.assertTrue((a, c, b, g, e, h, m, k, f) == k.inorder_nodes())
        h.rotate()
        self.assertTrue((a, c, b, g, e, h, m, k, f) == k.inorder_nodes())

    def test_preorder(self):
        """Test preorder traversal"""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue((k, g, c, a, b, h, e, m, f) == k.preorder_nodes())
        self.assertTrue((k, g, c, a, b, h, e, m, f) == k.preorder_keys())
        a.rotate()
        self.assertTrue((k, g, a, c, b, h, e, m, f) == k.preorder_nodes())
        h.rotate()
        self.assertTrue((k, h, g, a, c, b, e, m, f) == k.preorder_nodes())

    def test_postorder(self):
        """Test postorder traversal."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue((a, b, c, e, m, h, g, f, k) == k.postorder_nodes())
        self.assertTrue((a, b, c, e, m, h, g, f, k) == k.postorder_keys())
        a.rotate()
        self.assertTrue((b, c, a, e, m, h, g, f, k) == k.postorder_nodes())
        h.rotate()
        self.assertTrue((b, c, a, e, g, m, h, f, k) == k.postorder_nodes())

    def test_subtree_encoding(self):
        """Test that we get proper subtree encodings."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue("lllprpprlprppprp" == k.subtree_encoding())

    # Self Adjustment Tests

    def test_splay(self):
        """Test the splay method works."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        a.splay()
        self.assertTrue((a, k, c, g, b, h, e, m, f) == a.preorder_nodes())
        e.splay()
        self.assertTrue((e, a, c, g, b, k, h, m, f) == e.preorder_nodes())
        # sequential access
        nodes = [a, c, b, g, e, h, m, k, f]
        for x in nodes:
            x.splay()
        self.assertTrue((f, k, m, h, e, g, b, c, a) == f.preorder_nodes())
        for x in nodes:
            self.assertTrue(x.right is None)
        # Test simple splay zig-zag.
        a.splay()
        b.splay()
        self.assertTrue((b, a, c, h, g, e, k, m, f) == b.preorder_nodes())

    def test_simple_splay(self):
        """Test simple splay method works."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        a.simple_splay()
        self.assertTrue((a, k, c, g, b, h, e, m, f) == a.preorder_nodes())
        e.simple_splay()
        # First difference from splay
        self.assertTrue((e, a, g, c, b, k, h, m, f) == e.preorder_nodes())
        # Test zig-zag difference
        a.simple_splay()
        h.simple_splay()
        self.assertTrue((h, e, a, g, c, b, k, m, f) == h.preorder_nodes())
        # sequential access
        nodes = [a, c, b, g, e, h, m, k, f]
        for x in nodes:
            x.simple_splay()
        self.assertTrue((f, k, m, h, e, g, b, c, a) == f.preorder_nodes())
        for x in nodes:
            self.assertTrue(x.right is None)

    def test_move_to_root(self):
        """Test properties of move-to-root"""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        m.move_to_root()
        self.assertTrue((m, g, c, a, b, h, e, k, f) == m.preorder_nodes())
        e.move_to_root()
        self.assertTrue((e, g, c, a, b, m, h, k, f) == e.preorder_nodes())


class TestTree(unittest.TestCase):
    """Test the binary search tree."""

    def test_from_encoding(self):
        """Test a bst may be properly recreated from an encoding."""
        T = Tree.from_encoding('lllprpprlprppprp')
        self.assertEqual(9, len(T.inorder()))
        self.assertEqual(tuple(range(1, 10)), T.inorder())
        self.assertEqual((8, 4, 2, 1, 3, 6, 5, 7, 9), T.preorder())
        Q = Tree.from_encoding('lllprpprlprpppr')
        self.assertEqual(T.preorder(), Q.preorder())
        # More tests from before
        t1 = Tree.from_encoding("lllpprr")
        t2 = Tree.from_encoding("lrrppll")
        t3 = Tree.from_encoding("lrrppllp")
        t4 = Tree.from_encoding("lrrppllppp")
        self.assertEqual(t1.preorder(), t2.preorder())
        self.assertEqual(t1.preorder(), t3.preorder())
        self.assertEqual(t1.preorder(), t4.preorder())
        with self.assertRaises(ValueError):
            Tree.from_encoding("lrruull")
        with self.assertRaises(AttributeError):
            Tree.from_encoding("lrrppllpppp")
        with self.assertRaises(AssertionError):
            Tree.from_encoding("lrrppllppl")
        t = Tree.from_encoding("lllrpppprlprpp")
        self.assertEqual((5, 4, 3, 1, 2, 7, 6, 8), t.preorder())
        self.assertEqual((1, ), Tree.from_encoding("").preorder())

    def test_findsert(self):
        """Test we can find and insert a node."""
        T = Tree()
        for char in "kgcabhemkf":
            T.findsert(char)
        self.assertEqual("abcefghkm", "".join(T.inorder()))
        self.assertEqual("kgcabefhm", "".join(T.preorder()))
        for char in "kgcabhemkf":
            T.findsert(char)
        self.assertEqual("abcefghkm", "".join(T.inorder()))
        self.assertEqual("kgcabefhm", "".join(T.preorder()))
        for char in "kgcabhemkf":
            T.findsert(Node(char))
        self.assertEqual("abcefghkm", "".join(T.inorder()))
        self.assertEqual("kgcabefhm", "".join(T.preorder()))
        with self.assertRaises(AssertionError):
            T.findsert(Node("q"))


if __name__ == '__main__':
    unittest.main()
