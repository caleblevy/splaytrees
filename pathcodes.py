"""A new version of bottom-up splay and move-to-root carrying less baggage."""

import unittest


class Node(object):
    """BST node with parents."""

    __slots__ = "key parent left right".split()

    def __init__(x, key):
        x.key = key
        x.parent = None
        x.left = None
        x.right = None

    def __repr__(x):
        return x.__class__.__name__ + '(%s)' % ", ".join([
            "key=%s" % x.key,
            "parent=%s" % getattr(x.parent, 'key', None),
            "left=%s" % getattr(x.left, 'key', None),
            "right=%s" % getattr(x.right, 'key', None)
        ])

    def rotate(x):
        """Rotate the edge between x and its parent."""
        # Normalize to kozma's definition, page 8 of thesis
        y = x.parent
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
        """Traverse subtree rooted at x inorder."""
        current = x
        stack = []
        while True:
            # Reach left most node of current's subtree
            if current is not None:
                # Place pointer to a tree node on the stack before traversing
                # left subtree.
                stack.append(current)
                current = current.left
            # Backtrack from empty subtree and visit node at top of stack.
            # However, if stack is empty, we are doen.
            else:
                if stack:
                    current = stack.pop()
                    yield current.key
                    # We have visited the node and its left subtree. Now visit
                    # right subtree.
                    current = current.right
                else:
                    break

    def preorder(x):
        """Traverse subtree rooted at x inorder."""
        current = x
        stack = []
        while True:
            if current is not None:
                yield current.key
                stack.append(current)
                current = current.left
            else:
                if stack:
                    current = stack.pop()
                    current = current.right
                else:
                    break

    def postorder(x):
        """Return postorder of subtree rooted at x."""
        s1 = [x]
        s2 = []
        while s1:
            node = s1.pop()
            s2.append(node)
            # push left and right children of removed item to s1
            if node.left is not None:
                s1.append(node.left)
            if node.right is not None:
                s1.append(node.right)
            # gives us a "reverse" postorder
        while s2:
            yield s2.pop().key

    def _splay_step(x):
        """Perform zig, zig-zag or zig-zig appropriately."""
        y = x.parent
        z = y.parent  # parent checked for in "splay"
        # zig
        if z is None:
            x.rotate()
        # zig-zag
        elif (y is z.left and x is y.right) or (y is z.right and x is y.left):
            x.rotate()
            x.rotate()
        # zig-zig
        else:
            y.rotate()
            x.rotate()

    def _simple_splay_step(x):
        """Do a simple splay step."""
        y = x.parent
        z = y.parent  # parent checked for in "splay"
        # zig
        if z is None:
            x.rotate()
        elif (y is z.left and x is y.right) or (y is z.right and x is y.left):
            x.rotate()
        # zig-zig
        else:
            y.rotate()
            x.rotate()

    def splay(x):
        """Proper bottom-up splay to the top."""
        while x.parent is not None:
            x._splay_step()

    def simple_splay(x):
        """Proper bottom-up simple splay to the top."""
        while x.parent is not None:
            x._simple_splay_step()

    def move_to_root(x):
        """Move straight to the root."""
        while x.parent is not None:
            x.rotate()

    def static(x):
        """Operation of a static search tree."""
        return


class TestNode(unittest.TestCase):

    def test_rotation(self):
        k = Node("k")
        g = k.left = Node("g");  g.parent = k
        c = g.left = Node("c");  c.parent = g
        a = c.left = Node("a");  a.parent = c
        b = c.right = Node("b");  b.parent = c
        h = g.right = Node("h");  h.parent = g
        e = h.left = Node("e");  e.parent = h
        m = h.right = Node("h");  m.parent = h
        f = k.right = Node("f");  f.parent = k
        parent_pairs = [
            (g, k), (c, g), (a, c), (b, c), (h, g), (e, h), (m, h), (f, k)
        ]
        #       k
        #      /  \
        #      g  f
        #    /   \
        #   c    h
        #  / \   /\
        # a   b e  m
        a.rotate()
        self.assertTrue(g.right is h)
        self.assertTrue(g.left is a)
        self.assertTrue(c.parent is a)
        self.assertTrue(a.parent is g)
        self.assertTrue(a.left is None)
        self.assertTrue(a.right is c)
        h.rotate()
        self.assertTrue(h.parent is k)
        self.assertTrue(k.left is h)
        self.assertTrue(k.right is f)
        self.assertTrue(h.right is m)
        self.assertTrue(h.left is g)
        self.assertTrue(g.parent is h)
        self.assertTrue(m.parent is h)
        self.assertTrue(e.parent is g)
        self.assertTrue(g.right is e)
        self.assertTrue(g.left is a)
        # Reverse these rotations
        c.rotate();  g.rotate()
        for x, y in parent_pairs:
            self.assertTrue(x.parent is y)

    def test_inorder(self):
        """Test inorder traversal."""
        k = Node("k")
        g = k.left = Node("g");  g.parent = k
        c = g.left = Node("c");  c.parent = g
        a = c.left = Node("a");  a.parent = c
        b = c.right = Node("b");  b.parent = c
        h = g.right = Node("h");  h.parent = g
        e = h.left = Node("e");  e.parent = h
        m = h.right = Node("m");  m.parent = h
        f = k.right = Node("f");  f.parent = k
        order = list("acbgehmkf")
        self.assertTrue(order == list(k.inorder()))
        a.rotate()
        order = list("acbgehmkf")
        self.assertTrue(order == list(k.inorder()))
        h.rotate()
        order = list("acbgehmkf")
        self.assertTrue(order == list(k.inorder()))

    def test_preorder(self):
        """Test preorder traversal"""
        k = Node("k")
        g = k.left = Node("g");  g.parent = k
        c = g.left = Node("c");  c.parent = g
        a = c.left = Node("a");  a.parent = c
        b = c.right = Node("b");  b.parent = c
        h = g.right = Node("h");  h.parent = g
        e = h.left = Node("e");  e.parent = h
        m = h.right = Node("m");  m.parent = h
        f = k.right = Node("f");  f.parent = k
        pre = list("kgcabhemf")
        self.assertTrue(pre == list(k.preorder()))
        a.rotate()
        pre = list("kgacbhemf")
        self.assertTrue(pre == list(k.preorder()))
        h.rotate()
        pre = list("khgacbemf")
        self.assertTrue(pre == list(k.preorder()))

    def test_postorder(self):
        """Test postorder traversal."""
        k = Node("k")
        g = k.left = Node("g");  g.parent = k
        c = g.left = Node("c");  c.parent = g
        a = c.left = Node("a");  a.parent = c
        b = c.right = Node("b");  b.parent = c
        h = g.right = Node("h");  h.parent = g
        e = h.left = Node("e");  e.parent = h
        m = h.right = Node("m");  m.parent = h
        f = k.right = Node("f");  f.parent = k
        post = list("abcemhgfk")
        self.assertTrue(post == list(k.postorder()))
        a.rotate()
        post = list("bcaemhgfk")
        self.assertTrue(post == list(k.postorder()))
        h.rotate()
        post = list("bcaegmhfk")
        self.assertTrue(post == list(k.postorder()))

    def test_splay(self):
        """Test the splay method works."""
        k = Node("k")
        g = k.left = Node("g");  g.parent = k
        c = g.left = Node("c");  c.parent = g
        a = c.left = Node("a");  a.parent = c
        b = c.right = Node("b");  b.parent = c
        h = g.right = Node("h");  h.parent = g
        e = h.left = Node("e");  e.parent = h
        m = h.right = Node("m");  m.parent = h
        f = k.right = Node("f");  f.parent = k
        a.splay()
        pre = list("akcgbhemf")
        self.assertTrue(pre == list(a.preorder()))
        e.splay()
        pre = list("eacgbkhmf")
        self.assertTrue(pre == list(e.preorder()))

if __name__ == '__main__':
    unittest.main()