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
        [1, "b", 0, 9, 5, "c", 1, 0, 0, "a", 1, 0, 0]
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

    def __len__(T):
        return len(T._arr)

    def _find(T, key):
        """Return index of key, if found."""
        x = T[root]
        if x == null:
            return root
        while x != null:
            y = x
            if key < T[x]:
                x = T[x + left]
            elif key > T[x]:
                x = T[x + right]
            else:
                break
        return y

    def find(T, key):
        """See if key is in T."""
        return key == T[T._find(key)]

    def insert(T, key):
        """Insert key into T."""
        x = T._find(key)
        if x != root and key == T[x]:
            return
        if x == root:
            T[x] = len(T)
        elif key < T[x]:
            T[x + left] = len(T)
        else:
            T[x + right] = len(T)
        T._arr.extend([key, x, 0, 0])

    def _rotate(T, x):
        y = T[x + parent]
        assert y != root  # Do not rotate root
        if x is T[y + right]:
            x, y = y, x
        if x is T[y + left]:
            # Shift around subtree
            w = T[x + right]
            T[y + left] = w
            if w != null:
                T[w + parent] = y
            # Switch up parent pointers
            z = T[y + parent]
            T[x + parent] = z
            if y == T[z + right]:
                T[z + right] = x
            elif y == T[z + left]:
                T[z + left] = x
            else:
                T[root] = x  # y was root
            T[x + right] = y
            T[y + parent] = x
        else:  # y is x.right
            # Shift around subtree
            w = T[y + left]
            T[x + right] = w
            if w != null:
                T[w + parent] = x
            #switch up paret
            z = T[x + parent]
            T[y + parent] = z
            if x == T[z + right]:
                T[z + right] = y
            elif x == T[z + left]:
                T[z + left] = y
            else:
                T[root] = y
            T[y + left] = x
            T[x + parent] = y

    def _walk(T, order=None):
        """Do all three edge traversals at once."""
        x = T[root]
        if x == null:
            return
        l = r = False  # l is true if all node's in x.left are visited
        while True:
            if order is None:
                yield T[x]
            if not l:
                if order == -1:
                    yield T[x]
                y = T[x + left]
                if y == null:
                    l = True
                else:
                    if order == "":
                        yield "l"
                    x = y
            elif not r:
                if order == 0:
                    yield T[x]
                y = T[x + right]
                if y == null:
                    r = True
                else:
                    if order == "":
                        yield "r"
                    x = y
                    l = False
            else:
                if order == 1:
                    yield T[x]
                y = T[x + parent]
                if y == root:
                    return
                elif x == T[y + left]:
                    r = False
                if order == "":
                    yield "p"
                x = y

    def walk(T):
        return tuple(T._walk())

    def encoding(T):
        """Encode cursor movements traversing the subtree rooted at x."""
        return "".join(T._walk(""))

    def preorder(T):
        return tuple(T._walk(-1))

    def inorder(T):
        return tuple(T._walk(0))

    def postorder(T):
        return tuple(T._walk(1))


class TestArrayTree(unittest.TestCase):

    def test_private_find(self):
        """Test index math"""
        T = ArrayTree("bca")
        self.assertEqual(9, T._find(" "))
        self.assertEqual(9, T._find("a "))
        self.assertEqual(9, T._find("a"))
        self.assertEqual(1, T._find("b"))
        self.assertEqual(5, T._find("ba"))
        self.assertEqual(5, T._find("ca"))
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
        self.assertEqual(17, T._find(" a"))
        T2 = ArrayTree()
        T2.insert(4)
        self.assertFalse(ArrayTree().find(7))
        self.assertEqual([1, 4, 0, 0, 0], T2._arr)

    def test_rotate(self):
        """Test rotation."""
        T = ArrayTree("bca")
        T._rotate(T._find("a"))
        r = T[0]
        rr = T[r + right]
        rrr = T[rr + right]
        self.assertEqual("a", T[r])
        self.assertEqual("b", T[rr])
        self.assertEqual("c", T[rrr])
        T._rotate(T._find("b"))
        self.assertEqual(ArrayTree("bca")._arr, T._arr)
        T.insert("d")
        T.insert("ba")
        q = T.preorder()
        T._rotate(T._find("c"))
        self.assertEqual(("c", "b", "a", "ba", "d"), T.preorder())
        T._rotate(T._find("b"))
        self.assertEqual(q, T.preorder())

    def test_walks(self):
        """Test pre, post, in-order, encoding and walk"""
        T = ArrayTree("bca")
        R = ArrayTree("bac")
        self.assertEqual("lprp", T.encoding())
        self.assertEqual(tuple("baaabcccb"), T.walk())
        self.assertEqual(tuple("abc"), T.inorder())
        self.assertEqual(tuple("bac"), T.preorder())
        self.assertEqual(tuple("acb"), T.postorder())
        self.assertEqual(T.encoding(), R.encoding())
        self.assertEqual(T.walk(), R.walk())
        self.assertEqual(T.inorder(), R.inorder())
        self.assertEqual(T.preorder(), R.preorder())
        self.assertEqual(T.postorder(), R.postorder())
        self.assertNotEqual(T._arr, R._arr)


if __name__ == '__main__':
    unittest.main()
