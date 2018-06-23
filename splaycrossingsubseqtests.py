from bst import *
from random import shuffle


n = 10000
X = list(range(1, n+1))
shuffle(X)

cr_x = [len(x.crossing_nodes()) for x in splay_nodes(X)]
cost_x = sum(cr_x)
print('cost(X) = %s' % cost_x)

i = cr_x.index(7)
Y = X[:]
Y.pop(i)
cr_y = [len(y.crossing_nodes()) for y in splay_nodes(Y)]
cost_y = sum(cr_y)

j = cr_y.index(7)
Z = Y[:]
Z.pop(i)

print('cost(Y) = %s' % cost_y)
print('cross_splay(Z) = %s' % splay_crossing_cost(Z))
print('mr_cross_cost(X) = %s' % mr_crossing_cost(X))
print('mr_cross_cost(Y) = %s' % mr_crossing_cost(Y))