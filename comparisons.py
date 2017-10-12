"""A 'fair' comparison between splay and wilber 2."""

try:
    import cPickle as pickle
except ImportError:
    import pickle

from pathcodes import Node
from wilber import scores, wilber2

def w2(encodings):
    """Compute wilber2 of encoded paths, after decoding with splay."""
    encodings = list(encodings)
    splay_cost = sum(1+len(e) for e in encodings)
    root = Node()
    nodes = []
    for e in encodings:
        x = root.decode(e)
        nodes.append(x)
        root = x.splay()
    keys = root.node_to_key()
    s = map(keys.__getitem__, nodes)
    root = root.reset()
    postorder = list(map(keys.__getitem__, root.postorder()))
    print(root.numbered_preorder())
    n = len(postorder)
    s = postorder + s
    full_scores = scores(s)
    w2 = sum(1+c for c in full_scores[n:])
    print(splay_cost, w2, wilber2(s))


if __name__ == '__main__':
    w2([
        "10000101000",
        "1001000110",
        "0010001000001000000001",
        "1001100101101110",
        "0101010001010",
        "11101110000100011100101101"
    ])
    with open("encodings.pkl") as f:
        encodings = pickle.load(f)
    w2(encodings)