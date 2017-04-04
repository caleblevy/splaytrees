"""Find the diameter and cost overhead of Splaying any tree of four nodes into
another."""

import itertools
from propersplay import SplayTree, Node

def _tree_from_preorder(preorder):
    """Slow way to build a tree from the preorder permutation p."""
    if preorder:
        root_item = preorder[0]
        left_items = [item for item in preorder if item < root_item]
        right_items = [item for item in preorder if item > root_item]
        root = Node(root_item)
        root.left = _tree_from_preorder(left_items)
        root.right = _tree_from_preorder(right_items)
        if root.left is not None:
            root.left.parent = root
        if root.right is not None:
             root.right.parent = root
        return root


def tree_from_preorder(p):
    """Return splay tree with preorder sequence P."""
    T = SplayTree()
    T.root = _tree_from_preorder(p)
    return T


four_node_trees = [
    (4, 3, 2, 1), (1, 2, 3, 4),  # Il, Ir
    (3, 2, 1, 4), (2, 1, 3, 4),  # Vl, Vr
    (4, 1, 3, 2), (1, 4, 2, 3),  # Zl, Zr
    (4, 1, 2, 3), (1, 4, 3, 2),  # Pl, Pr
    (3, 1, 2, 4), (2, 1, 4, 3),  # Ul, Ur
    (4, 3, 1, 2), (1, 2, 4, 3),  # Ll, Lr
    (4, 2, 1, 3), (1, 3, 2, 4),  # Yl, Yr
]

G = {T: [] for T in four_node_trees}
for T in G:
    assert tuple(tree_from_preorder(T).preorder()) == T

for p in itertools.permutations(range(1, 5)):
    if p not in G:
        print(p)
        assert tuple(tree_from_preorder(T).preorder()) != p


for p in G:
    for x in p[1:]:
        T = tree_from_preorder(p)
        T.access(x)
        G[p].append((tuple(T.preorder()), T.count))


weighted_edges = []
for T1 in G:
    for T2, d in G[T1]:
        weighted_edges.append((T1, T2, d))


print(len(weighted_edges))
