from scheme_types.node import *
from util.stdlib import *
from util.env import *
def makeDefaultEnv():
    """Create a default environment by mapping all the built-in names (true,
    false, empty list, and the built-in functions)"""
    poundF = BoolNode(False)
    poundT = BoolNode(True)
    empty = ConsNode(None, None)
    e = Env(None, poundF, poundT, empty)
    # [mfs] Still a lot to do here:
    addMathFuncs(e)
    addListFuncs(e)
    addStringFuncs(e)
    addVectorFuncs(e)
    return e


def makeInnerEnv(outer):
    """Create an inner scope that links to its parent"""
    return Env(outer, outer.poundF, outer.poundT, outer.empty)
