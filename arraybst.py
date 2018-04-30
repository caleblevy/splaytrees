"""Implementation of Array-Based BST."""

import unittest


def _iskey(ind):
    """Return if index corresponds to tree."""
    return not (ind-1) % 4


def _isleft(ind):
    """Return if index corresponds to parent."""
    return not (ind-3) % 4


def _isright(ind):
    if ind == 0:
        return False
    return (ind-4) % 4


class ArrayTree(object):
    """Tree stored with each "node" is contiguous "key, parent, left, right"
    eg.
        [None, "b", 0, 9, 5, "c", 1, 0, 0, "a", 1, 0, 0]
    is equivalent to 
        b
       / \
      a  c
    """

    def __init__(T, items=None):
        T._arr = [None]
        if items is not None:
            for key in items:
                T.insert(key)

    def __getitem__(T, ind):
        return T._arr[ind]

    def _find(T, key):
        """Return index of key, if found."""
        if len(T._arr) == 1:
            return 0
        ind = 1
        while T[ind] is not None:
            prev_ind = ind
            if key < T[ind]:
                ind = T[ind + 2]
            elif key > T[ind]:
                ind = T[ind + 3]
            else:
                break
        if key > T[prev_ind]:
            return prev_ind + 3
        elif key < T[prev_ind]:
            return prev_ind + 2
        else:
            return prev_ind

    def find(T, key):
        """See if key is in T."""
        return _iskey(T._find(key))

    def insert(T, key):
        """Insert key into T."""
        ind = T._find(key)
        if _iskey(ind):
            return
        node = [key, 0, 0, 0]
        if ind != 0:
            T._arr[ind] = len(T._arr)
            direction = (ind - 1) % 4
            parent = ind - direction
            node[1] = parent
        T._arr.extend(node)

    def _rotate(T, ind):
        parent = T[ind + 1]
        


class TestArrayTree(unittest.TestCase):

    def test_private_find(self):
        """Test index math"""
        T = ArrayTree("bca")
        self.assertEqual(11, T._find(" "))
        self.assertEqual(12, T._find("a "))
        self.assertEqual(9, T._find("a"))
        self.assertEqual(1, T._find("b"))
        self.assertEqual(7, T._find("ba"))
        self.assertEqual(8, T._find("ca"))
        self.assertEqual(5, T._find("c"))
        self.assertTrue(T.find("a"))
        self.assertTrue(T.find("b"))
        self.assertTrue(T.find("c"))
        self.assertFalse(T.find(" "))
        self.assertFalse(T.find("a "))
        self.assertFalse(T.find("ba"))
        self.assertFalse(T.find("ca"))
        arr_old = T._arr[:]
        T.insert("a")
        self.assertEqual(arr_old, T._arr)
        T.insert("a ")
        self.assertEqual(13, T._find("a "))
        T.insert(" ")
        self.assertEqual(17, T._find(" "))
        self.assertEqual(20, T._find(" a"))
        T2 = ArrayTree()
        T2.insert(4)
        self.assertFalse(ArrayTree().find(7))
        self.assertEqual([None, 4, 0, 0, 0], T2._arr)


if __name__ == '__main__':
    unittest.main()