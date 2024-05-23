def getFromStdin(prompt):
    """Read a line from standard input (typically the keyboard).  If nothing is
    provided, return an empty string."""
    try:
        return input(prompt).rstrip()
    except EOFError:
        # we print a newline, because this is going to cause an exit, and it
        # will be a bit more uniform if all ways of exiting have a newline
        # before the shell is back in control
        print("")
        return ""


def getFile(filename):
    """Read a file and return its contents as a single string"""
    source_file = open(filename, "r")
    code = source_file.read()
    source_file.close()
    return code


def printHelp():
    """Print a help message"""
    print("simple-scheme -- An interpreter for a subset of Scheme, written in Python")
    print("  Usage: simple-scheme [mode] [filename]")
    print("    * If no filename is given, a REPL will read and evaluate one line of stdin at a time")
    print("    * If a filename is given, the entire file will be loaded and evaluated")
    print("  Modes:")
    print("    -help       Display this message and exit")
    print("    -scan       Scan Scheme code, output tokens as XML")
    print("    -parse      Parse from XML tokens, output an XML AST")
    print("    -interpret  Interpret from XML AST")
    print("    -full       Scan, parse, and interpret Scheme code")
