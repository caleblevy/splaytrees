"""Implementation of a threaded node for a BST, outlined in ST85 for Splay
Trees. This ridiculously complicated way to implement nodes allows constant
time access to a nodes parents while keeping at most two pointers per node."""

import functools
import unittest


@functools.total_ordering
class ThreadedNode(object):
    """Threaded node using only two pointers for left, right, parent."""

    __slots__ = ("down", "side", "key")

    def __init__(x, key):
        x.key = key
        x.down = None
        x.side = None

    def __lt__(x, y):
        if isinstance(y, x.__class__):
            return x.key < y.key
        else:
            return x.key < y

    def __eq__(x, y):
        if isinstance(y, x.__class__):
            return x.key == y.key
        else:
            return x.key == y

    def __ne__(x, y):
        return not x == y

    @property
    def left(x):
        y = x.down
        if y is not None and y < x:
            return y
        else:
            return None

    @property
    def right(x):
        y = x.down
        if y is not None:
            if y > x:
                return y
            else:
                z = y.side
                if z is not x:
                    return z
                else:
                    return None
        else:
            return None

    @property
    def parent(x):
        y = x.side
        if y is not None:
            if y < x:
                return y  # x is right child of parent
            else:
                z = y.side
                if z is None:
                    return y  # x's parent y is the root
                elif x < z < y:
                    return z  # only case where y is not parent
                else:
                    return y  # proof this works is casewise
        else:
            return None

    def _detach(x):
        """Detach node x from its parent."""
        y = x.parent
        if y is None:
            return
        else:
            if x is y.right:
                z = y.left
                if z is None:
                    y.down = None
                else:
                    z.side = y
            else:
                z = y.right
                if z is None:
                    y.down = None
                else:
                    y.down = z
            x.side = None

    @left.deleter
    def left(x):
        if x.left is not None:
            x.left._detach()

    @right.deleter
    def right(x):
        if x.right is not None:
            x.right._detach()

    @parent.deleter
    def parent(x):
        x._detach()

    @left.setter
    def left(x, y):
        if not isinstance(y, x.__class__):
            raise TypeError("Left child must be of type ThreadedNoded")
        elif y.parent is not None:
            raise ValueError("Node y already has parent")
        elif x <= y:
            raise ValueError("Left child must be less than x")
        del x.left  # takes care of x's left pointers
        z = x.right
        if z is None:
            y.side = x
        else:
            y.side = z
        x.down = y

    @right.setter
    def right(x, y):
        if not isinstance(y, x.__class__):
            raise TypeError("Right child must be of type ThreadedNode")
        elif y.parent is not None:
            raise TypeError("Node y already has parent")
        elif y <= x:
            raise ValueError("Right child must be greater than x")
        del x.right
        z = x.left
        if z is None:
            x.down = y
        else:
            z.side = y
        y.side = x


class TestThreadedNode(unittest.TestCase):

    def test_ordering(self):
        """Test nodes all behave in correct fashion."""
        a = ThreadedNode(5)
        b = ThreadedNode(7)
        c = ThreadedNode(5)
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
        a = ThreadedNode(5)
        b = ThreadedNode(7)
        c = ThreadedNode(3)
        d = ThreadedNode(6)
        e = ThreadedNode(4)
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
        b_new = ThreadedNode(8)
        a.right = b_new
        # Test on removed block b
        self.assertTrue(b.left is d)
        self.assertTrue(b.parent is None)
        self.assertTrue(d.parent is b)
        # Test on old block
        self.assertTrue(c.parent is a)
        self.assertTrue(b_new.parent is a)
        self.assertTrue(a.right.left is None)

    # TODO: behavior of del x.left/x.right and treatment of parents is
    # semantically incorrect. Fix it.
    # TODO: detach should be a public API


if __name__ == '__main__':
    unittest.main()
