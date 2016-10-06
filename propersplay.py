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


def _inorder_walk(x):
    """Helper function to print nodes in order."""
    if x is not None:
        for key in _inorder_walk(x.left):
            yield key
        yield x.key
        for key in _inorder_walk(x.right):
            yield key


def _preorder_walk(x):
    """Helper function for preorder tree walk."""
    if x is not None:
        yield x.key
        for key in _preorder_walk(x.left):
            yield key
        for key in _preorder_walk(x.right):
            yield key


def _postorder_walk(x):
    """Helper function for postorder tree walk."""
    if x is not None:
        for key in _postorder_walk(x.left):
            yield key
        for key in _postorder_walk(x.right):
            yield key
        yield x.key


# TODO: implement from preorder
# TODO: Add root.


class SplayTree(object):
    """A splay tree implemented with top-down splaying."""
    # Add elements by finding them and splaying there.
    def __init__(self, iterable=None):
        self.root = None
        self.count = 0  # Total length of access paths
        if iterable is not None:
            for x in iterable:
                self._simple_add(x)

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

    def _simple_add(self, v):
        """Add a node with value v to the binary search tree while maintaining
        symmetric search order."""
        z = Node(v)
        y = None
        x = self.root
        while x is not None:
            y = x
            if v < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is None:
            self.root = z
        elif v < y.key:
            y.left = z
        else:
            y.right = z
        return z

    def inorder(self):
        """Output tree nodes in order."""
        return _inorder_walk(self.root)

    def preorder(self):
        """Output tree nodes in preorder."""
        return _preorder_walk(self.root)

    def postorder(self):
        """Output tree nodes in postorder."""
        return _postorder_walk(self.root)


a = SplayTree([4, 1, 2, 5, 7, 6])
print(a.root)
print(a.root.right)
print(a.root.right.right)
print(a._find_with_depth(5))
print("inorder")
for x in a.inorder():
    print(x)
print("preorder")
for x in a.preorder():
    print(x)
print("postorder")
for x in a.postorder():
    print(x)