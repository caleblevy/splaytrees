from __future__ import print_function
"""Implementations a top-down splay tree using simple splaying."""

import functools
import unittest


def listmaker(generator):
    """Takes a generator function and wraps it to return a list of the items it
    generates.
    """
    @functools.wraps(generator)
    def lister(*args, **kwargs):
        return list(generator(*args, **kwargs))
    return lister


@functools.total_ordering
class _GlobalMax(object):
    """Represent a global maximum."""
    __slots__ = ()

    def __lt__(self, other):
        return False


@functools.total_ordering
class _GlobalMin(object):
    """Represent a global minimum."""
    __slots__ = ()

    def __lt__(self, other):
        return True


# Cannot use functools.total_ordering; LUB objects are not totally ordered
class LUB(object):
    """The Least Upper Bound of x: x < LUB(x) < y for all y > x."""
    __slots__ = ("_x")

    def __init__(self, x):
        self._x = x

    def __lt__(self, other):
        return self._x < other

    def __le__(self, other):
        return self._x < other

    def __ge__(self, other):
        return self._x >= other

    def __gt__(self, other):
        return self._x >= other

    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return NotImplemented

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self._x)


class GLB(object):
    """The Greatest Lower Bound of x: y < GLB(x) < x for all y < x."""
    __slots__ = ("_x")

    def __init__(self, x):
        self._x = x

    def __lt__(self, other):
        return self._x <= other

    def __le__(self, other):
        return self._x <= other

    def __ge__(self, other):
        return self._x > other

    def __gt__(self, other):
        return self._x > other

    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return NotImplemented

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self._x)


Inf = _GlobalMax()
NegInf = _GlobalMin()


class BinaryNode(object):
    __slots__ = ("left", "right", "key")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class SplayTree(object):

    __slots__ = ("root", "header")

    def __init__(self, iterable=None):
        self.root = None
        self.header = BinaryNode(None)
        if iterable is not None:
            for x in iterable:
                self.insert(x)

    def insert(self, key):
        """Insert key into tree."""
        if self.root is None:
            self.root = BinaryNode(key)
            return
        self.splay(key)
        if key == self.root.key:
            # raise KeyError("Key already in set")
            return
        n = BinaryNode(key)
        if key < self.root.key:
            n.left = self.root.left
            n.right = self.root
            self.root.left = None
        else:
            n.right = self.root.right
            n.left = self.root
            self.root.right = None
        self.root = n

    def remove(self, key):
        """Remove from the tree."""
        self.splay(key)
        if key != self.root.key:
            # Throw new error
            return
        # Now delete the root
        if self.root.left is None:
            self.root = self.root.right
        else:
            x = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = x

    def min(self):
        """Find the smallest item in the tree"""
        self.splay(NegInf)
        if self:
            return self.root.key
        else:
            raise ValueError("Cannot find min() of empty tree")

    def max(self):
        """Find the largest item in the tree."""
        self.splay(Inf)
        if self:
            return self.root.key
        else:
            raise ValueError("Cannot find max() of empty tree")

    def __contains__(self, key):
        """Find an item in the tree."""
        if not self:
            return False
        self.splay(key)
        # Must adjust itself even when raising error to maintain behavior
        # (otherwise we could spam it with invalid requests)
        if self.root.key != key:
            return False
        return True

    def __bool__(self):
        """Test if tree is logically empty."""
        return self.root is not None

    __nonzero__ = __bool__

    def splay(self, key):
        l = r = self.header
        t = self.root
        self.header.left = self.header.right = None
        while True:
            if key < t.key:
                if t.left is None:
                    break
                if key < t.left.key:
                    y = t.left  # Rotate right
                    t.left = y.right
                    y.right = t
                    t = y
                    if t.left is None:
                        break
                r.left = t  # Link right
                r = t
                t = t.left
            elif key > t.key:
                if t.right is None:
                    break
                if key > t.right.key:
                    y = t.right  # rotate left
                    t.right = y.left
                    y.left = t
                    t = y
                    if t.right is None:
                        break
                l.right = t  # link left
                l = t
                t = t.right
            else:
                break
        l.right = t.left  # assemble
        r.left = t.right
        t.left = self.header.right
        t.right = self.header.left
        self.root = t

    @listmaker
    def inorder_stack(self):
        """Traverse descendents in symmetric order."""
        # Taken from http://www.geeksforgeeks.org/inorder-tree-traversal-without-recursion/
        current = self.root
        stack = []
        done = False
        while not done:
            if current is not None:
                stack.append(current)
                current = current.left
            else:
                if stack:
                    current = stack.pop()
                    yield current.key
                    current = current.right
                else:
                    done = True

    # My idea of "successor" requires at least four things.
    # 1) I will define iteration over the tree by repeated calls to successor
    # 2) I need to be able to access, insert and delete items DURING iteration
    # 3) I need to guarentee at least the O(log n) time bounds, homefully the
    #    other theorems as well
    # 4) In particular, if the sequential access theorem holds for simple
    #    splaying, then iterating in symmetric order should require no more
    #    than linear time assuming no other access/insert/delete during the
    #    loop.
    # 5) It should not require parent pointers if at all possible.
    #
    # For the 3rd point, since insertion can/will allow us to increase the size
    # of the tree as we iterate, or for that matter we can delete and add back
    # our current node, I merely require that at each step in the iteration,
    # the next key yielded is the successor of the previous yielded key at the
    # time next() is called.
    #
    # There are several ways of iterating the tree in symmetric order, so I
    # will outline mine, and their advantages/disadvantages to red-black trees.
    # First, the recursive solution is out. Using recursion in production
    # environments is already usually not the best choice, but we can usually
    # get away with it in BALANCED binary trees since they guarentee
    # logorithmic height, and so we generally won't cause a stack overflow with
    # the number of nodes we can store in memory (or even on disk).
    #
    # Iteration is out, as is recursion, even with parent pointers, first for
    # failing to meet (2), and then for more subtle reasons. Even with the
    # parent pointers, the structure of splay trees does not guarentee that,
    # should we access elements in the iteration, that we will have linear
    # time to travel between. Imagine an adversary lining up the path at each
    # step. (should see if example can be constructed).
    #
    # Now, I would like to just "top-down splay" directly from i.key to
    # (i+1).key just like we do when we want to find a key. Now we don't even
    # know what key we are looking for, which is a problem. See, not knowing
    # "where" a key is is not the problem, but knowing "when to stop".
    #
    # Even for the case of finding the max or min, we can actually be more
    # clever than Sleater (not easy to do!) and search for a key defined to be
    # larger than all others. Why not just define a "supremum" of x.key, return
    # sup(x)>y iff y>x?
    #
    # The problem is illustrated by this great program:
    # http://stackoverflow.com/a/6335263. Probably my favorite of those that
    # failed because its constant space, O(log n) time, and does not requre
    # finding the key itself initially.
    #
    # The very issue is in the single constant it stores. Search for 13 in
    #
    #    20
    #   /
    #  10
    #   \
    #   11
    #    \
    #    12
    #     \
    #     13
    #
    # We won't know that we've hit the right node until we go all the way down
    # the right branch at 10. We then need to either go down twice to find the
    # key and then splay (for guarentees), or splay multiple times (no
    # guarentees).
    #
    # The Inf and NegInf do not face this problem since they are not it left or
    # right subtrees.
    #
    # I believe even holding rank info, you would need to look for rank of key,
    # then go to next rank, so I think this problem is inherent.
    #
    # Proper way to do it: splay to the key itself, then find the successor
    # using the LUB/GLB objects. O(log(n)) since its two splays.

    def successor(self, key):
        """Find the smallest element greater than key."""
        if not self:
            raise KeyError("Empty tree has no successor")
        self.splay(key)
        self.splay(LUB(key))
        return self.root.key

    def predecessor(self, key):
        """Find the largest element smaller than key."""
        if not self:
            raise KeyError("Empty tree has no predecessor")
        self.splay(key)
        self.splay(GLB(key))
        return self.root.key

    def __iter__(self):
        """Traverse the elements of the tree in Symmetric Order."""
        # Use splaying to do this and preserve our running time heuristics.
        # If traversal conjecture is true for simple splaying, this take linear
        # time assuming the tree is not altered.
        if self.root is None:
            return
        prev_key = NegInf
        key = self.min()
        while prev_key < key:
            yield key
            prev_key = key
            key = self.successor(prev_key)

    def __reversed__(self):
        """Traverse the elements of the tree in reverse Symmetric Order."""
        if self.root is None:
            return
        prev_key = Inf
        key = self.max()
        while key < prev_key:
            yield key
            prev_key = key
            key = self.predecessor(prev_key)


class TestSimpleSplay(unittest.TestCase):

    def test_simple_splaying(self):
        t = SplayTree()
        nums = 40000
        gap = 307
        print("Checking... (no bad output means success)")

        i = gap
        while i:
            t.insert(i)
            i = (i + gap) % nums
        print("Inserts complete")

        for i in range(1, nums, 2):
            t.remove(i)
        print("Removes complete")

        self.assertEqual(t.min(), 2)
        self.assertEqual(t.max(), nums-2)

        for i in range(2, nums, 2):
            self.assertIn(i, t)
            self.assertEqual(i, t.root.key)

        for i in range(1, nums, 2):
            self.assertNotIn(i, t)
            self.assertIn(i, {t.root.key-1, t.root.key+1})

        100 in t  # Splaying of random things
        18199 in t
        29512 in t
        39153 in t
        20711 in t
        36126 in t

        self.assertEqual(39136, t.root.right.left.right.key)

    def test_tree_truthiness(self):
        """Test tree is False iff it is empty."""
        r = SplayTree()
        r.insert(100)
        s = SplayTree()
        self.assertTrue(r)
        self.assertFalse(not r)
        self.assertFalse(s)
        self.assertTrue(not s)

    def test_successor_and_predecessor(self):
        """Test we get the same preorder and postorder."""


class TestExtrema(unittest.TestCase):

    def test_least_upper_bound(self):
        """Test the necessary properties of the Least Upper Bound"""
        a = LUB(7)
        # Test when called by reflected methods
        self.assertTrue(7 < a)
        self.assertTrue(7 <= a)
        self.assertFalse(7 > a)
        self.assertFalse(7 >= a)
        # Test regular methods
        self.assertTrue(a > 7)
        self.assertTrue(a >= 7)
        self.assertFalse(a < 7)
        self.assertFalse(a <= 7)
        # Test reflected methods of upper bound
        self.assertTrue(8 > a)
        self.assertTrue(8 >= a)
        self.assertFalse(8 < a)
        self.assertFalse(8 <= a)
        # Test regular methods of upper bound
        self.assertTrue(a < 8)
        self.assertTrue(a <= 8)
        self.assertFalse(a > 8)
        self.assertFalse(a >= 8)
        # Test reflected methods of lower bound
        self.assertTrue(6 < a)
        self.assertTrue(6 <= a)
        self.assertFalse(6 > a)
        self.assertFalse(6 >= a)
        # Test regular methods of lower bound
        self.assertTrue(a > 6)
        self.assertTrue(a >= 6)
        self.assertFalse(a < 6)
        self.assertFalse(a <= 6)

    def test_greatest_lower_bound(self):
        """Test the necessary properties of the greatest lower bound."""
        b = GLB(7)
        # Test the reflected methods against itself
        self.assertTrue(7 > b)
        self.assertTrue(7 >= b)
        self.assertFalse(7 < b)
        self.assertFalse(7 <= b)
        # Test the regular methods against itself
        self.assertTrue(b < 7)
        self.assertTrue(b <= 7)
        self.assertFalse(b >= 7)
        self.assertFalse(b > 7)
        # Test the reflected methods of the upper bounds
        self.assertTrue(8 > b)
        self.assertTrue(8 >= b)
        self.assertFalse(8 < b)
        self.assertFalse(8 <= b)
        # Test the regular methods of upper bounds
        self.assertTrue(b < 8)
        self.assertTrue(b <= 8)
        self.assertFalse(b > 8)
        self.assertFalse(b >= 8)
        # Test the reflected methods of lower bounds
        self.assertTrue(6 < b)
        self.assertTrue(6 <= b)
        self.assertFalse(6 > b)
        self.assertFalse(6 >= b)
        # Test the regular methods of lower bounds
        self.assertTrue(b > 6)
        self.assertTrue(b >= 6)
        self.assertFalse(b < 6)
        self.assertFalse(b <= 6)


if __name__ == '__main__':
    unittest.main()
