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

    @maker(tuple)
    def move_to_root(x):
        """Proper bottom-up splay to the top."""
        while x.parent is not None:
            yield (x, x.parent)
            x.rotate()


@maker(tuple)
def access_path(x):
    """Return path of nodes from x to the root."""
    yield x
    while x.parent is not None:
        x = x.parent
        yield x


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
        R.append(list((d_inv[x], d_inv[y]) for x, y in rots))
    return R


def mr_rotations(s):
    """Rotations performed by splay operations starting from the right path."""
    q = sorted(set(s))
    n = len(q)
    t = RotationTracker.from_cursor("r"*(n-1))
    d = dict(zip(q, t.preorder()))
    d_inv = {node: key for key, node in d.items()}
    R = []
    for x in s:
        rots = d[x].move_to_root()
        R.append(list((d_inv[x], d_inv[y]) for x, y in rots))
    return R


def splay_paths(s):
    """Compute the splay paths."""
    


# print splay_rotations(range(16, 0, -1))
# for rots in splay_rotations([1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]):
#     print(rots)
# print(splay_rotations([1,2,3]))
# for rots in mr_rotations([1, 9, 8, 10, 7, 6, 3, 12, 11, 5, 14, 4, 2, 16, 13, 15, 9]):
#     print(rots)
print mr_rotations(range(16,0,-1))
print mr_rotations([1,2,3])