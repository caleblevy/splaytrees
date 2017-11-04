"""Implementation of a node maintaining structural properties (depth and
turn-depth) and potentials (weight, size, rank, potential)."""

import functools
import unittest


@functools.total_ordering
class Node(object):
    """Node object maintaining all properties under rotation."""

    # __slots__ = ("_left", "_right", "_parent", "key",
    #              "_size", "_weight", "_rank", "_potential",
    #              "_depth", "_turn_depth")

    def __init__(x, key, weight=1):
        x.key = key
        x.weight = weight
        x.left = x.right = x.parent = None

    # @property
    # def left(x):
    #     return x._left

    # @left.setter
    # def left(x, y):
    #     if not (is_node(y) or y is None):
    #         raise TypeError("Node's left child must be a node.")
    #     elif y.key >= x.

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


def is_node(x):
    return isinstance(x, Node)


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


if __name__ == '__main__':
    unittest.main()