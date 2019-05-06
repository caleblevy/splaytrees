def offset_ind(i, D):
    offsets = [j for (j, d) in enumerate(D, start=1) if d <= i]
    if not offsets:
        return 0
    return max(offsets)



for i in range(1,10):
    print(i, offset_ind(i, [1, 2, 4, 8]))