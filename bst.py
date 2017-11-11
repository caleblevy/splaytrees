"""Simple, bare-bones implementation of a splay tree and a binary search
tree."""

import functools
import unittest


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
        if not is_node(y):
            raise TypeError("Left child must be of type ThreadedNoded")
        if y.parent is not None:
            raise ValueError("Node y already has parent")
        elif x <= y:
            raise ValueError("Left child must be less than x")
        detach(x.left)
        x._left = y
        y._parent = x

    @right.setter
    def right(x, y):
        if not is_node(y):
            raise TypeError("Left child must be of type ThreadedNoded")
        if y.parent is not None:
            raise ValueError("Node y already has parent")
        elif y <= x:
            raise ValueError("Right child must be greater than x")
        detach(x.right)
        x._right = y
        y._parent = x

    def rotate(x):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        y = x.parent
        # Ensures x < y
        if x is y.right:
            x, y = y, x
        if x is y.left:
            # Shift around subtree
            b = x.right
            y.left = b
            if is_node(b):
                b.parent = y
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
            b = y.left
            x.right = b
            if is_node(b):
                b.parent = x
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

    def test_error(self):
        """Test that the error checks work."""
        a = Node(5)
        b = a.right = Node(10)
        c = b.left = Node(4)
        d = c.right = Node(9)
        with self.assertRaises(TypeError):
            c.left = 3
        with self.assertRaises(ValueError):
            d.left = Node(11)
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
    unittest.main()