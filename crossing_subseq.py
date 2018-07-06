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


def small_counter_ex(n=4):
    r = list(range(n))
    shuffle(r)
    c_splay = splay_crossing_cost(r)
    c_mr = mr_crossing_cost(r)
    while c_splay >= c_mr:
        print(c_splay - c_mr)
        shuffle(r)
        c_splay = splay_crossing_cost(r)
        c_mr = mr_crossing_cost(r)
    print(c_splay - c_mr)
    print(r)


def break_splay_crossing_subseq(n=5):
    r = list(range(n))
    while True:
        shuffle(r)
        t = list(r)
        shuffle(t)
        X = r + t
        t.pop(0)
        Y = r + t
        c_x = splay_crossing_cost(X)
        c_y = splay_crossing_cost(Y)
        print(c_x - c_y)
        if c_x < c_y:
            break
    # print(c_x - c_y)
    print(X)


if __name__ == '__main__':
    # r = list(range(2**7))
    # shuffle(r)
    # subseq_compare(r)
    # x = list(range(1000))
    # shuffle(x)
    # cx = splay_crossing_cost(x)
    # for i in range(1000):
    #     y = x[:]
    #     y.pop(i)
    #     cy = splay_crossing_cost(y)
    #     print(cx, cy, cx - cy)
    # small_counter_ex()
    break_splay_crossing_subseq()