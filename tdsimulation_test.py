"""Test if we can make a simple simulation embedding with top-down splay"""

from topdownsplay import TDSplayTree, tdfrompre


def isTransformable(p1, p2=None):
    """Determine if top-down Splay can transform from p1 to p2 (and if so, what
    path.)"""
    p1 = tuple(p1)
    p2 = tuple(p2)
    seen = {p1}  # Preorders so far seen
    parent = {}  # Node to Splay in preorder at to get to parent preorder
    while True:
        latest = set()
        for p in seen:
            for k in p1:
                t = tdfrompre(p)  # Initial Tree preorder
                t.splay(k)
                pp = t.preorder()
                if pp not in seen:
                    latest.add(pp)
                    if pp not in parent:
                        parent[pp] = (p, k)
        if not latest:
            break
        seen.update(latest)
    accesses = []
    p = p2
    while p in parent:
        p, k = parent[p]
        accesses.append(k)
    accesses = list(reversed(accesses))
    print(accesses)
    t = tdfrompre(p1)
    for k in accesses:
        t.splay(k)
    assert t.preorder() == p2


isTransformable((1,2,3,4), (4,3,2,1))

start = 'zmaxvuwy'
rot_u = 'zmaxuvwy'
rot_v = 'zmavuxwy'
rot_w = 'zmaxwvuy'
rot_y = 'zmayxvuw'

isTransformable(start, rot_u)
isTransformable(start, rot_v)
isTransformable(start, rot_w)
isTransformable(start, rot_y)