from propersplay import SplayTree
from pathcodes import Node

from treecodecs import decoder, encoder, za_count, zi_count
from noted_list import perm

seq = perm
subseq = list(perm)
subseq.pop(20)


def findpath(splaytree, key):
    """Returns findpath of key in splaytree."""
    chars = []
    x = splaytree.root
    while True:
        if x.key < key:
            x = x.right
            chars.append("1")
        elif x.key > key:
            x = x.left
            chars.append("0")
        else:
            break
    return "".join(chars)


def make_keyless(splaytree):
    """Make keyless bst from splaytree"""
    r = Node()
    for k in splaytree.inorder():
        r.decode(findpath(splaytree, k))
    assert r.numbered_preorder() == splaytree.preorder()
    return r


t = SplayTree(seq)
r = make_keyless(t)
kn = r.key_to_node()
requested_nodes = list(map(kn.__getitem__, perm))


code = []
for node in requested_nodes:
    code.append(node.encode())
    node.splay()

print(code)
print(sum(len(e)+1 for e in code))
subsequence = list(requested_nodes)
subsequence.pop(20)
r = r.reset()
sub_code = []
for node in subsequence:
    sub_code.append(node.encode())
    node.splay()

print(sum(len(e)+1 for e in sub_code))
