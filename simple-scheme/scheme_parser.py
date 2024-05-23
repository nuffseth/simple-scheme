from scheme_scanner import *
from util.constants import *
from scheme_types.node import *
from scheme_types.token import *
 
class Parser:
    """The parser class is responsible for parsing a stream of tokens to produce
    an AST"""

    def __init__(self, true, false, empty):
        """Construct a parser by caching the environmental constants true,
        false, and empty"""
        self.true = true
        self.false = false
        self.empty = empty

    def parse(self, tokens: TokenStream):
        return self.getProgram(tokens)
    def getProgram(self, tokens):
        node = []
        while(tokens.nextToken().type != EOFTOKEN):
            node.append(self.getForm(tokens))
        return node

    def getForm(self, tokens: TokenStream):
        if(tokens.nextToken().type == LEFTPAREN and tokens.nextNextToken().type == DEFINE):
            form = self.getDefinition(tokens)
        else:
            form = self.getExpression(tokens)
        return form

    def getDefinition(self, tokens: TokenStream):
        tokens.popToken() # popping LPAREN
        tokens.popToken() # popping DEFINE
        if(tokens.nextToken().type == IDENTIFIER):
            identifier = IdentifierNode(tokens.nextToken().tokenText)
            tokens.popToken()
            expression = self.getExpression(tokens)
            if(tokens.nextToken().type == RIGHTPAREN):
                tokens.popToken()
                return DefineNode(identifier, expression)
            else: 
                raise Exception("No Right Paren for Definition")
        else:
            raise Exception("No Identifier")

    def getExpression(self, tokens: TokenStream):
        next: Token = tokens.nextToken()
        nextnext: Token = tokens.nextNextToken()
        # LPAREN QUOTE <datum> RPAREN
        if next.type == LEFTPAREN and nextnext.type == QUOTE:
            tokens.popToken() # pops Left Paren
            tokens.popToken() # pops Quotef
            next = tokens.nextToken()
            val = QuoteNode(self.getDatum(tokens))
            tokens.popToken() # pops Right Paren
            return val
        # LPAREN LAMBDA <formals> <body> RPAREN
        elif next.type == LEFTPAREN and nextnext.type == LAMBDA:
            tokens.popToken() # pops Left Paren
            tokens.popToken() # pops Lambda
            next = tokens.nextToken()
            val = LambdaDefNode(self.getFormals(tokens), self.getBody(tokens))
            tokens.popToken() # pops Right Paren
            return val
        # LPAREN IF <expression> <expression> <expression> RPAREN
        elif next.type == LEFTPAREN and nextnext.type == IF:
            tokens.popToken()
            tokens.popToken()
            first = self.getExpression(tokens)
            second = self.getExpression(tokens)
            third = self.getExpression(tokens)
            val = IfNode(first, second, third)
            tokens.popToken()
            return val     
        # LPAREN SET IDENTIFIER <expression> RPAREN
        elif next.type == LEFTPAREN and nextnext.type == SET:
            tokens.popToken()
            tokens.popToken()
            next = tokens.nextToken()
            if next.type == IDENTIFIER:
                idt = IdentifierNode(next.tokenText)
                tokens.popToken()
                expression = self.getExpression(tokens)
                if(tokens.nextToken().type == RIGHTPAREN):
                    tokens.popToken()
                    return SetNode(idt, expression)
                else:
                    raise Exception("No Right Paren for Set")
            else:
                raise Exception("No Identifier")
        # LPAREN AND <expression>+ RPAREN
        elif next.type == LEFTPAREN and nextnext.type == AND:
            tokens.popToken()
            tokens.popToken()
            expressions = []
            expressions.append(self.getExpression(tokens))
            next = tokens.nextToken()
            while next.type != RIGHTPAREN:
                expressions.append(self.getExpression(tokens))
                next = tokens.nextToken()
            tokens.popToken()
            return AndNode(expressions)
        # LPAREN OR <expression>+ RPAREN
        elif next.type == LEFTPAREN and nextnext.type == OR:
            tokens.popToken()
            tokens.popToken()
            expressions = []
            expressions.append(self.getExpression(tokens))
            next = tokens.nextToken()
            while next.type != RIGHTPAREN:
                expressions.append(self.getExpression(tokens))
                next = tokens.nextToken()
            tokens.popToken()
            return OrNode(expressions)
        # LPAREN BEGIN <expression>+ RPAREN
        elif next.type == LEFTPAREN and nextnext.type == BEGIN:
            tokens.popToken()
            tokens.popToken()
            expressions = []
            expressions.append(self.getExpression(tokens))
            next = tokens.nextToken()
            while next.type != RIGHTPAREN:
                expressions.append(self.getExpression(tokens))
                next = tokens.nextToken()
            tokens.popToken()
            return BeginNode(expressions)
        # LPAREN COND <condition>+ RPAREN
        elif next.type == LEFTPAREN and nextnext.type == COND:
            tokens.popToken()
            tokens.popToken()
            conditions = []
            conditions.append(self.getCondition(tokens))
            next = tokens.nextToken()
            while next.type != RIGHTPAREN:
                conditions.append(self.getCondition(tokens))
                next = tokens.nextToken()
            tokens.popToken()
            return CondNode(conditions)
        # ABBREV <datum>
        elif next.type == ABBREV:
            tokens.popToken()
            datum = self.getDatum(tokens)
            return TickNode(datum)
        # IDENTIFIER
        elif next.type == IDENTIFIER:
            tokens.popToken()
            return IdentifierNode(next.tokenText)
        # <constant>
        elif self.isConstant(next):
            return self.getDatum(tokens)
        # <application>
        else:
            expressions = self.getApp(tokens)
            return ApplyNode(expressions)


    def getCondition(self, tokens: TokenStream):
        expressions = []
        if(tokens.nextToken().type == LEFTPAREN):
            tokens.popToken()
            test = self.getExpression(tokens)
            while(tokens.nextToken().type != RIGHTPAREN):
                expressions.append(self.getExpression(tokens))
            tokens.popToken() # Pops Right Paren 
            return {"test": test, "expressions": expressions}
        else:
            raise Exception("Invalid format for Condition")

    def getBody(self, tokens: TokenStream):
        result = []
        next: Token = tokens.nextToken()
        nextnext = tokens.nextNextToken()
        while next.type == LEFTPAREN and nextnext.type == DEFINE:
            result.append(self.getDefinition(tokens))
            next = tokens.nextToken()
            nextnext = tokens.nextNextToken()
        result.append(self.getExpression(tokens))
        return result

    def getApp(self, tokens: TokenStream):
        result = []
        next: Token = tokens.nextToken()
        if(next.type == LEFTPAREN):
            tokens.popToken()
            result.append(self.getExpression(tokens))
            while(tokens.nextToken().type != RIGHTPAREN):
                result.append(self.getExpression(tokens))
            tokens.popToken()
            return result
        else:
            raise Exception("Invalid format for Application")

    def getDatum(self, tokens: TokenStream):
        nodes = []
        next: Token = tokens.nextToken()
        if(next.type == BOOL):
            tokens.popToken()
            if(next.tokenText == "#t"):
                return self.true
            else:
                return self.false
        elif(next.type == INT):
            tokens.popToken()
            return IntNode(next.literal)
        elif(next.type == DBL):
            tokens.popToken()
            return DblNode(next.literal)
        elif(next.type == CHAR):
            tokens.popToken()
            return CharNode(next.literal)
        elif(next.type == STR):
            tokens.popToken()
            return StrNode(next.literal)
        elif(next.type == IDENTIFIER):
            tokens.popToken()
            return SymbolNode(next.tokenText)
        elif(next.type == LEFTPAREN):
            tokens.popToken()
            next = tokens.nextToken()
            while(next.type != RIGHTPAREN):
                nodes.append(self.getDatum(tokens))
                next = tokens.nextToken()
            tokens.popToken()
            return ConsNode(nodes, self.empty) if len(nodes) != 0 else self.empty
        elif(next.type == VEC):
            tokens.popToken()
            next = tokens.nextToken()
            while(next.type != RIGHTPAREN):
                nodes.append(self.getDatum(tokens))
                next = tokens.nextToken()
            tokens.popToken()
            return VecNode(nodes)
        else:
            raise Exception("Incorrect format for Datum")
    def getFormals(self, tokens: TokenStream):
        formals = []
        next = tokens.nextToken()
        if(next.type == LEFTPAREN):
            tokens.popToken()
            next = tokens.nextToken()
            while(next.type == IDENTIFIER):
                formals.append(IdentifierNode(next.tokenText))
                tokens.popToken()
                next = tokens.nextToken()
            if(next.type == RIGHTPAREN):
                tokens.popToken()
                return formals
            else:
                raise Exception("Incorrect format for formals")
        else:
            raise Exception("Incorrect format for formals") 
    def isConstant(self, tempToken: Token):
        if(tempToken.type == BOOL or tempToken.type == INT or tempToken.type == STR or tempToken.type == CHAR or tempToken.type == DBL):
            return True
        return False