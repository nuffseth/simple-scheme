import re
from scheme_types.token import *
from util.constants import *

class Scanner:
    # class variable
    addEOF = True

    def __init__(self):
        pass

    def isBlank(self, checkChar):
        """
        Checks if the given character is a space, tab, or newline.

        :param checkChar: The character to be checked.
        :type checkChar: str
        :return: True if the character is a space, tab, or newline. Else return False.
        :rtype: bool
        """
        blank = [' ', '\t', '\n']
        for i in blank:
            if i == checkChar:
                return True
        return False
    
    def containsDelim(self, checkChar):
        """
        Determines if the given character is a delimiter. 
        Delimiter is any of the following characters: ', ", newline, tab, LPAREN, RPAREN, or space.

        :param checkChar: The character to be checked.
        :type checkChar: str
        :return: True if the character is a delimiter. Else return False.
        :rtype: bool
        """
        delimiters = ['\'', '\"', '\n', '\t', '(', ')', ' ']
        for i in delimiters:
            if(checkChar == i):
                return True
        return False
    
    def scanTokens(self, source: str):
        """
        This method scans the source code and transforms it into a list of tokens.
        It adds an EOF token at the end, unless there is an error.

        :param source: The source code of the program, as one big string, or a line of code from the REPL.
        :type source: str
        :return: A list of tokens
        :rtype: list
        """
        tokenbuket = []  # the list to hold the each identifier.
        temp = ''  # tokenTex
        col = 0
        row = 0
        tempStr = ''
        inComment = False
        escaped = False
        isString = False
        escapedError = False
        # split source String by line store into array.
        line = source.splitlines()  # Spilt source String by line store in to String list
        # Reference for spiltlines() https://stackoverflow.com/questions/172439/how-do-i-split-a-multi-line-string-into-multiple-lines

        for x in line:
            charBucket = list(x)  # divide each char
            charBucket.append('\n')
            for y in charBucket:
                # check the whether or not it is comment
                if y == ';' and inComment == False:
                    inComment = True
                    continue  # cause the loop continue work

                # keep going to next character until it reaches newline or EOF
                elif inComment:
                    if (y == '\n' or y == '\0'):
                        inComment = False
                        continue
                    continue
                # if the string is in escaped state
                if escaped:
                    tempStr += y
                    if (y == '\"' or y == '\\' or y == 't' or y == 'n'):
                        escaped = False
                        continue
                    #instr+ ERROR
                    else:
                        escapedError = True
                        escaped = False
                        continue
                    # check if it is reading str and the current character is escaped so it can go into escaped checking mode.
                elif (isString and y == '\\'):
                    tempStr += y
                    escaped = True
                    continue
                # check current character is in deliminator.
                if self.containsDelim(y):
                    # check if temp is not empty
                    if len(temp) > 0:
                        # VCB cases that have LPAREN and turns into vector
                        if temp == '#' and y == '(':
                            temp += y
                            self.convertToken(
                                temp, row + 1, col - 1, tokenbuket)
                            temp = ''
                            continue
                        # VCB cases that have newline, space, tab, and goes to next character
                        # PRECHAR case that doesn't satisfy CHAR.
                        if temp == "#\\":
                            if (self.isBlank(y) == True):
                                # Not sure how to write this part
                                tokenbuket.append(Token(temp + " is not a valid character!", row + 1, col - 2, ERROR, None))
                                temp = ""
                                self.addEOF = False
                                continue
                            else:
                                temp += y
                                tokenbuket.append(
                                    Token(temp, row + 1, col - 2, CHAR, temp[2]))
                                temp = ""
                                continue
                        # Adds character to tempString until current character is ".
                        elif isString:
                            if y == '\"':
                                if (escapedError):
                                    tokenbuket.append(
                                        Token(tempStr, row + 1, col, ERROR, " is an invalid escaped character"))
                                    isString = False
                                    escapedError = False
                                    tempStr = ''
                                    temp = ''
                                    self.addEOF = False
                                    continue
                                else:
                                    tokenbuket.append(Token(tempStr, row + 1, col - len(temp), STR, tempStr.replace("\\n", "\n")
                                                            .replace("\\t", "\t")
                                                            .replace("\\\"", "\"")
                                                            .replace("\\\\", "\\")))
                                    isString = False
                                    tempStr = ""
                                    temp = ""
                                    continue
                            else:
                                tempStr += y
                                continue
                        else:
                            self.convertToken(temp, row + 1,col - len(temp), tokenbuket)
                            temp = ""
                        
                    if not self.isBlank(y):
                        if (y == '\"'):
                            if (isString == False):
                                # adds " to temp just in case error
                                temp += y
                                isString = True
                                continue
                        else:
                            self.convertToken(y + "", row + 1, col, tokenbuket)
                            temp = ""
                            continue    
                else:
                    # stores in tempString if
                    if isString:
                        tempStr += y
                    else:
                        temp += y
                col += 1 # increment column
            row += 1 # increment the row
            col = 0 # clean the column manually

        # check for unclosed string
        if (isString):
            tokenbuket.append(Token("does not contain closing double quotes (\").", 
                row, len(line[len(line) - 1]) - 1, ERROR, None))
            self.addEOF = False
        if (self.addEOF):
            tokenbuket.append(Token("\0", len(line), len(
                line[len(line) - 1]) - 1, EOFTOKEN, None))
        return TokenStream(tokenbuket)
    
    # We get the token from scanner and convert the corresponded token
    def convertToken(self, tokenText, line, col, bucket):  # l is the tokenbucket
        """
        This method takes a token from the scanner and converts it into a corresponding token.

        :param tokenText: The token to be converted.
        :type tokenText: str
        :param line: The line number where the token is found.
        :type line: int
        :param col: The column number where the token is found.
        :type col: int
        :param bucket: The token bucket where the token will be added.
        :type bucket: list

        :return: None
        """
        # keywords scanner
        if (tokenText == "and"):
            bucket.append(Token(tokenText, line, col, AND, None))
        elif (tokenText == "begin"):
            bucket.append(Token(tokenText, line, col, BEGIN, None))
        elif (tokenText == "cond"):
            bucket.append(Token(tokenText, line, col, COND, None))
        elif (tokenText == "define"):
            bucket.append(Token(tokenText, line, col, DEFINE, None))
        elif (tokenText == "lambda"):
            bucket.append(Token(tokenText, line, col, LAMBDA, None))
        elif (tokenText == "if"):
            bucket.append(Token(tokenText, line, col, IF, None))
        elif (tokenText == "or"):
            bucket.append(Token(tokenText, line, col, OR, None))
        elif (tokenText == "quote"):
            bucket.append(Token(tokenText, line, col, QUOTE, None))
        elif (tokenText == "set!"):
            bucket.append(Token(tokenText, line, col, SET, None))
        elif (tokenText == "("):  # special
            bucket.append(Token(tokenText, line, col, LEFTPAREN, None))
        elif (tokenText == ")"):
            bucket.append(Token(tokenText, line, col, RIGHTPAREN, None))
        elif (tokenText == "\'"):
            bucket.append(Token(tokenText, line, col, ABBREV, None))
        elif (tokenText == "#\\newline"):  # SPECIAL CHAR
            bucket.append(Token(tokenText, line, col, CHAR, '\n'))
        elif (tokenText == "#\\space"):
            bucket.append(Token(tokenText, line, col, CHAR, ' '))
        elif (tokenText == "#\\tab"):
            bucket.append(Token(tokenText, line, col, CHAR, '\t'))
        elif (tokenText == "#("):
            bucket.append(Token(tokenText, line, col, VEC, None))
        elif (tokenText == "#t"):
            bucket.append(Token(tokenText, line, col, BOOL, True))
        elif (tokenText == "#f"):
            bucket.append(Token(tokenText, line, col, BOOL, True))
        elif (tokenText == "#\\\0"):
            bucket.append(Token(tokenText + " is not a valid character",
                     line, col, ERROR, None))
            self.addEOF = False
        elif (tokenText == "+" or tokenText == "-"):
            bucket.append(Token(tokenText, line, col, IDENTIFIER, None))
        else:
            # PRECHAR->CHAR
            if re.match("^#\\\\.$", tokenText) is not None:
                literalchar = tokenText[2]
                bucket.append(Token(tokenText, line, col, CHAR, literalchar))
            # Checks if the begining of the string starts with [A-Za-z!$%&*/:<=>?~^] and zero or more occurrences of [A-Za-z!$%&*/:<=>?~^0-9.+\\-]
            elif re.match("^[A-Za-z!$%&*/:<=>?~_^][A-Za-z!$%&*/:<=>?~_^0-9.+\\-]*$", tokenText) is not None:
                bucket.append(Token(tokenText, line, col, IDENTIFIER, None))
            # Checks for all integers
            elif re.match("^[+-]?\\d+$", tokenText) is not None:
                bucket.append(Token(tokenText, line, col, INT, int(tokenText)))
            # Checks for all doubles
            elif re.match("^[+-]?\\d+\\.\\d+$", tokenText) is not None:
                bucket.append(Token(tokenText, line, col, DBL, float(tokenText)))
            else:
                bucket.append(Token(tokenText + " is not a valid token",line, col, ERROR, None))
                self.addEOF = False