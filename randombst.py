import random


def _generate_balanced_string(n):
    k = 2*n
    r = 0
    while r != k:
        if r == 0 or random.uniform(0, 1) >= r*(r+k+2)/(2*k*(r+1)):  # open
            yield "("
            r += 1
        else:
            yield ")"
            r -= 1
        k -= 1
    while k > 0:
        k -= 1
        yield ")"


def generate_balanced_string(n):
    return "".join(_generate_balanced_string(n))


if __name__ == '__main__':
    from collections import Counter
    c = Counter()
    for _ in range(4):
        c[generate_balanced_string(3)] += 1
    print(c)
