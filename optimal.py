"""Attempts to simulate the optimal algorithm."""

from random import shuffle
from wilber import critical_nodes


def inside_nodes(s):
    """Return list of inside node sets from critical nodes."""
    for i in range(1, len(s)+1):
        _, _, _, v = critical_nodes(s, i)
        yield tuple(v)


def randperm(n):
    """Random permutation of nodes 1 to n."""
    l = list(range(1, n+1))
    shuffle(l)
    return l

r = randperm(120)
print(r)

for i in inside_nodes(r):
    print(i)


def remove_doubletaps(s):
    """Remove consecutive repetitons from a sequence.
    E.g. (1, 2, 2, 1, 1, 3, 2, 2, 3) -> (1, 2, 1, 3, 2, 3)."""
    d = []
    previous = object()
    for x in s:
        if previous != x:
            d.append(x)
        previous = x
    return d


print(remove_doubletaps((1, 2, 2, 1, 1, 3, 2, 2, 3)))


def augmented_sequence(s):
    """Augment s to a supersequence containing inside nodes."""
    t = []
    for x, b in zip(s, inside_nodes(s)):
        t.extend(b)
        t.append(x)
    return remove_doubletaps(t)

R = augmented_sequence(r)
print(R)
RR = augmented_sequence(R)
print(RR)
print(augmented_sequence(RR))
print(augmented_sequence(augmented_sequence(RR)))


for i in range(20):
    print(len(R))
    R = augmented_sequence(R)