import string
import argparse
from time import time
from enum import Enum
from typing import Optional

class ScannerException(Exception):
    pass

class StringStream:
    def __init__(self, input_string: str) -> None:
        self.string = input_string

    def is_empty(self) -> bool:
        return len(self.string) == 0

    def peek_char(self) -> Optional[str]:
        if not self.is_empty():
            return self.string[0]
        return None

    def eat_char(self) -> None:
        # take the first character off the string
        self.string = self.string[1:]


# put characters to ignore in this array
IGNORE = [" ", "\n"]
NUMS   = [str(x) for x in range(10)]

alphabet_string = string.ascii_lowercase
CHARS = list(alphabet_string)

class Token(Enum):
    ADD    = "ADD"
    MULT   = "MULT"
    ASSIGN = "ASSIGN"
    SEMI   = "SEMI"
    INCR   = "INCR"
    ID     = "ID"
    NUM    = "NUM"

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"

class NaiveScanner:

    def __init__(self, input_string:str) -> None:
        self.ss = StringStream(input_string)

    # helper methods (allowed: new functions)
    def _skip_ignored(self) -> None:
        while self.ss.peek_char() in IGNORE:
            self.ss.eat_char()

    def _scan_id(self) -> Lexeme:
        # precondition: first char is a lowercase letter
        value = ""
        # first char must be a letter
        value += self.ss.peek_char()
        self.ss.eat_char()

        # after that, letters OR digits are allowed
        while True:
            c = self.ss.peek_char()
            if c is None:
                break
            if (c in CHARS) or (c in NUMS):
                value += c
                self.ss.eat_char()
            else:
                break
        return Lexeme(Token.ID, value)

    def _scan_num(self) -> Lexeme:
        # precondition: first char is a digit
        value = ""

        # read leading digits
        while self.ss.peek_char() in NUMS:
            value += self.ss.peek_char()
            self.ss.eat_char()

        # optional decimal part
        if self.ss.peek_char() == ".":
            value += "."
            self.ss.eat_char()

            # MUST have at least one digit after the dot
            if self.ss.peek_char() not in NUMS:
                raise ScannerException()

            while self.ss.peek_char() in NUMS:
                value += self.ss.peek_char()
                self.ss.eat_char()

        # IMPORTANT: do NOT raise if the next char is '.'
        # Example: "1.2.3" should return NUM("1.2") first,
        # then fail on the next token() call when it sees '.'

        return Lexeme(Token.NUM, value)

    def token(self) -> Optional[Lexeme]:

        # First handle the ignore case
        self._skip_ignored()

        # If there is nothing to return, return None
        if self.ss.is_empty():
            return None

        # multi-char operator must be checked before single-char
        if self.ss.peek_char() == "+":
            # INCR: "++"
            self.ss.eat_char()
            if self.ss.peek_char() == "+":
                self.ss.eat_char()
                return Lexeme(Token.INCR, "++")
            # otherwise it's just ADD
            return Lexeme(Token.ADD, "+")

        # Scan for the single character tokens
        if self.ss.peek_char() == "*":
            self.ss.eat_char()
            return Lexeme(Token.MULT, "*")

        if self.ss.peek_char() == "=":
            self.ss.eat_char()
            return Lexeme(Token.ASSIGN, "=")

        if self.ss.peek_char() == ";":
            self.ss.eat_char()
            return Lexeme(Token.SEMI, ";")

        # Scan for the multi character tokens
        if self.ss.peek_char() in CHARS:
            return self._scan_id()

        if self.ss.peek_char() in NUMS:
            return self._scan_num()

        # if we cannot match a token, throw an exception
        raise ScannerException()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    f = open(args.file_name)
    f_contents = f.read()
    f.close()

    verbose = args.verbose

    s = NaiveScanner(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if (verbose):
            print(t)
    end = time()
    print("time to parse (seconds): ", str(end-start))