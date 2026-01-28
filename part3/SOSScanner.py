import re
from time import time
import argparse
import sys
import os
from typing import Callable, List, Tuple, Optional

import importlib.util
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
candidates = [
    os.path.join(THIS_DIR, "..", "part2", "tokens.py"),
    os.path.join(THIS_DIR, "part2", "tokens.py"),
]
TOKENS_PATH = None
for p in candidates:
    p = os.path.normpath(p)
    if os.path.isfile(p):
        TOKENS_PATH = p
        break

if TOKENS_PATH is None:
    raise ImportError("Could not find part2/tokens.py")

spec = importlib.util.spec_from_file_location("hw_tokens", TOKENS_PATH)
tokmod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(tokmod)
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