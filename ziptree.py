"""Implementations for zip trees."""

import functools
import unittest

from random import choice, shuffle


def cointoss():
    return choice([0, 1])


def geometricvariate():
    """Toss coin until heads."""
    c = 0
    while cointoss():
        c += 1
    return c


def _ranksizevariate(n):
    """Sample size of largest rank among n nodes."""
    s = 0
    for _ in range(n):
        s = max(s, len(bin(geometricvariate()))-2)
    return s


def _maker(maptype):
    """Turn a generator into a specified type of sequence."""
    def outputter(generator):
        @functools.wraps(generator)
        def mapper(*args, **kwargs):
            return maptype(generator(*args, **kwargs))
        return mapper
    return outputter


class Node(object):
    __slots__ = ("key", "rank", "left", "right")

    def __init__(x, key):
        x.key = key
        x.left = x.right = None
        x.rank = geometricvariate()


def _zip(x, y):
    if x is None:
        return y
    if y is None:
        return x
    if x.rank < y.rank:
        y.left = _zip(x, y.left)
        return y
    x.right = _zip(x.right, y)
    return x


def _insert_zip(x, root):
    """Insert x into tree with given root, and return root of new tree."""
    if root is None:
        return x
    if x.key < root.key:
        if x is _insert_zip(x, root.left):
            if x.rank < root.rank:
                root.left = x
            else:
                root.left = x.right
                x.right = root
                return x
    else:
        if x is _insert_zip(x, root.right):
            if x.rank <= root.rank:
                root.right = x
            else:
                root.right = x.left
                x.left = root
                return x
    return root


def _delete_zip(x, root):
    """Delete x from tree and return resulting root."""
    if x.key == root.key:
        return _zip(root.left, root.right)
    if x.key < root.key:
        if x.key == root.left.key:
            root.left = _zip(root.left.left, root.left.right)
        else:
            _delete_zip(x, root.left)
    else:
        if x.key == root.right.key:
            root.right = _zip(root.right.left, root.right.right)
        else:
            _delete_zip(x, root.right)
    return root


class ZipTree(object):
    __slots__ = "root"

    def __init__(T, items=None):
        T.root = None
        if items is not None:
            T.update_zip(items)

    def update_zip(T, items):
        for k in items:
            T.insert_zip(k)

    def search(T, k):
        x = T.root
        while x is not None:
            if k < x.key:
                x = x.left
            elif k > x.key:
                x = x.right
            else:
                return True
        return False

    def _insert_zip_with_rank(T, k, rank=None):
        if not T.search(k):
            z = Node(k)
            if rank is not None:
                z.rank = rank
            T.root = _insert_zip(z, T.root)

    def insert_zip(T, k):
        T._insert_zip_with_rank(k)

    def delete_zip(T, k):
        if T.search(k):
            T.root = _delete_zip(Node(k), T.root)

    @_maker(tuple)
    def _preorder(T):
        """Traverse subtree rooted at x inorder."""
        x = T.root
        stack = []
        while True:
            if x is not None:
                yield x.key
                stack.append(x)
                x = x.left
            else:
                if stack:
                    x = stack.pop()
                    x = x.right
                else:
                    break


class TestZipTree(unittest.TestCase):

    def test_find(self):
        """Test finding nodes."""
        T = ZipTree()
        self.assertFalse(T.search(1))
        self.assertFalse(T.search("a"))
        T.insert_zip("a")
        T.insert_zip("b")
        self.assertTrue(T.search("b"))
        self.assertTrue(T.search("a"))
        T.insert_zip("ab")
        self.assertFalse(T.search("abb"))

    def test_insert_rank(self):
        """Test Zip Tree insert."""
        T = ZipTree()
        for i in range(1, 5):
            T._insert_zip_with_rank(i, 0)
        for i in range(6, 11):
            T._insert_zip_with_rank(i, 0)
        self.assertEqual((1, 2, 3, 4, 6, 7, 8, 9, 10), T._preorder())
        T._insert_zip_with_rank(5, 1)
        self.assertEqual((5, 1, 2, 3, 4, 6, 7, 8, 9, 10), T._preorder())
        lst = [(i, geometricvariate()) for i in range(100)]
        T1 = ZipTree()
        for k, r in lst:
            T1._insert_zip_with_rank(k, r)
        shuffle(lst)
        T2 = ZipTree()
        for k, r in lst:
            T2._insert_zip_with_rank(k, r)
        self.assertEqual(T1._preorder(), T2._preorder())

    def test_delete_zip(self):
        """Test Zip Tree delete"""
        T = ZipTree()
        T.delete_zip(1)
        T.update_zip([1])
        T.delete_zip(1)
        self.assertEqual(T._preorder(), ())
        lst = [(i, geometricvariate()) for i in range(100)]
        T1 = ZipTree()
        for k, r in lst:
            T1._insert_zip_with_rank(k, r)
        for k, _ in lst[70:]:
            T1.delete_zip(k)
        print(T1._preorder())
        T2 = ZipTree()
        for k, r in lst[:70]:
            T2._insert_zip_with_rank(k, r)
        self.assertEqual(T1._preorder(), T2._preorder())


if __name__ == '__main__':
    unittest.main()
