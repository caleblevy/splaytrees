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


def random_bst(n):
    """Uniform random binary search tree of size n."""
    parents = []
    has_left = []
    root = None
    s = [True]
    s.extend(_generate_balanced_string(n))
    s.append(False)
    v = 1
    i = 0
    while i < len(s):
        if s[i]:
            i += 1
            if not s[i]:
                # mark left child as handled for this node
                has_left.pop()
                has_left.append(True)
            else:
                node = Node(v)
                v += 1
                if parents:
                    if has_left[-1]:
                        parents[-1].right = node
                    else:  # left child hasn't been handled yet
                        parents[-1].left = node
                        has_left.pop()
                        has_left.append(True)
                else:  # no parent found; make this the root
                    root = node
                parents.append(node)
                has_left.append(False)
        else:
            parents.pop()
            has_left.pop()
        i += 1
    return root


def _generate_balanced_string(n):
    k = 2*n
    r = 0
    s = []
    while k > 0:
        if k > r and (r == 0 or random.uniform(0, 1) >= r*(r+k+2)/(2*k*(r+1))):
            yield True
            r += 1
        else:
            yield False
            r -= 1
        k -= 1


def _relabel(node, start=0):
    if node is not None:
        start = _relabel(node, start) + 1
        node.value = start
        start = _relabel(node, start)
    return start


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
