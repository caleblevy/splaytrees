"""Implement a proper splay tree, as described in the paper, so we know
sequential access, etc. holds exactly."""


class Node(object):

    def __init__(self, x):
        self.key = x
        self.parent = None
        self.left = None
        self.right = None


# TODO: implement from preorder
# TODO: Add root.


class SplayTree(object):
    """A splay tree implemented with top-down splaying."""
    # Add elements by finding them and splaying there.
    def __init__(self, node):
        self.root = node
        self.count = 0  # Total length of access paths

    def find(self, x):
        """Find a node with key x."""
        if self.root is None:
            return None
        depth = 0
        current = self.root
        while current is not None:
            depth += 1
            if current.key == x or current is None:
                break
            else:
                if current.key < x:
                    return 