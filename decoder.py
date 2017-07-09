"""Test decoding subsequences."""

from functools import partial
from re import finditer
import unittest

from pathcodes import Node, splay, move_to_root, simple_splay, static


def _count_overlapping(substring, string):
    """Count all occurrences of string in substring."""
    matches = finditer(r'(?=(%s))' % substring, string)
    return sum(1 for _ in matches)


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


def za_count(encodings):
    """Count number of zig-zags on encoding paths."""
    c = 0
    for e in encodings:
        c += _count_overlapping("01", e) + _count_overlapping("10", e)
    return c


def zi_count(encodings):
    """count number of zig-zigs on encoding paths."""
    c = 0
    for e in encodings:
        c += _count_overlapping("11", e) + _count_overlapping("00", e)
    return c


def encoder(nodes, op=splay):
    """Given starting tree and nodes, encode them with given op."""
    encodings = []
    for node in nodes:
        encodings.append(node.encode())
        op(node)
    return encodings


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

    def test_counters(self):
        """Ensure path counters correctly get zig-zigs and zig-zags."""
        code_1 = ["1", "111", "11111", "1", "11111"]
        self.assertTrue(zi_count(code_1) == 10)
        self.assertTrue(za_count(code_1) == 0)
        code_2 = ["0", "10", "001", "101"]
        self.assertTrue(zi_count(code_2) == 1)
        self.assertTrue(za_count(code_2) == 4)

    def test_encoder(self):
        """Test that we properly encode everything."""
        code_1 = ["1", "111", "11111", "1", "11111"]
        _, static_nodes = decoder(code_1, static)
        self.assertTrue(code_1 == encoder(static_nodes, static))
        _, splay_nodes = decoder(code_1)
        self.assertTrue(code_1 == encoder(splay_nodes))
        self.assertTrue(
            encoder(static_nodes, splay) ==
            ["1", "11", "11", "0000", "11"])
        code_2 = ["0", "10", "001", "101"]
        _, static_nodes = decoder(code_2, static)
        self.assertTrue(code_2 == encoder(static_nodes, static))


if __name__ == '__main__':
    unittest.main()
