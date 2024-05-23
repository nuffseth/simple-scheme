from util.constants import *
from scheme_types.token import *

def tokenToXml(token):  
    if token.type == ABBREV:
        return basicToken("AbbrevToken", token)
    elif token.type == AND:
        return basicToken("AndToken", token)
    elif token.type == BEGIN:
        return basicToken("AndToken", token)
    elif token.type == BOOL:
        return "<BoolToken line=" + str(token.line) + " col=" + str(token.col) + " val= " + "true" if token.literal == True else "False" + " />"
    elif token.type == CHAR:
        return "<CharToken line=" + str(token.line) + " col=" + str(token.col) + " val='" + escape(token.literal) + "' />"
    elif token.type == COND:
        return basicToken("CondToken", token)
    elif token.type == DBL:
        return "<DblToken line=" + str(token.line) + " col=" + str(token.col) + " val='" + str(token.literal) + "' />"
    elif token.type == DEFINE:
        return basicToken("DefineToken", token)
    elif token.type == EOFTOKEN:
        return "<EofToken />"
    elif token.type == IDENTIFIER:
        return "<IdentifierToken line=" + str(token.line) + " col=" + str(token.col) + " val='" + escape(token.tokenText) + "' />"
    elif token.type == IF:
        return basicToken("IfToken", token)
    elif token.type == INT:
        return "<IntToken line=" + str(token.line) + " col=" + str(token.col) + " val='" + str(token.literal) + "' />"
    elif token.type == LAMBDA:
        return basicToken("LambdaToken", token)
    elif token.type == LEFTPAREN:
        return basicToken("LParenToken", token)
    elif token.type == OR:
        return basicToken("OrToken", token)
    elif token.type == QUOTE:
        return basicToken("QuoteToken", token)
    elif token.type == RIGHTPAREN:
        return basicToken("RParenToken", token)
    elif token.type == SET:
        return basicToken("SetToken", token)
    elif token.type == STR:
        return "<StrToken line=" + str(token.line) + " col=" + str(token.col) + " val='" + escape(token.literal) + "' />"
    elif token.type == VEC:
        return basicToken("VectorToken", token)
    else:
        return "<ErrorToken line=" + str(token.line) + " col=" + str(token.col) + " val='" + token.tokenText + "' />"
def XmlToTokens(xml: str):
    """
    Given a string that is assumed to represent the output of tokenToXML,
    re-create the token stream
    """

    # we're just going to split the string into its lines, then look for
    # attributes and closing tags and use them to get all the parts
    res = []
    for token in xml.split("\n"):
        if token == "":
            continue
        firstSpace = int(token.find(" "))
        type = token[1: firstSpace]
        if type == "EofToken":
            res.append(Token("", 0, 0, EOFTOKEN, None))
            continue

        lineStart = token.find("line=")
        lineEnd = token.find(" ", lineStart + 2)
        colStart = token.find("col=")
        colEnd = token.find(" ", colStart + 2)
        line = int(token[lineStart + 5: lineEnd])
        col = int(token[colStart + 4: colEnd])

        valStart, valEnd = token.find("val="), len(token) - 3

        # so many of the tokens are done in the same way, so we can create a
        # hash of their name/type pairs, and use them to eliminate most of the
        # cases
        basicTokens = {"AbbrevToken": ("'", ABBREV), "AndToken": ("and", AND), "BeginToken": ("begin", BEGIN), "CondToken": ("cond", COND), "DefineToken": ("define", DEFINE), "IfToken": ("if", IF), "LambdaToken": (
            "lambda", LAMBDA), "LParenToken": ("(", LEFTPAREN), "OrToken": ("or", OR), "QuoteToken": ("quote", QUOTE), "RParenToken": (")", RIGHTPAREN), "SetToken": ("set!", SET), "VectorToken": ("#(", VEC)}
        if type in basicTokens.keys():
            val = basicTokens[type]
            res.append(Token(val[0], line, col, val[1], None))
        # All that remain are identifiers and datum tokens:
        elif type == "BoolToken":
            if token[valStart + 5: valEnd - 1] == "true":
                res.append(Token("#t", line, col, BOOL, True))
            else:
                res.append(Token("#f", line, col, BOOL, False))
        elif type == "CharToken":
            val = unescape(token[valStart + 5: valEnd - 1])
            literal = val[0]
            if val == "\\":
                literal, val = '\\',  "#\\\\"
            elif val == "\\t":
                literal, val = '\t', "#\\tab"
            elif val == "\\n":
                literal, val = '\n', "#\\newline"
            elif val == "\\'":
                literal, val = '\'', "#\\'"
            elif val == " ":
                val = "#\\space"
            else:
                val = "#\\" + val
            res.append(Token(val, line, col, CHAR, literal))
        elif type == "DblToken":
            val = token[valStart + 5: valEnd - 1]
            res.append(Token(val, line, col, DBL, float(val)))
        elif type == "IdentifierToken":
            res.append(
                Token(unescape(token[valStart + 5: valEnd - 1]), line, col, IDENTIFIER, None))
        elif type == "IntToken":
            val = token[valStart + 5: valEnd - 1]
            res.append(Token(val, line, col, INT, int(val)))
        elif type == "StrToken":
            val = unescape(token[valStart + 5: valEnd - 1])
            res.append(Token(val, line, col, STR, val))
        else:
            raise Exception("Unrecognized type: " + type)
    return TokenStream(res)

# Helper functions for this module
def unescape(s):
    """un-escape backslash, newline, tab, and apostrophe"""
    return s.replace("\\'", "'").replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")
def escape(s):
    result = s.replace("\\", "\\\\")
    result = s.replace("\t", "\\t")
    result = s.replace("\n", "\\n")
    result = s.replace("'", "\\'")
    return result
# The basic format of the print out
def basicToken(name, tok):  
    return "<" + name + " line=" + str(tok.line) + " col=" + str(tok.col) + " />"