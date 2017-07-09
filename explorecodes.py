from propersplay import SplayTree
from pathcodes import Node
from wilber import wilber2

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
requests = list(map(kn.__getitem__, perm))

r_sub = Node.from_cursor(r.cursor())
# assert r_sub.is_isomorphic_to(r)
kn_sub = r_sub.key_to_node()
sub_requests = list(map(kn_sub.__getitem__, subseq))



code = []
for node in requests:
    code.append(node.encode())
    node.splay()

sub_code = []
for node in sub_requests:
    sub_code.append(node.encode())
    node.splay()


print('Splay X: ', sum(len(e)+1 for e in code))
print('Splay Y: ', sum(len(e)+1 for e in sub_code))

print("za X: ", za_count(code))
print("za Y: ", za_count(sub_code))
print("zi X: ", zi_count(code))
print("zi Y: ", zi_count(sub_code))
# print("wilber X: ", sum(wilber2(perm)))
# print("wilber Y: ", sum(wilber2(subseq)))


r = r.reset()
r_sub = Node.from_cursor(r.cursor())
print(code[20])
print(code[19])
print(code[21])
print(sub_code[19])
print(sub_code[21])
