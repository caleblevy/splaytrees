"""Test decoding subsequences."""
from functools import partial
import unittest

from pathcodes import Node, splay, move_to_root, simple_splay, static


def decoder(encodings, op=splay):
    """Return starting tree and splayed nodes given encodings."""
    r = Node()
    nodes = []
    for e in encodings:
        x = r.decode(e)
        nodes.append(x)
        r = op(x)
    r = r.reset()
    return (r, nodes)


class TestDecoder(unittest.TestCase):
    """Test decoder works as expected."""

    def test_static_decoder(self):
        """Test encoding of static tree is same."""
        code_1 = ["1", "111", "11111", "1", "11111"]
        t, nodes = decoder(code_1, static)
        self.assertTrue(t.is_isomorphic_to(Node.from_cursor('r'*5)))
        for e, node in zip(code_1, nodes):
            self.assertTrue(e == node.encode())
        code_2 = ["0", "10", "001", "101"]
        t, nodes = decoder(code_2, static)
        self.assertTrue(t.is_isomorphic_to(Node.from_cursor('llrppprlr')))
        for e, node in zip(code_2, nodes):
            self.assertTrue(e == node.encode())

    def test_splay_decoder(self):
        """Test encoding of splay trees."""
        code_1 = ["1", "111", "11111", "1", "11111"]
        t, nodes = decoder(code_1)
        self.assertTrue(t.is_isomorphic_to(Node.from_cursor('r'*15)))
        for e, node in zip(code_1, nodes):
            self.assertTrue(e == node.encode())
            node.splay()
        code_2 = ["0", "10", "001", "101"]
        t, nodes = decoder(code_2)
        self.assertTrue(t.is_isomorphic_to(Node.from_cursor('llrpprl')))
        for e, node in zip(code_2, nodes):
            self.assertTrue(e == node.encode())
            node.splay()


if __name__ == '__main__':
    unittest.main()
