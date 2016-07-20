"""Implementations a top-down splay tree using simple splaying."""

import functools


@functools.total_ordering
class _GlobalMax(object):
    """Represent a global maximum."""

    def __lt__(self, other):
        return False


class _GlobalMin(object):
    """Represent a global minimum."""

    def __lt__(self, other):
        return True


Inf = _GlobalMax()
NegInf = _GlobalMin()


class BinaryNode(object):
    __slots__ = ("left", "right", "key")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def inorder_recursive(self):
        """Traverse descendents in symmetric order recursively."""
        if self.left is not None:
            for x in self.left.inorder_recursive():
                yield x
        yield self.key
        if self.right is not None:
            for x in self.right.inorder_recursive():
                yield x


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

    def __iter__(self):
        """Traverse the elements of the tree in Symmetric Order."""
        # Use splaying to do this and preserve our running time heuristics
        if self.root is None:
            return
        min = 1


if __name__ == '__main__':
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

    if t.min() != 2 or t.max() != nums-2:
        print("Find min or find max error")

    for i in range(2, nums, 2):
        if i not in t or t.root.key != i:
            print("Error: find fails for " + str(i))

    for i in range(1, nums, 2):
        if i in t:
            print("Error: found deleted item " + str(i))

    100 in t
    18199 in t
    29512 in t
    39153 in t
    20711 in t
    36126 in t
    print(t.root.right.left.right.key)
    r = SplayTree()
    r.insert(100)
    s = SplayTree()
    if r:
        print(1)
    if not r:
        print(2)
    if s:
        print(3)
    if not s:
        print(4)
    print(s.root)
    print(bool(s.root))
    print(bool(s))

    def newsamp():
        samp = BinaryNode(15)
        samp.left = BinaryNode(10)
        samp.left.left = BinaryNode(5)
        samp.right = BinaryNode(25)
        samp.right.right = BinaryNode(30)
        tsamp = SplayTree()
        tsamp.root = samp
        return tsamp

    ts1 = newsamp()
    11 in ts1
    print("ts1: ", ts1.root.key)
    # Should print 10. Want succ_item to be 15
    ts2 = newsamp()
    26 in ts2
    print("ts2: ", ts2.root.key)
    # Should print 30. Want prev_item to be 25.
