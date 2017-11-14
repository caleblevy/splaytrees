"""Attempt(s) to separate Splay from Wilber2 using zig-zags."""
from __future__ import print_function

import pprint

from bst import *


def all_costs(s):
    """Print all costs for s in a pretty fashion."""
    print("Move-to-Root:")
    print("  Crossing:", mr_crossing_cost(s))
    print("  Inside:", mr_inside_cost(s))
    print("  Critical:", mr_critical_cost(s))
    print("Splay:")
    print("  Crossing:", splay_crossing_cost(s))
    print("  Inside:", splay_inside_cost(s))
    print("  Critical:", splay_critical_cost(s))
    print("  Total:", splay_cost(s))


if __name__ == '__main__':
    s = tuple(range(1, 63)) + (1, 2, 4, 8, 16, 32)
    (M, x), (S, y) = last(dual_execution(s))
    print(M.encoding())
    print(S.encoding())
    s = list("aihjgfclkendbpmoi")
    for x in mr_nodes(s):
        print(x.crossing_nodes())
    all_costs(s)
