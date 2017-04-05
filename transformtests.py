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


def splaytransformtests(n):
    """Do tests for connectedness, hamiltonian, weight."""
    G = nx.DiGraph()
    for p in treegen(n):
        for x in p[1:]:
            t = SplayTree(p)
            t.access(x)
            G.add_edge(p, t.preorder(), weight=t.count)
    print("Splay stats for n=%s:" % n)
    print("----------------------")
    print("B(%s) = %s" % (n, B(n)))
    scc = nx.is_strongly_connected(G)
    print("Is strongly connected: %s" % nx.is_strongly_connected(G))
    if scc:
        print("Access Overhead: %s" % nx.diameter(G))
        print("Cost Overhead: %s" % weighted_diameter(G))
    else:
        G = nx.condensation(G)
    pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_labels(G, pos, font_size=6, font_family='sans-serif')
    plt.axis("off")
    plt.savefig("weighted_graph.png") # save as png
    return G

splaytransformtests(7)