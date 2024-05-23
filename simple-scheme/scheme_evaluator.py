from scheme_types.node import *
from util.default_env import *

def evaluate(expr: dict, env: Env):
    """Evaluate is responsible for visiting an expression and producing a
    value"""
    result = None
    if(expr["type"] == AND):
        # iterate through the list of expressions in the and
        for e in expr["expressions"]:
            if evaluate(e,env) == env.poundF:
                return env.poundF
        return env.poundT
    elif(expr["type"] == APPLY):
        first = evaluate(expr["expressions"][0], env)
        if (first["type"] == BUILTIN):
            values = []
            for e in expr["expressions"][1:]:
                values.append(evaluate(e, env))
            result = first["func"](values)
        elif(first["type"] == LAMBDAVAL):
            if(len(first["lambda"]["formals"]) != len(expr["expressions"]) - 1):
                raise Exception("Incorrect number of arguments")
            inner = makeInnerEnv(first["env"])
            for i in range(len(first["lambda"]["formals"])):
                inner.put(first["lambda"]["formals"][i]["name"], evaluate(expr["expressions"][i + 1], env))
            for r in first["lambda"]["expressions"]:
                result = evaluate(r, inner)
        else:
            raise Exception("Not a built-in function or lambda value")
        return result
    elif(expr["type"] == BEGIN):
        for e in expr["expressions"]:
            result = evaluate(e, env)
        return result
    elif(expr["type"] == BOOL):
        return expr
    elif(expr["type"] == BUILTIN):
        return expr
    elif(expr["type"] == CHAR): 
        return expr
    elif(expr["type"] == COND):
        for e in expr["conditions"]:
            result = None
            if evaluate(e["test"], env) == env.poundT or evaluate(e["test"], env) != env.poundF:
                for f in e["expressions"]:
                    result = evaluate(f, env)
                return result
        return result
    elif(expr["type"] == CONS):
        return expr
    elif(expr["type"] == DBL):
        return expr
    elif(expr["type"] == DEFINE):
        env.put(expr["identifier"]["name"], evaluate(expr["expression"], env))
        return None
    elif(expr["type"] == IDENTIFIER):
        if(env.get(expr["name"]) != None):
            return env.get(expr["name"])
        else:
            raise Exception("Identifier not found")
    elif(expr["type"] == IF):
        if(evaluate(expr["cond"], env) == env.poundT or evaluate(expr["cond"], env) != env.poundF):
            return evaluate(expr["true"], env)
        else:
            return evaluate(expr["false"], env)
    elif(expr["type"] == INT): 
        return expr
    elif(expr["type"] == LAMBDADEF):
        result = None
        inner = makeInnerEnv(env) # Create a new environment
        result = LambdaValNode(inner, expr)
        return result
    elif(expr["type"] == LAMBDAVAL): 
        return expr
    elif(expr["type"] == OR):
        for e in expr["expressions"]:
            if evaluate(e, env) == env.poundT or evaluate(e, env) != env.poundF:
                return env.poundT
        return env.poundF
    elif(expr["type"] == QUOTE): 
        return expr["datum"]
    elif(expr["type"] == SET):
        env.update(expr["identifier"]["name"], evaluate(expr["expression"], env))
        return None
    elif(expr["type"] == STR):
        return expr
    elif(expr["type"] == SYMBOL):
        return expr
    elif(expr["type"] == TICK):
        return expr["datum"]
    elif(expr["type"] == VEC):
        return expr
    else:
        raise Exception("Unknown expression type: " + str(expr["type"]))


def AstToScheme(expr, indentation, inList, empty):
    """Print an AST as nicely-formatted Scheme code"""
    def __indent():
        """Helper function for indentation"""
        return " " * indentation

    # for each of the AST Node types, print it as if it were scheme code
    if expr["type"] == IDENTIFIER:
        return __indent() + expr[1]
    if expr["type"] == DEFINE:
        res = __indent() + "(define\n"
        res += AstToScheme(expr[1], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[2], indentation+1, inList, empty) + ")"
        return res
    if expr["type"] == BOOL:
        return __indent() + "#f" if not expr["val"] else "#t"
    if expr["type"] == INT:
        return __indent() + str(expr["val"])
    if expr["type"] == DBL:
        return __indent() + str(expr["val"])
    if expr["type"] == LAMBDADEF:
        res = __indent() + "(lambda ("
        for f in expr[1]:
            res += "\n" + AstToScheme(f, indentation+1, inList, empty)
        res += ")"
        for e in expr[2]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res
    if expr["type"] == IF:
        res = __indent() + "(if\n"
        res += AstToScheme(expr[1], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[2], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[3], indentation+1, inList, empty) + ")"
        return res
    if expr["type"] == SET:
        res = __indent() + "(set!\n"
        res += AstToScheme(expr[1], indentation+1, inList, empty) + "\n"
        res += AstToScheme(expr[2], indentation+1, inList, empty) + ")"
        return res
    if expr["type"] == AND:
        res = __indent() + "(and"
        for e in expr[1]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == OR:
        res = __indent() + "(or"
        for e in expr[1]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == BEGIN:
        res = __indent() + "(begin"
        for e in expr[1]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == APPLY:
        res = __indent()+"("
        for e in expr["expressions"]:
            res += "\n" + AstToScheme(e, indentation+1, inList, empty)
        return res + ")"
    # FIX: Printing list prints in new lines
    if expr["type"] == CONS:
        res = __indent()
        if expr is empty:
            res += "()"
            return res
        first = False
        if not inList:
            res += "("
            inList = True
            indentation += 1
            first = True
        res += "\n"
        car = expr["car"]
        cdr = expr["cdr"]
        if car is None:
            res += __indent() + "()"
        elif car["type"] == CONS:
            res += AstToScheme(car, indentation, False, empty)
        else:
            res += __indent() + AstToScheme(car, indentation, inList, empty)
        if cdr is not empty:
            if cdr["type"] != CONS:
                res += ".\n" + __indent() + AstToScheme(cdr, indentation, inList, empty)
            else:
                res += __indent() + AstToScheme(cdr, indentation, inList, empty)
        if first:
            res += ")"
            inList = False
            indentation -= 1
        return res
    if expr["type"] == VEC:
        res = __indent() + "#("
        for i in expr["items"]:
            res += "\n" + __indent() + AstToScheme(i, indentation+1, inList, empty)
        return res + ")"
    if expr["type"] == SYMBOL:
        return __indent() + expr["name"]
    if expr["type"] == QUOTE:
        return __indent() + "(quote\n" + AstToScheme(expr[1], indentation+1, inList, empty) + ")"
    if expr["type"] == TICK:
        return __indent()+"'\n" + AstToScheme(expr[1], indentation+1, inList, empty)
    if expr["type"] == CHAR:
        return __indent() + "#\\" + expr["val"]
    if expr["type"] == STR:
        return __indent() + expr["val"]
    if expr["type"] == BUILTIN:
        return __indent() + "Built-in Function ("+expr["name"]+")"
    if expr["type"] == LAMBDAVAL:
        return __indent() + "Lambda with " + str(len(expr["lambda"]["formals"])) + " args"
    if expr["type"] == COND:
        res = __indent() + "(cond"
        for c in expr[1]:
            res += "\n"+__indent() + "(\n"
            res += AstToScheme(c[0], indentation+1, inList, empty)
            for e in c[1]:
                res += "\n" + AstToScheme(e, indentation+1, inList, empty)
            res += ")"
        return res + ")"