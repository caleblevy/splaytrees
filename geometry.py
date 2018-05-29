"""Treaps, the Geometry of Binary Search Trees, GreedyFuture, and Dynamic
Optimality."""

import unittest

from bst import maker


Left = object()
Right = object()


class Node(object):

    def __init__(x, key, priority):
        x.key = key
        x.priority = priority
        x.left = None
        x.right = None
        x.parent = None

    def _walk(x, order=None):
        """Do all three edge traversals at once."""
        z = x.parent
        l = r = False  # l is true if all node's in x.left are visited
        while True:
            if order is None:
                yield x
            if not l:
                if order == -1:
                    yield x
                y = x.left
                if not is_node(y):
                    l = True
                else:
                    if order == "":
                        yield "l"
                    x = y
            elif not r:
                if order == 0:
                    yield x
                y = x.right
                if not is_node(y):
                    r = True
                else:
                    if order == "":
                        yield "r"
                    x = y
                    l = False
            else:
                if order == 1:
                    yield x
                y = x.parent
                if y is z:
                    return
                elif x is y.left:
                    r = False
                if order == "":
                    yield "p"
                x = y

    def subtree_encoding(x):
        """Encode cursor movements traversing the subtree rooted at x."""
        return "".join(x._walk(""))

    def walk_nodes(x):
        return tuple(x._walk())

    def preorder_nodes(x):
        return tuple(x._walk(-1))

    def inorder_nodes(x):
        return tuple(x._walk(0))

    def postorder_nodes(x):
        return tuple(x._walk(1))

    def walk_keys(x):
        return tuple(n.key for n in x._walk())

    def preorder_keys(x):
        return tuple(n.key for n in x._walk(-1))

    def inorder_keys(x):
        return tuple(n.key for n in x._walk(0))

    def postorder_keys(x):
        return tuple(n.key for n in x._walk(1))

    @maker(tuple)
    def path(x):
        while x is not None:
            yield x
            x = x.parent

    # New to this module

    @maker(tuple)
    def split_path_subtrees(x):
        for y in sorted(x.path()):
            if y.key <= x.key:
                z = y.left
                if z is not None:
                    z.parent = None
                y.left = None
                yield z
            if y.key >= x.key:
                z = y.right
                if z is not None:
                    z.parent = None
                y.right = None
                yield z

    @maker(tuple)
    def attachment_slots(x):
        for x in x.inorder_nodes():
            if x.left is None:
                yield (x, Left)
            if x.right is None:
                yield (x, Right)


def is_node(x):
    return isinstance(x, Node)


class Inf(object):

    def __repr__(inf):
        return "Inf"

    def __gt__(inf, x):
        return x is not Inf

    def __ge__(inf, x):
        return True

    def __lt__(inf, x):
        return False

    def __le__(inf, x):
        return x is Inf


Inf = Inf()


def treap(tau, pi):
    tau = list(tau)
    pi = list(pi)
    assert len(tau) == len(pi)
    if not tau:
        return
    x = Node(tau[0], pi[0])
    for key, priority in zip(tau[1:], pi[1:]):
        y = Node(key, priority)
        if y.priority > x.priority:
            x.right = y
            y.parent = x
        else:
            z = x.parent
            while z is not None and z.priority > y.priority:
                x = z
                z = z.parent
            y.left = x
            x.parent = y
            if z is not None:
                z.right = y
                y.parent = z
        x = y
    while x.parent is not None:
        x = x.parent
    return x


def complete_bst(k):
    """Complete BST on 2**(k-1) nodes."""
    n = 2**k-1
    keys = range(1, n+1)
    priorities = [0]*n
    p = n
    for i in range(1, k+1):
        current = 2**(i-1)
        increment = 2**i
        while current <= n:
            priorities[current-1] = p
            p -= 1
            current += increment
    return treap(keys, priorities)


def attach(t, subtrees):
    """Attach subtrees to t."""
    slots = t.attachment_slots()
    subtrees = list(subtrees)
    assert len(slots) == len(subtrees)
    for (x, direction), s in zip(slots, subtrees):
        if direction is Left:
            x.left = s
        elif direction is Right:
            x.right = s
        if s is not None:
            s.parent = x


class TestUtilities(unittest.TestCase):

    def test_infinity(self):
        """Test Infinite Ordering"""
        self.assertTrue(Inf > 1)
        self.assertTrue(Inf > "a")
        self.assertTrue(1 < Inf)
        self.assertTrue("a" < Inf)
        self.assertFalse(Inf < 1)
        self.assertFalse(Inf < "a")
        self.assertFalse(1 > Inf)
        self.assertFalse("a" > Inf)
        self.assertTrue(Inf >= 1)
        self.assertTrue(Inf >= "a")
        self.assertTrue(1 <= Inf)
        self.assertTrue("a" <= Inf)
        self.assertFalse(Inf <= 1)
        self.assertFalse(Inf <= "a")
        self.assertFalse(1 >= Inf)
        self.assertFalse("a" >= Inf)
        arr = list(range(10))
        arr[3], arr[7] = arr[7], arr[3]
        arr.insert(5, Inf)
        arr.insert(0, Inf)
        self.assertEqual(sorted(arr), list(range(10))+[Inf, Inf])
        self.assertTrue(Inf == Inf)
        self.assertFalse(Inf != Inf)
        self.assertTrue(Inf <= Inf)
        self.assertFalse(Inf < Inf)
        self.assertTrue(Inf >= Inf)
        self.assertFalse(Inf > Inf)

    def testtreap(self):
        """Test Internal Treap."""
        x = treap(range(1, 11), [7, 10, 9, 8, 3, 2, 6, 4, 5, 1])
        self.assertEqual(x.inorder_keys(), tuple(range(1, 11)))
        self.assertEqual(
            x.preorder_keys(),
            (10, 6, 5, 1, 4, 3, 2, 8, 7, 9)
        )
        y = treap(range(1, 11), [Inf, 1, 2, 3, Inf, 9, 5, 7, 6, 10])
        self.assertEqual(y.inorder_keys(), tuple(range(1, 11)))
        self.assertEqual(y.preorder_keys(), (2, 1, 3, 4, 7, 6, 5, 9, 8, 10))
        for node in y.preorder_nodes()[1:]:
            self.assertTrue(node.parent.priority < node.priority)
        for node in y.inorder_nodes():
            if node.priority == Inf:
                self.assertTrue(node.left is node.right is None)
        infp = range(1, 16)
        infp[2] = Inf
        infp[5:7] = [Inf]*2
        infp[12:14] = [Inf]*2
        z = treap(range(15), infp)
        self.assertEqual(z.inorder_keys(), tuple(range(15)))
        self.assertEqual(
            z.preorder_keys(),
            (0, 1, 3, 2, 4, 7, 6, 5, 8, 9, 10, 11, 14, 13, 12)
        )
        self.assertTrue(treap([], []) is None)

    def test_complete_bst(self):
        """Test complete binary search tree utility."""
        self.assertEqual(complete_bst(1).preorder_keys(), (1, ))
        self.assertEqual(complete_bst(2).preorder_keys(), (2, 1, 3))
        self.assertEqual(
            complete_bst(3).preorder_keys(),
            (4, 2, 1, 3, 6, 5, 7)
        )

    def test_path_split(self):
        """Test path subtree splitting."""
        t = complete_bst(4)
        u = t.left.right.left  # v = 5
        v, w, x, y, z = u.split_path_subtrees()
        self.assertEqual(v.key, 2)
        self.assertEqual(v.parent, None)
        self.assertEqual(v.preorder_keys(), (2, 1, 3))
        self.assertEqual(w, None)
        self.assertEqual(x, None)
        self.assertEqual(y.key, 7)
        self.assertEqual(y.preorder_keys(), (7, ))
        self.assertEqual(y.parent, None)
        self.assertEqual(z.key, 12)
        self.assertEqual(z.preorder_keys(), (12, 10, 9, 11, 14, 13, 15))
        self.assertEqual(z.parent, None)
        self.assertEqual(t.preorder_keys(), (8, 4, 6, 5))
        self.assertEqual(t.inorder_keys(), (4, 5, 6, 8))
        a = complete_bst(4)
        b = a.left.right
        c, d, e, f = b.split_path_subtrees()
        self.assertEqual(c.key, 2)
        self.assertEqual(c.preorder_keys(), (2, 1, 3))
        self.assertEqual(c.parent, None)
        self.assertEqual(d.key, 5)
        self.assertEqual(d.preorder_keys(), (5, ))
        self.assertEqual(d.parent, None)
        self.assertEqual(e.key, 7)
        self.assertEqual(e.preorder_keys(), (7, ))
        self.assertEqual(e.parent, None)
        self.assertEqual(f.key, 12)
        self.assertEqual(f.preorder_keys(), (12, 10, 9, 11, 14, 13, 15))
        self.assertEqual(f.parent, None)
        self.assertEqual(a.preorder_keys(), (8, 4, 6))
        self.assertEqual(a.inorder_keys(), (4, 6, 8))

    def test_attachment_slots(self):
        """Test points of attachment."""
        t = complete_bst(4)
        a = []
        for i in range(1, 16, 2):
            a.append((i, Left))
            a.append((i, Right))
        b = [(x.key, direction) for x, direction in t.attachment_slots()]
        self.assertEqual(b, a)
        r = treap(range(1, 11), range(1, 11))
        ar = [(i, Left) for i in range(1, 11)] + [(10, Right)]
        br = [(x.key, direction) for x, direction in r.attachment_slots()]
        self.assertEqual(br, ar)
        l = treap(range(1, 11), range(11, 1, -1))
        al = [(1, Left)] + [(i, Right) for i in range(1, 11)]
        bl = [(x.key, direction) for x, direction in l.attachment_slots()]
        self.assertEqual(al, bl)

    def test_attach(self):
        """Test (re)-attachment to the tree."""
        t = complete_bst(4)
        u = t.left.right.left  # v = 5
        s = u.split_path_subtrees()
        self.assertEqual(len(t.preorder_keys()), 4)
        attach(t, s)
        self.assertEqual(t.preorder_keys(), complete_bst(4).preorder_keys())
        self.assertEqual(t.inorder_keys(), complete_bst(4).inorder_keys())
        a = u.parent
        b = a.split_path_subtrees()
        self.assertEqual(len(t.preorder_keys()), 3)
        attach(t, b)
        self.assertEqual(t.preorder_keys(), complete_bst(4).preorder_keys())
        self.assertEqual(t.inorder_keys(), complete_bst(4).inorder_keys())

if __name__ == '__main__':
    unittest.main()
