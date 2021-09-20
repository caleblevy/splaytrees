import random

OPEN = False
CLOSED = True


class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def preorder(self):
        return list(preorder(self.root))


def preorder(node):
    if node is not None:
        yield from preorder(node.left)
        yield node.value
        yield from preorder(node.right)


def _generate_balanced_string(n):
    k = 2*n
    r = 0
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
    for _ in range(1000):
        c[random_balanced_string(5)] += 1
    print(c)
    print(len(c))
