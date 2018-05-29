from bst import *
from random import shuffle


def subseq_compare(x, k=20):
    y = x[:]
    y.pop(k)
    xe = mr_nodes(x)
    ye = mr_nodes(y)
    for _ in range(k):
        next(xe), next(ye)
    xk = next(xe)
    print(xk.crossing_nodes())
    for x_el, y_el in zip(xe, ye):
        print(x_el.crossing_nodes(), y_el.crossing_nodes())

if __name__ == '__main__':
    r = list(range(2**7))
    shuffle(r)
    subseq_compare(r)
    x = list(range(1000))
    shuffle(x)
    cx = splay_crossing_cost(x)
    for i in range(1000):
        y = x[:]
        y.pop(i)
        cy = splay_crossing_cost(y)
        print(cx, cy, cx - cy)