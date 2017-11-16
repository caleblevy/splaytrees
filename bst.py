"""Simple, bare-bones implementation of a splay tree and a binary search
tree."""

import functools
import unittest

__all__ = [
    "Node",
    "Tree",
    "mr_execution", "splay_execution", "dual_execution",
    "mr_nodes", "splay_nodes", "dual_nodes",
    "wilber2",
    "mr_cost", "mr_crossing_cost", "mr_inside_cost", "mr_critical_cost",
    "splay_cost", "splay_crossing_cost", "splay_inside_cost",
    "splay_critical_cost",
    "last"
]


def maker(maptype):
    """Turn a generator into a specified type of sequence."""
    def outputter(generator):
        @functools.wraps(generator)
        def mapper(*args, **kwargs):
            return maptype(generator(*args, **kwargs))
        return mapper
    return outputter


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

    def reset(x):
        """Reset the tree containing x to its initial state."""
        r = x.root()
        for node in r.inorder_nodes():
            node.parent = node.parent_init
            node.left = node.left_init
            node.right = node.right_init
        return r.root()

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
        while x.parent is not None:
            x = x.parent
        return x

    # Path encodings.

    @maker(tuple)
    def path(x):
        while x is not None:
            yield x
            x = x.parent

    @maker(tuple)
    def crossing_nodes(x):
        yield x
        y = x.parent
        while y is not None:
            z = y.parent
            if z is None:
                yield y
            else:
                if ((y is z.left and x is y.right) or
                        (y is z.right and x is y.left)):
                    yield y
            x = y
            y = x.parent

    @maker(tuple)
    def inside_nodes(x):
        for x in x.crossing_nodes():
            if x.parent is not None:
                yield x.parent

    @maker(tuple)
    def critical_subpath(x):
        y = x.parent
        for x in x.crossing_nodes():
            if x is not y:
                yield x
            y = x.parent
            if y is not None:
                yield y

    def crossing_split(x):
        """Split crossing nodes into left, right and center."""
        c = x.crossing_nodes()
        l = c[1::2]
        r = c[2::2]
        z = x.parent
        if z is not None and x is z.left:
            l, r = r, l
        return (x, l, r)

    def inside_split(x):
        """Split inside nodes into left and right."""
        b = x.inside_nodes()
        l = b[0::2]
        r = b[1::2]
        z = x.parent
        if z is not None and x is z.left:
            l, r = r, l
        return (l, r)

    def critical_split(x):
        y = x
        z = y.parent
        if z is None:
            return (x, (), ())
        elif y is z.left:
            b = False
        else:
            b = True
        l = []
        r = []
        for y in y.crossing_nodes():
            if y is not z:
                if not b:
                    l.append(y)
                else:
                    r.append(y)
            b = not b
            z = y.parent
            if z is not None:
                if y is z.left:
                    r.append(z)
                else:
                    l.append(z)
        if x is l[0]:
            l = l[1:]
        else:
            r = r[1:]
        return (x, tuple(l), tuple(r))

    def crossing_sorted(x):
        x, l, r = x.crossing_split()
        return tuple(reversed(l)) + (x, ) + r

    def inside_sorted(x):
        l, r = x.inside_split()
        return tuple(reversed(l)) + r

    def critical_sorted(x):
        x, l, r = x.critical_split()
        return tuple(reversed(l)) + (x, ) + r


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
    def from_encoding(cls, encoding=None):
        T = cls()
        if encoding is None:
            return T
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
        T.root = x
        return T

    def find(T, k):
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
        x = T.find(k)
        x.splay()
        T.root = x

    def move_to_root(T, k):
        x = T.find(k)
        x.move_to_root()
        T.root = x

    def simple_splay(T, k):
        x = T.find(k)
        x.simple_splay()
        T.root = x

    def inorder(T):
        return T.root.inorder_keys() if T else ()

    def preorder(T):
        return T.root.preorder_keys() if T else ()

    def postorder(T):
        return T.root.postorder_keys() if T else ()

    def encoding(T):
        if T:
            return T.root.subtree_encoding()
        else:
            return None

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


# Executors and nodes


def mr_execution(s):
    """Return tree and node state of move-to-root execution."""
    T = Tree()
    for k in s:
        x = T.find(k)
        yield (T, x)
        x.move_to_root()
        T.root = x


def splay_execution(s):
    """Return tree and node state of splay execution."""
    T = Tree()
    for k in s:
        x = T.find(k)
        yield (T, x)
        x.splay()
        T.root = x


def dual_execution(s):
    """Return tree and node state of move-to-root and splay in parallel."""
    s = list(s)
    mr = mr_execution(s)
    sp = splay_execution(s)
    for k in s:
        yield next(mr), next(sp)


def mr_nodes(s):
    for (_, x) in mr_execution(s):
        yield x


def splay_nodes(s):
    for (_, x) in splay_execution(s):
        yield x


def dual_nodes(s):
    for (M, x), (S, y) in dual_execution(s):
        yield (x, y)


# Different Counts


def wilber2(s):
    """Compute the value of Wilber's second lower bound."""
    w2 = 0
    seen = set()
    for x in mr_nodes(s):
        w2 += len(x.crossing_nodes())
        if x.key not in seen:
            w2 -= 1
            seen.add(x.key)
    return w2+1 if w2 else w2


def mr_cost(s):
    return sum(len(x.path()) for x in mr_nodes(s))


def mr_crossing_cost(s):
    return sum(len(x.crossing_nodes()) for x in mr_nodes(s))


def mr_inside_cost(s):
    return sum(len(x.inside_nodes()) for x in mr_nodes(s))


def mr_critical_cost(s):
    return sum(len(x.critical_subpath()) for x in mr_nodes(s))


def splay_cost(s):
    return sum(len(x.path()) for x in splay_nodes(s))


def splay_crossing_cost(s):
    return sum(len(x.crossing_nodes()) for x in splay_nodes(s))


def splay_inside_cost(s):
    return sum(len(x.inside_nodes()) for x in splay_nodes(s))


def splay_critical_cost(s):
    return sum(len(x.critical_subpath()) for x in splay_nodes(s))


def last(iterable):
    """Return the last element of an iterable."""
    for x in iterable:
        pass
    return x


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

    # Test Path Functions

    def test_path(self):
        """Test the path is correctly yielded."""
        [k, g, c, a, b, h, e, m, f] = _test_tree()
        self.assertTrue((k, ) == k.path())
        self.assertTrue((a, c, g, k) == a.path())
        self.assertTrue((b, c, g, k) == b.path())


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

    def test_find(self):
        """Test we can find and insert a node."""
        T = Tree()
        for char in "kgcabhemkf":
            T.find(char)
        self.assertEqual("abcefghkm", "".join(T.inorder()))
        self.assertEqual("kgcabefhm", "".join(T.preorder()))
        for char in "kgcabhemkf":
            T.find(char)
        self.assertEqual("abcefghkm", "".join(T.inorder()))
        self.assertEqual("kgcabefhm", "".join(T.preorder()))
        for char in "kgcabhemkf":
            T.find(Node(char))
        self.assertEqual("abcefghkm", "".join(T.inorder()))
        self.assertEqual("kgcabefhm", "".join(T.preorder()))
        with self.assertRaises(AssertionError):
            T.find(Node("q"))

    def test_empty_tree(self):
        """Test methods on empty tree."""
        T = Tree()
        T.splay(1)
        self.assertEqual((1, ), T.preorder())
        self.assertEqual((), Tree().inorder())
        self.assertEqual((), Tree().preorder())
        self.assertEqual((), Tree().postorder())
        self.assertEqual((), Tree.from_encoding().preorder())
        self.assertEqual((1, ), Tree.from_encoding("").preorder())

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


def _new_path(encoding):
    """Return new path, since interface not set up."""
    T = Tree.from_encoding(encoding)
    return T.find(T.postorder()[0])


class TestWilber(unittest.TestCase):
    """Test Wilber bounds and related functionality."""
    from wilber import critical_nodes
    from wilber import wilber2 as w2
    from random import shuffle

    def test_crossings(self):
        """Test nodes correctly cross."""
        x = _new_path("rrrllrlrrllrlr")
        self.assertEqual(
            (9, 8, 10, 7, 12, 5, 13, 4, 15, 1),
            x.crossing_nodes())
        y = _new_path("lllrrr")
        self.assertEqual((4, 1, 7), y.crossing_nodes())
        self.assertEqual(
            (9, (8, 7, 5, 4, 1), (10, 12, 13, 15)),
            x.crossing_split())
        self.assertEqual((4, (1, ), (7, )), y.crossing_split())
        n = Node(None)
        self.assertEqual((n, ), n.crossing_nodes())
        z = _new_path("llrlrrll")
        self.assertEqual((4, 6, 2, 7, 1, 9), z.crossing_nodes())
        self.assertEqual((4, (2, 1), (6, 7, 9)), z.crossing_split())
        self.assertEqual(
            (1, 4, 5, 7, 8, 9, 10, 12, 13, 15),
            x.crossing_sorted())
        self.assertEqual((1, 4, 7), y.crossing_sorted())
        self.assertEqual((1, 2, 4, 6, 7, 9), z.crossing_sorted())

    def test_inside(self):
        """Test parents of crossing nodes."""
        x = _new_path("rrrllrlrrllrlr")
        y = _new_path("lllrrr")
        self.assertEqual((8, 10, 7, 11, 6, 13, 4, 14, 3), x.inside_nodes())
        self.assertEqual((3, 5), y.inside_nodes())
        self.assertEqual(((8, 7, 6, 4, 3), (10, 11, 13, 14)), x.inside_split())
        self.assertEqual(((3, ), (5, )), y.inside_split())
        n = Node(None)
        self.assertEqual((), n.inside_nodes())
        z = _new_path("llrlrrll")
        self.assertEqual((5, 3, 7, 1, 8), z.inside_nodes())
        self.assertEqual(((3, 1), (5, 7, 8)), z.inside_split())
        self.assertEqual(
            (3, 4, 6, 7, 8, 10, 11, 13, 14),
            x.inside_sorted())
        self.assertEqual((3, 5), y.inside_sorted())
        self.assertEqual((1, 3, 5, 7, 8), z.inside_sorted())

    def test_critical(self):
        """Test the critical nodes."""
        x = _new_path("rrrllrlrrllrlr")
        y = _new_path("lllrrr")
        self.assertEqual(
            (9, 8, 10, 7, 11, 12, 6, 5, 13, 4, 14, 15, 3, 1),
            x.critical_subpath())
        self.assertEqual((4, 3, 1, 5, 7), y.critical_subpath())
        self.assertEqual(
            (9, (8, 7, 6, 5, 4, 3, 1), (10, 11, 12, 13, 14, 15)),
            x.critical_split())
        self.assertEqual((4, (3, 1), (5, 7)), y.critical_split())
        z = _new_path("llrlrrll")
        self.assertEqual((4, 5, 6, 3, 2, 7, 1, 8, 9), z.critical_subpath())
        self.assertEqual((4, (3, 2, 1), (5, 6, 7, 8, 9)), z.critical_split())
        self.assertEqual(
            (1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
            x.critical_sorted())
        self.assertEqual((1, 3, 4, 5, 7), y.critical_sorted())
        self.assertEqual((1, 2, 3, 4, 5, 6, 7, 8, 9), z.critical_sorted())

    def test_wilber_example(self):
        """Test Wilber2 on paper example."""
        s = list("aihjgfclkendbpmoi")
        for (t, _) in mr_execution(s[:-1]):
            pass
        x = t.find("i")
        w = tuple(reversed("obkfjhi"))
        v = tuple(reversed("mekgjh"))
        self.assertEqual(w, x.crossing_nodes())
        self.assertEqual(v, x.inside_nodes())
        self.assertEqual(37, wilber2(s))

    def compare_to_wilber2(self):
        """Compare paths and counts to wilber2 exactly."""
        s = list("aihjgfclkendbpmoi")
        self.assertEqual(w2(s), wilber2(s))
        seen = set()
        for i, x in enumerate(mr_execution(s), start=1):
            b_w2 = tuple(critical_nodes(s, i)[3])
            c_w2 = tuple(critical_nodes(s, i)[1])
            b = tuple(reversed(x.inside_nodes()))
            c = tuple(reversed(x.crossing_nodes()))
            if x.key not in seen:
                b = b[:-1]
                c = c[:-1]
            self.assertEqual(b_w2, b)
            self.assertEqual(c_w2, c)
        r = list(range(50)) + list(range(1, 70, 5))
        shuffle(r)
        self.assertEqual(w2(r), wilber2(r))


if __name__ == '__main__':
    unittest.main()
