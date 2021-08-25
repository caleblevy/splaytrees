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
    assert 1 <= k <= floorlog(n)
    b = floorpow(k)
    l = -(-n//b)
    return tuple(tuple(range((i-1)*b+1, min(i*b, n)+1)) for i in range(1, l+1))


def roundrobin(n, k):
    return list(_roundrobin(generate_bins(n, k)))


def _gentuples(tup):
    for i in range(len(tup)):
        yield tup[:i] + tup[i+1:]


def _roundrobin(C):
    t = max(len(B) for B in C)
    if t == 0:
        yield ()
    else:
        s = min(len(B) for B in C if len(B) > 0)
        if t == s:
            if (t % 2 == 0):
                b_star = C[0]
            else:
                b_star = C[-1]
        else:
            
            if len(C[0]) < t:
                b_star = C.


if __name__ == '__main__':
    print(roundrobin(100, 3))