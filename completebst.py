def complete_bst_preorder(d, root=None):
    """Return preorder sequence of complete BST of depth d on nodes
    1...2^d-1. """
    if root is None:
        root = 2**(d-1)
    yield root
    if d > 1:
        for node in complete_bst_preorder(d-1, root-2**(d-2)):
            yield node
        for node in complete_bst_preorder(d-1, root+2**(d-2)):
            yield node



for n in complete_bst_preorder(5):
    print(n)
