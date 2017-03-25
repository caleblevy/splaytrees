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
        y = x.down
        if y is not None and y < x:
            return y
        else:
            return None

    @property
    def right(x):
        y = x.down
        if y is not None:
            if y > x:
                return y
            else:
                z = y.side
                if z is not x:
                    return z
                else:
                    return None
        else:
            return None

    @property
    def parent(x):
        y = x.side
        if y is not None:
            if y < x:
                return y  # x is right child of parent
            else:
                z = y.side
                if z is None:
                    return y  # x's parent y is the root
                elif x < z < y:
                    return z  # only case where y is not parent
                else:
                    return y  # proof this works is casewise
        else:
            return None