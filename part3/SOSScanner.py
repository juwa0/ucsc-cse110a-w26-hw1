import re
from functools import reduce
from time import time
import argparse
import sys

# allow importing tokens from part2
sys.path.append("../part2/")
from tokens import tokens, Token, Lexeme
from typing import Callable, List, Tuple, Optional


# No line number this time
class ScannerException(Exception):
    pass


class SOSScanner:
    def __init__(self, tokens: List[Tuple[Token, str, Callable[[Lexeme], Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string: str) -> None:
        self.istring = input_string

    def token(self) -> Optional[Lexeme]:
        # If input is empty, we are done
        if len(self.istring) == 0:
            return None

        matches = []

        # Try matching each token at the START of the string
        for t in self.tokens:
            tok, pattern, action = t
            m = re.match(pattern, self.istring)
            if m is not None:
                value = m.group(0)
                matches.append((tok, value, action))

        # If nothing matches at position 0, it's a scanner error
        if len(matches) == 0:
            raise ScannerException()

        # Choose the longest match (maximal munch)
        longest = matches[0]
        for cand in matches[1:]:
            if len(cand[1]) > len(longest[1]):
                longest = cand

        tok, value, action = longest

        # Apply token action (used for keywords)
        lex = action(Lexeme(tok, value))

        # Remove matched prefix from input string
        self.istring = self.istring[len(value):]

        # Skip IGNORE tokens
        if lex.token == Token.IGNORE:
            return self.token()

        return lex


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    with open(args.file_name) as f:
        f_contents = f.read()

    verbose = args.verbose

    s = SOSScanner(tokens)
    s.input_string(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if verbose:
            print(t)
    end = time()

    print("time to parse (seconds): ", str(end - start))