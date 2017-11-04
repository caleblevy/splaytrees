"""Implementation of a node maintaining
   - Depth
   - Zig-Zag depth
   - Zig-Zig depth
   - Weight
   - Size
   - Rank
"""


class Node(object):
    """Node object maintaining all properties under rotation."""

    __slots__ = ("_left", "_right", "_parent", "key",
                 "_size", "_weight", "_rank", "_potential",
                 "_depth", "_turn_depth")

    def __init__(x, key, weight):
        x.key = key
        x.left = x.right = x.parent = None
        x.weight = 1

    @property
    def left(x):
        return x._left

    @left.setter
    def left(x, y):
        if not (is_node(y) or y is None):
            raise TypeError("Node's left child must be a node.")
        elif y.key >= x.


def is_node(x):
    return isinstance(x, Node)