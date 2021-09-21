from collections import deque, Counter
import random

LEFT = 0
RIGHT = 1
UP = 2


class Node:

    def __init__(self, value=None):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def preorder(self):
        return tuple(_preorder(self))


def relabel(node, start=0):
    if type(node) is Node:
        start = relabel(node.left, start) + 1
        node.value = start
        start = relabel(node.right, start)
    return start
    


def _preorder(node):
    if node is not None:
        yield node.value
        yield from _preorder(node.left)
        yield from _preorder(node.right)


def preorder(node):
    return tuple(_preorder(node))


def random_balanced_bools(n):
    k = 2*n
    r = 0
    while k > 0:
        if k > r and (r == 0 or random.randrange(2*k*(r+1)) >= r*(r+k+2)):
            yield True
            r += 1
        else:
            yield False
            r -= 1
        k -= 1


def balanced_string(s):
    return "".join("(" if c else ")" for c in s)


def random_balanced_string(n):
    return balanced_string(random_balanced_bools(n))


def bst(s):
    def recurse(i):
        i += 1
        if i >= len(s) or not s[i]:
            return (None, i)
        node = Node()
        (node.left, i) = recurse(i)
        (node.right, i) = recurse(i)
        return (node, i)
    root = recurse(-1)[0]
    if root is not None:
        relabel(root)
    return root


def random_bst(n):
    return bst(list(random_balanced_bools(n)))


def good_bst(s):
    sentinal = Node()
    current = None
    v = 0
    for c in s:
        if c:
            node = Node()
            node.parent = current
            if current is not None:
                if current.left is None:
                    current.left = node
                else:
                    current.right = node
            current = node
        else:
            if current.left is None:
                current.left = sentinal
            else:
                while True:
                    if current.left is sentinal:
                        current.left = None
                    current = current.parent
                    if current.right is None:
                        break
            v += 1
            current.value = v
    while current is not None:
        if current.left is sentinal:
            current.left = None
        parent = current.parent
        if parent is None:
            break
        current = parent
    return current


def good_random_bst(n):
    return good_bst(random_balanced_bools(n))


if __name__ == '__main__':
    c = Counter()
    for _ in range(10000):
        c[preorder(good_random_bst(3))] += 1
    print(c)
    print(len(c))
    print(preorder(good_bst(random_balanced_bools(50))))
    a = good_random_bst(1_000_00)