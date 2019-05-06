import numpy as np
import numpy.linalg as lin
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection, LineCollection

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


def plot_info(T):
    """Return rudiments necessary to make acceptable plot."""
    # k[i] = key of ith largest node
    # d[i] = depth of ith largest node
    # p[i] = index of k[i].parent (i.e. k[p[i]] == k[i].parent.key)
    k = keys = T.root.inorder_keys()
    d = tuple(map(T.root.depths().__getitem__, k))
    k_inv = {y: x for x, y in enumerate(k)}
    p_keys = [getattr(y.parent, "key", y.key) for y in T.root.inorder_nodes()]
    p = tuple(map(k_inv.__getitem__, p_keys))
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


def plot_tree(T, *args, **kwargs):
    k,l,e = plot_info(T)
    make_plot(k,l,e, *args, **kwargs)


def find_from_encoding(T, pathcode):
    """Find node with pathcode in T."""
    x = T.root
    for c in pathcode:
        if c == 'l':
            x = x.left
        elif c == 'r':
            x = x.right
        else:
            raise ValueError("Blah!")
    return x


def wilber_plot(pathcode):
    """Plot Wilber's bound for pathcode"""
    if 'p' in pathcode:
        raise ValueError("Pathcode has no parents.")
    X = Tree.from_encoding(pathcode)
    Y = Tree.from_encoding(pathcode)
    x = find_from_encoding(X, pathcode).key
    X.move_to_root(x)
    k, l, e = plot_info(Y)
    k_x, l_x, e_x = plot_info(X)
    r = np.max(l[:, 0])+2
    l_x[:, 0] += r
    e_x[:, :, 0] += r
    k += k_x
    l = np.concatenate((l, l_x))
    e = np.concatenate((e, e_x))
    make_plot(k,l,e,show=True)

if __name__ == '__main__':
    # plot_tree(cbst(5), show=True)
    wilber_plot('rrrlllrrlrll')