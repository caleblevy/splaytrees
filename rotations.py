"""Module to track the exact rotations by splay and move-to-root."""

from pathcodes import Node, maker


class RotationTracker(Node):
    """Track rotations of node class."""
    __slots__ = ()

    @maker(tuple)
    def splay(x):
        """Proper bottom-up splay to the top."""
        while x.parent is not None:
            y = x.parent
            z = y.parent  # parent checked for in "splay"
            # zig
            if z is None:
                yield (x, x.parent)
                x.rotate()
            elif (y is z.left and x is y.right) or (y is z.right and x is y.left):
                yield (x, x.parent)
                x.rotate()
                yield (x, x.parent)
                x.rotate()
            # zig-zig
            else:
                yield (y, y.parent)
                y.rotate()
                yield (x, x.parent)
                x.rotate()


def splay_rotations(s):
    """Rotations performed by splay operations starting from the right path."""
    q = sorted(set(s))
    n = len(q)
    t = RotationTracker.from_cursor("r"*(n-1))
    d = dict(zip(q, t.preorder()))
    d_inv = {node: key for key, node in d.items()}
    R = []
    for x in s:
        rots = d[x].splay()
        R.extend((d_inv[x], d_inv[y]) for x, y in rots)
    return R


# print splay_rotations(range(16, 0, -1))