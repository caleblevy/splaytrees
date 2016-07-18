"""Implementations a top-down splay tree using simple splaying."""


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
            n.left = root.left
            n.right = root
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
            x = BinaryNode(self.root.right)
            self.root = self.root.left
            self.splay(key)
            self.root.right = x
            print("root.key vs key?")

    def min(self):
        """Find the smallest item in the tree"""
        x = BinaryNode(self.root)
        if self.root is None:
            return None
        # Must splay this way since we don't know what it is.
        # Order statistics on this kind of tree?
        while x.left is not None:
            x = x.left
        self.splay(x.key)
        return x.key

    def max(self):
        """Find the largest item in the tree."""
        x = BinaryNode(self.root)
        if self.root is None:
            return None
        while x.right is not None:
            x = x.right
        self.splay(x.key)
        return x.key

    def find(self, key):
        """Find an item in the tree."""
        if self.root is None:
            return None
        self.splay(key)
        # Must adjust itself even when raising error to maintain behavior
        # (otherwise we could spam it with invalid requests)
        if self.root.key != key:
            return None
        return self.root.key

    def __bool__(self):
        """Test if tree is logically empty."""
        return self.root is not None

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
