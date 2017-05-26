"""Implementation of move-to-root. For now, its a hacked version of splay."""

from propersplay import SplayTree, Node


def movetoroot(self):
    while self.parent is not None:
        self.rotate()


Node._splay = movetoroot


T = SplayTree(range(1, 9))
T.access(5)
print(T.preorder())
T.access(8)
print(T.preorder())
T.access(3)
print(T.preorder())
T.access(2)
print(T.preorder())