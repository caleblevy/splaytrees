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
    a = list("aihjgfclkendbpmoi")
    b = range(2000) + range(2000) + range(2000) + range(2000)
    shuffle(b)
    a_w = wilber2(a)
    a_m = MRBound(a)
    a_s = SplayBound(a)
    b_w = wilber2(b)
    b_m = MRBound(b)
    b_s = SplayBound(b)
    print(sum(a_w), sum(a_m), sum(a_s))
    for w, m, s in zip(a_w, a_m, a_s):
        print(max(w, m, s) - min(w, m, s))
    print(sum(b_w), sum(b_m), sum(b_s))
    for w, m, s in zip(b_w, b_m, b_s):
        print(max(w, m, s) - min(w, m, s), min(w, m, s))
