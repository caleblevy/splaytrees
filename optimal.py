"""Attempts to simulate the optimal algorithm."""

from random import shuffle
from wilber import critical_nodes
from pathcodes import Node


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

r = randperm(2000)
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
        t.extend(sorted(b + (x,)))
    return remove_doubletaps(t)

for i in range(20):
    print(len(r))
    r = augmented_sequence(r)


def first_appearances(s):
    """Return subsequence of s consisting of first occurance of each item.
    E.g. [1, 2, 4, 2, 3, 8, 4, 8, 5] -> [1, 2, 4, 3, 8, 5]"""
    seen = set()
    d = []
    for x in s:
        if x not in seen:
            d.append(x)
            seen.add(x)
    return d


print(first_appearances([1, 2, 4, 2, 3, 8, 4, 8, 5]))

def move_to_root(s):
    """Return the insertion tree sequence of x."""
    