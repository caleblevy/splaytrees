"""Find the diameter and cost overhead of Splaying any tree of four nodes into
another."""

import networkx as nx
import matplotlib.pyplot as plt

from topdownsplay import tdfrompre
from treerank import treegen, B
from bst import Tree
from draw import plot_subtree


def splaytransformtests(n):
    """Do tests for connectedness, hamiltonian, weight."""
    G = nx.DiGraph()
    for p in treegen(n):
        for x in p[1:]:
            t = tdfrompre(p)
            t.__contains__(x)
            G.add_edge(p, t.preorder())
    print("Splay stats for n=%s:" % n)
    print("----------------------")
    print("B(%s) = %s" % (n, B(n)))
    print("Is strongly connected: %s" % nx.is_strongly_connected(G))
    # print("Access Overhead: %s" % nx.diameter(G))
    # print("Cost Overhead: %s" % weighted_diameter(G))
    for c in nx.strongly_connected_components(G):
        if len(c) > 2:
            break
    for i, pre in enumerate(c):
        print(i)
        T = Tree(pre)
        plot_subtree(T.root, "treeplots/tree_" + str(i)+'.pdf')
    H = nx.condensation(G)
    pos = nx.shell_layout(H)
    nx.draw_networkx_nodes(H, pos, node_size=700)
    nx.draw_networkx_edges(H, pos, width=1)
    nx.draw_networkx_labels(H, pos, font_size=6, font_family='sans-serif')
    plt.axis("off")
    plt.savefig("weighted_graph.png") # save as png
    return G


splaytransformtests(8)