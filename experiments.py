"""Experiments with the cost of splaying certain trees."""

from propersplay import SplayTree, complete_bst_preorder
from scipy.stats.mstats import gmean


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
    """Efficiently make a new left spline on [n]."""
    T = SplayTree()
    for i in range(1, n+1):
        T.add(i)
    return T


def complete_bst(d):
    """Generate a complete BST of depth d."""
    T = left_spline(2**d-1)
    for i in range(d):
        T.access(2**i)
    T.count = 0
    return T


def right_spline(n):
    """Make a new right spline on [n]."""
    T = SplayTree()
    for i in range(n, 0, -1):
        T.add(i)
    return T


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
    X = list(range(n, 0, -1)) + list(range(2, n+1))
    Y = range(1, n+1)
    cost_x = access_cost(T1, X)
    cost_y = access_cost(T2, Y)
    print("Cost of splaying [%s,..., 1,..., %s]: %s" % (n, n, cost_x))
    print("Cost of splaying [1,..., %s]: %s" % (n, cost_y))


def splay_left_spline_on_complete_bst(d):
    """Compute cost of splaying left spline on complete bst of depth d."""
    T = left_spline(2**d-1)
    cost = access_cost(T, complete_bst_preorder(d))
    print("Cost of splaying complete bst of depth %s: %s" % (d, cost))
    print("Cost per node %s" % (1.*cost/(2**d-1)))


def depths_right_spline_on_complete_bst(d):
    """Return the splay depths for right spline on complete bst of depth d."""
    T = right_spline(2**d-1)
    return access_depths(T, complete_bst_preorder(d))


def splay_right_spline_on_complete_bst(d):
    """Compute cost of splaying right spline on complete bst of depth d."""
    T = right_spline(2**d-1)
    cost = access_cost(T, complete_bst_preorder(d))
    print("Cost of splaying complete bst of depth %s: %s" % (d, cost))
    print("Cost per node %s" % (1.*cost/(2**d-1)))


def splay_complete_bst_sequentially(d):
    """Compute the cost of splaying a complete bst of depth d sequentially"""
    # The main purpose of this is to determine if the costs/node increase as
    # quickly.
    T = complete_bst(d)
    cost = access_cost(T, range(1, 2**d))
    print("Cost of sequential splay of complete bst depth %s: %s" % (d, cost))
    print("Cost per node: %s" % (1.*cost/(2**d-1)))


def odd_depths(d):
    """Depths of odd nodes in right spline splayed at cbst(d)"""
    depths = depths_right_spline_on_complete_bst(d)
    cbp = complete_bst_preorder(d)
    for d, i in zip(depths, cbp):
        if i % 2:
            print(i, d)


def assign_depth(n):
    """For lack of something more clever, determine the depth of a node
    iteratively."""
    i = 1
    while not(n % 2**i):
        i += 1
    return i


def separate_by_depth(d):
    """Separate out costs by depth for each depth so chosen."""
    costs = depths_right_spline_on_complete_bst(d)
    cbp = complete_bst_preorder(d)
    levels = [0 for _ in range(d)]
    for c, n in zip(costs, cbp):
        levels[assign_depth(n)-1] += c
    for l in range(d):
        numels = 2**(d-l-1)
        levels[l] /= 1.*numels
    print('\n\n\n------')
    print("Tree depth: %s" % d)
    print('--------------')
    print("Depth\tAverage Cost")
    for d, l in enumerate(levels):
        print(d, l/2**d)
    print
    print("Depth\tRatios")
    l = levels[0]
    ratios = []
    for l in range(1, len(levels)):
        ratios.append(levels[l]/levels[l-1])
        print(l, levels[l]/levels[l-1])
    print(gmean(ratios))


def splay_cbst_postorder(n):
    """Find cost ratios for splay in post order."""
    for i in range(1, n+1):
        T = complete_bst(i)
        post = T.postorder()
        cost_per_node = 1.*access_cost(T, post)/len(post)
        print("Splay CBST Postorder %s: %s" % (i, cost_per_node))


def preorder_twice(T1, T2=None):
    """Test weather splaying twice in preorder of T is same as once?"""
    if T2 is None:
        T2 = T1
    pre = T2.preorder()
    for x in pre:
        T1.access(x)
    p1 = T1.preorder()
    for x in pre:
        T1.access(x)
    p2 = T1.preorder()
    return p1, p2, p1==p2


print(preorder_twice(complete_bst(6)))


if __name__ == '__main__':

    print(right_spline(4).preorder())

    for i in range(20):
        compare_left_right_subsequence(i)

    for i in range(1, 10):
        splay_left_spline_on_complete_bst(i)

    for i in range(1, 15):
        splay_complete_bst_sequentially(i)

    print(depths_right_spline_on_complete_bst(6))

    print(odd_depths(10))

    for d in range(1, 15):
        splay_right_spline_on_complete_bst(d)

    print(map(assign_depth, complete_bst_preorder(5)))

    separate_by_depth(5)
    separate_by_depth(6)
    separate_by_depth(7)
    separate_by_depth(8)
    separate_by_depth(9)
    separate_by_depth(10)
    separate_by_depth(11)

    separate_by_depth(12)
    separate_by_depth(13)
    separate_by_depth(14)
    separate_by_depth(15)
    separate_by_depth(16)
    separate_by_depth(17)
    separate_by_depth(18)
    separate_by_depth(19)
    separate_by_depth(20)
