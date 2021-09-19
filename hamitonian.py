class Node:

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None


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
    return root


print(list(preorder(hamiltonian_path(5))))
