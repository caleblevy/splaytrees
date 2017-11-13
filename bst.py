"""Simple, bare-bones implementation of a splay tree and a binary search
tree."""

import functools
import unittest


class Placeholder(object):
    """Slot for a null node, allowing them to be linked together."""

    __slots__ = ("parent_init")

    def __init__(p):
        p.parent_init = None


@functools.total_ordering
class Node(object):
    """Node object maintaining all properties under rotation."""

    __slots__ = ("parent", "left", "right", "key",
                 "parent_init", "left_init", "right_init")

    def __init__(x, key):
        assert not is_node(key)
        x.key = key
        x.parent = x.parent_init = None
        x.left = x.left_init = Placeholder()
        x.right = x.right_init = Placeholder()
        x.left.parent_init = x.right.parent_init = x

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

    def insert_left(x, k):
        """Insert new node with key k to the left of x."""
        assert x.left is None
        x.left = Node(k)
        return x.left

    def insert_left(x, k):
        """Insert a node to the left of x."""
        assert not is_node(x.left)
        p = x.left
        x_init = p.parent_init
        y = Node(k)
        y.parent_init = x_init
        if p is x_init.left_init:
            x_init.left_init = y
        else:
            x_init.right_init = y
        x.left = y
        y.parent = x
        return y

    def insert_right(x, k):
        """Insert new node with key k to the right of x."""
        assert not is_node(x.right)
        p = x.right
        x_init = p.parent_init
        y = Node(k)
        y.parent_init = x_init
        if p is x_init.left_init:
            x_init.left_init = y
        else:
            x_init.right_init = y
        x.right = y
        y.parent = x
        return y

    def rotate(x):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        y = x.parent
        # Ensures x < y
        if x is y.right:
            x, y = y, x
        if x is y.left:
            # Shift around subtree
            w = x.right
            y.left = w
            if is_node(w):
                w.parent = y
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
            w = y.left
            x.right = w
            if is_node(w):
                w.parent = x
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
                if not is_node(y):
                    l = True
                else:
                    if order == "":
                        yield "l"
                    x = y
            elif not r:
                if order == 0:
                    yield x
                y = x.right
                if not is_node(y):
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

    def walk_nodes(x):
        return tuple(x._walk())

    def preorder_nodes(x):
        return tuple(x._walk(-1))

    def inorder_nodes(x):
        return tuple(x._walk(0))

    def postorder_nodes(x):
        return tuple(x._walk(1))

    def walk_keys(x):
        return tuple(n.key for n in x._walk())

    def preorder_keys(x):
        return tuple(n.key for n in x._walk(-1))

    def inorder_keys(x):
        return tuple(n.key for n in x._walk(0))

    def postorder_keys(x):
        return tuple(n.key for n in x._walk(1))

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

    def root(x):
        """Return the root of x."""
        while x.parent is not None:
            x = x.parent
        return x

    def reset(x):
        """Reset the tree containing x to its initial state."""
        r = x.root()
        for node in r.inorder_nodes():
            node.parent = node.parent_init
            node.left = node.left_init
            node.right = node.right_init
        return r.root()


def is_node(x):
    return isinstance(x, Node)


class Tree(object):
    """A binary search tree."""

    def __init__(T, iterable=None):
        T.root = None
        if iterable is not None:
            for k in first_appearances(iterable):
                T.splay(k)
        T.reset()

    def __repr__(T):
        return "%s(%r)" % (type(T).__name__, list(T.preorder()))

    def __bool__(T):
        return T.root is not None

    __nonzero__ = __bool__

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
        x = x.root()
        for k, z in enumerate(x.inorder_nodes(), start=1):
            z.key = k
        T = cls()
        T.root = x
        return T

    def findsert(T, k):
        """Find node in tree with key k, and create it if not present."""
        x = T.root
        y = None
        while is_node(x):
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
        return T.root.inorder_keys() if T else ()

    def preorder(T):
        return T.root.preorder_keys() if T else ()

    def postorder(T):
        return T.root.postorder_keys() if T else ()

    def reset(T):
        if T:
            T.root = T.root.reset()

    def checkpoint(T):
        """Create new copy of T in current shape."""
        T = Tree(T.preorder())
        T.reset()
        return T


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
            self.assertFalse(is_node(obj))
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
        self.assertFalse(is_node(a.left))
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
            self.assertFalse(is_node(x.right))
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
            self.assertFalse(is_node(x.right))

    def test_move_to_root(self):
        """Test properties of move-to-root"""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        m.move_to_root()
        self.assertTrue((m, g, c, a, b, h, e, k, f) == m.preorder_nodes())
        e.move_to_root()
        self.assertTrue((e, g, c, a, b, m, h, k, f) == e.preorder_nodes())

    def test_reset(self):
        """Test tree is properly reset"""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        orig = k.preorder_nodes()
        k.reset()
        self.assertTrue(orig == k.preorder_nodes())
        a.splay()
        self.assertFalse(orig == k.preorder_nodes())
        a.reset()
        self.assertTrue(orig == k.preorder_nodes())
        for x in k.inorder_nodes():
            x.splay()
        x.reset()
        self.assertTrue(orig == k.preorder_nodes())


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

    def test_empty_tree(self):
        """Test methods on empty tree."""
        T = Tree()
        T.splay(1)
        self.assertEqual((1, ), T.preorder())
        self.assertEqual((), Tree().inorder())
        self.assertEqual((), Tree().preorder())
        self.assertEqual((), Tree().postorder())

    def test_reset(self):
        """Test tree is reset."""
        T = Tree()
        for k in "kgcabhemkf":
            T.splay(k)
        self.assertEqual("fecbakghm", "".join(T.preorder()))
        T.reset()
        self.assertEqual("abcefghkm", "".join(T.inorder()))
        self.assertEqual("kgcabefhm", "".join(T.preorder()))

    def test_checkpoint(self):
        """Test tree is copied in the appropriate state."""
        T = Tree("kgcabhemkf")
        for k in T.inorder():
            T.splay(k)
        Q = T.checkpoint()
        self.assertEqual("mkhgfecba", "".join(Q.preorder()))
        Q.reset()
        self.assertEqual("mkhgfecba", "".join(Q.preorder()))


if __name__ == '__main__':
    unittest.main()
