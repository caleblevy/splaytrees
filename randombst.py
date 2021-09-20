import random

LEFT = 0
RIGHT = 1
UP = 2


class Node:

    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def preorder(self):
        return list(preorder(self))


def relabel(node, start=0):
    if node is not None:
        start = relabel(node.left, start) + 1
        node.value = start
        start = relabel(node.right, start)
    return start
    


def preorder(node):
    if node is not None:
        yield node.value
        yield from preorder(node.left)
        yield from preorder(node.right)


def _generate_balanced_string(n):
    k = 2*n
    r = 0
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
    return "".join("(" if c else ")" for c in _generate_balanced_string(n))

t1 = [True, True, True, True, True, True, False, True, False, True, True, True, False, False, True, False, False, True, True, False, True, False, False, True, True, False, False, False, False, False, True, True, False, True, False, True, False, True, True, False, True, False, True, True, True, True, False, True, True, True, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, True, False, True, True, True, False, True, True, True, True, True, False, False, True, True, False, False, True, False, False, False, False, True, True, False, True, False, False, False, True, False, False, True, False, False]
t2 = [True, False, True, True, False, True, False, True, True, True, True, False, True, True, False, True, False, True, True, True, True, True, True, False, False, False, True, True, False, True, True, True, False, False, False, False, True, False, True, False, False, True, False, False, False, True, False, True, False, True, False, False, True, False, True, True, True, False, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, True, False, False, True, False, True, False, True, True, False, False, False, True, True, True, True, False, False, False, False, True, True, False, False, True, False]


def random_bst(s):
    i = 0
    def recurse():
        nonlocal i
        if i >= len(s) or not s[i]:
            i += 1
            return None
        i += 1
        node = Node()
        node.left = recurse()
        if i >= len(s) or not s[i]:
            i += 1
            return node
        node.right = recurse()
        return node
    root = recurse()
    relabel(root)
    return root


if __name__ == '__main__':
    print(list(random_bst(t1).preorder()))
    print(list(random_bst(t2).preorder()))
    # from collections import Counter
    # c = Counter()
    # for _ in range(10000):
    #     c[tuple(random_bst(5).preorder())] += 1
    # print(c)
    # print(len(c))
    # t = Node()
