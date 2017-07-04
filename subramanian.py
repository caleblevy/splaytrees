"""Implementation of Supervisor-based local bottom up splay-like algorithms."""

def Supervisor(Ruleset):
    """Output splay-like algorithm given Ruleset[Template, Result].
    Assumes Ruleset is applied to longest subpath applicable."""
    H_max = max(map(len, Ruleset.keys())) - 1
    