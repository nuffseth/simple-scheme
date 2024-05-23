from util.constants import *
from scheme_types.node import *

def AstToXml(expr: dict, indent="")->str:
    """
    Converts an Abstract Syntax Tree (AST) to an XML string.

    Parameters:
    - expr (dict): The Abstract Syntax Tree to be converted to XML.
    - indent (str): An optional string to be used as indentation in the XML output.

    Returns:
    - str: The XML representation of the given AST.

    Raises:
    - Exception: If an unknown XML tag is encountered during parsing.
    """
    global identation
    type = expr["type"]
    if type == IDENTIFIER:
        return f"{ident()}<Identifier val='{escape(expr['name'])}' />\n"
    elif type == DEFINE:
        str = f"{ident()}<Define>\n"
        identation += 1
        str += AstToXml(expr["identifier"], ident())
        str += AstToXml(expr["expression"], ident())
        str += "</Define>\n"
        identation -= 1
        return str
    elif type == BOOL:
        return f"{ident()}<Bool val='{expr['val']}' />\n"
    elif type == INT:
        return f"{ident()}<Int val='{expr['val']}' />\n"
    elif type == DBL:
        return f"{ident()}<Dbl val='{expr['val']}' />\n"
    elif type == LAMBDADEF:
        str = f"{ident()}<Lambda>\n"
        identation += 1
        str += f"{ident()}<Formals>\n"
        identation += 1
        for formal in expr["formals"]:
            str += AstToXml(formal, ident())
        identation -= 1
        str += f"{ident()}</Formals>\n"
        str += f"{ident()}<Expressions>\n"
        identation += 1
        for body in expr["expressions"]:
            str += AstToXml(body, ident())
        identation -= 1
        str += f"{ident()}</Expressions>\n"
        identation -= 1
        str += f"{ident()}</Lambda>\n"
        return str
    elif type == IF:
        str = f"{ident()}<If>\n"
        identation += 1
        str += AstToXml(expr["cond"], ident())
        str += AstToXml(expr["ifTrue"], ident())
        str += AstToXml(expr["ifFalse"], ident())
        identation -= 1
        str += f"{ident()}</If>\n"
        return str
    elif type == SET:
        str = f"{ident()}<Set>\n"
        identation += 1
        str += AstToXml(expr["identifier"], ident())
        str += AstToXml(expr["expression"], ident())
        identation -= 1
        str += f"{ident()}</Set>\n"
        return str
    elif type == AND:
        str = f"{ident()}<And>\n"
        identation += 1
        for expression in expr["expressions"]:
            str += AstToXml(expression, ident())
        identation -= 1
        str += f"{ident()}</And>\n"
        return str
    elif type == OR:
        str = f"{ident()}<Or>\n"
        identation += 1
        for expression in expr["expressions"]:
            str += AstToXml(expression, ident())
        identation -= 1
        str += f"{ident()}</Or>\n"
        return str
    elif type == BEGIN:
        str = f"{ident()}<Begin>\n"
        identation += 1
        for expression in expr["expressions"]:
            str += AstToXml(expression, ident())
        identation -= 1
        str += f"{ident()}</Begin>\n"
        return str
    elif type == APPLY:
        str = f"{ident()}<Apply>\n"
        identation += 1
        for expression in expr["expressions"]:
            str += AstToXml(expression, ident())
        identation -= 1
        str += f"{ident()}</Apply>\n"
        return str
    elif type == CONS:
        str = f"{ident()}<Cons>\n"
        identation += 1
        if (expr['car'] != None):
            str += AstToXml(expr["car"], ident())
        else:
            str += f"{ident()}<Null />\n"
        if(expr['cdr'] != None):
            str += AstToXml(expr["cdr"], ident())
        else:
            str += f"{ident()}<Null />\n"
        identation -= 1
        str += f"{ident()}</Cons>\n"
        return str
    elif type == VEC:
        str = f"{ident()}<Vector>\n"
        identation += 1
        for item in expr["items"]:
            str += AstToXml(item, ident())
        identation -= 1
        str += f"{ident()}</Vector>\n"
        return str
    elif type == SYMBOL:
        return f"{ident()}<Symbol val='{escape(expr['name'])}' />\n"
    elif type == QUOTE:
        str = f"{ident()}<Quote>\n"
        identation += 1
        str += AstToXml(expr["datum"], ident())
        identation -= 1
        str += f"{ident()}</Quote>\n"
        return str
    elif type == TICK:
        str = f"{ident()}<Tick>\n"
        identation += 1
        str += AstToXml(expr["datum"], ident())
        identation -= 1
        str += f"{ident()}</Tick>\n"
        return str
    elif type == CHAR:
        return f"{ident()}<Char val='{escape(expr['val'])}' />\n"
    elif type == STR:
        return f"{ident()}<Str val='{escape(expr['val'])}' />\n"
    elif type == COND:
        str = f"{ident()}<Cond>\n"
        identation += 1
        for condition in expr['conditions']:
            str += f"{ident()}<Condition>\n"
            identation += 1
            str += f"{ident()}<Test>\n"
            identation += 1
            str += AstToXml(condition['test'], ident())
            identation -= 1
            str += f"{ident()}</Test>\n"
            str += f"{ident()}<Actions>\n"
            identation += 1
            for action in condition['expressions']:
                str += AstToXml(action, ident())
            identation -= 1
            str += f"{ident()}</Actions>\n"
            identation -= 1
            str += f"{ident()}</Condition>\n"
        identation -= 1
        str += f"{ident()}</Cond>\n"
        return str
    else: 
        return f"{ident()}<Unknown type='{type}' />\n"


def XmlToAst(xml, env):
    """
    Converts an Abstract Syntax Tree (AST) to an XML string.

    Parameters:
    - expr (dict): The Abstract Syntax Tree to be converted to XML.
    - indent (str): An optional string to be used as indentation in the XML output.

    Returns:
    - str: The XML representation of the given AST.

    Raises:
    - Exception: If an unknown XML tag is encountered during parsing.
    """

    res = []
    lines = xml.split("\n")
    next = 0

    def __unescape(s: str) -> str:
        """un-escape backslash, newline, tab, and apostrophe"""
        return s.replace("'", "\\'").replace("\n", "\\n").replace("\t", "\\t").replace("\\", "\\\\")

    def parseNext():
        """A helper function for parsing the next AST node"""
        nonlocal lines
        nonlocal next
        while next < len(lines) and lines[next] == "":
            next += 1
        if next >= len(lines):
            return None
        valStart = lines[next].find("val=")
        valEnd = len(lines[next]) - 3
        if lines[next].find("<Identifier") > -1:
            val = __unescape(lines[next][valStart + 5: valEnd - 1])
            next += 1
            return IdentifierNode(val)
        if lines[next].find("<Define") > -1:
            next += 1
            identifier = parseNext()
            expression = parseNext()
            next += 1
            return DefineNode(identifier, expression)
        if lines[next].find("<Bool") > -1:
            val = lines[next][valStart + 5: valEnd - 1]
            next += 1
            return env.poundT if val == "true" else env.poundF
        if lines[next].find("<Int") > -1:
            val = lines[next][valStart + 5: valEnd - 1]
            next += 1
            return IntNode(int(val))
        if lines[next].find("<Dbl") > -1:
            val = lines[next][valStart + 5: valEnd - 1]
            next += 1
            return DblNode(float(val))
        if lines[next].find("<Lambda") > -1:
            next += 2
            formals = []
            while lines[next].find("</Formals>") == -1:
                formals.append(parseNext())
            next += 2
            body = []
            while lines[next].find("</Expressions>") == -1:
                body.append(parseNext())
            next += 2
            return LambdaDefNode(formals, body)
        if lines[next].find("<If") > -1:
            next += 1
            cond = parseNext()
            true = parseNext()
            false = parseNext()
            next += 1
            return IfNode(cond, true, false)
        if lines[next].find("<Set") > -1:
            next += 1
            identifier = parseNext()
            expression = parseNext()
            next += 1
            return SetNode(identifier, expression)
        if lines[next].find("<And") > -1:
            next += 1
            exprs = []
            while lines[next].find("</And>") == -1:
                exprs.append(parseNext())
            next += 1
            return AndNode(exprs)
        if lines[next].find("<Or") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Or>") == -1:
                exprs.append(parseNext())
            next += 1
            return OrNode(exprs)
        if lines[next].find("<Begin") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Begin>") == -1:
                exprs.append(parseNext())
            next += 1
            return BeginNode(exprs)
        if lines[next].find("<Apply") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Apply>") == -1:
                exprs.append(parseNext())
            next += 1
            return ApplyNode(exprs)
        if lines[next].find("<Cons") > -1:
            next += 1
            car = None
            cdr = None
            if lines[next].find("<Null />") == -1:
                car = parseNext()
            else:
                next += 1
            if lines[next].find("<Null />") == -1:
                cdr = parseNext()
            else:
                next += 1
            next += 1
            return ConsNode(car, cdr) if car is not None and cdr is not None else env.empty
        if lines[next].find("<Vector") > -1:
            next += 1
            exprs = []
            while lines[next].find("</Vector>") == -1:
                exprs.append(parseNext())
            next += 1
            return VecNode(exprs)
        if lines[next].find("<Quote") > -1:
            next += 1
            datum = parseNext()
            next += 1
            return QuoteNode(datum)
        if lines[next].find("<Tick") > -1:
            next += 1
            datum = parseNext()
            next += 1
            return TickNode(datum)
        if lines[next].find("<Char") > -1:
            val = __unescape(lines[next][valStart + 5: valEnd - 1])
            next += 1
            literal = val[0]
            if val == "\\":
                literal = '\\'
            elif val == "\\t":
                literal = '\t'
            elif val == "\\n":
                literal = '\n'
            elif val == "\\'":
                literal = '\''
            return CharNode(literal)
        if lines[next].find("<Str") > -1:
            val = __unescape(lines[next][valStart + 5: valEnd - 1])
            next += 1
            return StrNode(val)
        if lines[next].find("<Symbol") > -1:
            val = __unescape(lines[next][valStart + 5: valEnd - 1])
            next += 1
            return SymbolNode(val)
        if lines[next].find("<Cond") > -1:
            next += 1
            conditions = []
            while lines[next].find("<Condition>") > -1:
                next += 2
                test = parseNext()
                next += 2
                exprs = []
                while lines[next].find("</Actions>") == -1:
                    exprs.append(parseNext())
                next += 2
                conditions.append({"test": test, "exprs": exprs})
            next += 1
            return CondNode(conditions)
        raise Exception("Unrecognized XML tag: " + lines[next])

    # given our helper function, we can just iterate through the lines, passing
    # each to parseNext.
    while next < len(lines):
        tmp = parseNext()
        if tmp:
            res.append(tmp)
    return res

# [mfs] AstToScheme's indentation isn't great, and its pretty-printing really
#       stinks.  It's worth revisiting this: do we really need to print whole
#       ASTs as Scheme source, or just values?

#Helper Methods
identation = 0
def escape(s):
    return s.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("'", "\\'")
def ident():
    global identation
    identString = ""
    for i in range(identation):
        identString += " "
    return identString