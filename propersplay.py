"""Implement a proper splay tree, as described in the paper, so we know
sequential access, etc. holds exactly."""


class Node(object):

    def __init__(self, x):
        self.key = x
        self.parent = None
        self.left = None
        self.right = None

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % ", ".join([
            "key=%s" % self.key,
            "parent=%s" % getattr(self.parent, 'key', None),
            "left=%s" % getattr(self.left, 'key', None),
            "right=%s" % getattr(self.right, 'key', None)
        ])


# TODO: implement from preorder
# TODO: Add root.


class SplayTree(object):
    """A splay tree implemented with top-down splaying."""
    # Add elements by finding them and splaying there.
    def __init__(self):
        self.root = None
        self.count = 0  # Total length of access paths

    def _find_with_depth(self, k):
        """Find a node with key k."""
        x = x_prev = self.root
        while x is not None and k != x.key:
            x_prev = x
            if k < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def add(self, v):
        """Add a node with value v to the binary search tree while maintaining
        symmetric search order."""
        z = Node(v)
        y = None
        x = self.root
        while x is not None:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y  # TODO: Understand why we need this.
        if y is None:
            self.root = z  # tree was empty
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z


a = SplayTree()
a.add(4)
a.add(1)
a.add(2)
a.add(5)
a.add(7)
a.add(6)
print(a.root)
print(a.root.right)
print(a.root.right.right)
print(a._find_with_depth(5))