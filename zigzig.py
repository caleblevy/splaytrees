"""Emperically determine whether number of zig-zigs on the search paths is
bounded by size of initial tree + wilber 2."""
from __future__ import print_function

from pathcodes import Node, splay, SplayBound


def treeNodes(movements):
    """Return mapping of 1...n to the nodes described by the cursor
    movements."""
    t = Node.from_cursor(movements)
    return dict(enumerate(t.inorder(), start=1))


def rightPath(n): return treeNodes("r"*(n-1))


if __name__ == '__main__':
    s = [1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]
    s2 = [1, 2, 3, 4, 5, 4, 3, 2, 1] + [6+x for x in s]
    print(SplayBound(s2))
    print(SplayBound(s))
    print(sum(SplayBound(s2)))
    print(sum(SplayBound(s)))
