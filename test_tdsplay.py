"""Separate unit tests for top-down-splay, since it was most complicated to
implement, and not based on reference implementation."""

import unittest

from topdownsplay import TDSplayTree, BinaryNode
from propersplay import SplayTree


def _tree_from_preorder(preorder):
    """Slow way to build a tree from the preorder permutation p."""
    if preorder:
        root_item = preorder[0]
        left_items = [item for item in preorder if item < root_item]
        right_items = [item for item in preorder if item > root_item]
        root = BinaryNode(root_item)
        root.left = _tree_from_preorder(left_items)
        root.right = _tree_from_preorder(right_items)
        return root


def tdpreorder(preorder):
    root = _tree_from_preorder(preorder)
    T = TDSplayTree()
    T.root = root
    return T


class TestTDSplay(unittest.TestCase):

    pass
