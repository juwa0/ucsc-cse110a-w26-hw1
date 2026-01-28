import re
from time import time
import argparse
import sys
import os
from typing import Callable, List, Tuple, Optional

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Try both layouts (root-level or inside part4/)
CANDIDATES = [
    os.path.normpath(os.path.join(THIS_DIR, "part2")),
    os.path.normpath(os.path.join(THIS_DIR, "..", "part2")),
]
for p in CANDIDATES:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

import tokens as tokmod

# ✅ required by Gradescope: `from NGScanner import NGScanner, tokens`
tokens = tokmod.tokens


class ScannerException(Exception):
    pass


class NGScanner:
    def __init__(self, tokens: List[Tuple[tokmod.Token, str, Callable[[tokmod.Lexeme], tokmod.Lexeme]]]) -> None:
        self.tokens = tokens

        parts = []
        self.name_to_token = {}
        self.token_to_action = {}

        for (tok, pattern, action) in self.tokens:
            parts.append(f"(?P<{tok.value}>{pattern})")
            self.name_to_token[tok.value] = tok
            self.token_to_action[tok] = action

        self.master = re.compile("|".join(parts))

    def input_string(self, input_string: str) -> None:
        self.istring = input_string

    def token(self) -> Optional[tokmod.Lexeme]:
        while True:
            if len(self.istring) == 0:
                return None

            m = self.master.match(self.istring)
            if m is None:
                raise ScannerException()

            name = m.lastgroup
            if name is None:
                raise ScannerException()

            text = m.group(name)
            tok = self.name_to_token[name]
            action = self.token_to_action[tok]

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

    s = NGScanner(tokens)
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