from itertools import chain


def floorlog(n):
    return n.bit_length() - 1


def floorpow(k):
    b_prev = 1
    b = 2
    while b <= 2**k:
        b_prev = b
        b *= 2
    return b_prev


def generate_bins(n, k):
    assert 1 <= k <= n
    return tuple(tuple(range((i-1)*k+1, min(i*k, n)+1)) for i in range(1, (n//k)+1))


def roundrobin(n, k):
    return list(_roundrobin(generate_bins(n, k)))


def _gentuples(tup):
    for i in reversed(range(len(tup))):
        yield tup[i], tup[:i] + tup[i+1:]


def _roundrobin(C):
    t = max(len(B) for B in C)
    if t == 0:
        yield ()
    else:
        s = min(len(B) for B in C if len(B) > 0)
        if s == t:
            if (t % 2 == 0):
                b_star = min(i for i, B in enumerate(C) if len(B) > 0)
            else:
                b_star = max(i for i, B in enumerate(C) if len(B) > 0)
        else:
            if len(C[0]) < t:
                b_star = min(i for i, B in enumerate(C) if len(B) == t)
            else:
                b_star = max(i for i, B in enumerate(C) if len(B) == t)
        for (x, B) in _gentuples(C[b_star]):
            for p in _roundrobin(C[:b_star] + (B, ) + C[b_star+1:]):
                yield p + (x, )


if __name__ == '__main__':
    print(roundrobin(13, 3))
