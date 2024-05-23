import math
from scheme_types.node import *
from util.constants import *
from util.env import *

# Helper functions for math operations
    # (+ number...) (one or more values)
    # (- number...) (one or more values)
    # (* number...) (one or more values)
    # (/ number...) (one or more values)
    # (% number...) (one or more values)
    # (== number...) (one or more values)
    # (> number...) (one or more values)
    # (>= number...) (one or more values)
    # (< number...) (one or more values)
    # (<= number...) (one or more values)
    # (abs number)
    # (sqrt number)
    # (acos number)
    # (asin number)
    # (atan number)
    # (cos number)
    # (cosh number)
    # (sin number)
    # (sinh number)
    # (tan number)
    # (tanh number)
    # (integer? number)
    # (double? number)
    # (number? number)
    # (symbol? number)
    # (procedure? number)
    # (log10 number)
    # (loge number)
    # (pow baseNum expNum)
    # (not val)
    # (integer->double int)
    # (double->integer double)
    # (null?)
    # (and vals...) (one or more values)
    # (or vals...) (one or more values)
def addMathFuncs(env: Env) -> None:
    env.put("pi", DblNode(math.pi))
    env.put("e",  DblNode(math.e))
    env.put("tau", DblNode(math.pi * 2))
    env.put("inf+", DblNode(float("inf")))
    env.put("inf-", DblNode(float("-inf")))
    env.put("nan", DblNode(float("nan")))
    env.put("+", BuiltInNode("+", lambda args: operantHelper("+", args)))
    env.put("-", BuiltInNode("-", lambda args: operantHelper("-", args)))
    env.put("*", BuiltInNode("*", lambda args: operantHelper("*", args)))
    env.put("/", BuiltInNode("/", lambda args: operantHelper("/", args)))
    env.put("%", BuiltInNode("%", lambda args: operantHelper("%", args)))
    env.put("pow", BuiltInNode("pow", lambda args: operantHelper("pow", args)))
    env.put("min", BuiltInNode("min", lambda args: operantHelper("min", args)))
    env.put("max", BuiltInNode("max", lambda args: operantHelper("max", args)))
    env.put("abs", BuiltInNode("abs", lambda args: operantHelper("abs", args)))
    env.put("==", BuiltInNode("==", lambda args: conditionOperationHelper("==", args)))
    env.put("!=", BuiltInNode("!=", lambda args: conditionOperationHelper("!=", args)))
    env.put("<", BuiltInNode("<", lambda args: conditionOperationHelper("<", args)))
    env.put(">", BuiltInNode(">", lambda args: conditionOperationHelper(">", args)))
    env.put("<=", BuiltInNode("<=", lambda args: conditionOperationHelper("<=", args)))
    env.put(">=", BuiltInNode(">=", lambda args: conditionOperationHelper(">=", args)))
    env.put("sqrt", BuiltInNode("sqrt", lambda args: advancedOperationHelper("sqrt", args)))
    env.put("acos", BuiltInNode("acos", lambda args: advancedOperationHelper("acos", args)))
    env.put("asin", BuiltInNode("asin", lambda args: advancedOperationHelper("asin", args)))
    env.put("atan", BuiltInNode("atan", lambda args: advancedOperationHelper("atan", args)))
    env.put("cos", BuiltInNode("cos", lambda args: advancedOperationHelper("cos", args)))
    env.put("sin", BuiltInNode("sin", lambda args: advancedOperationHelper("sin", args)))
    env.put("tan", BuiltInNode("tan", lambda args: advancedOperationHelper("tan", args)))
    env.put("cosh", BuiltInNode("cosh", lambda args: advancedOperationHelper("cosh", args)))
    env.put("sinh", BuiltInNode("sinh", lambda args: advancedOperationHelper("sinh", args)))
    env.put("tanh", BuiltInNode("tanh", lambda args: advancedOperationHelper("tanh", args)))
    env.put("log10", BuiltInNode("log10", lambda args: advancedOperationHelper("log10", args)))
    env.put("loge", BuiltInNode("loge", lambda args: advancedOperationHelper("loge", args)))
    env.put("null?", BuiltInNode("null?", lambda args: oneArgsOperationHelper("null?", args)))
    env.put("number?", BuiltInNode("number?", lambda args: oneArgsOperationHelper("number?", args)))
    env.put("double?", BuiltInNode("double?", lambda args: oneArgsOperationHelper("double?", args)))
    env.put("symbol?", BuiltInNode("string?", lambda args: oneArgsOperationHelper("string?", args)))
    env.put("integer?", BuiltInNode("integer?", lambda args: oneArgsOperationHelper("integer?", args)))
    env.put("procedure?", BuiltInNode("procedure?", lambda args: oneArgsOperationHelper("procedure?", args)))
    env.put("integer->double", BuiltInNode("integer->double", lambda args: oneArgsOperationHelper("integer->double", args)))
    env.put("double->integer", BuiltInNode("double->integer", lambda args: oneArgsOperationHelper("double->integer", args)))
    env.put("not", BuiltInNode("not", lambda args: oneArgsOperationHelper("not", args)))

    # Helper function for returning the correct type of node
    def IntOrDouble(args: list, computedValue) -> dict:
        if all(arg["type"] == INT for arg in args):
            return IntNode(computedValue)
        else:
            return DblNode(computedValue)

    def operantHelper(operation: str, args: list) -> dict:
        if(len(args) == 0):
            raise Exception("operantHelper: no arguments")
        if(not all((arg["type"] == DBL) or (arg["type"] == INT) for arg in args)):
            raise Exception("operantHelper: not all arguments are numbers")
        if operation == "+":
            computedValue = sum(arg["val"] for arg in args)
            return IntOrDouble(args, computedValue)
        elif operation == "-":
            computedValue = args[0]["val"]
            for arg in args[1:]:
                computedValue -= arg["val"]
            return IntOrDouble(args, computedValue)
        elif operation == "*":
            computedValue = 1
            for arg in args:
                computedValue *= arg["val"]
            return IntOrDouble(args, computedValue)
        elif operation == "/":
            computedValue = args[0]["val"]
            for arg in args[1:]:
                computedValue /= arg["val"]
            return IntOrDouble(args, computedValue)
        elif operation == "%":
            computedValue = args[0]["val"]
            for arg in args[1:]:
                computedValue %= arg["val"]
            return IntOrDouble(args, computedValue)
        elif operation == "pow":
            computedValue = args[0]["val"]
            for arg in args[1:]:
                computedValue **= arg["val"]
            return IntOrDouble(args, computedValue)
        elif operation == "min":
            computedValue = min(arg["val"] for arg in args)
            return IntOrDouble(args, computedValue)
        elif operation == "max":
            computedValue = max(arg["val"] for arg in args)
            return IntOrDouble(args, computedValue)
        elif operation == "abs":
            computedValue = abs(args[0]["val"])
            return IntOrDouble(args, computedValue)
        else:
            pass
        
    def advancedOperationHelper(operation: str, args: list) -> dict:
        if(len(args) != 1):
            raise Exception("advancedOperationHelper: not one argument")
        if operation == "sqrt":
            return DblNode(math.sqrt(args[0]["val"]))
        elif operation == "acos":
            return DblNode(math.acos(args[0]["val"]))
        elif operation == "asin":
            return DblNode(math.asin(args[0]["val"]))
        elif operation == "atan":
            return DblNode(math.atan(args[0]["val"]))
        elif operation == "cos":
            return DblNode(math.cos(args[0]["val"]))
        elif operation == "cosh":
            return DblNode(math.cosh(args[0]["val"]))
        elif operation == "sin":
            return DblNode(math.sin(args[0]["val"]))
        elif operation == "sinh":
            return DblNode(math.sinh(args[0]["val"]))
        elif operation == "tan":
            return DblNode(math.tan(args[0]["val"]))
        elif operation == "tanh":
            return DblNode(math.tanh(args[0]["val"]))
        elif operation == "log10":
            return DblNode(math.log10(args[0]["val"]))
        elif operation == "loge":
            return DblNode(math.log(args[0]["val"]))
        else:
            pass
    
    def oneArgsOperationHelper(operation: str, args: list) -> dict:
        if(len(args) != 1):
            raise Exception("oneArgsOperationHelper: not one argument")
        if operation == "not":
            return env.poundT if args[0] == env.poundF else env.poundF
        elif operation == "null?":
            return env.poundT if args[0] == env.empty else env.poundF
        elif operation == "integer?":
            return env.poundT if args[0]["type"] == INT else env.poundF
        elif operation == "double?":
            return env.poundT if args[0]["type"] == DBL else env.poundF
        elif operation == "number?":
            return env.poundT if args[0]["type"] == DBL or args[0]["type"] == INT else env.poundF
        elif operation == "symbol?":
            return env.poundT if args[0]["type"] == SYMBOL else env.poundF
        elif operation == "procedure?":
            return env.poundT if args[0]["type"] == BUILTIN or args[0]["type"] == LAMBDAVAL else env.poundF
        elif operation == "integer->double":
            return DblNode(float(args[0]["val"]))
        elif operation == "double->integer":
            return IntNode(int(args[0]["val"]))
        else:
            pass

# (== number...) (one or more values)
# (> number...) (one or more values)
# (>= number...) (one or more values)
# (< number...) (one or more values)
# (<= number...) (one or more values)
# Fix for one or more not JUST two
    def conditionOperationHelper(operation: str, args: list) -> dict:
        if(len(args) <= 1):
            raise Exception("conditionOperationHelper: no arguments")
        if not all(arg["type"] == INT or arg["type"] == DBL for arg in args):
            raise Exception("conditionOperationHelper: not all numbers")
        if operation == "==":
            for arg in args[1:]:
                if args[0]["val"] != arg["val"]:
                    return env.poundF
            return env.poundT
        elif operation == "!=":
            for arg in args[1:]:
                if args[0]["val"] == arg["val"]:
                    return env.poundF
            return env.poundT
        elif operation == ">":
            for arg in args[1:]:
                if args[0]["val"] <= arg["val"]:
                    return env.poundF
            return env.poundT
        elif operation == ">=":
            for arg in args[1:]:
                if args[0]["val"] < arg["val"]:
                    return env.poundF
            return env.poundT
        elif operation == "<":
            for arg in args[1:]:
                if args[0]["val"] >= arg["val"]:
                    return env.poundF
            return env.poundT
        elif operation == "<=":
            for arg in args[1:]:
                if args[0]["val"] > arg["val"]:
                    return env.poundF
            return env.poundT
        else:
            pass
        
def addListFuncs(env: Env) -> None:
    env.put("car", BuiltInNode("car", lambda args: addListHelper("car", args)))
    env.put("cdr", BuiltInNode("cdr", lambda args: addListHelper("cdr", args)))
    env.put("cons", BuiltInNode("cons", lambda args: addListHelper("cons", args)))
    env.put("list", BuiltInNode("list", lambda args: addListHelper("list", args)))
    env.put("list?", BuiltInNode("list?", lambda args: addListHelper("list?", args)))
    env.put("set-car!", BuiltInNode("set-car!", lambda args: addListHelper("set-car!", args)))
    env.put("set-cdr!", BuiltInNode("set-cdr!", lambda args: addListHelper("set-cdr!", args)))

    # universal helper function for list functions
    def addListHelper(operation: str, args: list) -> dict:
        # one or more args: list
        # one args: car, cdr, list?
        if operation == "car" or operation == "cdr" or operation == "list?":
            if(len(args) != 1):
                raise Exception("Error: " + operation + " takes one argument")
        # two args: cons, set-car!, set-cdr!
        elif operation == "cons" or operation == "set-car!" or operation == "set-cdr!":
            if(len(args) != 2):
                raise Exception("Error: " + operation + " takes two arguments" + str(len(args)) + str(args))
        if operation == "list":
            result = env.empty
            for i in range(len(args) - 1, -1, -1):
                result = ConsNode(args[i],result)
            return result
        elif operation == "car":
            if args[0]["type"] != CONS:
                raise Exception("Error: car takes a cons cell")
            return args[0]["car"]
        elif operation == "cdr":
            if args[0]["type"] != CONS:
                raise Exception("Error: cdr takes a cons cell")
            return args[0]["cdr"]
        elif operation == "cons":
            return ConsNode(args[0], args[1])
        elif operation == "list?":
            if args[0]["type"] == CONS:
                return env.poundT
            return env.poundF
        elif operation == "set-car!":
            if args[0]["type"] != CONS:
                raise Exception("Error: set-car! takes a cons cell")
            args[0]["car"] = args[1]
            return None
        elif operation == "set-cdr!":
            if args[0]["type"] != CONS:
                raise Exception("Error: set-cdr! takes a cons cell")
            args[0]["cdr"] = args[1]
            return None
        else:
            raise Exception("Error: " + operation + " is not a valid list function")
    
def addStringFuncs(env: Env) -> None:
    """Add standard string functions to the given environment"""
    # (string-append str str)
    # (string-length str)
    # (substring str fromInc toExc) (fromInc and toExc are integers; first is inclusive, second is exclusive)
    # (string? val)
    # (string-ref str int)
    # (string-equal? str str)
    # (string chars...) (zero or more characters)
    env.put("string-append", BuiltInNode("string-append", lambda args: addStringFunc(args, "string-append")))
    env.put("string-length", BuiltInNode("string-length", lambda args: addStringFunc(args, "string-length")))
    env.put("string?", BuiltInNode("string?", lambda args: addStringFunc(args, "string?")))
    env.put("string-ref", BuiltInNode("string-ref", lambda args: addStringFunc(args, "string-ref")))
    env.put("string-equal?", BuiltInNode("string-eqaul?", lambda args: addStringFunc(args, "string-equal?")))
    env.put("string", BuiltInNode("string", lambda args: addStringFunc(args, "string")))
    env.put("substring", BuiltInNode("substring", lambda args: addStringFunc(args, "substring")))

    # universal helper function for string functions
    def addStringFunc(args: list, operation: str) -> dict:
        # run if statements and split into categories based on anticipated number of arguments
        if(operation == "string?" or operation == "string-length"):
            if(len(args) != 1):
                raise Exception("addStringFunc: not one argument")
            if operation == "string-length":
                if(args[0]["type"] != STR):
                    raise Exception("addStringFunc: not a string")
                return IntNode(len(args[0]["val"]))
            elif operation == "string?":
                return env.poundT if args[0]["type"] == STR else env.poundF
            else: 
                pass
        elif(operation == "string-append" or operation == "string-equal?" or operation == "string-ref"):
            if(len(args) != 2):
                raise Exception("addStringFunc: not two arguments")
            if operation == "string-append":
                if not all(arg["type"] == STR for arg in args):
                    raise Exception("addStringFunc: not a string")
                appendString = args[0]["val"] + args[1]["val"]
                return StrNode(appendString)
            elif operation == "string-equal?":
                if not all(arg["type"] == STR for arg in args):
                    raise Exception("addStringFunc: not a string")
                return env.poundT if args[0]["val"] == args[1]["val"] else env.poundF
            elif operation == "string-ref":
                if(args[0]["type"] != STR or args[1]["type"] != INT):
                    raise Exception("addStringFunc: not a string or int")
                return CharNode(args[0]["val"][args[1]["val"]]) # get the char at the index
            else:
                pass
        elif(operation == "substring"):
            if(len(args) != 3):
                raise Exception("addStringFunc: not three arguments")
            if not (args[0]["type"] == STR and args[1]["type"] == INT and args[2]["type"] == INT):
                raise Exception("addStringFunc: not a string or int")
            return StrNode(args[0]["val"][args[1]["val"]:args[2]["val"]]) # get the substring from 
                                                                                       # the first index to the second index
        elif operation == "string":
            appendString = ""
            for arg in args:
                if(arg["type"] != CHAR):
                    raise Exception("addStringFunc: not a char")
                appendString += arg["val"]
            return StrNode("".join(appendString))
        else:
            pass
    pass

# vector function uses different helper functions per each number of arguments
def addVectorFuncs(env: Env) -> None:
    # (vector-length vec)
    # (vector-get vec idx)
    # (vector-set! vec idx val)
    # (vector vals...) (zero or more values)
    # (vector? val)
    # (make-vector size)
    env.put("vector-length", BuiltInNode("vector-length", lambda args: OneArg("vector-length", args)))
    env.put("vector?",  BuiltInNode("vector?", lambda args: OneArg("vector?", args)))
    env.put("make-vector", BuiltInNode("make-vector", lambda args: OneArg("make-vector", args)))
    env.put("vector-get", BuiltInNode("vector-get", lambda args: TwoArgs("vector-get", args)))
    env.put("vector-set!", BuiltInNode("vector-set!", lambda args: ThreeArgs("vector-set!", args)))
    env.put("vector", BuiltInNode("vector", lambda args: vectorHelper(args)))
    
    def vectorHelper(args: list) -> dict:
        return VecNode(args)
    
    def OneArg(operation: str, args: list) -> dict:
        if len(args) != 1:
            raise Exception("OneArg: wrong number of arguments")
        if operation == "vector-length":
            if args[0]["type"] == VEC:
                return IntNode(len(args[0]["items"]))
            else:
                raise Exception("vector-length: argument is not a vector")
        elif operation == "vector?":
            if args[0]["type"] == VEC:
                return env.poundT
            else:
                return env.poundF
        elif operation == "make-vector":
            if args[0]["type"] == INT:
                size = args[0]["val"]
                if size < 0:
                    raise Exception("make-vector: size is negative")
                return VecNode([env.poundF] * size)
            else:
                raise Exception("make-vector: argument is not an integer")
        else:
            pass
    
    def TwoArgs(operation: str, args: list) -> dict:
        if len(args) != 2:
            raise Exception("twoArgs: wrong number of arguments")
        if operation == "vector-get":
            if args[0]["type"] == VEC:
                if args[1]["type"] == INT:
                    index = args[1]["val"]
                    if index < 0 or index >= len(args[0]["items"]):
                        raise Exception("vector-get: index out of bounds")
                    # args is a dictionary, 
                    return args[0]["items"][index]
                else:
                    raise Exception("vector-get: index is not an integer")
            else:
                raise Exception("vector-get: argument is not a vector")
        else:
            pass
    
    def ThreeArgs(operation: str, args: list) -> dict:
        if len(args) != 3:
            raise Exception("threeArgs: wrong number of arguments")
        if operation == "vector-set!":
            if args[0]["type"] == VEC:
                if args[1]["type"] == INT:
                    index = args[1]["val"]
                    if index < 0 or index >= len(args[0]["items"]):
                        raise Exception("vector-set!: index out of bounds")
                    args[0]["items"][index] = args[2]
                else:
                    raise Exception("vector-set!: index is not an integer")
            else:
                raise Exception("vector-set!: argument is not a vector")
        else:
            pass