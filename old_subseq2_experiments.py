"""New, more serious set of subsequence experiments."""

from random import shuffle, sample

from propersplay import SplayTree
from experiments import access_depths, access_cost
from treerank import randtree


def randperm(n):
    r = range(1, n+1)
    shuffle(r)
    return r


def extract_subseq(X, s):
    """Extract subsequence of X excluding indices s."""
    Y = []
    s = iter(sorted(s))
    ind = next(s, None)
    for i, x in enumerate(X):
        if i == ind:
            ind = next(s, None)
        else:
            Y.append(x)
    return Y


def test_random_subseq(n, k):
    """Test subsequence on random start tree, random perm."""
    X = randperm(n)
    P = randtree(n)
    T = SplayTree(P)
    U = SplayTree(P)
    s = sample(range(len(X)), k)
    Y = extract_subseq(X, [1, 10, 20])
    cost_x = access_cost(T, X)
    cost_y = access_cost(U, Y)
    print(X)
    print(Y)
    print("Cost to access X: %s" % cost_x)
    print("Cost to access Y: %s" % cost_y)

a = randperm(10)
b = extract_subseq(a, [1,4,6])
print(a)
print(b)
a = test_random_subseq(100, 4)