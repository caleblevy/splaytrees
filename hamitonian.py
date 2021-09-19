class Node:

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None


class BST:

    def __init__(self):
        self.root = None
        self._node = {}

    def __getitem__(self, value):
        return self._node[value]

    def __contains__(self, value):
        return value in self._node

    def insert(self, value):
        current = self.root
        while current is not None:
            if value < current.value:
                if current.left is None:
                    current.left = self._new_node(value, current)
                    return
                else:
                    current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = self._new_node(value, current)
                    return
                else:
                    current = current.right
            else:
                return
        self.root = self._new_node(value, current)

    def _new_node(self, value, parent):
        node = Node(value)
        node.parent = parent
        self._node[value] = node
        return node

    def rotate(self, value):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        x = self._node[value]
        y = x.parent
        if y is self.root:
            self.root = x
        # Ensures x < y
        if x is y.right:
            x, y = y, x
        if x is y.left:
            # Shift around subtree
            w = x.right
            y.left = w
            if w is not None:
                w.parent = y
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
            w = y.left
            x.right = w
            if w is not None:
                w.parent = x
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

    def preorder(self):
        return tuple(preorder(self.root))


def hamiltonian_path(n):
    if n == 0:
        return
    t = BST()
    t.insert(1)
    for i in range(2, n+1):
        t.insert(i)
        t.rotate(i)

    def generate(k):
        """Generate binary trees with induced subtree T[range(1, k)]"""
        if k not in t:
            yield t
        else:
            yield from generate(k+1)
            if t[k].left is None:
                while t[k].parent is not None and t[k].parent.value <= k:
                    t.rotate(k)
                    yield from generate(k+1)
            else:
                while t[k].left is not None:
                    t.rotate(t[k].left.value)
                    yield from generate(k+1)

    yield from generate(2)


def preorder(node):
    if node is None:
        return
    yield node.value
    yield from preorder(node.left)
    yield from preorder(node.right)


if __name__ == '__main__':
    for n in range(1, 6):
        s = list(t.preorder() for t in hamiltonian_path(n))
        for t in s:
            print(t)
        print(f"--------------\n{n} nodes, {len(set(s))} trees")
