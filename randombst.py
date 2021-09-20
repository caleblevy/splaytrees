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
    if node is not None:
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
    root = current = None
    while k > 0:
        if k > r and (r == 0 or random.uniform(0, 1) >= r*(r+k+2)/(2*k*(r+1))):
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
    return bst(random_balanced_bools(n))


def good_bst(s):
    sentinal = object()
    current = None
    for c in s:
        if c:
            node = Node()
            if current is None:
                current = node
            elif current.left is None:
                current.left = node
                current.left.parent = current
                current = current.left
            else:
                current.right = node
                current.right.parent = current
                current = current.right
        else:
            if current.left is None:
                current.left = sentinal
            else:
                if current.left is sentinal:
                    current.left = None
                current = current.parent
    parent = current
    while parent is not None:
        if current.left is sentinal:
            current.left = None
        current = parent
        parent = current.parent
    relabel(current)
    return current


t1 = [True, True, True, True, True, True, False, True, False, True, True, True, False, False, True, False, False, True, True, False, True, False, False, True, True, False, False, False, False, False, True, True, False, True, False, True, False, True, True, False, True, False, True, True, True, True, False, True, True, True, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, True, False, True, True, True, False, True, True, True, True, True, False, False, True, True, False, False, True, False, False, False, False, True, True, False, True, False, False, False, True, False, False, True, False, False]
t2 = [True, False, True, True, False, True, False, True, True, True, True, False, True, True, False, True, False, True, True, True, True, True, True, False, False, False, True, True, False, True, True, True, False, False, False, False, True, False, True, False, False, True, False, False, False, True, False, True, False, True, False, False, True, False, True, True, True, False, False, True, True, False, True, False, True, False, False, False, False, False, False, True, True, False, True, False, False, True, False, True, False, True, True, False, False, False, True, True, True, True, False, False, False, False, True, True, False, False, True, False]


if __name__ == '__main__':
    print(list(bst(t1).preorder()))
    print(list(bst(t2).preorder()))
    s = list(random_balanced_bools(7))
    print(s)
    print(balanced_string(s))
    print(preorder(bst(s)))
    print(preorder(good_bst(s)))