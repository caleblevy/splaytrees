"""Experiments with the cost of splaying certain trees."""

from propersplay import SplayTree


def access_depths(T, X):
    """Return sequence of costs of accessing each item in T from X."""
    costs = []
    for x in X:
        cost = T.access(x)
        costs.append(cost)
    return costs


def access_cost(T, X):
    """Return total cost to splay an access sequence X with starting tree T."""
    return sum(access_depths(T, X))


def left_spline(n):
    """Make a new left spline on [n]."""
    return SplayTree(range(n, 0, -1))


def right_spline(n):
    """Make a new right spline on [n]."""
    return SplayTree(range(1, n+1))


def compare_left_right_subsequence(n):
    """Compares the access cost of subsequences. Suppose we start out with
    right spline and splay in increasing order.
    Ex: 3
       / 
      2
     /
    1  splayed with (1, 2, 3).

    The cost of doing this is clearly more than if we had the right spline to
    start. Now suppose that we splay [3, 2, 1, 1, 2, 3]. Will this cost less
    than splaying [1, 2, 3]?"""
    T1 = left_spline(n)
    T2 = left_spline(n)
    X = list(range(n-4, 0, -1)) + list(range(2, n+1))
    Y = range(1, n+1)
    cost_x = access_cost(T1, X)
    cost_y = access_cost(T2, Y)
    print("Cost of splaying [%s,..., 1, 1,..., %s]: %s" % (n, n, cost_x))
    print("Cost of splaying [1,..., %s]: %s" % (n, cost_y))


compare_left_right_subsequence(19)