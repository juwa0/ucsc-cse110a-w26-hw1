import re
from time import time
import argparse
import sys
import os
from typing import Callable, List, Tuple, Optional

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Try both layouts (root-level or inside part3/)
CANDIDATES = [
    os.path.normpath(os.path.join(THIS_DIR, "part2")),
    os.path.normpath(os.path.join(THIS_DIR, "..", "part2")),
]
for p in CANDIDATES:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

import tokens as tokmod

# ✅ required by Gradescope: `from SOSScanner import SOSScanner, tokens`
tokens = tokmod.tokens


class ScannerException(Exception):
    pass


class SOSScanner:
    def __init__(self, tokens: List[Tuple[tokmod.Token, str, Callable[[tokmod.Lexeme], tokmod.Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string: str) -> None:
        self.istring = input_string

    def token(self) -> Optional[tokmod.Lexeme]:
        while True:
            if len(self.istring) == 0:
                return None

            matches = []
            for (tok, pattern, action) in self.tokens:
                m = re.match(pattern, self.istring)
                if m is not None:
                    matches.append((tok, m.group(0), action))

            if not matches:
                raise ScannerException()

            # maximal munch (longest match); ties -> token order
            best = matches[0]
            for cand in matches[1:]:
                if len(cand[1]) > len(best[1]):
                    best = cand

            tok, text, action = best
            out = action(tokmod.Lexeme(tok, text))
            self.istring = self.istring[len(text):]

            if out.token == tokmod.Token.IGNORE:
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