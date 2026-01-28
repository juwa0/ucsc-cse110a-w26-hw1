import re
from time import time
import argparse
import sys
import os
from typing import Callable, List, Tuple, Optional
from part2.tokens import tokens, Token, Lexeme

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PART2_DIR = os.path.normpath(os.path.join(THIS_DIR, "..", "part2"))
if PART2_DIR not in sys.path:
    sys.path.insert(0, PART2_DIR)

class ScannerException(Exception):
    pass

class SOSScanner:
    def __init__(self, tokens: List[Tuple[Token, str, Callable[[Lexeme], Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string: str) -> None:
        self.istring = input_string

    def token(self) -> Optional[Lexeme]:
        while True:
            if len(self.istring) == 0:
                return None

            matches = []

            # Match each token ONCE at start-of-string
            for (tok, pattern, action) in self.tokens:
                m = re.match(pattern, self.istring)
                if m is not None:
                    text = m.group(0)
                    matches.append((tok, text, action))

            if len(matches) == 0:
                raise ScannerException()

            # Maximal munch: pick the longest match (ties -> token list order)
            best = matches[0]
            for cand in matches[1:]:
                if len(cand[1]) > len(best[1]):
                    best = cand

            tok, text, action = best
            out = action(Lexeme(tok, text))

            # Chop off matched prefix
            self.istring = self.istring[len(text):]

            # Skip IGNORE tokens
            if out.token == Token.IGNORE:
                continue

            return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str)
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    with open(args.file_name) as f:
        f_contents = f.read()

    s = SOSScanner(tokens)
    s.input_string(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if args.verbose:
            print(t)
    end = time()
    print("time to parse (seconds): ", str(end - start))