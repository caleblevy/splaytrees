"""Experiments with the cost of splaying certain trees."""

from propersplay import SplayTree


def access_depths(T, X):
    """Return sequence of costs of accessing each item in T from X."""
    costs = []
    for x in X:
        cost = T.access(x)
        costs.append(cost)
    return costs


def left_spline(n):
    """Make a new left spline on [n]."""
    return SplayTree(range(n, 0, -1))


def right_spline(n):
    """Make a new right spline on [n]."""
    return SplayTree(range(1, n+1))


print(left_spline(14).preorder())
print(right_spline(14).preorder())
