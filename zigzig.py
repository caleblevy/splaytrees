"""Emperically determine whether number of zig-zigs on the search paths is
bounded by size of initial tree + wilber 2."""
from __future__ import print_function

from pathcodes import Node, splay, SplayBound, SplayZigs


def treeNodes(movements):
    """Return mapping of 1...n to the nodes described by the cursor
    movements."""
    t = Node.from_cursor(movements)
    return dict(enumerate(t.inorder(), start=1))


def padded(k):
    """Do splay zig-zig count on w2 example with added padding."""
    s = [1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]
    return list(range(1, k+1)) + list(range(k, 0, -1)) + [x+k for x in s]
    


if __name__ == '__main__':
    s = [1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]
    print(sum(SplayBound(s)))
    print(SplayBound(s))
    print(SplayZigs(s))
    print(sum(SplayZigs(padded(30))))
    print(sum(SplayBound(padded(30))))
