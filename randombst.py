import random


def _generate_balanced_string(n):
    k = 2*n
    r = 0
    s = []
    while k > 0:
        if k > r and (r == 0 or random.uniform(0, 1) >= r*(r+k+2)/(2*k*(r+1))):
            yield "("
            r += 1
        else:
            yield ")"
            r -= 1
        k -= 1


def random_balanced_string(n):
    return "".join(_generate_balanced_string(n))



def random_bst(n):
    """Uniform random binary search tree of size n."""
    s = generate_balanced_string(n)
    def recur(i):
        if i >= len(s) or s[i] == ")":
            i += 1
            return None
            


if __name__ == '__main__':
    from collections import Counter
    c = Counter()
    for _ in range(100000):
        c[random_balanced_string(3)] += 1
    print(c)
