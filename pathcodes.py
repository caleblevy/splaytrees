"""A new version of bottom-up splay and move-to-root carrying less baggage."""


class Node(object):
    """BST node with parents."""

    __slots__ = "key parent left right".split()

    def __init__(x, key):
        x.key = key
        x.parent = None
        x.left = None
        x.right = None

    def __repr__(self):
        return self.__class__.__name__ + '(%s)' % ", ".join([
            "key=%s" % self.key,
            "parent=%s" % getattr(self.parent, 'key', None),
            "left=%s" % getattr(self.left, 'key', None),
            "right=%s" % getattr(self.right, 'key', None)
        ])

    def rotate(self):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        x = self
        y = self.parent
        # Ensures x < y
        if x is y.right:
            x, y = y, x
        if x is y.left:
            # Shift around subtree
            B = x.right
            y.left = B
            if B is not None:
                B.parent = y
            # Switch up parent pointers
            z = y.parent
            x.parent = z
            if z is not None:
                if y is z.right:
                    z.right = x
                else:
                    z.left = x
            x.right = y
            y.parent = x
        else:  # y is x.right
            B = y.left
            x.right = B
            if B is not None:
                B.parent = x
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

    def inorder(x):
        stack = [x]
        while stack:
            if stack[-1].left is not None:
                stack.append(stack[-1].left)
            else:
                while stack[-1].right is None:
                    yield stack.pop()
                stack.append(stack[-1].right)
                yield stack.pop()


k = Node("k")
g = k.left = Node("g")
c = g.left = Node("c")
a = c.left = Node("a")
b = c.right = Node("b")
h = g.right = Node("h")
e = h.left = Node("e")
m = h.right = Node("h")
f = k.right = Node("f")

for i in k.inorder():
    print(i)