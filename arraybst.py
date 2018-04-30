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


root = null = 0
parent = 1
left = 2
right = 3


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
        T._arr = [null]
        if items is not None:
            for key in items:
                T.insert(key)

    def __getitem__(T, ind):
        return T._arr[ind]

    def __setitem__(T, ind, v):
        T._arr[ind] = v

    def _find(T, key):
        """Return index of key, if found."""
        x = T[root]
        if x == null:
            return null
        while x != null:
            y = x
            if key < T[x]:
                x = T[x + left]
            elif key > T[x]:
                x = T[x + right]
            else:
                break
        if key > T[y]:
            return y + right
        elif key < T[y]:
            return y + left
        else:
            return y

    def find(T, key):
        """See if key is in T."""
        return _iskey(T._find(key))

    def insert(T, key):
        """Insert key into T."""
        ind = T._find(key)
        if _iskey(ind):
            return
        node = [key, 0, 0, 0]
        T[ind] = len(T._arr)
        if ind != 0:
            direction = (ind - 1) % 4
            p = ind - direction
            node[1] = p
        T._arr.extend(node)

    def _rotate(T, ind):
        x = ind
        y = T[ind + parent]
        assert y != 0  # Do not rotate root
        if x is T[y + right]:
            x, y = y, x
        if x is T[y + left]:
            # Shift around subtree
            w = T[x + right]
            T[y + left] = w
            if w != 0:
                T[w + parent] = y
            # Switch up parent pointers
            z = T[y + parent]
            T[x + parent] = z
            # y is the root
            if z != 0:
                if y is T[z + right]:
                    T[z + right] = x
                else:
                    T[z + left] = x
            else:
                T[0] = x
            


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
        self.assertEqual([1, 4, 0, 0, 0], T2._arr)


if __name__ == '__main__':
    unittest.main()
