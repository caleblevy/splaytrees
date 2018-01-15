"""Drawings of BSTs. This is 'mockup' for now."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection, LineCollection

from bst import *


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
    locations = np.array(zip(range(n), d))
    bottom_inds = [i for i in range(n) if i != p[i]]
    top_inds = map(p.__getitem__, bottom_inds)
    u = np.array(map(locations.__getitem__, bottom_inds)).reshape(-1, 1, 2)
    v = np.array(map(locations.__getitem__, top_inds)).reshape(-1, 1, 2)
    edges = np.hstack([u, v])
    return keys, locations, edges


def plot_subtree(x):
    keys, locs, edges = _plot_points(x)
    n = len(keys)
    fig = plt.figure()
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
    # Setup
    ax.autoscale_view()
    plt.show()


if __name__ == '__main__':
    t = Tree.from_encoding("lllprrlpppprpprlrpprlppp")
    assert t.preorder() == (8, 6, 2, 1, 3, 5, 4, 7, 11, 9, 10, 13, 12)
    k, d, p = _plot_info(t.root)
    assert k == tuple(range(1, 14)), k
    assert d == (4, 3, 4, 6, 5, 2, 3, 1, 3, 4, 2, 4, 3), d
    assert p == (1, 5, 1, 4, 2, 7, 5, 7, 10, 8, 7, 12, 10), p

    keys, locs, edges = _plot_points(t.root)
    plot_subtree(t.root)
