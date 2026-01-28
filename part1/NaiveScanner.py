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

    def peek_next_char(self) -> Optional[str]:
        if len(self.string) >= 2:
            return self.string[1]
        return None

    def eat_char(self) -> None:
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

    def _skip_ignored(self) -> None:
        while self.ss.peek_char() in IGNORE:
            self.ss.eat_char()

    def _scan_id(self) -> Lexeme:
        # first char is lowercase letter
        value = ""
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
        value = ""

        # optional leading digits
        while self.ss.peek_char() in NUMS:
            value += self.ss.peek_char()
            self.ss.eat_char()

        # optional decimal part
        if self.ss.peek_char() == ".":
            value += "."
            self.ss.eat_char()

            # must have at least one digit after '.'
            if self.ss.peek_char() not in NUMS:
                raise ScannerException()

            while self.ss.peek_char() in NUMS:
                value += self.ss.peek_char()
                self.ss.eat_char()

        return Lexeme(Token.NUM, value)

    def token(self) -> Optional[Lexeme]:
        self._skip_ignored()

        if self.ss.is_empty():
            return None

        # INCR must be checked before ADD
        if self.ss.peek_char() == "+":
            self.ss.eat_char()
            if self.ss.peek_char() == "+":
                self.ss.eat_char()
                return Lexeme(Token.INCR, "++")
            return Lexeme(Token.ADD, "+")

        if self.ss.peek_char() == "*":
            self.ss.eat_char()
            return Lexeme(Token.MULT, "*")

        if self.ss.peek_char() == "=":
            self.ss.eat_char()
            return Lexeme(Token.ASSIGN, "=")

        if self.ss.peek_char() == ";":
            self.ss.eat_char()
            return Lexeme(Token.SEMI, ";")

        if self.ss.peek_char() in CHARS:
            return self._scan_id()

        # NUM can start with a digit OR '.' followed by a digit
        if self.ss.peek_char() in NUMS or (self.ss.peek_char() == "." and self.ss.peek_next_char() in NUMS):
            return self._scan_num()

        raise ScannerException()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    with open(args.file_name) as f:
        f_contents = f.read()

    s = NaiveScanner(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if args.verbose:
            print(t)
    end = time()
    print("time to parse (seconds): ", str(end-start))