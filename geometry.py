"""Treaps, the Geometry of Binary Search Trees, GreedyFuture, and Dynamic
Optimality."""

import unittest
from operator import attrgetter

from bst import maker


Left = object()
Right = object()


class Node(object):

    def __init__(x, key, priority):
        x.key = key
        x.priority = priority
        x.label = None
        x.left = None
        x.right = None
        x.parent = None

    __lt__ = __le__ = __gt__ = __ge__ = None

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

    @maker(tuple)
    def sorted_path(x):
        return sorted(x.path(), key=attrgetter("key"))

    # New to This Module

    @maker(tuple)
    def split_path_subtrees(x):
        for y in x.sorted_path():
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

    def search(x, k):
        while x is not None:
            if k < x.key:
                x = x.left
            elif k > x.key:
                x = x.right
            else:
                return x
        return None

    @maker(tuple)
    def path_comparison_labels(x):
        """Return dictionary mapping keys to weights."""
        d = {}
        path = x.sorted_path()
        subtree_labels = []
        for y in path:
            if y.key <= x.key:
                subtree_labels.append(Inf if y.left is None else y.left.label)
            if y.key >= x.key:
                subtree_labels.append(
                    Inf if y.right is None else y.right.label
                )
        for i, y in enumerate(path):
            l_label = subtree_labels[i]
            r_label = subtree_labels[i+1]
            c_label = min(y.priority, l_label, r_label)
            yield (c_label, l_label, r_label)


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

    def __neg__(inf):
        return NegInf


class NegInf(object):

    def __repr__(neginf):
        return "-Inf"

    def __gt__(neginf, x):
        return False

    def __ge__(neginf, x):
        return x is NegInf

    def __lt__(neginf, x):
        return x is not NegInf

    def __le__(neginf, x):
        return True

    def __neg__(neginf):
        return Inf


Inf = Inf()
NegInf = NegInf()


def priority_compare(x, y):
    assert x.key < y.key
    return x.priority < y.priority


def label_compare(x, y):
    """Is x on top of y?"""
    assert x.key < y.key
    return (x.priority[0], x.priority[1]) < (y.priority[0], y.priority[2])


def treap(tau, pi, heap_winner=priority_compare):
    """Binary search tree with nodes tau ordered by MIN-heap pi."""
    tau = list(tau)
    pi = list(pi)
    assert len(tau) == len(pi)
    if not tau:
        return
    x = Node(tau[0], pi[0])
    for key, priority in zip(tau[1:], pi[1:]):
        y = Node(key, priority)
        if heap_winner(x, y):
            x.right = y
            y.parent = x
        else:
            z = x.parent
            while z is not None and not heap_winner(z, y):
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


def access_times(X):
    """For x in X, d[x] is stack of access times for x. First time at top."""
    d = {}
    X = list(X)
    m = len(X)
    for i, k in enumerate(reversed(X)):
        if k not in d:
            d[k] = [Inf]
        d[k].append(m-i)
    return d


def first_access_times(X):
    """Return mapping of keys in X to their first access times"""
    t = access_times(X)
    return {k: s[-1] for k, s in t.items()}


def canonical_tree(X):
    d = first_access_times(X)
    keys = sorted(d.keys())
    priorities = list(map(d.__getitem__, keys))
    return treap(keys, priorities)


def _update_labels(nodes):
    # You are assumed to input the postorder yourself
    for x in nodes:
        candidates = [x.priority]
        if x.left is not None:
            candidates.append(x.left.label)
        if x.right is not None:
            candidates.append(x.right.label)
        x.label = min(candidates)


def initial_tree(X, T=None):
    # Use canonical initial tree if T is None
    if T is None:
        T = canonical_tree(X)
    else:
        d = first_access_times(X)
        assert set(X).issubset(T.inorder_keys())
        T = canonical_tree(T.preorder_keys())  # Copy to prevent overwrite
        nodes = T.inorder_nodes()
        for x in nodes:
            x.priority = d.get(x.key, Inf)
    _update_labels(T.postorder_nodes())
    return T


# def min_priority(X, i, j, k):
#     """Return first index l greater than i such that j< X[l] < k."""
#     for l in range(i, len(X)+1):
#         if j < X[l] < k:
#             return l
#     return Inf

# def


def GreedyExecution(X, T=None):
    """Execute greedy algorithm from Lucas 89."""
    T = initial_tree(X, T)
    A = access_times(X)
    for k in X:
        x = T.search(k)
        yield (T, x)
        A[k].pop()
        x.priority = A[k][-1]
        labels = x.path_comparison_labels()
        keys = tuple(y.key for y in x.sorted_path())
        Q = treap(keys, labels, heap_winner=label_compare)
        Q_post = Q.postorder_nodes()
        for y in Q.inorder_nodes():
            y.priority = y.priority[0]
        subtrees = x.split_path_subtrees()
        attach(Q, subtrees)
        _update_labels(Q_post)
        T = Q


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
        # Neg Inf
        self.assertFalse(NegInf > 1)
        self.assertFalse(NegInf > "a")
        self.assertFalse(1 < NegInf)
        self.assertFalse("a" < NegInf)
        self.assertTrue(NegInf < 1)
        self.assertTrue(NegInf < "a")
        self.assertTrue(1 > NegInf)
        self.assertTrue("a" > NegInf)
        self.assertFalse(NegInf >= 1)
        self.assertFalse(NegInf >= "a")
        self.assertFalse(1 <= NegInf)
        self.assertFalse("a" <= NegInf)
        self.assertTrue(NegInf <= 1)
        self.assertTrue(NegInf <= "a")
        self.assertTrue(1 >= NegInf)
        self.assertTrue("a" >= NegInf)
        arr = list(range(10))
        arr[3], arr[7] = arr[7], arr[3]
        arr.insert(5, NegInf)
        arr.insert(0, NegInf)
        self.assertEqual(sorted(arr), [NegInf, NegInf] + list(range(10)))
        self.assertTrue(NegInf == NegInf)
        self.assertFalse(NegInf != NegInf)
        self.assertTrue(NegInf <= NegInf)
        self.assertFalse(NegInf < NegInf)
        self.assertTrue(NegInf >= NegInf)
        self.assertFalse(NegInf > NegInf)
        # Interaction
        self.assertFalse(Inf == NegInf)
        self.assertFalse(NegInf == Inf)
        self.assertTrue(NegInf != Inf)
        self.assertTrue(Inf != NegInf)
        self.assertTrue(NegInf < Inf)
        self.assertTrue(NegInf <= Inf)
        self.assertTrue(Inf > NegInf)
        self.assertTrue(Inf >= NegInf)
        self.assertFalse(NegInf > Inf)
        self.assertFalse(NegInf >= Inf)
        self.assertFalse(Inf < NegInf)
        self.assertFalse(Inf <= NegInf)
        # Negation
        self.assertTrue(NegInf is -Inf)
        self.assertTrue(Inf is -NegInf)
        self.assertTrue(-Inf < "a" <= Inf)

    def test_treap(self):
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
        infp = list(range(1, 16))
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

    def test_sorted_path(self):
        """Test path is indeed sorted."""
        t = complete_bst(4)
        u = t.left.right.left
        self.assertEqual(tuple(x.key for x in u.sorted_path()), (4, 5, 6, 8))
        self.assertEqual(
            tuple(x.key for x in u.parent.sorted_path()),
            (4, 6, 8)
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

    def test_node_comparisons_are_forbidden(self):
        """Test bug just described."""
        t = complete_bst(4)
        with self.assertRaises(TypeError):
            sorted(t.inorder_nodes())
        with self.assertRaises(TypeError):
            t <= t

    def test_binary_search(self):
        """Test binary search on a node."""
        x = treap(range(1, 11), [7, 10, 9, 8, 3, 2, 6, 4, 5, 1])
        self.assertEqual(x.search(2).key, 2)
        self.assertEqual(x.search(2.5), None)
        self.assertEqual(x.left.right.search(2), None)
        self.assertEqual(x.left.right.search(9).key, 9)


class TreapExecutionTests(unittest.TestCase):

    def test_access_times(self):
        X = [4, 10, 6, 8, 9, 4, 6, 10, 11, 2, 6]
        self.assertEqual(
            access_times(X),
            {
                2: [Inf, 10],
                4: [Inf, 6, 1],
                6: [Inf, 11, 7, 3],
                8: [Inf, 4],
                9: [Inf, 5],
                10: [Inf, 8, 2],
                11: [Inf, 9]
            }
        )

    def test_first_access_times(self):
        """Test first access time."""
        X = [4, 10, 6, 8, 9, 4, 6, 10, 11, 2, 6]
        self.assertEqual(
            first_access_times(X),
            {4: 1, 10: 2, 6: 3, 8: 4, 9: 5, 11: 9, 2: 10}
        )
        Y = [4, 6, 5, 4, 2, 7, 7, 3, 1]
        self.assertEqual(
            first_access_times(Y),
            {4: 1, 6: 2, 5: 3, 2: 5, 7: 6, 3: 8, 1: 9}
        )

    def test_canonical_tree(self):
        """Test Initial Treap."""
        t = canonical_tree([4, 10, 6, 8, 9, 4, 6, 10, 11, 2, 6])
        self.assertEqual(t.preorder_keys(), (4, 2, 10, 6, 8, 9, 11))
        u = canonical_tree([4, 6, 5, 4, 2, 7, 7, 3, 1])
        self.assertEqual(u.preorder_keys(), complete_bst(3).preorder_keys())

    def test_update_labels(self):
        """Test label updating, Inf handling, etc."""
        x = treap(range(1, 11), [7, 10, 9, 8, 3, 2, 6, 4, 5, 1])
        # Labels in canonical treap work
        x_copy = treap(range(1, 11), [7, 10, 9, 8, 3, 2, 6, 4, 5, 1])
        _update_labels(x.postorder_nodes())
        for y, z in zip(x.inorder_nodes(), x_copy.inorder_nodes()):
            self.assertTrue(y.priority == y.label == z.priority)
        # Change a priority
        w = x.left.left.left.right
        w.priority = 2
        _update_labels(x.postorder_nodes())
        new_labels = [y.label for y in x.postorder_nodes()]
        self.assertEqual(new_labels, [10, 9, 2, 2, 2, 6, 5, 4, 2, 1])
        # Set it back
        w.priority = 8
        _update_labels(x.postorder_nodes())
        for y, z in zip(x.inorder_nodes(), x_copy.inorder_nodes()):
            self.assertTrue(y.priority == y.label == z.priority)
        k = x.left.right
        k.priority = Inf
        k.left.priority = Inf
        _update_labels(x.postorder_nodes())
        inf_labels = [y.label for y in x.postorder_nodes()]
        self.assertEqual(inf_labels, [10, 9, 8, 7, 3, Inf, 5, 5, 2, 1])

    def test_initial_tree(self):
        """Test Kozma's tree with priorities."""
        kozma_preorder = (4, 2, 1, 3, 10, 6, 5, 8, 7, 9, 11)
        # Simple Initial Tree
        t = initial_tree(kozma_preorder)
        self.assertEqual(t.preorder_keys(), kozma_preorder)
        t_priorities = [x.priority for x in t.preorder_nodes()]
        t_labels = [x.label for x in t.preorder_nodes()]
        self.assertTrue(list(range(1, 12)) == t_labels == t_priorities)
        # Main Point: Non-Canonical Initial Tree
        X_Kozma = (8, 9, 4, 6, 10, 11, 2, 6)
        T_Kozma = initial_tree(X_Kozma, t)
        self.assertEqual(T_Kozma.preorder_keys(), kozma_preorder)
        reference_priorities = [Inf, Inf, 7, Inf, Inf, 2, 1, 4, 6, 5, 3]
        test_priorities = [x.priority for x in T_Kozma.postorder_nodes()]
        self.assertEqual(test_priorities, reference_priorities)
        reference_labels = [Inf, Inf, 7, Inf, Inf, 2, 1, 1, 6, 1, 1]
        test_labels = [x.label for x in T_Kozma.postorder_nodes()]
        self.assertEqual(reference_labels, test_labels)
        # Test Update Nodes on Subtree
        accessed_node = T_Kozma.search(8)
        accessed_node.priority = Inf
        _update_labels(accessed_node.path())
        starting_labels = [Inf, Inf, 7, Inf, Inf, 2, 2, 2, 6, 2, 2]
        test_start = [x.label for x in T_Kozma.postorder_nodes()]
        self.assertEqual(test_start, starting_labels)

    # def test_min_priority(self):
    #     """Test minimum priorities"""
    #     X = (8, 9, 4, 6, 10, 11, 2, 6)
    #     self.assertEqual(min_priority(X, 1, 6, 10), 1)
    #     self.assertEqual(min_priority(X, 1, 8, Inf), 1)
    #     self.assertEqual(min_priority(X, 1, -Inf, 6), 2)
    #     self.assertEqual(min_priority(X, 1, 4, 8), 3)

    def test_path_comparison_labels(self):
        """Ensure we can test these labels."""
        # Setup for Fig 2.4 of Lazlo Kozma Thesis
        kozma_preorder = (4, 2, 1, 3, 10, 6, 5, 8, 7, 9, 11)
        t = initial_tree(kozma_preorder)
        X_Kozma = (8, 9, 4, 6, 10, 11, 2, 6)
        T_Kozma = initial_tree(X_Kozma, t)
        accessed_node = T_Kozma.search(8)
        accessed_node.priority = Inf
        _update_labels(accessed_node.path())
        # Actual tests
        d = accessed_node.path_comparison_labels()
        self.assertTrue(d[0] == (3, 7, Inf))
        self.assertTrue(d[1] == (4, Inf, Inf))
        self.assertTrue(d[2] == (2, Inf, 2))
        self.assertTrue(d[3] == (2, 2, 6))

    def test_greedy_execution(self):
        """At long last, test the greedy execution."""
        X = (8, 9, 4, 6, 10, 11, 2, 6)
        T = canonical_tree((4, 2, 1, 3, 10, 6, 5, 8, 7, 9, 11))
        E = GreedyExecution(X, T)
        t1, x = next(E)
        self.assertEqual(x.key, 8)
        self.assertEqual(t1.preorder_keys(), T.preorder_keys())
        t2, y = next(E)
        self.assertEqual(y.key, 9)
        self.assertEqual(
            t2.preorder_keys(),
            (10, 8, 4, 2, 1, 3, 6, 5, 7, 9, 11)
        )
        t3, z = next(E)
        self.assertEqual(z.key, 4)
        self.assertEqual(
            t3.preorder_keys(),
            (8, 4, 2, 1, 3, 6, 5, 7, 10, 9, 11)
        )


if __name__ == '__main__':

    unittest.main()
