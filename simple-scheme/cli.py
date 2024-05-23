import sys
from scheme_evaluator import *
from scheme_scanner import *
from scheme_parser import *
from serializer.token_serializer import *
from serializer.ast_serializer import *
from util.args import *
from util.default_env import *

def main(args):
    """Run the Scheme interpreter"""
    filename, mode, numModes, numFiles = "", "", 0, 0
    for a in args:
        if a in ["-help", "-scan", "-parse", "-interpret", "-full"]:
            mode = a
            numModes += 1
        else:
            filename = a
            numFiles += 1
    if numModes != 1 or numFiles > 1 or mode == "-help":
        return printHelp()

    defaultEnv = makeDefaultEnv()

    # Run the REPL loop, but only once if we have a valid filename
    while True:
        # Get some code
        codeToRun = ""
        if filename != "":
            codeToRun = getFile(filename)
        else:
            print(
                "Reading input from stdin is not supported in p4.  Please exit and try again")
            break
        if codeToRun == "":
            break

        # Process it according to the mode we're in
        try:
            # SCAN mode
            if mode == "-scan":
                tokens = Scanner().scanTokens(codeToRun)
                while tokens.hasNext():
                    print(tokenToXml(tokens.nextToken()))
                    tokens.popToken()
            # PARSE mode
            if mode == "-parse":
                try:
                    expressions = Parser(defaultEnv.poundT, defaultEnv.poundF, defaultEnv.empty).parse(XmlToTokens(codeToRun))
                except Exception as e:
                    print("Parse error: " + str(e))
                    break
                for expr in expressions:
                    print(AstToXml(expr))

            # INTERPRET mode
            if mode == "-interpret":
                expressions = XmlToAst(codeToRun, defaultEnv)
                for expr in expressions:
                    result = evaluate(expr, defaultEnv)
                    if result is not None:
                        print("; " + AstToScheme(result,
                              0, False, defaultEnv.empty))

            # FULL mode
            if mode == "-full":
                tokens = Scanner().scanTokens(codeToRun)
                try:
                    expressions = Parser(defaultEnv.poundT, defaultEnv.poundF,defaultEnv.empty).parse(tokens)
                except Exception as e:
                    print("Parse error: " + str(e))
                    break
                for expr in expressions:
                    result = evaluate(expr, defaultEnv)
                    if result is not None:
                        print("; " + AstToScheme(result,
                             0, False, defaultEnv.empty))

            # exit if we just processed a file
            if filename != "":
                break

        # any syntax error is going to just print and then exit the interpreter
        except SyntaxError as err:
            print(err)
            break

if __name__ == "__main__":
    main(sys.argv[1:])