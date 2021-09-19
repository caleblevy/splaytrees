import random

def generate_balanced_string(n):
    nonlocal k
    nonlocal r
    k = 2*n
    r = 0
    def open_string():
        nonlocal k, r
        r += 1
        k -= 1
        return "("
    def close_string():
        r -= 1
        k += 1
        return ")"
    def prob_close():
        return ((r*(r+k+2))/(2*k*(r+1)))
    while r != k:
        if r == 0:
            yield open_string()
        elif random.random() < prob_close():
            yield close_string()
        else:
            yield open_string()
    while k != 0:
        yield close_string()


for _ in range(100):
    generate_balanced_string(3)