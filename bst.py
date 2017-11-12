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
        x.key = key
        x._left = x._right = x._parent = None

    def __repr__(x):
        return "%s(%s)" % (x.__class__.__name__, x.key)

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
            if not is_node(y):
                raise TypeError("invalid type for left child: %s" % type(y))
            if y.parent is not None:
                raise ValueError("Node y already has parent")
            detach(x.left)
            x._left = y
            y._parent = x

    @right.setter
    def right(x, y):
        if y is None:
            detach(x.right)
        else:
            if not is_node(y):
                raise TypeError("invalide type for right child: %s" % type(y))
            if y.parent is not None:
                raise ValueError("Node y already has parent")
            detach(x.right)
            x._right = y
            y._parent = x

    def insert_left(x, k):
        """Insert new node with key k to the left of x."""
        if x.left is not None:
            raise ValueError("node already has left child")
        x.left = Node(k)
        return x.left

    def insert_right(x, k):
        """Insert new node with key k to the right of x."""
        if x.right is not None:
            raise ValueError("node already has right child")
        x.right = Node(k)
        return x.right

    def rotate(x):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
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
        """Return tuple of the nodes in a given walk."""
        return tuple(x._walk(order))

    def walk_nodes(x):
        """Depth first search of tree edges, always going left before right."""
        return x._walk_nodes()

    def preorder_nodes(x):
        """Return preorder of the subtree rooted at x."""
        return x._walk_nodes(-1)

    def inorder_nodes(x):
        """Return nodes of subtree rooted at x in symmetric order."""
        return x._walk_nodes(0)

    def postorder_nodes(x):
        """Return postorder of the subtree rooted at x."""
        return x._walk_nodes(1)

    def _walk_keys(x, order=None):
        """Return tuple of the keys a given walk."""
        return tuple(n.key for n in x._walk(order))

    def walk_keys(x):
        """Output tree keys in preorder."""
        return x._walk_keys()

    def preorder_keys(x):
        """Output tree keys in preorder."""
        return x._walk_keys(-1)

    def inorder_keys(x):
        """Output keys in symmetric order."""
        return x._walk_keys(0)

    def postorder_keys(x):
        """Output keys in postorder."""
        return x._walk_keys(1)


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
        with self.assertRaises(TypeError):
            c.left = 3
        with self.assertRaises(ValueError):
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
        with self.assertRaises(ValueError):
            x.insert_right("")
        with self.assertRaises(ValueError):
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


if __name__ == '__main__':
    unittest.main()
