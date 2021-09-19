class Node:

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def find(self, value):
        current = self
        while current is not None:
            if current.value < value:
                current = current.right
            elif current.value > value:
                current = current.left
            else:
                return current
        return None

    def rotate(x):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        y = x.parent
        # Ensures x < y
        if x is y.right:
            x, y = y, x
        if x is y.left:
            # Shift around subtree
            w = x.right
            y.left = w
            if is_node(w):
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
            if is_node(w):
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


def preorder(node):
    if node is None:
        return
    yield node.value
    yield from preorder(node.left)
    yield from preorder(node.right)


def hamiltonian_path(n):
    if n == 0:
        return
    root = previous = Node(1)
    for i in range(2, n+1):
        current = Node(i)
        previous.right = current
        current.parent = previous
        previous = current
    for _ in _hamiltonian_path(t, n):
        yield root


def _hamiltonian_path(t, n):
    if t is None:
        yield
    yield from _hamiltonian_path(t.find(t.value + 1))
    if t.left is not None:
        if while t.value != n:
            


print(list(preorder(hamiltonian_path(5))))
