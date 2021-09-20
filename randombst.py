import random

OPEN = False
CLOSED = True


class Node:

    def __init__(self, value=None):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self._filled = False

    def insert_left(self, value=None):
        assert self.left is None
        node = Node(value)
        node.parent = self
        self.left = node
        return node

    def insert_right(self, value=None):
        assert self.right is None
        node = Node(value)
        node.parent = self
        self.right = node
        return node

    def inorder(self):
        return list(inorder(self))


def relabel(node, start=0):
    if node is not None:
        start = relabel(node.left, start) + 1
        node.value = start
        start = relabel(node.right, start)
    return start
    


def inorder(node):
    if node is not None:
        yield from inorder(node.left)
        yield node.value
        yield from inorder(node.right)


def _generate_balanced_string(n):
    k = 2*n
    r = 0
    v = 1
    root = current = None
    while k > 0:
        if k > r and (r == 0 or random.uniform(0, 1) >= r*(r+k+2)/(2*k*(r+1))):
            yield True
            r += 1
        else:
            yield False
            r -= 1
        k -= 1


def random_balanced_string(n):
    return "".join("(" if p else ")" for p in _generate_balanced_string(n))


if __name__ == '__main__':
    # print(list(preorder(random_bst(5))))
    from collections import Counter
    c = Counter()
    for _ in range(10000):
        c[random_balanced_string(5)] += 1
    print(c)
    print(len(c))
    t = Node()
    t.insert_left()
    t.left.insert_left()
    t.insert_right()
    t.right.insert_right()
    t.right.insert_left()
    t.right.left.insert_right()
    print(t.inorder())
    relabel(t)
    print(t.inorder())
