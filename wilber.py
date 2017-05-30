"""Attempt to implement Wilber 2 in code."""

from random import shuffle

from topdownsplay import Inf, NegInf
from propersplay import complete_bst_preorder
from pathcodes import SplayBound, MRBound


def compute_kappa(s, i):
    """Attempt to compute the score of node i of k."""
    # Have 0 index placeholder for all lists, since Wilber's work assumes this.
    b = [None]*(i+1);  c = [None]*(i+1);  v = [None]*(i+1);  w = [None]*(i+1)
    s = [None] + s
    if i == 1:
        return 0
    c[1] = i-1
    w[1] = s[i-1]
    if w[1] < s[i]:
        v[0] = Inf
    else:
        v[0] = NegInf
    l = 1
    while True:
        if w[l] == s[i]:
            return l-1
        elif w[l] < s[i]:
            Q = {j for j in range(1, c[l]) if s[i] <= s[j] < v[l-1]}
            if not Q:
                return l-1
            c[l+1] = max(Q)
            w[l+1] = s[c[l+1]]
            v[l] = max(s[j] for j in range(c[l+1]+1, c[l]+1) if s[j] < s[i])
            b[l] = max(j for j in range(c[l+1]+1, c[l]+1) if s[j] == v[l])
        elif w[l] > s[i]:
            Q = {j for j in range(1, c[l]) if v[l-1] < s[j] <= s[i]}
            if not Q:
                return l-1
            c[l+1] = max(Q)
            w[l+1] = s[c[l+1]]
            v[l] = min(s[j] for j in range(c[l+1]+1, c[l]+1) if s[j] > s[i])
            b[l] = max(j for j in range(c[l+1]+1, c[l]+1) if s[j] == v[l])
        l += 1


def wilber2(s):
    """Computer wilber2 bound for access sequence s."""
    m = len(s)
    return [1 + compute_kappa(s, i) for i in range(1, m+1)]


def bitrev(k):
    """Bit reversal key for k"""
    return ''.join(reversed(bin(k)[2:]))


if __name__ == "__main__":
    print("Basic\n-------")
    a = list("aihjgfclkendbpmoi")
    print(sum(wilber2(a)), sum(MRBound(a)), sum(SplayBound(a)))
    print("Complete BSTs\n---------------")
    for i in range(1, 12):
        b = list(complete_bst_preorder(i))
        b_w = wilber2(b)
        b_m = MRBound(b)
        b_s = SplayBound(b)
        print(len(b), sum(b_w), sum(b_m), sum(b_s))
    print("Full Perms\n----------------")
    for i in range(1, 7):
        b = range(i*1000)
        shuffle(b)
        b_w = wilber2(b)
        b_m = MRBound(b)
        b_s = SplayBound(b)
        print(i*1000, sum(b_w), sum(b_m), sum(b_s))
    print("Split Up Perms\n-------------")
    for i in range(1, 7):
        b = range(i*1000//4)*4
        shuffle(b)
        b_w = wilber2(b)
        b_m = MRBound(b)
        b_s = SplayBound(b)
        print(i*1000, sum(b_w), sum(b_m), sum(b_s))