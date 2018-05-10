"""Drawings of BSTs. This is 'mockup' for now."""

import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection, LineCollection
from matplotlib.backends.backend_pdf import PdfPages

from bst import *


def cbst(k):
    """Complete binary search tree of size 2^k-1."""
    n = 2**k - 1
    t = Tree(range(n, 0, -1))
    i = 1
    while i < n:
        t.splay(i)
        i *= 2
    return t


def _plot_info(x):
    """Return rudiments necessary to make acceptable plot."""
    # k[i] = key of ith largest node
    # d[i] = depth of ith largest node
    # p[i] = index of k[i].parent (i.e. k[p[i]] == k[i].parent.key)
    k = x.inorder_keys()
    d = tuple(map(x.depths().__getitem__, k))
    k_inv = {y: x for x, y in enumerate(k)}
    p_keys = [getattr(y.parent, "key", y.key) for y in x.inorder_nodes()]
    p = tuple(map(k_inv.__getitem__, p_keys))
    return k, d, p


def _plot_points(x):
    keys, d, p = _plot_info(x)
    n = len(keys)
    d = 1 - np.array(d)
    locations = np.array(list(zip(range(n), d)))
    locations = locations/np.sqrt(2)
    bottom_inds = [i for i in range(n) if i != p[i]]
    top_inds = map(p.__getitem__, bottom_inds)
    u = np.array(list(map(locations.__getitem__, bottom_inds))).reshape(-1, 1, 2)
    v = np.array(list(map(locations.__getitem__, top_inds))).reshape(-1, 1, 2)
    edges = np.hstack([u, v])
    return keys, locations, edges


def make_plot(keys, locs, edges, fname="myplot.pdf", labels=True, show=False, fontsize=12, verttextoffset=0, arrows=None):
    y_min = np.min(locs[:, 1])
    y_max = np.max(locs[:, 1])
    x_min = np.min(locs[:, 0])
    x_max = np.max(locs[:, 0])
    fig = plt.figure(figsize=(1.1*(x_max-x_min), 1.1*(y_max-y_min)))  # Figsize needed to ensure text isn't scrunched up
    ax = fig.gca()
    # Add Edges
    edgeCol = LineCollection(
        edges,
        color=(0,0,0),
        linewidth=.5,
        zorder=1)
    ax.add_collection(edgeCol)
    # Add Points
    vertsCol = PatchCollection(
        [plt.Circle(p, 0.25) for p in locs],
        facecolors="white",
        edgecolors="black",
        linewidths=0.5,
        zorder=2)
    ax.add_collection(vertsCol)
    # Add text
    if labels:
        for p, k in zip(locs, keys):
            x, y = p
            plt.text(
                x, y-verttextoffset,
                str(k),
                fontsize=fontsize,
                horizontalalignment='center',
                verticalalignment='center')
    if arrows is not None:
        for arrow in arrows:
            x1, y1, x2, y2 = arrow
            ax.arrow(x1, y1, x2, y2, head_width=0.15, head_length=0.1, fc='k', ec='k')
    # Setup
    plt.axis('off')
    ax.autoscale_view()
    ax.set_aspect(1)  # Needed to ensure circles are circular
    plt.savefig(fname, dpi=100, bbox_inches="tight")
    if show:
        plt.show()


def ham_cycle_plot():
    """Plot the Hamiltonian cycle of splay's transition graph."""
    T = Tree((1,2,3,4))
    requests = [4,1,3,4,1,2,4,1,4,2,1,4,3,1]
    m = len(requests)
    keys = []
    locs = edges = None
    t = [-2*np.pi*i/m for i in range(m)]
    x = np.cos(t)
    y = np.sin(t)
    circle_points = np.stack([x, y]).T
    circle_points *= 10
    for r, p in zip(requests, circle_points):
        _, l, e = _plot_points(T.root)
        k = [""]*4
        k[r-1] = "*"
        center = np.mean(l, axis=0)
        l += p - center
        e += p - center
        if locs is None:
            locs = l
            edges = e
        else:
            locs = np.vstack([locs, l])
            edges = np.vstack([edges, e])
        keys += k
        T.splay(r)
    source = circle_points
    dest = np.roll(circle_points, -1, axis=0)
    units = (dest - source)/lin.norm(dest- source, axis=1)[:, np.newaxis]
    r = 2
    source += r*units 
    dest -= r* units
    circle_points = np.concatenate([source, dest-source], axis=1)
    make_plot(keys, locs, edges, fname="ham-cycle.pdf", show=False, fontsize=16, verttextoffset=.05, arrows=circle_points)


ham_cycle_plot()


def plot_subtree(x, fname="myplot.pdf", labels=True, show=False):
    keys, locs, edges = _plot_points(x)
    make_plot(keys, locs, edges, fname, labels, show)


if __name__ == '__main__':
    t = Tree.from_encoding("lllprrlpppprpprlrpprlppp")
    assert t.preorder() == (8, 6, 2, 1, 3, 5, 4, 7, 11, 9, 10, 13, 12)
    k, d, p = _plot_info(t.root)
    assert k == tuple(range(1, 14)), k
    assert d == (4, 3, 4, 6, 5, 2, 3, 1, 3, 4, 2, 4, 3), d
    assert p == (1, 5, 1, 4, 2, 7, 5, 7, 10, 8, 7, 12, 10), p

    keys, locs, edges = _plot_points(t.root)
    plot_subtree(t.root, "tree_sample.pdf")

    t2 = cbst(7)
    plot_subtree(t2.root, "complete_7.pdf")
    plot_subtree(cbst(5).root, "complete_5.pdf")
    t_samp = Tree()
    for i in "aihjgfclkendbpmo":
        t_samp.move_to_root(i)
    plot_subtree(t_samp.root, "wilber_sample.pdf")
    t_post = Tree(t_samp.postorder())
    plot_subtree(t_post.root, "postorder.pdf")
