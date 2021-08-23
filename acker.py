def ackermann(i, j):
    if i == 0:
        return 2*j
    elif i == 1:
        return 2**j
    elif i >= 2 and j == 1:
        return ackermann(i-1, 2)
    else:
        return ackermann(i-1, ackermann(i, j-1))


def inverse(n):
    k = 1
    while ackermann(k, 1) < n:
        k += 1
    return k


if __name__ == '__main__':
    print(ackermann(0, 1))
    print(ackermann(1, 1))
    print(ackermann(2, 1))
    print(ackermann(3, 1))
    print(ackermann(2, 2))
    print(ackermann(2, 16))
    print(ackermann(4, 1))