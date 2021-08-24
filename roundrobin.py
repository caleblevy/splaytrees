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


def roundrobin(n, k):
    assert 2 <= k <= floorlog(n)
    b = floorpow(k)
    l = n // b
    sets = [set(range(i*b+1, (i+1)*b+1)) for i in range(l)]
    remainder = list(range(l*b+1, n+1))
    print(sets)
    print(remainder)


def _generate(sets, num_cycles_remaining, current_bin_number):
    print(sets)
    if current_bin_number == 2*len(sets):
        if num_cycles_remaining == -1:
            yield ()
        else:
            yield from _generate(sets, num_cycles_remaining-1, 0)
    else:
        if current_bin_number < len(sets):
            bin_index = current_bin_number
        else:
            bin_index = 2*len(sets) - current_bin_number - 1
        for item_index in range(len(sets[bin_index])):
            value = sets[bin_index].pop(item_index)
            for permutation in _generate(sets, num_cycles_remaining, current_bin_number+1):
                yield (value, ) + permutation
            sets[bin_index].insert(item_index, value)


if __name__ == '__main__':
    roundrobin(100, 3)
    print(floorpow(3.1))
    print(list(_generate([[1,2,3,4],[5,6,7,8],[9,10,11,12]], 2, 0)))