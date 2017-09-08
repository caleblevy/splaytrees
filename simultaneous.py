"""Test evolution of simultaneous transforms in splay and move-to-root."""
from __future__ import print_function

from pathcodes import Node


def printFinal(keys):
    """Start from 1-2-3-4, print final splay and move-to-root tree preorders
    after splaying keys."""
    sp = Node.from_cursor("rrr")
    spKeyToNode = sp.key_to_node()
    mr = Node.from_cursor("rrr")
    mrKeyToNode = mr.key_to_node()
    for k in keys:
        spKeyToNode[k].splay()
        mrKeyToNode[k].move_to_root()
    print(sp.root().numbered_preorder())
    print(mr.root().numbered_preorder())

print("A")
printFinal([3,1,4,1])
print("B")
printFinal([2, 3, 4, 1, 2, 1])
print("C")
printFinal([2, 3, 4, 1, 3, 1])
print("D")
printFinal([2, 3, 4, 2, 4, 1])
print("E")
printFinal([2])
print("F")
printFinal([2, 3, 4, 2, 4, 1, 2])