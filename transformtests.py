"""Find the diameter and cost overhead of Splaying any tree of four nodes into
another."""

import networkx as nx
import matplotlib.pyplot as plt

from propersplay import SplayTree, Node
from treerank import treegen, B

# For fun
four_node_trees = [
    (4, 3, 2, 1), (1, 2, 3, 4),  # Il, Ir
    (3, 2, 1, 4), (2, 1, 3, 4),  # Vl, Vr
    (4, 1, 3, 2), (1, 4, 2, 3),  # Zl, Zr
    (4, 1, 2, 3), (1, 4, 3, 2),  # Pl, Pr
    (3, 1, 2, 4), (2, 1, 4, 3),  # Ul, Ur
    (4, 3, 1, 2), (1, 2, 4, 3),  # Ll, Lr
    (4, 2, 1, 3), (1, 3, 2, 4),  # Yl, Yr
]

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


def weighted_diameter(G):
    """Wrapper for graph diameter of weighted networkx graph."""
    paths = nx.shortest_path(G, weight="weight")
    maxcost = -float('inf')
    i = 0
    for u in paths:
        for v in paths[u]:
            if u != v:
                current_path = paths[u][v]
                w_prev = current_path[0]
                cost = 0
                # Since their shortest path alg does not preserve weight info
                for w in current_path[1:]:
                    cost += G.get_edge_data(w_prev, w)["weight"]
                    w_prev = w
                maxcost = max(cost, maxcost)
    return maxcost


def hamilton(G):
    """Determine if graph has hamiltonian cycle"""
    F = [(G,[G.nodes()[0]])]
    n = G.number_of_nodes()
    while F:
        graph,path = F.pop()
        confs = []
        for node in graph.neighbors(path[-1]):
            conf_p = path[:]
            conf_p.append(node)
            conf_g = nx.Graph(graph)
            conf_g.remove_node(path[-1])
            confs.append((conf_g,conf_p))
        for g,p in confs:
            if len(p)==n:
                return p
            else:
                F.append((g,p))
    return None


def splaytransformtests(n):
    """Do tests for connectedness, hamiltonian, weight."""
    G = nx.DiGraph()
    for p in treegen(n):
        for x in p[1:]:
            t = tree_from_preorder(p)
            t.access(x)
            G.add_edge(p, t.preorder(), weight=t.count)
    print("Splay stats for n=%s:" % n)
    print("----------------------")
    print("B(%s) = %s" % (n, B(n)))
    print("Is strongly connected: %s" % nx.is_strongly_connected(G))
    print("Access Overhead: %s" % nx.diameter(G))
    print("Cost Overhead: %s" % weighted_diameter(G))
    pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')
    plt.axis("off")
    plt.savefig("weighted_graph.png") # save as png
    return G

splaytransformtests(4)