"""Functions based on "A numbering system for binary trees," Gary Knott,
1977."""


class memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        return self.memo[args]


@memoize
def B(n):
    """Quick way to compute Catalan #'s; B(n)=(1/(n+1))*(2n n)"""
    if n == 0:
        return 1
    else:
        return 4*B(n-1) - 6*B(n-1)//(n+1)


@memoize
def G(j, n):
    """The number of binary trees with n nodes whose left subtree has j
    nodes."""
    return B(j)*B(n-j-1)


@memoize
def irank(i, n):
    p = [0]*n
    j = 0
    while i > G(j, n):
        i = i - G(j, n)
        j = j + 1
    p[0] = j+1
    i2 = 1 + (i-1) % B(n-j-1)
    i1 = (i-i2)//B(n-j-1) + 1
    for k in range(2, j+2):
        p[k-1] = irank(i1, j)[k-2]
    for k in range(j+2, n+1):
        p[k-1] = irank(i2, n-j-1)[k-j-2] + j + 1
    return p


def treegen(n):
    """Generate BST preorders on n nodes."""
    for i in range(1, B(n)+1):
        yield tuple(irank(i, n))
