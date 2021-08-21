class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def inorder(node):
    if node is None:
        return
    yield from inorder(node.left)
    yield node.value
    yield from inorder(node.right)


def preorder(node):
    if node is None:
        return
    yield node.value
    yield from preorder(node.left)
    yield from preorder(node.right)

def postorder(node):
    if node is None:
        return
    yield from postorder(node.left)
    yield from postorder(node.right)
    yield node.value


class Tree:

    def __init__(self, iterable=None):
        self.root = None
        if iterable is not None:
            for element in iterable:
                self.insert(element)

    def __contains__(self, value):
        current = self.root
        while current is not None:
            if value < current.value:
                current = current.left
            elif value > current.value:
                current = current.right
            else:
                return True
        return False

    def insert(self, value):
        current = self.root
        while current is not None:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return
                current = current.right
            else:
                return
        self.root = Node(value)

    def __iter__(self):
        return inorder(self.root)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.preorder()})"

    def inorder(self):
        return list(inorder(self.root))

    def preorder(self):
        return list(preorder(self.root))

    def postorder(self):
        return list(postorder(self.root))


if __name__ == '__main__':
    tree = Tree([6, 4, 2, 10, 6, 12, 7, 7, 8, 4])
    print(tree)
    