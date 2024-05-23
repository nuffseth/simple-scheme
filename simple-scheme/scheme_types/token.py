class Token:
    """The Token class will be used for all token types in slang, since we
    don't need to subclass it for different literal types"""

    def __init__(self, tokenText, line, col, type, literal):
        """Construct a token from the text it corresponds to, the line/column
        where the text appears the token type, and an optional literal (an
        interpretation of that text as its real type)"""
        self.tokenText = tokenText
        self.line = line
        self.col = col
        self.type = type
        self.literal = literal

class TokenStream:
    """TokenStream is a transliteration of the Java TokenStream.  It's just a
    sort of iterator-with-lookahead wrapper around a list of tokens"""

    def __init__(self, tokens):
        """Construct a TokenStream by setting the list to `tokens` and resetting
        the iterator position to 0"""
        self.__tokens = tokens
        self.__next = 0

    def reset(self):
        """Reset the token stream iterator to the first token"""
        self.__next = 0

    def nextToken(self):
        """Return (by peeking) the next token in the stream, if it exists"""
        return None if not self.hasNext() else self.__tokens[self.__next]

    def nextNextToken(self):
        """Return (by peeking) the token that is two positions forward in the
        stream, if it exists"""
        return None if not self.hasNextNext() else self.__tokens[self.__next + 1]

    def popToken(self):
        """Advance the token stream by one"""
        self.__next += 1

    def hasNext(self):
        """Report whether a peek forward will find a token or not"""
        return self.__next < len(self.__tokens)

    def hasNextNext(self):
        """Report whether a peek forward by two positions will find a token or
        not"""
        return (self.__next + 1) < len(self.__tokens)
    