from bst import *


Right = 1
Left = 0


def crossing_path(bins, direction=Left):
    encoding = []
    nextnode = [list('rllprpp'), list('lrlprpp')]
    firstnode = [list('lllprpp'), list('rrlprpp')]
    finalconnector = [['r'], ['l']]
    encoding.extend(nextnode[direction][1:] + (bins[0]-1)*nextnode[direction])
    for k in bins[1:]:
        direction = not direction
        encoding.extend(firstnode[direction] + (k-1)*nextnode[direction])
    encoding.extend(finalconnector[direction]+list('llprpprlpr'))
    T = Tree.from_encoding(encoding)
    print(T.find(28).crossing_nodes())
    return T


def delta_gs0(i,j):
    return max(-1, 2*i-4+min(1, j-1))

print(delta_gs0(1,1))
print(delta_gs0(1,2))
print(delta_gs0(1,3))
print(delta_gs0(2,1))
print(delta_gs0(2,2))
print(delta_gs0(2,3))
print(delta_gs0(3,1))
if __name__ == '__main__':
    pass
    # crossing_path([1])
    # from draw import *
    # plot_subtree(crossing_path([3,3,2,1,1,2],0).root, show=True)