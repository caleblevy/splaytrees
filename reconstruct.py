"""Reconstruct original tree and accessed nodes given list of binary encodings
of splay paths."""

import unittest


def path_decode(b):
    """Decode binary encoded path, 0 is left, 1 is right."""
    l = r = x = 0  # accessed node defined arbitrarily as 0
    p = [x]
    for bit in reversed(b):
        if bit == "1":
            l -= 1
            p.append(l)
        else:
            r += 1
            p.append(r)
    return list(reversed(p))


class TestPathDecode(unittest.TestCase):

    def test_path_decoder(self):
        """Test simple binary paths."""
        p = path_decode("1101")
        self.assertEqual([-3, -2, 1, -1, 0], path_decode("1101"))
        self.assertEqual([0], path_decode(""))
        self.assertEqual([1, 0], path_decode("0"))
        self.assertEqual([-1, 0], path_decode("1"))


if __name__ == '__main__':
    unittest.main()