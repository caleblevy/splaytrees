"""Implementation of Supervisor-based local bottom up splay-like algorithms."""

def Supervisor(Ruleset, doc=None, name=None):
    """Output splay-like algorithm given Ruleset: Template -> Result.
    Assumes Ruleset is applied to longest subpath applicable."""
    H_max = max(map(len, Ruleset.keys())) - 1
    def apply_rule(node):
        for i in range(H_max, -1 -1):
            if encodestring in Ruleset:
                ...
    def algorithm(x):
        while x not parent:
            x = apply_rule
        return x