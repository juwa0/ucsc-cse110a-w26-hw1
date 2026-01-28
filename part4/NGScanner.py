import re
from time import time
import argparse
import sys
import os
from typing import Callable, List, Tuple, Optional
try:
    import part2.tokens as tokmod
except Exception:
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    PART2_DIR = os.path.normpath(os.path.join(THIS_DIR, "..", "part2"))
    if PART2_DIR not in sys.path:
        sys.path.insert(0, PART2_DIR)
    import tokens as tokmod
tokens = tokmod.tokens

class ScannerException(Exception):
    pass


class NGScanner:
    def __init__(self, tokens: List[Tuple[tokmod.Token, str, Callable[[tokmod.Lexeme], tokmod.Lexeme]]]) -> None:
        self.tokens = tokens

        # Build one giant named-group regex:
        # (?P<TOKENNAME>pattern)|(?P<OTHERTOKEN>pattern)|...
        # We keep token order because ties should resolve by token list order.
        parts = []
        for (tok, pattern, _action) in self.tokens:
            group_name = tok.value  # e.g., "ID", "NUM", "PLUS"
            parts.append(f"(?P<{group_name}>{pattern})")

        self.master_pattern = re.compile("|".join(parts))

        # Map group name back to the Token object
        self.name_to_token = {tok.value: tok for (tok, _pattern, _action) in self.tokens}

        # For applying actions, map Token -> action
        self.token_to_action = {tok: action for (tok, _pattern, action) in self.tokens}

    def input_string(self, input_string: str) -> None:
        self.istring = input_string

    def token(self) -> Optional[tokmod.Lexeme]:
        while True:
            if len(self.istring) == 0:
                return None

            m = self.master_pattern.match(self.istring)
            if m is None:
                raise ScannerException()

            # Determine which named group matched
            group_name = m.lastgroup
            if group_name is None:
                raise ScannerException()

            text = m.group(group_name)
            tok = self.name_to_token[group_name]
            action = self.token_to_action[tok]

            out = action(tokmod.Lexeme(tok, text))

            # Consume the matched prefix
            self.istring = self.istring[len(text):]

            # Skip IGNORE tokens
            if tok.name == "IGNORE":
                continue

            return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str)
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    with open(args.file_name) as f:
        f_contents = f.read()

    s = NGScanner(tokmod.tokens)
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