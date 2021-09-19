class Node:

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None


def hamiltonian_path(n):
    if n == 0:
        return
    t = {}
    t[n] = t["root"] = Node(n)
    for i in range(n-1, 0, -1):
        t[i] = Node(i)
        t[i+1].left = t[i]
        t[i].parent = t[i+1]
    t[n+1] = None

    def rotate(x):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        y = x.parent
        if y is t["root"]:
            t["root"] = x
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

    def generate(k):
        """Generate binary trees with induced subtree T[range(1, k)]"""
        if t[k] is None:
            yield t["root"]
        else:
            yield from generate(k+1)
            if t[k].left is None:
                while t[k].parent is not None and t[k].parent.value <= k:
                    rotate(t[k])
                    yield from generate(k+1)
            else:
                while t[k].left is not None:
                    rotate(t[k].left)
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
        s = list(tuple(preorder(t)) for t in hamiltonian_path(n))
        print(f"{n} nodes, {len(set(s))} trees:\n----------------")
        for t in s:
            print(t)
