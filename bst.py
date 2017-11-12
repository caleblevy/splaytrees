"""Simple, bare-bones implementation of a splay tree and a binary search
tree."""

import functools
import unittest


Left = object()
Right = object()


def maker(maptype):
    """Turn a generator into a specified type of sequence."""
    def outputter(generator):
        @functools.wraps(generator)
        def mapper(*args, **kwargs):
            return maptype(generator(*args, **kwargs))
        return mapper
    return outputter


@functools.total_ordering
class Node(object):
    """Node object maintaining all properties under rotation."""

    def __init__(x, key):
        x.key = key
        x._left = x._right = x._parent = None

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

    @maker(tuple)
    def walk(x):
        """Do all three edge traversals at once."""
        z = x.parent
        l = r = False  # l is true if all node's in x.left are visited
        while True:
            yield x
            if not l:
                y = x.left
                if y is None:
                    l = True
                else:
                    x = y
            elif not r:
                y = x.right
                if y is None:
                    r = True
                else:
                    x = y
            else:
                y = x.parent
                if y is z:
                    return
                elif x is y.left:
                    r = False
                x = y

    @maker(tuple)
    def preorder(x):
        """Return preorder of the subtree rooted at x."""
        first = set()
        for x in x.walk():
            if x not in first:
                yield x
                first.add(x)

    @maker(tuple)
    def inorder(x):
        """Return nodes of subtree rooted at x in symmetric order."""
        first = set()
        second = set()
        for x in x.walk():
            if x in first and x not in second:
                yield x
                second.add(x)
            first.add(x)


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


class TestNode(unittest.TestCase):

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

    def test_left_right_insert(self):
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

    def test_error(self):
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

    def test_rotation(self):
        """Test rotation works properly."""
        # a = Node()
        # b = Node()
        # c = Node()
        # d = Node()


if __name__ == '__main__':
    r = Node(0)
    a = r.right = Node(1)
    b = a.left = Node(2)
    c = a.right = Node(3)
    # b.rotate()
    print(list(n.key for n in a.walk()))
    print(list(n.key for n in a.preorder()))
    print(list(n.key for n in a.inorder()))
    unittest.main()