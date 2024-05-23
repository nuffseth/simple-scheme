from scheme_types.node import *

class Env:
    """An environment/scope in which variables are defined"""

    def __init__(self, outer, poundF, poundT, empty):
        """Construct an environment.  We need a single global value for false,
        for true, and for empty.  We optionally have a link to an enclosing
        scope"""
        self.outer = outer
        self.map = {}
        self.poundF = poundF
        self.poundT = poundT
        self.empty = empty

    def put(self, key, val):
        """Unconditionally put a key into this environment"""
        self.map[key] = val

    def get(self, key):
        """Look up the value for a given key; recurse to outer environments as
        needed.  Throw an exception on failure."""
        if key in self.map.keys():
            return self.map[key]
        elif self.outer != None:
            return self.outer.get(key) 
        else:
            raise Exception(key + " not defined at outermost scope")

    def update(self, key, val):
        """Update a key's value **in the scope where it is defined**"""
        if key in self.map:
            self.map[key] = val
        else:
            self.outer.update(key, val)
