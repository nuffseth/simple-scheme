from util.constants import *

def AndNode(expressions: list): return {"type": AND, "expressions": expressions}
def ApplyNode(expressions: list): return {"type": APPLY, "expressions": expressions}
def BeginNode(expressions: list): return {"type": BEGIN, "expressions": expressions}
def BoolNode(val: bool): return {"type": BOOL, "val": val}
def BuiltInNode(name: str, func: callable): return {"type": BUILTIN, "name": name, "func": func}
def CharNode(val: str): return {"type": CHAR, "val": val}
def CondNode(conditions: list): return {"type": COND, "conditions": conditions}
def ConsNode(car, cdr):
    if isinstance(car, list):
        if len(car) == 0:
            return "Cannot construct Cons from empty list"
        elif len(car) == 1:
            return {"type": CONS, "car": car[0], "cdr": cdr}
        else:
            return {"type": CONS, "car": car[0], "cdr": ConsNode(car[1:], cdr)}
    else:
        return {"type": CONS, "car": car, "cdr": cdr}
def DblNode(val: float): return {"type": DBL, "val": val}
def DefineNode(identifier, expression): return {"type": DEFINE, "identifier": identifier, "expression": expression}
def IdentifierNode(name: str): return {"type": IDENTIFIER, "name": name}
def IfNode(cond, ifTrue, ifFalse): return {"type": IF, "cond": cond, "true": ifTrue, "false": ifFalse}
def IntNode(val: int): return {"type": INT, "val": val}
def LambdaDefNode(formals: list, expressions: list): return {"type": LAMBDADEF, "formals": formals, "expressions": expressions}
def LambdaValNode(env, l): return {"type": LAMBDAVAL, "env": env, "lambda": l}
def OrNode(expressions: list): return {"type": OR, "expressions": expressions}
def QuoteNode(datum): return {"type": QUOTE, "datum": datum}
def SetNode(identifier, expression): return {"type": SET, "identifier": identifier, "expression": expression}
def StrNode(val: str): return {"type": STR, "val": val}
def SymbolNode(name: list): return {"type": SYMBOL, "name": name}
def TickNode(datum): return {"type": TICK, "datum": datum}
def VecNode(items: list): return {"type": VEC, "items": items}