import functools


class ThreadedNode(object):
    """Threaded node using only two pointers for left, right, parent."""

    __slots__ = ("down", "side", "val")

    def __init__(x, val):
        self.val = val
        self.down = None
        self.adj = None

    def __lt__(x, y):
        if isinstance(y, x.__class__):
            return x.val < y.val
        else:
            return x.val < y

    def __eq__(x, y):
        if isinstance(y, x.__class__):
            return x.val == y.val
        else:
            return x.val == y

    def __ne__(x, y):
        return not x == y

    @property
    def left(x):
        if x.down is not None and x.down < x:
            return x.down
        else:
            return None

    @property
    def right(x):
        if x.down is not None:
            if x.down > x:
                return x.down
            elif x.down.side is not x:
                return x.down.side
        else:
            return None

    @property
    def parent(self):
        if x.side is not None:
            if x.side.down is x:
                return x.side  # x.parent has one child
            else:
                return x.side.side  # 