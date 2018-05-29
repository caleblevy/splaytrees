"""Treaps, the Geometry of Binary Search Trees, GreedyFuture, and Dynamic
Optimality."""

import unittest


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


def is_node(x):
    return isinstance(x, Node)


class Inf(object):

    def __repr__(inf):
        return "Inf"

    def __gt__(inf, x):
        return True

    def __ge__(inf, x):
        return True

    def __lt__(inf, x):
        return False

    def __le__(inf, x):
        return False


Inf = Inf()


def _treap(tau, pi):
    tau = list(tau)
    pi = list(pi)
    assert len(tau) == len(pi)
    if not tau:
        return
    x = Node(tau[0], pi[0])
    for key, priority in zip(tau[1:], pi[1:]):
        y = Node(key, priority)
        if y.priority < x.priority:
            x.right = y
            y.parent = x
        else:
            z = x.parent
            while z is not None and z.priority < y.priority:
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


x = _treap(range(1,11),[4,1,2,3,8,9,5,7,6,10])
print(x.inorder_keys())
print(x.preorder_keys())
for y in x.preorder_nodes()[1:]:
    print(y.priority < y.parent.priority)


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


    def test_treap(self):
        """Test Internal Treap."""
        x = _treap(range(1,11),[4, 1, 2, 3, 8, 9, 5, 7, 6, 10])
        self.assertEqual(x.inorder_keys(), tuple(range(1, 11)))
        self.assertEqual(
            x.preorder_keys(),
            (10, 6, 5, 1, 4, 3, 2, 8, 7, 9)
        )
        # y = _treap(range(1,11),[Inf, 1, 2, 3, Inf, 9, 5, 7, 6, 10])





if __name__ == '__main__':
    unittest.main()
